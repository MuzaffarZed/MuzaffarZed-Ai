"""
Background Synchronization Daemon with Event-Driven + Coalescing Queue Architecture.
Windows WMI hodisalari (WmiMonitorBrightnessEvent) orqali lahzalik reaksiya.
Chuqur qorong'ulik (Deep Dimming): Past foizlarda kontrastni ham pasaytirib,
tashqi monitorni noutbuk kabi chuqur va xira qorong'ilikka tushiradi.
"""

import time
import threading
import logging
from typing import Optional, Callable
import win32com.client
import pythoncom
import pywintypes

from .controller import BrightnessController
from .config import ConfigManager

logger = logging.getLogger("BrightnessSyncDaemon")


class BrightnessSyncDaemon:
    """
    Noutbuk va tashqi monitor yorug'ligini avtomatik va lahzalik sinxronizatsiya qiluvchi dvigatel.
    """

    def __init__(
        self,
        config: Optional[ConfigManager] = None,
        controller: Optional[BrightnessController] = None,
        on_sync_callback: Optional[Callable[[int, int], None]] = None,
    ):
        self.config = config
        self.controller = controller or BrightnessController()
        self.on_sync_callback = on_sync_callback

        self._running = False
        self._target_brightness: Optional[int] = None
        self._target_contrast: Optional[int] = None
        self._last_applied_brightness: Optional[int] = None
        self._last_applied_contrast: Optional[int] = None
        self._last_laptop_brightness: Optional[int] = None

        self._worker_thread: Optional[threading.Thread] = None
        self._listener_thread: Optional[threading.Thread] = None
        self._cv = threading.Condition()

        self.enabled = True if not config else bool(config.get("sync_enabled", True))

    def _post_target_brightness(self, laptop_lvl: int):
        """Yangi noutbuk yorug'lik darajasini navbatga joylaydi."""
        if not self.enabled:
            return

        target_ext = (
            self.config.calculate_external(laptop_lvl)
            if self.config
            else laptop_lvl
        )
        target_contrast = (
            self.config.calculate_contrast(laptop_lvl)
            if self.config
            else None
        )

        with self._cv:
            self._target_brightness = target_ext
            self._target_contrast = target_contrast
            self._cv.notify_all()

    def _hardware_worker(self):
        """
        Apparatga yozish ishchi oqimi (Coalescing Worker).
        I2C shinasiga faqat bitta oqim ketma-ket yozadi, to'qnashuv va qotish bo'lmaydi.
        """
        logger.info("[WORKER] Apparat yozuvchisi ishga tushdi.")
        while self._running:
            target_b = None
            target_c = None
            with self._cv:
                while self._running and (
                    self._target_brightness is None
                    or (
                        self._target_brightness == self._last_applied_brightness
                        and self._target_contrast == self._last_applied_contrast
                    )
                ):
                    self._cv.wait(timeout=0.5)

                if not self._running:
                    break

                target_b = self._target_brightness
                target_c = self._target_contrast

            if target_b is not None:
                t0 = time.time()
                updated = self.controller.set_external_brightness_and_contrast(
                    target_b, target_c
                )
                dt = (time.time() - t0) * 1000
                self._last_applied_brightness = target_b
                self._last_applied_contrast = target_c
                logger.info(
                    "[SYNC] Monitor yangilandi: Yorug'lik %d%%, Kontrast %s%% (%d ta, %.1f ms)",
                    target_b,
                    str(target_c),
                    updated,
                    dt,
                )

                if self.on_sync_callback and self._last_laptop_brightness is not None:
                    self.on_sync_callback(self._last_laptop_brightness, updated)

        logger.info("[WORKER] Apparat yozuvchisi to'xtatildi.")

    def _wmi_event_listener(self):
        """
        Windows yadrosining WmiMonitorBrightnessEvent hodisalarini tinglovchi oqim.
        Fn tugmasi yoki Windows slayderi harakatlanganda lahzada uyg'onadi.
        """
        logger.info("[LISTENER] WMI hodisalarini kuzatish boshlandi.")
        pythoncom.CoInitialize()

        watcher = None
        try:
            wmi = win32com.client.GetObject(r"winmgmts:\\.\root\wmi")
            watcher = wmi.ExecNotificationQuery(
                "SELECT * FROM WmiMonitorBrightnessEvent"
            )
        except Exception as exc:
            logger.warning("[!] WMI hodisalarga ulanishda ogohlantirish: %s", exc)

        # Dastlabki qiymatni o'rnatish
        init_val = self.controller.get_laptop_brightness()
        if init_val is not None:
            self._last_laptop_brightness = init_val
            self._post_target_brightness(init_val)
            logger.info("[INIT] Boshlang'ich noutbuk yorug'ligi: %d%%", init_val)

        while self._running:
            got_event = False
            if watcher is not None:
                try:
                    event = watcher.NextEvent(300)
                    lvl = int(event.Brightness)
                    lvl = max(0, min(100, lvl))
                    self._last_laptop_brightness = lvl
                    self._post_target_brightness(lvl)
                    got_event = True
                    logger.debug("[EVENT] WmiMonitorBrightnessEvent: %d%%", lvl)
                except pywintypes.com_error:
                    pass
                except Exception as exc:
                    logger.debug("[!] WMI NextEvent xatoligi: %s", exc)

            if not got_event and self._running:
                cur = self.controller.get_laptop_brightness()
                if cur is not None and cur != self._last_laptop_brightness:
                    self._last_laptop_brightness = cur
                    self._post_target_brightness(cur)
                    logger.info("[KEEPALIVE] O'zgarish aniqlandi: %d%%", cur)

        pythoncom.CoUninitialize()
        logger.info("[LISTENER] WMI hodisalar kuzatuvi to'xtatildi.")

    def sync_once(self) -> Optional[int]:
        """Bir martalik qo'lda sinxronlash."""
        laptop_lvl = self.controller.get_laptop_brightness()
        if laptop_lvl is not None:
            self._last_laptop_brightness = laptop_lvl
            self._post_target_brightness(laptop_lvl)
        return laptop_lvl

    def start(self, non_blocking: bool = False):
        """Sinxronizatsiyani ishga tushirish."""
        if self._running:
            return

        self._running = True

        self._worker_thread = threading.Thread(
            target=self._hardware_worker,
            name="BrightnessHardwareWorker",
            daemon=True,
        )
        self._worker_thread.start()

        self._listener_thread = threading.Thread(
            target=self._wmi_event_listener,
            name="BrightnessWmiListener",
            daemon=True,
        )
        self._listener_thread.start()

        if not non_blocking:
            try:
                while self._running:
                    time.sleep(0.5)
            except (KeyboardInterrupt, SystemExit):
                self.stop()

    def stop(self):
        """Sinxronizatsiyani to'xtatish."""
        self._running = False
        with self._cv:
            self._cv.notify_all()

        if self._worker_thread and self._worker_thread.is_alive():
            self._worker_thread.join(timeout=1.0)
        if self._listener_thread and self._listener_thread.is_alive():
            self._listener_thread.join(timeout=1.0)

        self._worker_thread = None
        self._listener_thread = None
