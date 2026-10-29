"""
bridge/windows_controller.py — Universal Windows 10/11 Desktop Controller
Master-Level OS Integration Engine for J.A.R.V.I.S & Antigravity.

Features:
1. Deep UI Automation (UIA): Inspect control tree, locate elements by Name/AutomationId, invoke or click.
2. Win32 Window Management: Robust focus activation (bypassing Windows foreground restrictions), enumerate windows, minimize/maximize/close.
3. System Input Automation: Unicode-safe typing (Uzbek diacritics o‘, g‘, sh, ch), global hotkeys, coordinate mouse operations with fail-safe.
4. Application Orchestration: Instant launch of standard and custom Windows apps.
5. High-Resolution Perception: DPI-aware screen capture and window bbox grabbing.
6. Hardware Telemetry & Media: CPU, RAM, Disk, Battery, and master volume control.
"""

from __future__ import annotations

import base64
import ctypes
import io
import logging
import os
import subprocess
import sys
import threading
import time
import webbrowser
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar

import psutil

# Safe imports for GUI & OS automation
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.05
except ImportError:
    pyautogui = None  # type: ignore
    PYAUTOGUI_AVAILABLE = False

try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    pyperclip = None  # type: ignore
    PYPERCLIP_AVAILABLE = False

try:
    from PIL import Image, ImageGrab
    IMAGEGRAB_AVAILABLE = True
except ImportError:
    Image = None  # type: ignore
    ImageGrab = None  # type: ignore
    IMAGEGRAB_AVAILABLE = False

try:
    import win32con
    import win32gui
    import win32process
    import win32ui
    WIN32_AVAILABLE = True
except ImportError:
    win32gui = None  # type: ignore
    win32con = None  # type: ignore
    win32process = None  # type: ignore
    win32ui = None  # type: ignore
    WIN32_AVAILABLE = False

try:
    import uiautomation as uia
    UIA_AVAILABLE = True
except ImportError:
    uia = None  # type: ignore
    UIA_AVAILABLE = False

logger = logging.getLogger("JARVIS.Bridge.WindowsController")


@dataclass
class WindowInfo:
    """Represents a visible desktop window."""
    hwnd: int
    title: str
    process_name: str
    pid: int
    rect: Tuple[int, int, int, int]  # left, top, right, bottom
    is_active: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class UIControlInfo:
    """Represents a UI element in the Windows Accessibility / UI Automation tree."""
    name: str
    control_type: str
    automation_id: str
    class_name: str
    rect: Tuple[int, int, int, int]
    is_enabled: bool = True
    depth: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class WindowsController:
    """Master controller for all Windows 10/11 operating system interactions."""

    KNOWN_APPS: Dict[str, List[str]] = {
        "notepad": ["notepad.exe"],
        "bloknot": ["notepad.exe"],
        "calc": ["calc.exe"],
        "kalkulyator": ["calc.exe"],
        "calculator": ["calc.exe"],
        "explorer": ["explorer.exe"],
        "fayllar": ["explorer.exe"],
        "cmd": ["cmd.exe"],
        "terminal": ["wt.exe", "powershell.exe", "cmd.exe"],
        "powershell": ["powershell.exe"],
        "taskmgr": ["taskmgr.exe"],
        "vazifalar": ["taskmgr.exe"],
        "chrome": [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            "chrome.exe",
        ],
        "edge": [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            "msedge.exe",
        ],
        "telegram": [
            os.path.expandvars(r"%APPDATA%\Telegram Desktop\Telegram.exe"),
            "telegram.exe",
        ],
        "vscode": [
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"),
            "code.exe",
        ],
        "code": [
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"),
            "code.exe",
        ],
    }

    def run_on_default_desktop(self, target_func: Callable[[], Any]) -> Any:
        """
        Executes target_func on a dedicated worker thread attached to the interactive 'default' desktop.
        Essential on Windows when the primary process thread cannot switch desktops after COM/GDI initialization.
        """
        if sys.platform != "win32" or self.test_mode:
            return target_func()

        res: List[Any] = []
        exc: List[Exception] = []

        def worker() -> None:
            try:
                user32 = ctypes.windll.user32
                h_desk = user32.OpenDesktopW("default", 0, False, 0x01FF)
                if h_desk:
                    user32.SetThreadDesktop(h_desk)
                res.append(target_func())
            except Exception as e:
                exc.append(e)

        t = threading.Thread(target=worker, daemon=True)
        t.start()
        t.join(timeout=10.0)

        if exc:
            logger.debug("Exception in run_on_default_desktop: %s", exc[0])
            return None
        return res[0] if res else None

    def ensure_default_desktop(self) -> bool:
        """
        Attaches the calling thread to the user's interactive 'default' desktop on WinSta0.
        Essential for agents/runners executing inside sandboxed desktops or non-interactive window stations.
        """
        if sys.platform != "win32" or self.test_mode:
            return True
        try:
            user32 = ctypes.windll.user32
            # 0x01FF = DESKTOP_ALL_ACCESS
            h_desk = user32.OpenDesktopW("default", 0, False, 0x01FF)
            if h_desk:
                user32.SetThreadDesktop(h_desk)
                return True
        except Exception as e:
            logger.debug("Desktop attachment skipped or failed: %s", e)
        return False

    def __init__(self, workspace_root: Optional[str] = None) -> None:
        self.workspace_root = Path(workspace_root or Path(__file__).resolve().parent.parent)
        self.screenshots_dir = self.workspace_root / "screenshots"
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        self.test_mode = os.getenv("JARVIS_TEST_MODE", "0") == "1"

        self.ensure_default_desktop()

        if PYAUTOGUI_AVAILABLE:
            try:
                pyautogui.FAILSAFE = not self.test_mode
            except Exception:
                pass

        logger.info(
            "WindowsController initialized (TestMode: %s, Win32: %s, UIA: %s)",
            self.test_mode,
            WIN32_AVAILABLE,
            UIA_AVAILABLE,
        )

    # =========================================================================
    # 1. WINDOW DISCOVERY & MANAGEMENT
    # =========================================================================

    def list_windows(self, include_invisible: bool = False) -> List[WindowInfo]:
        """Lists all open windows with title, PID, process name, and rectangle."""
        if self.test_mode or not WIN32_AVAILABLE:
            return [
                WindowInfo(
                    hwnd=1001,
                    title="Visual Studio Code",
                    process_name="Code.exe",
                    pid=1234,
                    rect=(0, 0, 1920, 1080),
                    is_active=True,
                ),
                WindowInfo(
                    hwnd=1002,
                    title="Telegram",
                    process_name="Telegram.exe",
                    pid=5678,
                    rect=(100, 100, 900, 700),
                    is_active=False,
                ),
            ]

        def _do_list() -> List[WindowInfo]:
            windows: List[WindowInfo] = []
            active_hwnd = win32gui.GetForegroundWindow()

            def enum_handler(hwnd: int, extra: Any) -> bool:
                try:
                    if not include_invisible and not win32gui.IsWindowVisible(hwnd):
                        return True
                    title = win32gui.GetWindowText(hwnd).strip()
                    if not title:
                        return True

                    # Check if window has nonzero dimensions
                    rect = win32gui.GetWindowRect(hwnd)
                    width = rect[2] - rect[0]
                    height = rect[3] - rect[1]
                    if width <= 0 or height <= 0:
                        return True

                    proc_name = "unknown"
                    pid = 0
                    try:
                        _, pid = win32process.GetWindowThreadProcessId(hwnd)
                        if pid:
                            proc = psutil.Process(pid)
                            proc_name = proc.name()
                    except Exception:
                        pass

                    windows.append(
                        WindowInfo(
                            hwnd=hwnd,
                            title=title,
                            process_name=proc_name,
                            pid=pid,
                            rect=rect,
                            is_active=(hwnd == active_hwnd),
                        )
                    )
                except Exception:
                    pass
                return True

            try:
                win32gui.EnumWindows(enum_handler, None)
            except Exception:
                pass
            return windows

        result = self.run_on_default_desktop(_do_list)
        return result if result is not None else []

    def get_active_window(self) -> Optional[WindowInfo]:
        """Returns details of the currently focused foreground window."""
        if self.test_mode or not WIN32_AVAILABLE:
            return WindowInfo(
                hwnd=1001,
                title="Visual Studio Code",
                process_name="Code.exe",
                pid=1234,
                rect=(0, 0, 1920, 1080),
                is_active=True,
            )

        def _do_get() -> Optional[WindowInfo]:
            try:
                hwnd = win32gui.GetForegroundWindow()
                if not hwnd:
                    return None
                title = win32gui.GetWindowText(hwnd).strip()
                rect = win32gui.GetWindowRect(hwnd)
                proc_name = "unknown"
                pid = 0
                try:
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    if pid:
                        proc_name = psutil.Process(pid).name()
                except Exception:
                    pass
                return WindowInfo(
                    hwnd=hwnd,
                    title=title,
                    process_name=proc_name,
                    pid=pid,
                    rect=rect,
                    is_active=True,
                )
            except Exception as e:
                logger.error("Error getting active window: %s", e)
                return None

        return self.run_on_default_desktop(_do_get)

    def focus_window(self, query: str) -> bool:
        """
        Brings the matching window to foreground and gives it focus.
        Uses Win32 thread attachment trick to bypass Windows foreground lock.
        """
        if self.test_mode:
            logger.info("TestMode: focus_window('%s') succeeded", query)
            return True

        if not WIN32_AVAILABLE:
            logger.warning("Win32 not available for window focus")
            return False

        target_hwnd = None
        q_lower = query.lower()

        # Find best matching window
        for w in self.list_windows():
            if q_lower in w.title.lower() or q_lower in w.process_name.lower():
                target_hwnd = w.hwnd
                break

        if not target_hwnd:
            logger.warning("No window found matching: '%s'", query)
            return False

        try:
            # If minimized, restore it
            if win32gui.IsIconic(target_hwnd):
                win32gui.ShowWindow(target_hwnd, win32con.SW_RESTORE)
            else:
                win32gui.ShowWindow(target_hwnd, win32con.SW_SHOW)

            # Bypass Windows SetForegroundWindow lock using robust ALT keystroke & SwitchToThisWindow
            ctypes.windll.user32.keybd_event(0x12, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0x12, 0, 2, 0)

            win32gui.BringWindowToTop(target_hwnd)
            ctypes.windll.user32.SwitchToThisWindow(target_hwnd, True)
            try:
                win32gui.SetForegroundWindow(target_hwnd)
            except Exception:
                pass

            # Ensure topmost momentarily then normal to guarantee visibility
            win32gui.SetWindowPos(target_hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
            win32gui.SetWindowPos(target_hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

            time.sleep(0.2)
            return True
        except Exception as e:
            logger.error("Error focusing window %s: %s", target_hwnd, e)
            return False

    def close_window(self, query: str) -> bool:
        """Closes matching window gracefully via WM_CLOSE."""
        if self.test_mode:
            return True
        if not WIN32_AVAILABLE:
            return False

        q_lower = query.lower()
        for w in self.list_windows():
            if q_lower in w.title.lower() or q_lower in w.process_name.lower():
                try:
                    win32gui.PostMessage(w.hwnd, win32con.WM_CLOSE, 0, 0)
                    return True
                except Exception as e:
                    logger.error("Error closing window %s: %s", w.title, e)
                    return False
        return False

    # =========================================================================
    # 2. DEEP UI AUTOMATION (UIA)
    # =========================================================================

    def inspect_ui(self, window_query: Optional[str] = None, max_depth: int = 3) -> List[UIControlInfo]:
        """
        Inspects UI controls hierarchy inside the specified or active window.
        Returns controls with Name, ControlType, AutomationId, and Bounding Box.
        """
        self.ensure_default_desktop()
        results: List[UIControlInfo] = []

        if self.test_mode or not UIA_AVAILABLE:
            return [
                UIControlInfo(
                    name="File",
                    control_type="MenuItem",
                    automation_id="MenuBar.File",
                    class_name="MenuItem",
                    rect=(10, 10, 50, 30),
                    depth=1,
                ),
                UIControlInfo(
                    name="Save",
                    control_type="Button",
                    automation_id="Toolbar.Save",
                    class_name="Button",
                    rect=(60, 10, 100, 30),
                    depth=2,
                ),
            ]

        target_control = None
        try:
            if window_query:
                # 1. First attempt: resolve via HWND (fastest & robust)
                for w in self.list_windows():
                    if window_query.lower() in w.title.lower() or window_query.lower() in w.process_name.lower():
                        try:
                            target_control = uia.ControlFromHandle(w.hwnd)
                            if target_control:
                                break
                        except Exception:
                            pass

                # 2. Fallback: search UIA root children
                if not target_control:
                    root = uia.GetRootControl()
                    for child in root.GetChildren():
                        if window_query.lower() in child.Name.lower():
                            target_control = child
                            break
            else:
                active_win = self.get_active_window()
                if active_win:
                    try:
                        target_control = uia.ControlFromHandle(active_win.hwnd)
                    except Exception:
                        pass
                if not target_control:
                    target_control = uia.GetFocusedControl()
                    if target_control:
                        target_control = target_control.GetTopLevelControl()

            if not target_control:
                target_control = uia.GetRootControl()

            def traverse(ctrl: Any, current_depth: int) -> None:
                if current_depth > max_depth:
                    return

                try:
                    rect = ctrl.BoundingRectangle
                    b_rect = (rect.left, rect.top, rect.right, rect.bottom) if rect else (0, 0, 0, 0)
                    name = ctrl.Name or ""
                    c_type = ctrl.ControlTypeName or ""
                    a_id = ctrl.AutomationId or ""
                    c_name = ctrl.ClassName or ""

                    if name or a_id:
                        results.append(
                            UIControlInfo(
                                name=name,
                                control_type=c_type,
                                automation_id=a_id,
                                class_name=c_name,
                                rect=b_rect,
                                is_enabled=bool(ctrl.IsEnabled),
                                depth=current_depth,
                            )
                        )

                    for child in ctrl.GetChildren():
                        traverse(child, current_depth + 1)
                except Exception:
                    pass

            traverse(target_control, 1)
        except Exception as e:
            logger.error("Error inspecting UI controls: %s", e)

        return results

    def click_ui_element(
        self,
        element_name: str,
        window_query: Optional[str] = None,
        control_type: Optional[str] = None,
    ) -> bool:
        """
        Locates a UI element by Name or AutomationId in the UI Automation tree and clicks it.
        First tries native UIA InvokePattern / TogglePattern, then falls back to coordinate click.
        """
        self.ensure_default_desktop()
        if self.test_mode:
            logger.info("TestMode: click_ui_element('%s') succeeded", element_name)
            return True

        if not UIA_AVAILABLE:
            logger.warning("UIA not available, cannot click element by name")
            return False

        try:
            target_window = None
            if window_query:
                # Check via HWND first
                for w in self.list_windows():
                    if window_query.lower() in w.title.lower() or window_query.lower() in w.process_name.lower():
                        try:
                            target_window = uia.ControlFromHandle(w.hwnd)
                            if target_window:
                                break
                        except Exception:
                            pass

            if not target_window:
                root = uia.GetRootControl()
                target_window = root
                if window_query:
                    for child in root.GetChildren():
                        if window_query.lower() in child.Name.lower():
                            target_window = child
                            break

            target_el = None
            el_lower = element_name.lower()

            def find_child(ctrl: Any, depth: int) -> Optional[Any]:
                if depth > 5:
                    return None
                try:
                    ctrl_name = (ctrl.Name or "").lower()
                    ctrl_aid = (ctrl.AutomationId or "").lower()
                    if el_lower in ctrl_name or el_lower in ctrl_aid:
                        if not control_type or control_type.lower() in (ctrl.ControlTypeName or "").lower():
                            return ctrl

                    for ch in ctrl.GetChildren():
                        res = find_child(ch, depth + 1)
                        if res:
                            return res
                except Exception:
                    pass
                return None

            target_el = find_child(target_window, 1)

            if not target_el:
                logger.warning("UI Element '%s' not found in tree", element_name)
                return False

            # Try native invoke pattern
            try:
                invoke_pattern = target_el.GetInvokePattern()
                if invoke_pattern:
                    invoke_pattern.Invoke()
                    logger.info("UIA InvokePattern executed on '%s'", element_name)
                    return True
            except Exception:
                pass

            # Fallback to physical coordinate click
            rect = target_el.BoundingRectangle
            if rect:
                cx = (rect.left + rect.right) // 2
                cy = (rect.top + rect.bottom) // 2
                return self.mouse_click(cx, cy)

            return False
        except Exception as e:
            logger.error("Error clicking UI element '%s': %s", element_name, e)
            return False

    def set_control_text(
        self,
        element_name: str,
        text: str,
        window_query: Optional[str] = None,
    ) -> bool:
        """Sets text on an edit control using ValuePattern or focus + clipboard paste."""
        if self.test_mode:
            return True

        if not UIA_AVAILABLE:
            return False

        try:
            if self.click_ui_element(element_name, window_query=window_query, control_type="Edit"):
                time.sleep(0.1)
                return self.type_text(text)
            return False
        except Exception as e:
            logger.error("Error setting control text: %s", e)
            return False

    # =========================================================================
    # 3. SYSTEM INPUT & KEYBOARD / MOUSE AUTOMATION
    # =========================================================================

    def type_text(self, text: str) -> bool:
        """
        Types text safely. For Unicode and Uzbek characters (o‘, g‘, sh, ch),
        uses Windows clipboard paste (Ctrl+V) to avoid encoding corruption.
        Uses native Win32 keybd_event to remain immune to cursor parking at screen corners.
        """
        if self.test_mode:
            logger.info("TestMode: type_text('%s') succeeded", text)
            return True

        if not text:
            return True

        try:
            if PYPERCLIP_AVAILABLE:
                old_clip = ""
                try:
                    old_clip = pyperclip.paste()
                except Exception:
                    pass

                pyperclip.copy(text)
                time.sleep(0.05)

                pasted = False
                if sys.platform == "win32":
                    try:
                        user32 = ctypes.windll.user32
                        VK_CONTROL = 0x11
                        VK_V = 0x56
                        KEYEVENTF_KEYUP = 0x0002
                        user32.keybd_event(VK_CONTROL, 0, 0, 0)
                        user32.keybd_event(VK_V, 0, 0, 0)
                        user32.keybd_event(VK_V, 0, KEYEVENTF_KEYUP, 0)
                        user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)
                        pasted = True
                    except Exception:
                        pass

                if not pasted and PYAUTOGUI_AVAILABLE:
                    try:
                        pyautogui.hotkey("ctrl", "v")
                        pasted = True
                    except Exception:
                        pass

                time.sleep(0.05)
                return True
            elif PYAUTOGUI_AVAILABLE:
                try:
                    pyautogui.write(text, interval=0.01)
                    return True
                except Exception:
                    pass
            return False
        except Exception as e:
            logger.error("Error typing text: %s", e)
            return False

    def press_hotkey(self, *keys: str) -> bool:
        """
        Presses a key combination, e.g. press_hotkey('ctrl', 'shift', 'esc') or press_hotkey('alt', 'f4').
        Protected against PyAutoGUI FailSafe exceptions with Win32 fallback.
        """
        if self.test_mode:
            logger.info("TestMode: press_hotkey(%s) succeeded", keys)
            return True

        normalized_keys = [k.lower().strip() for k in keys if k]
        if not normalized_keys:
            return False

        if PYAUTOGUI_AVAILABLE:
            try:
                pyautogui.hotkey(*normalized_keys)
                return True
            except Exception as e:
                logger.debug("PyAutoGUI hotkey failed (%s), attempting Win32 keybd_event", e)

        # Win32 VK mapping fallback
        if sys.platform == "win32":
            vk_map = {
                "ctrl": 0x11, "control": 0x11,
                "alt": 0x12, "menu": 0x12,
                "shift": 0x10,
                "win": 0x5B, "windows": 0x5B,
                "enter": 0x0D, "return": 0x0D,
                "esc": 0x1B, "escape": 0x1B,
                "tab": 0x09, "space": 0x20,
                "backspace": 0x08,
                "f4": 0x73, "f5": 0x74, "f11": 0x7A, "f12": 0x7B,
                "c": 0x43, "v": 0x56, "a": 0x41, "s": 0x53, "z": 0x5A, "y": 0x59, "d": 0x44,
            }
            try:
                user32 = ctypes.windll.user32
                KEYEVENTF_KEYUP = 0x0002
                pressed_vks = []
                for k in normalized_keys:
                    vk = vk_map.get(k) or (ord(k.upper()) if len(k) == 1 and k.isalnum() else None)
                    if vk:
                        user32.keybd_event(vk, 0, 0, 0)
                        pressed_vks.append(vk)
                for vk in reversed(pressed_vks):
                    user32.keybd_event(vk, 0, KEYEVENTF_KEYUP, 0)
                return True
            except Exception as e:
                logger.error("Win32 hotkey fallback failed: %s", e)
        return False

    def mouse_click(self, x: int, y: int, button: str = "left", clicks: int = 1) -> bool:
        """Clicks at specified screen coordinates with bounds checking."""
        self.ensure_default_desktop()
        if self.test_mode:
            logger.info("TestMode: mouse_click(%d, %d, button=%s) succeeded", x, y, button)
            return True

        if not PYAUTOGUI_AVAILABLE:
            return False

        try:
            sw, sh = pyautogui.size()
            safe_x = max(0, min(sw - 1, int(x)))
            safe_y = max(0, min(sh - 1, int(y)))
            pyautogui.click(x=safe_x, y=safe_y, button=button, clicks=clicks)
            return True
        except Exception as e:
            logger.error("Error performing mouse click: %s", e)
            return False

    def mouse_move(self, x: int, y: int) -> bool:
        """Moves the mouse cursor to physical coordinates."""
        self.ensure_default_desktop()
        if self.test_mode:
            return True
        if not PYAUTOGUI_AVAILABLE:
            return False
        try:
            sw, sh = pyautogui.size()
            pyautogui.moveTo(max(0, min(sw - 1, int(x))), max(0, min(sh - 1, int(y))))
            return True
        except Exception as e:
            logger.error("Error moving mouse: %s", e)
            return False

    def mouse_scroll(self, clicks: int) -> bool:
        """Scrolls mouse wheel (positive = up, negative = down)."""
        self.ensure_default_desktop()
        if self.test_mode:
            return True
        if not PYAUTOGUI_AVAILABLE:
            return False
        try:
            pyautogui.scroll(clicks)
            return True
        except Exception as e:
            logger.error("Error scrolling mouse: %s", e)
            return False

    # =========================================================================
    # 4. APPLICATION LAUNCHING & LIFECYCLE
    # =========================================================================

    def launch_app(self, target: str) -> bool:
        """
        Launches standard apps (Chrome, Telegram, Notepad, Calc, Explorer, Terminal)
        or custom file paths, executable commands, or URLs.
        """
        if self.test_mode:
            logger.info("TestMode: launch_app('%s') succeeded", target)
            return True

        t_lower = target.lower().strip()

        # If it's a web URL
        if t_lower.startswith(("http://", "https://", "www.")):
            url = target if target.startswith("http") else f"https://{target}"
            webbrowser.open(url)
            return True

        # Check known apps dictionary
        if t_lower in self.KNOWN_APPS:
            for exe_candidate in self.KNOWN_APPS[t_lower]:
                try:
                    if os.path.isabs(exe_candidate) and os.path.exists(exe_candidate):
                        subprocess.Popen([exe_candidate])
                        return True
                    elif not os.path.isabs(exe_candidate):
                        subprocess.Popen([exe_candidate], shell=True)
                        return True
                except Exception:
                    continue

        # Try launching directly via os.startfile or subprocess
        try:
            if hasattr(os, "startfile"):
                os.startfile(target)
                return True
        except Exception:
            pass

        try:
            subprocess.Popen([target], shell=True)
            return True
        except Exception as e:
            logger.error("Failed to launch application '%s': %s", target, e)
            return False

    def kill_process(self, query: str) -> bool:
        """Terminates processes matching name or PID."""
        if self.test_mode:
            return True

        killed = False
        q_lower = query.lower()

        for proc in psutil.process_iter(["pid", "name"]):
            try:
                name = proc.info["name"] or ""
                pid = str(proc.info["pid"])
                if q_lower in name.lower() or q_lower == pid:
                    proc.kill()
                    killed = True
            except Exception:
                pass
        return killed

    # =========================================================================
    # 5. SCREEN PERCEPTION & CAPTURE
    # =========================================================================

    def capture_window(self, query_or_hwnd: Optional[Any] = None) -> Optional[Any]:
        """
        Captures a specific window using Win32 PrintWindow (PW_RENDERFULLCONTENT).
        Reliable across background and sandboxed window stations.
        """
        self.ensure_default_desktop()
        if self.test_mode or not WIN32_AVAILABLE or not win32ui or not Image:
            return Image.new("RGB", (1280, 720), color=(40, 40, 40)) if Image else None

        target_hwnd = None
        if isinstance(query_or_hwnd, int):
            target_hwnd = query_or_hwnd
        elif isinstance(query_or_hwnd, str) and query_or_hwnd:
            q_lower = query_or_hwnd.lower()
            for w in self.list_windows():
                if q_lower in w.title.lower() or q_lower in w.process_name.lower():
                    target_hwnd = w.hwnd
                    break
        else:
            active_w = self.get_active_window()
            if active_w and active_w.hwnd:
                target_hwnd = active_w.hwnd
            else:
                wins = self.list_windows()
                if wins:
                    target_hwnd = wins[0].hwnd

        if not target_hwnd:
            return None

        try:
            r = win32gui.GetWindowRect(target_hwnd)
            w = r[2] - r[0]
            h = r[3] - r[1]
            if w <= 0 or h <= 0:
                return None

            hwnd_dc = win32gui.GetWindowDC(target_hwnd)
            mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
            save_dc = mfc_dc.CreateCompatibleDC()
            save_bitmap = win32ui.CreateBitmap()
            save_bitmap.CreateCompatibleBitmap(mfc_dc, w, h)
            save_dc.SelectObject(save_bitmap)

            # 2 = PW_RENDERFULLCONTENT
            res = ctypes.windll.user32.PrintWindow(target_hwnd, save_dc.GetSafeHdc(), 2)
            im = None
            if res:
                bmpinfo = save_bitmap.GetInfo()
                bmpstr = save_bitmap.GetBitmapBits(True)
                im = Image.frombuffer("RGB", (bmpinfo["bmWidth"], bmpinfo["bmHeight"]), bmpstr, "raw", "BGRX", 0, 1)

            win32gui.DeleteObject(save_bitmap.GetHandle())
            save_dc.DeleteDC()
            mfc_dc.DeleteDC()
            win32gui.ReleaseDC(target_hwnd, hwnd_dc)
            return im
        except Exception as e:
            logger.error("Error capturing window %s: %s", target_hwnd, e)
            return None

    def capture_screen(
        self,
        bbox: Optional[Tuple[int, int, int, int]] = None,
        save_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Captures a high-resolution screenshot (full desktop, active window, or bbox).
        Returns base64 PNG data, dimensions, and saved file path if requested.
        """
        self.ensure_default_desktop()
        if self.test_mode or not Image:
            return {
                "success": True,
                "width": 1920,
                "height": 1080,
                "base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=",
                "file_path": save_path or str(self.screenshots_dir / "test_screen.png"),
            }

        img = None
        if IMAGEGRAB_AVAILABLE and ImageGrab:
            try:
                img = ImageGrab.grab(bbox=bbox, all_screens=True)
            except Exception as e:
                logger.debug("ImageGrab failed (%s), attempting PrintWindow fallback", e)

        if img is None:
            img = self.capture_window()

        if img is None and Image:
            # Fallback canvas
            img = Image.new("RGB", (1920, 1080), color=(25, 25, 35))

        if img is None:
            return {"success": False, "error": "Unable to initialize image capture buffer"}

        try:
            w, h = img.size
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            b64_str = base64.b64encode(buf.getvalue()).decode("utf-8")

            final_path = save_path
            if not final_path:
                ts = int(time.time())
                final_path = str(self.screenshots_dir / f"screenshot_{ts}.png")
            img.save(final_path, format="PNG")

            return {
                "success": True,
                "width": w,
                "height": h,
                "base64": b64_str,
                "file_path": final_path,
            }
        except Exception as e:
            logger.error("Error saving screen capture: %s", e)
            return {"success": False, "error": str(e)}

    # =========================================================================
    # 6. HARDWARE TELEMETRY & SYSTEM UTILITIES
    # =========================================================================

    def get_system_telemetry(self) -> Dict[str, Any]:
        """Retrieves CPU, RAM, Disk, and Battery hardware metrics."""
        telemetry: Dict[str, Any] = {
            "cpu_percent": 0.0,
            "ram_percent": 0.0,
            "ram_used_gb": 0.0,
            "ram_total_gb": 0.0,
            "disk_free_gb": 0.0,
            "disk_total_gb": 0.0,
            "battery_percent": None,
            "power_plugged": None,
        }

        try:
            telemetry["cpu_percent"] = psutil.cpu_percent(interval=0.1)
            mem = psutil.virtual_memory()
            telemetry["ram_percent"] = mem.percent
            telemetry["ram_used_gb"] = round(mem.used / (1024**3), 2)
            telemetry["ram_total_gb"] = round(mem.total / (1024**3), 2)

            disk = psutil.disk_usage("C:\\")
            telemetry["disk_free_gb"] = round(disk.free / (1024**3), 2)
            telemetry["disk_total_gb"] = round(disk.total / (1024**3), 2)

            battery = psutil.sensors_battery()
            if battery:
                telemetry["battery_percent"] = battery.percent
                telemetry["power_plugged"] = battery.power_plugged
        except Exception as e:
            logger.error("Error retrieving telemetry: %s", e)

        return telemetry

    def run_powershell(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        """Executes a PowerShell command with UTF-8 encoding support."""
        if self.test_mode:
            return {"success": True, "stdout": "Test mode execution OK", "stderr": "", "exit_code": 0}

        try:
            full_cmd = ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command]
            proc = subprocess.run(
                full_cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
            )
            return {
                "success": proc.returncode == 0,
                "stdout": proc.stdout.strip(),
                "stderr": proc.stderr.strip(),
                "exit_code": proc.returncode,
            }
        except Exception as e:
            logger.error("Error executing PowerShell command: %s", e)
            return {"success": False, "stdout": "", "stderr": str(e), "exit_code": -1}


_controller_instance: Optional[WindowsController] = None


def get_windows_controller() -> WindowsController:
    """Singleton getter for WindowsController."""
    global _controller_instance
    if _controller_instance is None:
        _controller_instance = WindowsController()
    return _controller_instance
