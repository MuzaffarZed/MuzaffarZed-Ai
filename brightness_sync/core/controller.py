"""
Core Brightness Controller for Windows.
Boshqaruv moduli: WMI (noutbuk ekrani) va VESA DDC/CI (dxva2.dll orqali tashqi monitorlar).
Arxitektura: Doimiy (persistent) apparat ushlagichlari va yuqori tezlikdagi I2C kanali.
Chuqur qorong'ulik (Deep Dimming): Yorug'lik va Kontrastni birgalikda boshqarish.
"""

import ctypes
from ctypes import wintypes
from typing import List, Dict, Optional, Tuple
import time
import logging
import threading
import win32com.client

logger = logging.getLogger("BrightnessController")


class PHYSICAL_MONITOR(ctypes.Structure):
    _fields_ = [
        ("hPhysicalMonitor", wintypes.HANDLE),
        ("szPhysicalMonitorDescription", wintypes.WCHAR * 128),
    ]


class BrightnessController:
    """
    Noutbuk va tashqi monitorlarning yorug'lik darajalarini o'qish va boshqarish.
    Doimiy ushlagichlar (persistent handles) orqali I2C shinasini ortiqcha ochish/yopishdan
    va apparat miltillashlaridan (flashing/reset) to'liq himoyalangan.
    """

    def __init__(self):
        self._user32 = ctypes.windll.user32
        self._dxva2 = ctypes.windll.dxva2
        self._lock = threading.RLock()
        self._cached_monitors: List[Tuple[wintypes.HANDLE, str]] = []
        self._last_set_level: Optional[int] = None
        self._last_set_contrast: Optional[int] = None
        self._init_physical_monitors()

    def _init_physical_monitors(self):
        """Tashqi monitorlarning apparat ushlagichlarini ochadi va keshlaydi."""
        with self._lock:
            self._close_handles_unlocked()
            monitors: List[wintypes.HMONITOR] = []

            def _enum_proc(h_mon, hdc, lprc, dw):
                monitors.append(h_mon)
                return True

            cb = ctypes.WINFUNCTYPE(
                wintypes.BOOL,
                wintypes.HMONITOR,
                wintypes.HDC,
                ctypes.POINTER(wintypes.RECT),
                wintypes.LPARAM,
            )(_enum_proc)

            self._user32.EnumDisplayMonitors(None, None, cb, 0)

            for h_mon in monitors:
                num = wintypes.DWORD()
                if not self._dxva2.GetNumberOfPhysicalMonitorsFromHMONITOR(
                    h_mon, ctypes.byref(num)
                ):
                    continue

                if num.value == 0:
                    continue

                arr = (PHYSICAL_MONITOR * num.value)()
                if not self._dxva2.GetPhysicalMonitorsFromHMONITOR(
                    h_mon, num.value, arr
                ):
                    continue

                for p in arr:
                    h_phys = p.hPhysicalMonitor
                    desc = str(p.szPhysicalMonitorDescription)
                    min_b, cur_b, max_b = (
                        wintypes.DWORD(),
                        wintypes.DWORD(),
                        wintypes.DWORD(),
                    )

                    # DDC/CI yorug'likni qo'llab-quvvatlashini tekshirish
                    if self._dxva2.GetMonitorBrightness(
                        h_phys,
                        ctypes.byref(min_b),
                        ctypes.byref(cur_b),
                        ctypes.byref(max_b),
                    ):
                        self._cached_monitors.append((h_phys, desc))
                        logger.info(
                            "Tashqi monitor ulandi: %s (Dastlabki: %d%%)",
                            desc,
                            cur_b.value,
                        )
                    else:
                        # DDC/CI qo'llab-quvvatlamasa (masalan noutbuk ichki paneli), yopamiz
                        self._dxva2.DestroyPhysicalMonitor(h_phys)

    def _close_handles_unlocked(self):
        """Keshdagi barcha apparat ushlagichlarini xavfsiz yopadi."""
        for h_phys, desc in self._cached_monitors:
            try:
                self._dxva2.DestroyPhysicalMonitor(h_phys)
            except Exception:
                pass
        self._cached_monitors.clear()

    def get_laptop_brightness(self) -> Optional[int]:
        """
        Noutbukning ichki displey yorug'ligini (0-100%) WMI orqali aniqlaydi.
        """
        try:
            import pythoncom

            pythoncom.CoInitialize()
            wmi = win32com.client.GetObject(r"winmgmts:\\.\root\wmi")
            results = wmi.ExecQuery(
                "SELECT CurrentBrightness FROM WmiMonitorBrightness WHERE Active = True"
            )
            for item in results:
                val = int(item.CurrentBrightness)
                return max(0, min(100, val))
        except Exception as exc:
            logger.warning("[!] WMI noutbuk yorug'ligini olishda xatolik: %s", exc)
        return None

    def set_laptop_brightness(self, level: int) -> bool:
        """
        Noutbukning ichki ekrani yorug'ligini dasturiy ravishda o'rnatish.
        """
        target = max(0, min(100, int(level)))
        try:
            import pythoncom

            pythoncom.CoInitialize()
            wmi = win32com.client.GetObject(r"winmgmts:\\.\root\wmi")
            methods = wmi.ExecQuery(
                "SELECT * FROM WmiMonitorBrightnessMethods WHERE Active = True"
            )
            for m in methods:
                in_params = m.Methods_("WmiSetBrightness").InParameters.SpawnInstance_()
                in_params.Timeout = 1
                in_params.Brightness = target
                m.ExecMethod_("WmiSetBrightness", in_params)
                return True
        except Exception as exc:
            logger.warning("[!] Noutbuk yorug'ligini o'rnatishda xatolik: %s", exc)
        return False

    def get_external_monitors_info(self) -> List[Dict[str, int]]:
        """
        DDC/CI ni qo'llab-quvvatlovchi barcha tashqi monitorlar ma'lumotlarini qaytaradi.
        """
        with self._lock:
            if not self._cached_monitors:
                self._init_physical_monitors()

            info_list = []
            for idx, (h_phys, desc) in enumerate(self._cached_monitors):
                min_b, cur_b, max_b = (
                    wintypes.DWORD(),
                    wintypes.DWORD(),
                    wintypes.DWORD(),
                )
                if self._dxva2.GetMonitorBrightness(
                    h_phys,
                    ctypes.byref(min_b),
                    ctypes.byref(cur_b),
                    ctypes.byref(max_b),
                ):
                    info_list.append(
                        {
                            "index": idx,
                            "description": desc,
                            "min": int(min_b.value),
                            "current": int(cur_b.value),
                            "max": int(max_b.value),
                        }
                    )
            return info_list

    def set_external_brightness_and_contrast(
        self,
        brightness: int,
        contrast: Optional[int] = None,
    ) -> int:
        """
        DDC/CI orqali yorug'lik va kontrastni birgalikda boshqaradi.
        Chuqur qorong'ulik rejimida past foizlarda kontrastni ham pasaytirib,
        tashqi monitorni noutbuk kabi chuqur xiralashtiradi.
        """
        target_b = max(0, min(100, int(brightness)))
        target_c = max(0, min(100, int(contrast))) if contrast is not None else None

        with self._lock:
            if not self._cached_monitors:
                self._init_physical_monitors()

            if not self._cached_monitors:
                return 0

            success_count = 0
            for h_phys, desc in self._cached_monitors:
                ok = True
                if self._last_set_level != target_b:
                    if not self._dxva2.SetMonitorBrightness(h_phys, target_b):
                        ok = False

                if target_c is not None and self._last_set_contrast != target_c:
                    if not self._dxva2.SetMonitorContrast(h_phys, target_c):
                        ok = False

                if ok:
                    success_count += 1
                else:
                    logger.warning("[!] %s ga parametr uzatilmadi, qayta ulanmoqda...", desc)
                    self._init_physical_monitors()
                    break

            if success_count > 0:
                self._last_set_level = target_b
                if target_c is not None:
                    self._last_set_contrast = target_c

            return success_count

    def set_external_brightness(
        self,
        level: int,
        smooth: bool = False,
        smooth_step: int = 4,
        smooth_delay: float = 0.02,
    ) -> int:
        """
        DDC/CI tashqi monitorlar yorug'ligini to'g'ridan-to'g'ri o'rnatadi.
        """
        return self.set_external_brightness_and_contrast(level, None)

    def set_all_brightness(self, level: int) -> bool:
        """
        Bir vaqtning o'zida ikkala displey yorug'ligini o'rnatadi.
        """
        ok_laptop = self.set_laptop_brightness(level)
        self.set_external_brightness(level)
        return ok_laptop

    def get_status(self) -> Dict:
        """
        Noutbuk va tashqi monitorlarning joriy holati.
        """
        laptop = self.get_laptop_brightness()
        externals = self.get_external_monitors_info()
        return {
            "laptop_brightness": laptop,
            "external_monitors": externals,
            "in_sync": all(ext["current"] == laptop for ext in externals)
            if externals and laptop is not None
            else False,
        }

    def close(self):
        """Resurslarni xavfsiz tozalash."""
        with self._lock:
            self._close_handles_unlocked()

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass
