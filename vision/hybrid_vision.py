"""vision/hybrid_vision.py - Advanced Multimodal Screen Vision with Window Topology & DPI Awareness.

Qobiliyatlar:
1. Majburiy DPI-awareness (100%, 125%, 150% masshtabda piksellarning 1:1 aniqligi).
2. Ochiq oynalar topologiyasi (z-order, koordinatalar, faol oyna sarlavhasi).
3. Kursorning real vaqtli koordinatalari va uning ostidagi oyna aniqlanishi.
4. Oyna holatini to'liq boshqarish: Alt+Tab, Maximize, Minimize, Restore, Center, SetForeground.
5. Multimodal modellar (Gemini 2.5 Flash) uchun to'liq vizual va semantik kontekst tayyorlash.
"""

from __future__ import annotations

import ctypes
import io
import logging
from dataclasses import dataclass, field
from typing import Any, Optional

import pyautogui
from PIL import Image

logger = logging.getLogger("Jarvis.HybridVision")

# Majburiy DPI-awareness o'rnatish
try:
    # PROCESS_PER_MONITOR_DPI_AWARE_V2 = 2
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
    DPI_STATUS = "PerMonitorV2"
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
        DPI_STATUS = "SystemDPIAware"
    except Exception as e:
        DPI_STATUS = f"Failed: {e}"

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
class WindowInfo:
    """Oyna haqida batafsil ma'lumot."""
    hwnd: int
    title: str
    rect: tuple[int, int, int, int]  # (left, top, right, bottom)
    width: int
    height: int
    is_active: bool
    is_minimized: bool
    is_maximized: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "hwnd": self.hwnd,
            "title": self.title,
            "rect": list(self.rect),
            "width": self.width,
            "height": self.height,
            "is_active": self.is_active,
            "is_minimized": self.is_minimized,
            "is_maximized": self.is_maximized,
        }


@dataclass
class VisualContext:
    """Modelga yuboriladigan to'liq vizual kontekst."""
    screenshot: Image.Image
    screen_width: int
    screen_height: int
    cursor_position: tuple[int, int]
    active_window: Optional[WindowInfo]
    visible_windows: list[WindowInfo]
    dpi_status: str

    def get_prompt_context(self) -> str:
        """Kognitiv model (Gemini) uchun formatlangan matnli kontekst."""
        lines = [
            f"Ekran o'lchami: {self.screen_width}x{self.screen_height} (DPI: {self.dpi_status})",
            f"Kursor hozirgi o'rni: X={self.cursor_position[0]}, Y={self.cursor_position[1]}",
        ]
        if self.active_window:
            lines.append(f"Faol oyna: '{self.active_window.title}' [Koordinatalar: {self.active_window.rect}]")

        if self.visible_windows:
            lines.append("Ko'rinadigan boshqa oynalar:")
            for w in self.visible_windows[:10]:
                if not w.is_active and w.title:
                    lines.append(f" - '{w.title}' [rect: {w.rect}]")

        return "\n".join(lines)


class HybridVisionEngine:
    """DPI-aware, oyna topologiyasi va multimodal ko'rish dvigateli."""

    def __init__(self) -> None:
        self.dpi_status = DPI_STATUS
        logger.info("HybridVisionEngine ishga tushirildi (DPI: %s, Win32: %s)", self.dpi_status, WIN32_AVAILABLE)

    def get_screen_size(self) -> tuple[int, int]:
        """Ekran o'lchamini (kenglik, balandlik) qaytaradi."""
        return pyautogui.size()

    def get_cursor_position(self) -> tuple[int, int]:
        """Kursorning joriy koordinatalarini qaytaradi."""
        pos = pyautogui.position()
        return (pos.x, pos.y)

    def capture_screen(self, region: Optional[tuple[int, int, int, int]] = None) -> Image.Image:
        """Ekrandan yuqori aniqlikdagi skrinshot oladi."""
        import os
        if os.getenv("JARVIS_TEST_MODE", "0") == "1":
            w, h = self.get_screen_size()
            return Image.new("RGB", (max(w, 800), max(h, 600)), color=(30, 30, 30))

        try:
            return pyautogui.screenshot(region=region)
        except Exception:
            try:
                from PIL import ImageGrab
                img = ImageGrab.grab(bbox=region)
                if img:
                    return img
            except Exception:
                pass
            w, h = self.get_screen_size()
            return Image.new("RGB", (max(w, 800), max(h, 600)), color=(30, 30, 30))

    def capture_as_bytes(self, format: str = "PNG") -> bytes:
        """Skrinshotni xotiradagi baytlar (RAM) sifatida qaytaradi."""
        img = self.capture_screen()
        buf = io.BytesIO()
        img.save(buf, format=format)
        return buf.getvalue()

    def get_window_topology(self) -> tuple[Optional[WindowInfo], list[WindowInfo]]:
        """Barcha ko'rinadigan oynalar va faol oynani aniqlaydi."""
        if not WIN32_AVAILABLE or win32gui is None:
            return None, []

        active_hwnd = win32gui.GetForegroundWindow()
        active_window: Optional[WindowInfo] = None
        visible_windows: list[WindowInfo] = []

        def enum_handler(hwnd: int, extra: Any) -> bool:
            if not win32gui.IsWindow(hwnd) or not win32gui.IsWindowVisible(hwnd):
                return True

            title = win32gui.GetWindowText(hwnd).strip()
            # Asosiy tizim fon oynalarini o'tkazib yuborish
            if not title or title in ("Program Manager", "Settings", "Windows Input Experience"):
                return True

            rect = win32gui.GetWindowRect(hwnd)
            width = rect[2] - rect[0]
            height = rect[3] - rect[1]

            if width <= 0 or height <= 0:
                return True

            placement = win32gui.GetWindowPlacement(hwnd)
            show_cmd = placement[1] if placement else 0
            is_min = (show_cmd == win32con.SW_SHOWMINIMIZED)
            is_max = (show_cmd == win32con.SW_SHOWMAXIMIZED)
            is_act = (hwnd == active_hwnd)

            win_info = WindowInfo(
                hwnd=hwnd,
                title=title,
                rect=rect,
                width=width,
                height=height,
                is_active=is_act,
                is_minimized=is_min,
                is_maximized=is_max,
            )

            if is_act:
                nonlocal active_window
                active_window = win_info

            visible_windows.append(win_info)
            return True

        try:
            win32gui.EnumWindows(enum_handler, None)
        except Exception as e:
            logger.error("EnumWindows xatosi: %s", e)

        return active_window, visible_windows

    def get_full_visual_context(self) -> VisualContext:
        """Skrinshot, kursor va oyna topologiyasini birlashtirgan to'liq kontekst."""
        screenshot = self.capture_screen()
        w, h = self.get_screen_size()
        cursor = self.get_cursor_position()
        active_win, vis_wins = self.get_window_topology()

        return VisualContext(
            screenshot=screenshot,
            screen_width=w,
            screen_height=h,
            cursor_position=cursor,
            active_window=active_win,
            visible_windows=vis_wins,
            dpi_status=self.dpi_status,
        )

    # =========================================================================
    # OYNALARNI BOSHQARISH VA MANIPULATSIYA
    # =========================================================================

    def find_window_by_title(self, search_text: str) -> Optional[int]:
        """Sarlavhasida ko'rsatilgan matn bo'lgan oynaning HWND raqamini topadi."""
        if not WIN32_AVAILABLE or win32gui is None:
            return None

        found_hwnd: Optional[int] = None
        search_lower = search_text.lower()

        def enum_win(hwnd: int, extra: Any) -> bool:
            nonlocal found_hwnd
            if win32gui.IsWindow(hwnd) and win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd).strip()
                if search_lower in title.lower():
                    found_hwnd = hwnd
                    return False
            return True

        try:
            win32gui.EnumWindows(enum_win, None)
        except Exception:
            pass

        return found_hwnd

    def activate_window(self, title_or_hwnd: str | int) -> bool:
        """Oynani oldingi fonga chiqaradi va faollashtiradi."""
        if not WIN32_AVAILABLE or win32gui is None:
            return False

        hwnd = title_or_hwnd if isinstance(title_or_hwnd, int) else self.find_window_by_title(title_or_hwnd)
        if not hwnd:
            return False

        try:
            # Agar minimallashtirilgan bo'lsa tiklash
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            return True
        except Exception as e:
            logger.warning("activate_window xatosi: %s", e)
            return False

    def maximize_window(self, title_or_hwnd: str | int) -> bool:
        """Oynani to'liq ekranga yoyadi (Maximize)."""
        if not WIN32_AVAILABLE or win32gui is None:
            return False

        hwnd = title_or_hwnd if isinstance(title_or_hwnd, int) else self.find_window_by_title(title_or_hwnd)
        if not hwnd:
            return False

        try:
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            return True
        except Exception as e:
            logger.warning("maximize_window xatosi: %s", e)
            return False

    def minimize_window(self, title_or_hwnd: str | int) -> bool:
        """Oynani vazifalar paneliga yig'adi (Minimize)."""
        if not WIN32_AVAILABLE or win32gui is None:
            return False

        hwnd = title_or_hwnd if isinstance(title_or_hwnd, int) else self.find_window_by_title(title_or_hwnd)
        if not hwnd:
            return False

        try:
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            return True
        except Exception as e:
            logger.warning("minimize_window xatosi: %s", e)
            return False

    def center_window(self, title_or_hwnd: str | int, width: int = 1200, height: int = 800) -> bool:
        """Oynani ekranning markaziga ko'chiradi va o'lchamini sozlaydi."""
        if not WIN32_AVAILABLE or win32gui is None:
            return False

        hwnd = title_or_hwnd if isinstance(title_or_hwnd, int) else self.find_window_by_title(title_or_hwnd)
        if not hwnd:
            return False

        try:
            screen_w, screen_h = self.get_screen_size()
            x = max(0, (screen_w - width) // 2)
            y = max(0, (screen_h - height) // 2)
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.MoveWindow(hwnd, x, y, width, height, True)
            win32gui.SetForegroundWindow(hwnd)
            return True
        except Exception as e:
            logger.warning("center_window xatosi: %s", e)
            return False

    def switch_window(self) -> None:
        """Alt+Tab orqali keyingi faol oynaga o'tadi."""
        pyautogui.hotkey("alt", "tab")


# Singleton
_hybrid_vision: Optional[HybridVisionEngine] = None


def get_hybrid_vision() -> HybridVisionEngine:
    """HybridVisionEngine yagona nusxasini qaytaradi."""
    global _hybrid_vision
    if _hybrid_vision is None:
        _hybrid_vision = HybridVisionEngine()
    return _hybrid_vision
