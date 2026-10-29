"""
JARVIS-Core — GUI Automation Engine (Actions Subsystem)
Production-Ready Features:
- PyAutoGUI mouse and keyboard automation with mandatory FAILSAFE protection
- Windows Win32 / UI Automation integration for window management (focus, minimize, maximize, close)
- Unicode-safe typing via pyperclip for flawless Uzbek diacritics (o‘, g‘, sh, ch)
"""

from __future__ import annotations
import os
import sys
import time
import logging
from typing import Optional, List, Tuple, Union

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
    pyautogui.FAILSAFE = True  # Dragging mouse to (0, 0) immediately triggers FailSafeException
    pyautogui.PAUSE = 0.05     # Brief pause between operations for system stability
except ImportError:
    PYAUTOGUI_AVAILABLE = False

try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False

try:
    import win32gui
    import win32con
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

try:
    import pygetwindow as gw
    PYGETWINDOW_AVAILABLE = True
except ImportError:
    PYGETWINDOW_AVAILABLE = False

logger = logging.getLogger("JARVIS.Actions.GuiActions")


class GuiActions:
    """
    Precision GUI and Window Controller for Windows 10 & 11.
    Integrates pixel automation with native OS window state management.
    """

    def __init__(self, screen_width: Optional[int] = None, screen_height: Optional[int] = None) -> None:
        self.test_mode = os.getenv("JARVIS_TEST_MODE", "0") == "1"
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._update_screen_dimensions()

    def _update_screen_dimensions(self) -> None:
        """Updates internal screen limits."""
        if self._screen_width and self._screen_height:
            return

        if PYAUTOGUI_AVAILABLE and not self.test_mode:
            try:
                sz = pyautogui.size()
                self._screen_width = int(sz[0])
                self._screen_height = int(sz[1])
                return
            except Exception:
                pass

        self._screen_width = 1920
        self._screen_height = 1080

    @property
    def screen_size(self) -> Tuple[int, int]:
        return self._screen_width or 1920, self._screen_height or 1080

    def _validate_coordinates(self, x: int, y: int) -> Tuple[int, int]:
        """Clamps coordinates safely to physical screen dimensions."""
        w, h = self.screen_size
        safe_x = max(2, min(w - 2, int(x)))
        safe_y = max(2, min(h - 2, int(y)))
        return safe_x, safe_y

    # -------------------------------------------------------------------------
    # 1. Native Window Management (Win32 & UI Automation)
    # -------------------------------------------------------------------------
    def get_active_window_title(self) -> str:
        """Returns the title of the current foreground window."""
        if self.test_mode or sys.platform != "win32":
            return "Visual Studio Code"

        try:
            if WIN32_AVAILABLE:
                hwnd = win32gui.GetForegroundWindow()
                if hwnd:
                    return win32gui.GetWindowText(hwnd).strip()
            elif PYGETWINDOW_AVAILABLE:
                active = gw.getActiveWindow()
                if active:
                    return active.title.strip()
        except Exception as e:
            logger.debug("Faol oyna sarlavhasini olishda xatolik: %s", e)
        return ""

    def focus_window(self, title_query: str) -> bool:
        """Finds a window by partial title match and brings it to the foreground."""
        if self.test_mode or sys.platform != "win32":
            logger.info("[MOCK] Window focused: %s", title_query)
            return True

        query = title_query.strip().lower()
        try:
            if WIN32_AVAILABLE:
                found_hwnd = None

                def _enum_cb(hwnd, _):
                    nonlocal found_hwnd
                    if win32gui.IsWindowVisible(hwnd):
                        txt = win32gui.GetWindowText(hwnd).lower()
                        if query in txt:
                            found_hwnd = hwnd
                            return False
                    return True

                try:
                    win32gui.EnumWindows(_enum_cb, None)
                except Exception:
                    pass

                if found_hwnd:
                    # Restore if minimized
                    win32gui.ShowWindow(found_hwnd, win32con.SW_RESTORE)
                    win32gui.SetForegroundWindow(found_hwnd)
                    time.sleep(0.1)
                    return True

            elif PYGETWINDOW_AVAILABLE:
                matches = gw.getWindowsWithTitle(title_query)
                if matches:
                    w = matches[0]
                    w.restore()
                    w.activate()
                    time.sleep(0.1)
                    return True
        except Exception as e:
            logger.error("Oynani faollashtirishda xatolik: %s", e)

        return False

    def minimize_active_window(self) -> bool:
        """Minimizes the currently active window."""
        if self.test_mode or sys.platform != "win32":
            return True

        try:
            if WIN32_AVAILABLE:
                hwnd = win32gui.GetForegroundWindow()
                if hwnd:
                    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
                    return True
        except Exception as e:
            logger.error("Oynani minimallashtirishda xatolik: %s", e)

        return self.press_hotkey("win", "down")

    def maximize_active_window(self) -> bool:
        """Maximizes the currently active window."""
        if self.test_mode or sys.platform != "win32":
            return True

        try:
            if WIN32_AVAILABLE:
                hwnd = win32gui.GetForegroundWindow()
                if hwnd:
                    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                    return True
        except Exception as e:
            logger.error("Oynani maksimallashtirishda xatolik: %s", e)

        return self.press_hotkey("win", "up")

    # -------------------------------------------------------------------------
    # 2. Mouse Operations
    # -------------------------------------------------------------------------
    def move_to(self, x: int, y: int, duration: float = 0.2) -> bool:
        """Moves cursor to (x, y) coordinates with smooth interpolation."""
        target_x, target_y = self._validate_coordinates(x, y)
        if self.test_mode or not PYAUTOGUI_AVAILABLE:
            logger.info("[MOCK] Mouse moved to (%d, %d)", target_x, target_y)
            return True

        try:
            pyautogui.moveTo(target_x, target_y, duration=duration)
            return True
        except pyautogui.FailSafeException:
            logger.critical("Favqulodda to'xtatish (FailSafe) faollashdi!")
            return False
        except Exception as e:
            logger.error("Sichqonchani siljitishda xatolik: %s", e)
            return False

    def click(
        self,
        x: Optional[int] = None,
        y: Optional[int] = None,
        button: str = "left",
        clicks: int = 1,
        interval: float = 0.1,
    ) -> bool:
        """Clicks at specified (x, y) coordinates or current position."""
        if self.test_mode or not PYAUTOGUI_AVAILABLE:
            logger.info("[MOCK] Clicked at (%s, %s) with %s button", x, y, button)
            return True

        try:
            if x is not None and y is not None:
                safe_x, safe_y = self._validate_coordinates(x, y)
                pyautogui.click(x=safe_x, y=safe_y, button=button, clicks=clicks, interval=interval)
            else:
                pyautogui.click(button=button, clicks=clicks, interval=interval)
            return True
        except pyautogui.FailSafeException:
            logger.critical("Favqulodda to'xtatish (FailSafe) faollashdi!")
            return False
        except Exception as e:
            logger.error("Bosishda xatolik: %s", e)
            return False

    def double_click(self, x: Optional[int] = None, y: Optional[int] = None) -> bool:
        """Double clicks at specified coordinates."""
        return self.click(x=x, y=y, clicks=2, interval=0.15)

    def right_click(self, x: Optional[int] = None, y: Optional[int] = None) -> bool:
        """Right clicks at specified coordinates."""
        return self.click(x=x, y=y, button="right")

    def drag_to(self, x: int, y: int, duration: float = 0.5, button: str = "left") -> bool:
        """Drags mouse to (x, y) from current position while holding mouse button."""
        target_x, target_y = self._validate_coordinates(x, y)
        if self.test_mode or not PYAUTOGUI_AVAILABLE:
            logger.info("[MOCK] Mouse dragged to (%d, %d)", target_x, target_y)
            return True

        try:
            pyautogui.dragTo(target_x, target_y, duration=duration, button=button)
            return True
        except pyautogui.FailSafeException:
            logger.critical("Favqulodda to'xtatish (FailSafe) faollashdi!")
            return False
        except Exception as e:
            logger.error("Sichqonchani tortib borishda xatolik: %s", e)
            return False

    def scroll(self, clicks: int, x: Optional[int] = None, y: Optional[int] = None) -> bool:
        """Scrolls mouse wheel. Positive for up, negative for down."""
        if self.test_mode or not PYAUTOGUI_AVAILABLE:
            logger.info("[MOCK] Scrolled %d clicks", clicks)
            return True

        try:
            if x is not None and y is not None:
                safe_x, safe_y = self._validate_coordinates(x, y)
                pyautogui.scroll(clicks, x=safe_x, y=safe_y)
            else:
                pyautogui.scroll(clicks)
            return True
        except Exception as e:
            logger.error("Skroll qilishda xatolik: %s", e)
            return False

    # -------------------------------------------------------------------------
    # 3. Keyboard Operations & Unicode Safety
    # -------------------------------------------------------------------------
    def type_text(self, text: str, interval: float = 0.02, use_clipboard: bool = True) -> bool:
        """
        Types given text into the active window.
        Uses clipboard paste (Ctrl+V) by default to guarantee 100% accurate Uzbek
        diacritics and Unicode characters (o‘, g‘, sh, ch, etc.) on Windows.
        """
        if self.test_mode:
            logger.info("[MOCK] Typed text: %s", text)
            return True

        if not text:
            return True

        has_unicode = any(ord(c) > 127 for c in text)

        if (use_clipboard or has_unicode) and PYPERCLIP_AVAILABLE:
            try:
                old_clip = ""
                try:
                    old_clip = pyperclip.paste()
                except Exception:
                    pass

                pyperclip.copy(text)
                time.sleep(0.05)
                self.press_hotkey("ctrl", "v")
                time.sleep(0.05)

                if old_clip:
                    try:
                        pyperclip.copy(old_clip)
                    except Exception:
                        pass
                return True
            except Exception as e:
                logger.warning("Clipboard paste failed, falling back to typewrite: %s", e)

        if PYAUTOGUI_AVAILABLE:
            try:
                pyautogui.typewrite(text, interval=interval)
                return True
            except Exception as e:
                logger.error("Matn kiritishda xatolik: %s", e)
                return False

        return False

    def press_hotkey(self, *keys: str) -> bool:
        """Executes hotkey combination, e.g. press_hotkey('ctrl', 'c')."""
        if self.test_mode or not PYAUTOGUI_AVAILABLE:
            logger.info("[MOCK] Pressed hotkey: %s", keys)
            return True

        try:
            pyautogui.hotkey(*keys)
            return True
        except Exception as e:
            logger.error("Tezkor tugmalarni bosishda xatolik: %s", e)
            return False

    def press_key(self, key: str, presses: int = 1) -> bool:
        """Presses a single key, e.g. 'enter', 'esc', 'tab'."""
        if self.test_mode or not PYAUTOGUI_AVAILABLE:
            logger.info("[MOCK] Pressed key: %s (x%d)", key, presses)
            return True

        try:
            pyautogui.press(key, presses=presses)
            return True
        except Exception as e:
            logger.error("Tugmani bosishda xatolik: %s", e)
            return False


_gui_actions: Optional[GuiActions] = None


def get_gui_actions() -> GuiActions:
    """Singleton getter for GuiActions."""
    global _gui_actions
    if _gui_actions is None:
        _gui_actions = GuiActions()
    return _gui_actions
