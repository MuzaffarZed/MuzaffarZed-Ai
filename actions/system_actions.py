"""
JARVIS-Core — System Actions Engine (Actions Subsystem)
Automates Windows desktop tasks:
- Native Windows keyboard media & volume control (sub-millisecond Win32)
- High-speed application launching (Chrome, Telegram, VS Code, Explorer, CMD, Taskmgr)
- Hardware telemetry monitoring (CPU, RAM, Disk, Battery) via psutil
- Timestamped screenshot capture via Pillow ImageGrab
- Clipboard reader & writer via pyperclip
- Web browsing and YouTube automation
"""

from __future__ import annotations
import os
import sys
import time
import shutil
import logging
import datetime
import subprocess
import webbrowser
from pathlib import Path
from typing import Optional, Dict, Any

import psutil

try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False

try:
    from PIL import ImageGrab
    IMAGEGRAB_AVAILABLE = True
except ImportError:
    IMAGEGRAB_AVAILABLE = False

logger = logging.getLogger("JARVIS.Actions.SystemActions")


class SystemActions:
    """
    Hands and tools of JARVIS on Windows OS.
    Executes real system actions cleanly with robust fallbacks.
    """

    # Win32 Virtual Key Codes
    VK_VOLUME_MUTE = 0xAD
    VK_VOLUME_DOWN = 0xAE
    VK_VOLUME_UP = 0xAF
    VK_MEDIA_NEXT_TRACK = 0xB0
    VK_MEDIA_PLAY_PAUSE = 0xB3

    def __init__(self, workspace_root: Optional[str] = None) -> None:
        self.workspace_root = Path(workspace_root or Path(__file__).resolve().parent.parent)
        self.screenshots_dir = self.workspace_root / "screenshots"
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        self.test_mode = os.getenv("JARVIS_TEST_MODE", "0") == "1"

    # -------------------------------------------------------------------------
    # 1. Application Launchers
    # -------------------------------------------------------------------------
    def open_notepad(self) -> bool:
        """Opens Windows Notepad."""
        try:
            subprocess.Popen(["notepad.exe"])
            return True
        except Exception as e:
            logger.error("Notepad ochishda xatolik: %s", e)
            return False

    def open_explorer(self, target_path: Optional[str] = None) -> bool:
        """Opens Windows File Explorer at target directory."""
        try:
            path = target_path or os.path.expanduser("~")
            if sys.platform == "win32" and hasattr(os, "startfile"):
                os.startfile(path)
            else:
                subprocess.Popen(["explorer.exe", path])
            return True
        except Exception as e:
            logger.error("Fayl boshqaruvchisini ochishda xatolik: %s", e)
            return False

    def open_cmd(self) -> bool:
        """Opens Windows Terminal or Command Prompt."""
        try:
            subprocess.Popen(["wt.exe"])
            return True
        except Exception:
            try:
                subprocess.Popen(["cmd.exe"])
                return True
            except Exception as e:
                logger.error("Terminal ochishda xatolik: %s", e)
                return False

    def open_taskmgr(self) -> bool:
        """Opens Windows Task Manager."""
        try:
            subprocess.Popen(["taskmgr.exe"])
            return True
        except Exception as e:
            logger.error("Task Manager ochishda xatolik: %s", e)
            return False

    def open_settings(self) -> bool:
        """Opens Windows Settings."""
        try:
            subprocess.Popen(["start", "ms-settings:"], shell=True)
            return True
        except Exception as e:
            logger.error("Sozlamalarni ochishda xatolik: %s", e)
            return False

    def open_calc(self) -> bool:
        """Opens Windows Calculator."""
        try:
            subprocess.Popen(["calc.exe"])
            return True
        except Exception as e:
            logger.error("Kalkulyator ochishda xatolik: %s", e)
            return False

    def open_vscode(self) -> bool:
        """Opens Visual Studio Code."""
        code_bin = shutil.which("code")
        if code_bin:
            try:
                subprocess.Popen([code_bin])
                return True
            except Exception:
                pass

        common_paths = [
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"),
            r"C:\Program Files\Microsoft VS Code\Code.exe",
        ]
        for p in common_paths:
            if os.path.exists(p):
                try:
                    subprocess.Popen([p])
                    return True
                except Exception:
                    pass
        return False

    def open_chrome(self, url: Optional[str] = None) -> bool:
        """Opens Google Chrome or default browser."""
        target = url or "https://www.google.com"
        try:
            webbrowser.open(target)
            return True
        except Exception as e:
            logger.error("Brauzer ochishda xatolik: %s", e)
            return False

    def open_telegram(self) -> bool:
        """Opens Telegram Desktop if installed."""
        tg_path = os.path.expandvars(r"%APPDATA%\Telegram Desktop\Telegram.exe")
        if os.path.exists(tg_path):
            try:
                subprocess.Popen([tg_path])
                return True
            except Exception:
                pass
        return False

    # -------------------------------------------------------------------------
    # 2. Volume & Media Controls (Win32 API)
    # -------------------------------------------------------------------------
    def _send_key(self, vk_code: int) -> bool:
        """Sends a Win32 virtual key press."""
        if self.test_mode or sys.platform != "win32":
            return True
        try:
            import ctypes
            user32 = ctypes.windll.user32
            user32.keybd_event(vk_code, 0, 0, 0)
            user32.keybd_event(vk_code, 0, 2, 0)  # KEYEVENTF_KEYUP
            return True
        except Exception as e:
            logger.error("Tugma yuborishda xatolik: %s", e)
            return False

    def volume_up(self, steps: int = 3) -> bool:
        """Increases system volume."""
        success = True
        for _ in range(steps):
            success = self._send_key(self.VK_VOLUME_UP) and success
            time.sleep(0.02)
        return success

    def volume_down(self, steps: int = 3) -> bool:
        """Decreases system volume."""
        success = True
        for _ in range(steps):
            success = self._send_key(self.VK_VOLUME_DOWN) and success
            time.sleep(0.02)
        return success

    def volume_mute(self) -> bool:
        """Toggles volume mute."""
        return self._send_key(self.VK_VOLUME_MUTE)

    def media_play_pause(self) -> bool:
        """Toggles media play/pause."""
        return self._send_key(self.VK_MEDIA_PLAY_PAUSE)

    def media_next(self) -> bool:
        """Skips to next media track."""
        return self._send_key(self.VK_MEDIA_NEXT_TRACK)

    # -------------------------------------------------------------------------
    # 3. System Telemetry
    # -------------------------------------------------------------------------
    def get_telemetry(self) -> str:
        """Collects real-time CPU, RAM, Disk, and Battery statistics."""
        try:
            cpu = psutil.cpu_percent(interval=0.1)
            mem = psutil.virtual_memory()

            disks = []
            for d in ("C:", "D:"):
                try:
                    usage = psutil.disk_usage(d + "\\")
                    disks.append(f"{d} bo'sh joy: {usage.free / (1024**3):.1f} GB")
                except Exception:
                    pass
            disk_str = ", ".join(disks) if disks else "Disklar tekshirildi"

            battery_info = ""
            if hasattr(psutil, "sensors_battery"):
                batt = psutil.sensors_battery()
                if batt:
                    plug = "quvvatlanmoqda" if batt.power_plugged else "batareyada"
                    battery_info = f", Batareya: {batt.percent:.0f}% ({plug})"

            return (
                f"Tizim holati: CPU: {cpu:.1f}%, RAM: {mem.percent:.1f}% "
                f"({mem.used / (1024**3):.1f}/{mem.total / (1024**3):.1f} GB), "
                f"Disk: {disk_str}{battery_info}, janob Muzaffar."
            )
        except Exception as e:
            return f"Telemetriyani o'qishda xatolik yuz berdi: {e}"

    # -------------------------------------------------------------------------
    # 4. Screenshot Capture
    # -------------------------------------------------------------------------
    def take_screenshot(self) -> Optional[str]:
        """Captures full screen and saves to screenshots directory."""
        if not IMAGEGRAB_AVAILABLE:
            return None
        try:
            img = ImageGrab.grab()
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            filepath = self.screenshots_dir / filename
            img.save(str(filepath))
            return str(filepath)
        except Exception as e:
            logger.error("Skrinshot olishda xatolik: %s", e)
            return None

    # -------------------------------------------------------------------------
    # 5. Web Search & Navigation
    # -------------------------------------------------------------------------
    def search_google(self, query: str) -> bool:
        """Performs Google search in browser."""
        import urllib.parse
        clean_q = query.strip().lower()
        if not clean_q or clean_q in ("och", "ochish", "o", "kir", "ochib ber"):
            return self.open_chrome("https://www.google.com")
        url = f"https://www.google.com/search?q={urllib.parse.quote_plus(query.strip())}"
        return self.open_chrome(url)

    def search_youtube(self, query: str) -> bool:
        """Performs YouTube search in browser."""
        import urllib.parse
        clean_q = query.strip().lower()
        if not clean_q or clean_q in ("och", "ochish", "o", "kir", "ochib ber"):
            return self.open_chrome("https://www.youtube.com")
        url = f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(query.strip())}"
        return self.open_chrome(url)

    # -------------------------------------------------------------------------
    # 6. Clipboard Management
    # -------------------------------------------------------------------------
    def read_clipboard(self) -> str:
        """Reads current clipboard text."""
        if not PYPERCLIP_AVAILABLE:
            return "Klipbord kutubxonasi mavjud emas, janob."
        try:
            content = pyperclip.paste().strip()
            if not content:
                return "Klipbord hozircha bo'sh, janob."
            # Truncate preview if too long
            preview = content[:200] + ("..." if len(content) > 200 else "")
            return f"Klipborddagi matn: {preview}"
        except Exception as e:
            return f"Klipbordni o'qib bo'lmadi: {e}"

    def copy_to_clipboard(self, text: str) -> bool:
        """Copies text to clipboard."""
        if not PYPERCLIP_AVAILABLE:
            return False
        try:
            pyperclip.copy(text)
            return True
        except Exception:
            return False

    # -------------------------------------------------------------------------
    # 7. Workstation Security
    # -------------------------------------------------------------------------
    def lock_screen(self) -> bool:
        """Locks Windows workstation."""
        if self.test_mode or sys.platform != "win32":
            return True
        try:
            import ctypes
            ctypes.windll.user32.LockWorkStation()
            return True
        except Exception as e:
            logger.error("Ekranni qulflashda xatolik: %s", e)
            return False


_system_actions: Optional[SystemActions] = None


def get_system_actions(workspace_root: Optional[str] = None) -> SystemActions:
    """Singleton getter for SystemActions."""
    global _system_actions
    if _system_actions is None:
        _system_actions = SystemActions(workspace_root=workspace_root)
    return _system_actions
