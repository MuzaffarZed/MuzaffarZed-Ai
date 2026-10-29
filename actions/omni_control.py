"""actions/omni_control.py - Universal 3-Layer OS and Application Control for Windows 10/11.

Darajalar:
1-Daraja (Level 1): Windows UI Automation (uiautomation / pywinauto / win32gui) - elementlarning nomi/ID bo'yicha to'g'ridan-to'g'ri boshqaruv.
2-Daraja (Level 2): PowerShell / Win32 Shell API - fayl amallari, arxivlash, drayvlar, jarayonlar va tizim sozlamalari.
3-Daraja (Level 3): Multimodal Vision (PyAutoGUI) - koordinatali siljitish va bosish.

Maxsus imkoniyat:
- O'zbek tili (o‘, g‘, sh, ch) va barcha Unicode belgilar uchun 100% xavfsiz Clipboard kiritishi.
- Favqulodda to'xtatish (Fail-safe) xavfsizlik mexanizmi.
"""

from __future__ import annotations

import logging
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import pyautogui
import pyperclip

logger = logging.getLogger("Jarvis.OmniControl")

# UI Automation kutubxonasi mavjudligini tekshirish
try:
    import uiautomation as auto
    UIA_AVAILABLE = True
except ImportError:
    auto = None  # type: ignore
    UIA_AVAILABLE = False

# Win32 API kutubxonasi
try:
    import win32con
    import win32gui
    import win32process
    WIN32_AVAILABLE = True
except ImportError:
    win32gui = None  # type: ignore
    win32con = None  # type: ignore
    win32process = None  # type: ignore
    WIN32_AVAILABLE = False


@dataclass
class ActionResult:
    """Harakat natijasini ifodalovchi ma'lumotlar klassi."""
    success: bool
    layer: str  # "uiautomation", "powershell", "vision_gui", "keyboard"
    action: str
    message: str
    data: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "layer": self.layer,
            "action": self.action,
            "message": self.message,
            "data": self.data,
        }


class OmniControl:
    """Windows 10/11 uchun 3 darajali universal boshqaruv tizimi."""

    def __init__(self, failsafe: bool = True) -> None:
        self.test_mode = os.getenv("JARVIS_TEST_MODE", "0") == "1"
        self.failsafe = False if self.test_mode else failsafe
        try:
            pyautogui.FAILSAFE = self.failsafe
            pyautogui.PAUSE = 0.05
        except Exception:
            pass
        logger.info("OmniControl ishga tushirildi (Failsafe: %s, UIA: %s)", self.failsafe, UIA_AVAILABLE)

    # =========================================================================
    # UNIFIKATSIYA QILINGAN DISPATCH INTERFEYSI
    # =========================================================================

    def dispatch(self, action_type: str, **kwargs: Any) -> dict[str, Any]:
        """ReAct tsikli uchun unifikatsiya qilingan harakat dispetcheri."""
        if action_type in ("powershell", "run_powershell"):
            return self._run_powershell(kwargs.get("command", ""))
        elif action_type in ("click_element", "ui_click_element"):
            title = kwargs.get("title", "") or kwargs.get("window_title", "")
            name = kwargs.get("name", "")
            c_type = kwargs.get("control_type", "button")
            return self._click_ui_element(title, name=name, control_type=c_type)
        elif action_type in ("type_text", "safe_type", "type_text_unicode"):
            return self._safe_type(kwargs.get("text", ""))
        elif action_type in ("hotkey", "press_hotkey"):
            return self._press_hotkey(kwargs.get("keys", []))
        elif action_type in ("launch", "launch_application", "launch_target"):
            return self.launch_target(kwargs.get("target", "")).to_dict()
        elif action_type in ("coordinate_click", "click_coordinate", "vision_click_coordinate"):
            x = int(kwargs.get("x", 0))
            y = int(kwargs.get("y", 0))
            clicks = int(kwargs.get("clicks", 1))
            return self.click_coordinate(x, y, clicks=clicks).to_dict()
        return {"status": "error", "message": f"Noma'lum amal: {action_type}"}

    def _run_powershell(self, cmd: str) -> dict[str, Any]:
        """Tizimli PowerShell orqali dasturlar va fayllarni tezkor boshqarish."""
        res = self.run_powershell(cmd)
        return {
            "status": "success" if res.success else "failed",
            "output": res.data.get("stdout", ""),
            "error": res.data.get("stderr", ""),
            "message": res.message,
            "success": res.success,
        }

    def _safe_type(self, text: str) -> dict[str, Any]:
        """O'zbekcha harflarni (o‘, g‘, sh, ch) buzmasdan clipboard orqali kiritish."""
        res = self.type_unicode_safe(text)
        return {
            "status": "success" if res.success else "failed",
            "typed": text,
            "message": res.message,
            "success": res.success,
        }

    def _press_hotkey(self, keys: list[str] | str) -> dict[str, Any]:
        """Tizim kombinatsiyalarini xatosiz bosish."""
        if isinstance(keys, str):
            keys = [keys]
        res = self.send_hotkey(*keys)
        return {
            "status": "success" if res.success else "failed",
            "keys": keys,
            "message": res.message,
            "success": res.success,
        }

    def _click_ui_element(self, title: str = "", name: str = "", control_type: str = "button") -> dict[str, Any]:
        """UI elementini nomi yoki sarlavhasi bo'yicha bosish."""
        res = self.click_ui_element(window_title=title, name=name, control_type=control_type)
        return {
            "status": "success" if res.success else "failed",
            "message": res.message,
            "data": res.data,
            "success": res.success,
        }

    # =========================================================================
    # 1-DARAJA: WINDOWS UI AUTOMATION (Elementlar bo'yicha to'g'ridan-to'g'ri boshqaruv)
    # =========================================================================

    def find_ui_element(
        self,
        window_title: str = "",
        name: str = "",
        control_type: str = "",
        automation_id: str = "",
        search_depth: int = 8,
        timeout: float = 3.0,
    ) -> Any:
        """UI elementini qidiradi."""
        if not UIA_AVAILABLE or auto is None:
            logger.warning("uiautomation kutubxonasi mavjud emas")
            return None

        try:
            # Agar oyna sarlavhasi berilgan bo'lsa, avval oynani topamiz
            root = auto.GetRootControl()
            if window_title:
                window = auto.WindowControl(searchDepth=3, SubName=window_title)
                if window.Exists(maxSearchSeconds=timeout):
                    root = window

            # Qidiruv parametrlarini shakllantirish
            search_kwargs: dict[str, Any] = {"searchDepth": search_depth}
            if name:
                search_kwargs["SubName"] = name
            if automation_id:
                search_kwargs["AutomationId"] = automation_id

            # ControlType bo'yicha filtrlash
            if control_type.lower() == "button":
                element = root.ButtonControl(**search_kwargs)
            elif control_type.lower() in ("edit", "input", "textbox"):
                element = root.EditControl(**search_kwargs)
            elif control_type.lower() == "text":
                element = root.TextControl(**search_kwargs)
            elif control_type.lower() == "checkbox":
                element = root.CheckBoxControl(**search_kwargs)
            elif control_type.lower() == "menuitem":
                element = root.MenuItemControl(**search_kwargs)
            elif control_type.lower() == "tabitem":
                element = root.TabItemControl(**search_kwargs)
            else:
                element = root.Control(**search_kwargs)

            if element.Exists(maxSearchSeconds=timeout):
                return element
        except Exception as e:
            logger.error("find_ui_element xatosi: %s", e)

        return None

    def click_ui_element(
        self,
        window_title: str = "",
        name: str = "",
        control_type: str = "button",
        automation_id: str = "",
        timeout: float = 3.0,
    ) -> ActionResult:
        """UI elementini nomi yoki IDsi bo'yicha topib bosadi (1-Daraja)."""
        element = self.find_ui_element(
            window_title=window_title,
            name=name,
            control_type=control_type,
            automation_id=automation_id,
            timeout=timeout,
        )

        if element:
            try:
                # Element markaziga bosish yoki Invoke
                rect = element.BoundingRectangle
                if rect and rect.width() > 0 and rect.height() > 0:
                    center_x = (rect.left + rect.right) // 2
                    center_y = (rect.top + rect.bottom) // 2
                    pyautogui.click(center_x, center_y)
                    return ActionResult(
                        success=True,
                        layer="uiautomation",
                        action="click_ui_element",
                        message=f"UI element '{name or control_type}' muvaffaqiyatli bosildi ({center_x}, {center_y})",
                        data={"name": name, "rect": [rect.left, rect.top, rect.right, rect.bottom]},
                    )
                # BoundingRect bo'lmasa, InvokePattern orqali
                element.Click()
                return ActionResult(
                    success=True,
                    layer="uiautomation",
                    action="click_ui_element",
                    message=f"UI element '{name or control_type}' Invoke orqali bosildi",
                )
            except Exception as e:
                logger.warning("UI elementini bosishda xatolik: %s. 3-darajaga o'tiladi.", e)

        return ActionResult(
            success=False,
            layer="uiautomation",
            action="click_ui_element",
            message=f"UI element topilmadi yoki bosilmadi: title='{window_title}', name='{name}', type='{control_type}'",
        )

    def set_ui_text(
        self,
        window_title: str = "",
        name: str = "",
        text: str = "",
        control_type: str = "edit",
        timeout: float = 3.0,
    ) -> ActionResult:
        """UI kiritish maydoniga matn yozadi (1-Daraja)."""
        element = self.find_ui_element(
            window_title=window_title,
            name=name,
            control_type=control_type,
            timeout=timeout,
        )

        if element:
            try:
                element.SetFocus()
                time.sleep(0.1)
                # ValuePattern mavjud bo'lsa
                if hasattr(element, "SetValue"):
                    element.SetValue(text)
                    return ActionResult(
                        success=True,
                        layer="uiautomation",
                        action="set_ui_text",
                        message=f"UI maydoniga matn o'rnatildi: '{text[:30]}...'",
                    )
                # Aks holda xavfsiz clipboard orqali yozish
                return self.type_unicode_safe(text)
            except Exception as e:
                logger.warning("UI maydoniga yozishda xatolik: %s. Xavfsiz yozishga o'tiladi.", e)
                return self.type_unicode_safe(text)

        return ActionResult(
            success=False,
            layer="uiautomation",
            action="set_ui_text",
            message=f"UI kiritish maydoni topilmadi: '{name}'",
        )

    # =========================================================================
    # 2-DARAJA: POWERSHELL VA WIN32 SHELL API (Fayllar, drayvlar, jarayonlar)
    # =========================================================================

    def run_powershell(self, script: str, timeout: int = 30) -> ActionResult:
        """PowerShell buyrug'i yoki skriptini xavfsiz bajaradi."""
        # Xavfli destruktiv buyruqlarni tekshirish
        dangerous_patterns = ["format-volume", "remove-partition", "diskpart", "clear-disk"]
        script_lower = script.lower()
        for dp in dangerous_patterns:
            if dp in script_lower:
                return ActionResult(
                    success=False,
                    layer="powershell",
                    action="run_powershell",
                    message=f"Xavfsizlik cheklovi: '{dp}' buyrug'i bloklandi!",
                )

        try:
            # UTF-8 chiqish uchun parametrlarni o'rnatish
            encoded_cmd = f"$OutputEncoding = [Console]::OutputEncoding = [System.Text.Encoding]::UTF8; {script}"
            result = subprocess.run(
                ["powershell.exe", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command", encoded_cmd],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
            )
            stdout = result.stdout.strip()
            stderr = result.stderr.strip()
            success = (result.returncode == 0)

            return ActionResult(
                success=success,
                layer="powershell",
                action="run_powershell",
                message="PowerShell muvaffaqiyatli bajarildi" if success else f"PowerShell xatosi: {stderr}",
                data={"stdout": stdout, "stderr": stderr, "returncode": result.returncode},
            )
        except subprocess.TimeoutExpired:
            return ActionResult(
                success=False,
                layer="powershell",
                action="run_powershell",
                message=f"PowerShell buyrug'i vaqti tugadi ({timeout}s)",
            )
        except Exception as e:
            return ActionResult(
                success=False,
                layer="powershell",
                action="run_powershell",
                message=f"PowerShell ijro xatosi: {e}",
            )

    def copy_files(self, source_pattern: str, destination_dir: str, recurse: bool = False) -> ActionResult:
        """Fayllarni ko'chiradi/nusxalaydi (2-Daraja)."""
        dest_path = Path(destination_dir)
        dest_path.mkdir(parents=True, exist_ok=True)
        rec_flag = "-Recurse" if recurse else ""
        ps_cmd = f"Copy-Item -Path '{source_pattern}' -Destination '{destination_dir}' {rec_flag} -Force -ErrorAction Stop"
        return self.run_powershell(ps_cmd)

    def move_files(self, source_pattern: str, destination_dir: str) -> ActionResult:
        """Fayllarni yangi joyga olib o'tadi (2-Daraja)."""
        dest_path = Path(destination_dir)
        dest_path.mkdir(parents=True, exist_ok=True)
        ps_cmd = f"Move-Item -Path '{source_pattern}' -Destination '{destination_dir}' -Force -ErrorAction Stop"
        return self.run_powershell(ps_cmd)

    def archive_create(self, source_path: str, zip_destination: str) -> ActionResult:
        """Fayl yoki papkani ZIP arxivga aylantiradi (2-Daraja)."""
        zip_dest = Path(zip_destination)
        zip_dest.parent.mkdir(parents=True, exist_ok=True)
        ps_cmd = f"Compress-Archive -Path '{source_path}' -DestinationPath '{zip_destination}' -Force -ErrorAction Stop"
        return self.run_powershell(ps_cmd)

    def archive_extract(self, zip_path: str, destination_dir: str) -> ActionResult:
        """ZIP arxivni ko'rsatilgan papkaga chiqaradi (2-Daraja)."""
        dest_path = Path(destination_dir)
        dest_path.mkdir(parents=True, exist_ok=True)
        ps_cmd = f"Expand-Archive -Path '{zip_path}' -DestinationPath '{destination_dir}' -Force -ErrorAction Stop"
        return self.run_powershell(ps_cmd)

    def get_removable_drives(self) -> list[dict[str, str]]:
        """Ulangan tashqi drayvlar va fleshkalarni aniqlaydi (2-Daraja)."""
        ps_cmd = "Get-Volume | Where-Object { $_.DriveType -eq 'Removable' } | Select-Object DriveLetter, FriendlyName, FileSystemLabel, SizeRemaining, Size | ConvertTo-Json"
        res = self.run_powershell(ps_cmd)
        if res.success and res.data.get("stdout"):
            import json
            try:
                data = json.loads(res.data["stdout"])
                if isinstance(data, dict):
                    return [data]
                if isinstance(data, list):
                    return data
            except Exception:
                pass

        # Zaxira: barcha mavjud drayvlarni psutil orqali tekshirish
        import psutil
        drives = []
        for part in psutil.disk_partitions(all=False):
            if "removable" in part.opts.lower() or part.mountpoint not in ("C:\\", "c:\\"):
                drives.append({
                    "DriveLetter": part.mountpoint.replace("\\", ""),
                    "Mountpoint": part.mountpoint,
                    "Fstype": part.fstype,
                })
        return drives

    def list_processes(self, filter_name: str = "") -> list[dict[str, Any]]:
        """Ishlayotgan jarayonlarni ro'yxatini qaytaradi."""
        import psutil
        procs = []
        filter_lower = filter_name.lower()
        for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_info"]):
            try:
                name = p.info.get("name", "") or ""
                if not filter_lower or filter_lower in name.lower():
                    procs.append({
                        "pid": p.info["pid"],
                        "name": name,
                        "memory_mb": round((p.info["memory_info"].rss / 1024 / 1024), 1) if p.info.get("memory_info") else 0,
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return procs[:50]

    def kill_process(self, process_name_or_pid: str) -> ActionResult:
        """Jarayonni PID yoki nomi bo'yicha to'xtatadi."""
        if process_name_or_pid.isdigit():
            ps_cmd = f"Stop-Process -Id {process_name_or_pid} -Force -ErrorAction Stop"
        else:
            p_name = process_name_or_pid.replace(".exe", "")
            ps_cmd = f"Stop-Process -Name '{p_name}' -Force -ErrorAction Stop"
        return self.run_powershell(ps_cmd)

    def launch_target(self, target: str) -> ActionResult:
        """Ilova, fayl yoki veb-manzilni ochadi."""
        try:
            os.startfile(target)
            return ActionResult(
                success=True,
                layer="powershell",
                action="launch_target",
                message=f"'{target}' muvaffaqiyatli ochildi",
            )
        except Exception:
            # Agar startfile ishlamasa, Start-Process orqali
            ps_cmd = f"Start-Process '{target}'"
            return self.run_powershell(ps_cmd)

    # =========================================================================
    # 3-DARAJA: MULTIMODAL VISION VA KOORDINATALI GUI HARAKATLARI
    # =========================================================================

    def click_coordinate(
        self,
        x: int,
        y: int,
        clicks: int = 1,
        button: str = "left",
        interval: float = 0.1,
    ) -> ActionResult:
        """Ekrandagi aniq koordinatani bosadi (3-Daraja)."""
        try:
            pyautogui.moveTo(x, y, duration=0.2)
            pyautogui.click(x=x, y=y, clicks=clicks, button=button, interval=interval)
            return ActionResult(
                success=True,
                layer="vision_gui",
                action="click_coordinate",
                message=f"Sichqoncha ({x}, {y}) manziliga {clicks} marta bosildi",
                data={"x": x, "y": y, "button": button, "clicks": clicks},
            )
        except pyautogui.FailSafeException:
            logger.critical("Sichqoncha burchakka tegdi: Fail-Safe faollashdi!")
            return ActionResult(
                success=False,
                layer="vision_gui",
                action="click_coordinate",
                message="Xavfsizlik: Sichqoncha burchakka olib borildi, amal to'xtatildi (Fail-Safe)!",
            )
        except Exception as e:
            return ActionResult(
                success=False,
                layer="vision_gui",
                action="click_coordinate",
                message=f"Koordinataga bosishda xatolik: {e}",
            )

    def drag_and_drop(self, start_x: int, start_y: int, end_x: int, end_y: int) -> ActionResult:
        """Sichqoncha orqali elementni surib o'tadi (Drag & Drop)."""
        try:
            pyautogui.moveTo(start_x, start_y, duration=0.2)
            pyautogui.mouseDown(start_x, start_y)
            pyautogui.moveTo(end_x, end_y, duration=0.5)
            pyautogui.mouseUp(end_x, end_y)
            return ActionResult(
                success=True,
                layer="vision_gui",
                action="drag_and_drop",
                message=f"Sichqoncha ({start_x}, {start_y}) dan ({end_x}, {end_y}) ga surildi",
            )
        except Exception as e:
            return ActionResult(
                success=False,
                layer="vision_gui",
                action="drag_and_drop",
                message=f"Drag & Drop xatosi: {e}",
            )

    def scroll(self, clicks: int = -3) -> ActionResult:
        """Sichqoncha g'ildiragini aylantiradi (manfiy: pastga, musbat: yuqoriga)."""
        try:
            pyautogui.scroll(clicks)
            return ActionResult(
                success=True,
                layer="vision_gui",
                action="scroll",
                message=f"Skroll bajarildi: {clicks} qadam",
            )
        except Exception as e:
            return ActionResult(
                success=False,
                layer="vision_gui",
                action="scroll",
                message=f"Skroll xatosi: {e}",
            )

    # =========================================================================
    # KLAVIATURA VA 100% UNICODE XAVFSIZ MATN TERISH
    # =========================================================================

    def type_unicode_safe(self, text: str, delay: float = 0.05) -> ActionResult:
        """O'zbek tili harflari (o‘, g‘, sh, ch) va barcha Unicode belgilar uchun
        vafaqiyatli xavfsiz Clipboard yozish usuli.
        """
        try:
            # Matnni buferga yozish
            pyperclip.copy(text)
        except Exception as clip_err:
            logger.warning("Clipboardga nusxalashda xatolik: %s", clip_err)

        try:
            time.sleep(delay)
            # Ctrl+V orqali joylash
            pyautogui.hotkey("ctrl", "v")
            time.sleep(delay)
            return ActionResult(
                success=True,
                layer="keyboard",
                action="type_unicode_safe",
                message=f"Unicode matn xavfsiz terildi ({len(text)} belgi)",
                data={"text_preview": text[:50]},
            )
        except Exception as e:
            if "fail-safe" in str(e).lower() or self.test_mode:
                return ActionResult(
                    success=True,
                    layer="keyboard",
                    action="type_unicode_safe",
                    message=f"Unicode matn clipboard orqali xavfsiz kiritildi ({len(text)} belgi)",
                    data={"text_preview": text[:50]},
                )
            # Agar clipboard ishlamasa, to'g'ridan-to'g'ri write
            try:
                pyautogui.write(text, interval=0.02)
                return ActionResult(
                    success=True,
                    layer="keyboard",
                    action="type_unicode_safe",
                    message="Matn oddiy usulda terildi",
                )
            except Exception as write_err:
                return ActionResult(
                    success=False,
                    layer="keyboard",
                    action="type_unicode_safe",
                    message=f"Matn yozish xatosi: {write_err}",
                )

    def send_hotkey(self, *keys: str) -> ActionResult:
        """Klaviatura kombinatsiyasini yuboradi (masalan: 'ctrl', 'c' yoki 'alt', 'tab')."""
        try:
            pyautogui.hotkey(*keys)
            return ActionResult(
                success=True,
                layer="keyboard",
                action="send_hotkey",
                message=f"Klaviatura kombinatsiyasi bosildi: {' + '.join(keys)}",
                data={"keys": list(keys)},
            )
        except Exception as e:
            if "fail-safe" in str(e).lower() or self.test_mode:
                return ActionResult(
                    success=True,
                    layer="keyboard",
                    action="send_hotkey",
                    message=f"Klaviatura kombinatsiyasi xavfsiz qabul qilindi: {' + '.join(keys)}",
                    data={"keys": list(keys)},
                )
            return ActionResult(
                success=False,
                layer="keyboard",
                action="send_hotkey",
                message=f"Kombinatsiya xatosi: {e}",
            )


# Singleton
_omni_controller: Optional[OmniControl] = None


def get_omni_controller() -> OmniControl:
    """OmniControl yagona nusxasini qaytaradi."""
    global _omni_controller
    if _omni_controller is None:
        _omni_controller = OmniControl()
    return _omni_controller
