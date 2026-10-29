"""
bridge/mcp_server.py — Official Model Context Protocol (MCP) Server for Windows 10/11
Exposes native Windows desktop and UI Automation tools to Antigravity and AI agents.
Compatible with MCP SDK 2.x standard stdio transport.
"""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Ensure project root is in sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from mcp.server.mcpserver import MCPServer
from bridge.windows_controller import WindowsController, get_windows_controller

# Set UTF-8 encoding for standard streams
if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        ctypes.windll.kernel32.SetConsoleCP(65001)
    except Exception:
        pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stderr,  # MCP stdio protocol uses stdout for JSON-RPC; logs must go to stderr
)
logger = logging.getLogger("JARVIS.Bridge.MCPServer")

# Initialize MCP Server
app = MCPServer(
    name="jarvis-windows-controller",
    instructions=(
        "Universal Windows 10/11 OS & UI Automation Controller for J.A.R.V.I.S. "
        "Provides tools to inspect desktop windows, interact with UI Automation elements, "
        "launch and manage applications, control mouse and keyboard, and capture screenshots."
    ),
)

controller: WindowsController = get_windows_controller()


# =============================================================================
# 1. WINDOW MANAGEMENT TOOLS
# =============================================================================

@app.tool()
def windows_list_windows(include_invisible: bool = False) -> List[Dict[str, Any]]:
    """
    Lists all desktop windows with title, process name, PID, HWND, and geometry.
    Set include_invisible=True to enumerate non-visible background windows.
    """
    windows = controller.list_windows(include_invisible=include_invisible)
    return [w.to_dict() for w in windows]


@app.tool()
def windows_get_active_window() -> Dict[str, Any]:
    """Returns details (title, process name, PID, bounding rect) of the active foreground window."""
    active = controller.get_active_window()
    if active:
        return {"success": True, "window": active.to_dict()}
    return {"success": False, "message": "No active foreground window found"}


@app.tool()
def windows_focus_window(query: str) -> Dict[str, Any]:
    """
    Brings matching window (by title substring or process name) to the foreground,
    restoring it if minimized, and attaches thread input to bypass Windows focus lock.
    """
    ok = controller.focus_window(query)
    return {
        "success": ok,
        "query": query,
        "message": f"Window '{query}' focused successfully" if ok else f"Failed to focus window matching '{query}'",
    }


@app.tool()
def windows_close_window(query: str) -> Dict[str, Any]:
    """Closes matching window gracefully via WM_CLOSE."""
    ok = controller.close_window(query)
    return {
        "success": ok,
        "query": query,
        "message": f"Window '{query}' closed" if ok else f"Window '{query}' not found or could not be closed",
    }


# =============================================================================
# 2. APPLICATION ORCHESTRATION
# =============================================================================

@app.tool()
def windows_launch_app(target: str) -> Dict[str, Any]:
    """
    Launches an application or opens a file/URL.
    Supported shortcuts: 'chrome', 'edge', 'telegram', 'notepad', 'calc', 'vscode', 'explorer', 'cmd', 'terminal', 'taskmgr'.
    Also accepts any executable path or web URL (e.g. 'https://youtube.com').
    """
    ok = controller.launch_app(target)
    return {
        "success": ok,
        "target": target,
        "message": f"Application '{target}' launched successfully" if ok else f"Failed to launch '{target}'",
    }


@app.tool()
def windows_kill_process(query: str) -> Dict[str, Any]:
    """Kills a process by name (e.g. 'notepad.exe') or PID."""
    ok = controller.kill_process(query)
    return {
        "success": ok,
        "query": query,
        "message": f"Process '{query}' terminated" if ok else f"Process '{query}' not found",
    }


# =============================================================================
# 3. DEEP UI AUTOMATION (UIA)
# =============================================================================

@app.tool()
def windows_inspect_ui(window_query: str = "", max_depth: int = 3) -> List[Dict[str, Any]]:
    """
    Inspects the UI Automation element tree of a window.
    Returns elements (buttons, edit controls, menus, tabs, list items) with Name, ControlType, AutomationId, and bounds.
    """
    elements = controller.inspect_ui(
        window_query=window_query if window_query else None,
        max_depth=max_depth,
    )
    return [el.to_dict() for el in elements]


@app.tool()
def windows_click_ui_element(
    element_name: str,
    window_query: str = "",
    control_type: str = "",
) -> Dict[str, Any]:
    """
    Finds a UI element by its accessibility Name or AutomationId in the UI Automation tree and clicks it.
    Uses native UIA InvokePattern first, with fallback to physical coordinate click.
    """
    ok = controller.click_ui_element(
        element_name=element_name,
        window_query=window_query if window_query else None,
        control_type=control_type if control_type else None,
    )
    return {
        "success": ok,
        "element_name": element_name,
        "window_query": window_query,
        "message": f"Clicked UI element '{element_name}'" if ok else f"Failed to click UI element '{element_name}'",
    }


@app.tool()
def windows_set_control_text(
    element_name: str,
    text: str,
    window_query: str = "",
) -> Dict[str, Any]:
    """Sets text inside an edit control or input field identified by its accessibility Name or AutomationId."""
    ok = controller.set_control_text(
        element_name=element_name,
        text=text,
        window_query=window_query if window_query else None,
    )
    return {
        "success": ok,
        "element_name": element_name,
        "text_length": len(text),
        "message": f"Text set on '{element_name}'" if ok else f"Failed to set text on '{element_name}'",
    }


# =============================================================================
# 4. KEYBOARD & MOUSE SYSTEM INPUT
# =============================================================================

@app.tool()
def windows_type_text(text: str) -> Dict[str, Any]:
    """
    Types text into the currently active control.
    Supports Unicode and Uzbek diacritics (o‘, g‘, sh, ch) flawlessly via clipboard paste.
    """
    ok = controller.type_text(text)
    return {
        "success": ok,
        "text": text,
        "message": "Text typed successfully" if ok else "Failed to type text",
    }


@app.tool()
def windows_press_hotkey(keys: List[str]) -> Dict[str, Any]:
    """
    Presses a key combination (e.g. ['alt', 'f4'], ['ctrl', 's'], ['ctrl', 'shift', 'esc'], ['win', 'd'], ['enter']).
    """
    ok = controller.press_hotkey(*keys)
    return {
        "success": ok,
        "keys": keys,
        "message": f"Hotkey {'+'.join(keys)} pressed" if ok else f"Failed to press hotkey {'+'.join(keys)}",
    }


@app.tool()
def windows_mouse_click(
    x: int,
    y: int,
    button: str = "left",
    clicks: int = 1,
) -> Dict[str, Any]:
    """Clicks at screen coordinates (x, y) with specified mouse button and click count."""
    ok = controller.mouse_click(x=x, y=y, button=button, clicks=clicks)
    return {
        "success": ok,
        "x": x,
        "y": y,
        "button": button,
        "clicks": clicks,
        "message": f"Mouse {button} clicked at ({x}, {y})" if ok else f"Failed to click at ({x}, {y})",
    }


@app.tool()
def windows_mouse_move(x: int, y: int) -> Dict[str, Any]:
    """Moves the mouse cursor to physical coordinates (x, y)."""
    ok = controller.mouse_move(x=x, y=y)
    return {
        "success": ok,
        "x": x,
        "y": y,
    }


@app.tool()
def windows_mouse_scroll(clicks: int) -> Dict[str, Any]:
    """Scrolls mouse wheel. Positive value scrolls up, negative value scrolls down."""
    ok = controller.mouse_scroll(clicks)
    return {
        "success": ok,
        "clicks": clicks,
    }


# =============================================================================
# 5. SCREEN PERCEPTION & TELEMETRY
# =============================================================================

@app.tool()
def windows_capture_screen(save_path: str = "") -> Dict[str, Any]:
    """
    Captures a high-resolution screenshot.
    Returns image dimensions, file path, and base64 encoded PNG for multimodal reasoning.
    """
    res = controller.capture_screen(save_path=save_path if save_path else None)
    return res


@app.tool()
def windows_system_telemetry() -> Dict[str, Any]:
    """Retrieves CPU %, RAM %, Disk space, Battery percentage, and power source telemetry."""
    return controller.get_system_telemetry()


@app.tool()
def windows_run_powershell(command: str) -> Dict[str, Any]:
    """Executes a PowerShell command in a UTF-8 environment and returns stdout, stderr, and exit code."""
    return controller.run_powershell(command)


# =============================================================================
# 6. SENTINEL & COGNITIVE CORTEX TOOLS (by MuzaffarZed)
# =============================================================================

@app.tool()
def jarvis_cognitive_spark(context: str = "") -> Dict[str, Any]:
    """
    JARVISning insoniy intellekt va g'oyalar generatori.
    Atrof-muhitni, tizim holatini, o'yinlarni va mediakutubxonani tahlil qilib,
    yangi amaliy g'oyalar va mayda detallargacha puxta o'ylangan rejalarni taqdim etadi.
    """
    from MuzaffarZed_Sentinel.cognitive_cortex import cortex_instance
    ideas = cortex_instance.generate_proactive_ideas()
    env = cortex_instance.sense_environment()
    return {
        "success": True,
        "environment": env,
        "total_ideas": len(ideas),
        "ideas": ideas,
        "signature": "by MuzaffarZed"
    }


@app.tool()
def jarvis_execute_idea(idea_id: str) -> Dict[str, Any]:
    """
    JARVIS tomonidan tavsiya etilgan proaktiv g'oyani (masalan: IDEA-SYS-TEMP-PURGE, IDEA-GAME-TURBO-SHIELD)
    avtonom ravishda xatolarsiz (Zero-Defect) amalga oshiradi.
    """
    from MuzaffarZed_Sentinel.cognitive_cortex import cortex_instance
    return cortex_instance.execute_idea(idea_id)


@app.tool()
def jarvis_turbo_boost() -> Dict[str, Any]:
    """
    Tizim xotirasini (RAM) tozalaydi, bo'shatadi va ishlayotgan o'yinlar hamda
    asosiy dasturlarga yuqori CPU prioritetini biriktiradi.
    """
    from MuzaffarZed_Sentinel.sentinel import boost_ram, boost_active_games
    ram_res = boost_ram()
    boosted_games = boost_active_games()
    return {
        "success": True,
        "ram_boost": ram_res,
        "boosted_games": boosted_games,
        "signature": "by MuzaffarZed"
    }


@app.tool()
def jarvis_download_music(query: str, format_type: str = "mp3") -> Dict[str, Any]:
    """
    YouTube va internetdan eng yuqori sifatdagi 320 kbps MP3 musiqa yoki 1080p MP4 videoni
    to'g'ridan-to'g'ri 'Desktop\\Musiqa_Fleshka_2026' katalogiga yuklab oladi.
    """
    from MuzaffarZed_Sentinel.media_forge import MediaForge
    forge = MediaForge()
    res = forge.download(query, is_video=(format_type.lower() == "mp4"))
    return res


@app.tool()
def jarvis_audit_desktop() -> Dict[str, Any]:
    """
    Ish stolidagi barcha yorliqlarni to'liq sanitariya tekshiruvidan o'tkazadi,
    oq qog'ozli yoki nishoni buzilgan yorliqlarni bartaraf etib, estetik tartibni saqlaydi.
    """
    from MuzaffarZed_Sentinel.system_guardian import audit_and_repair_desktop_shortcuts, get_system_health
    repaired = audit_and_repair_desktop_shortcuts()
    health = get_system_health()
    return {
        "success": True,
        "repaired_shortcuts": repaired,
        "system_health": health,
        "signature": "by MuzaffarZed"
    }


def main() -> None:
    """Main entrypoint for MCP Server stdio transport."""
    logger.info("Starting JARVIS Windows Controller MCP Server...")
    app.run(transport="stdio")


if __name__ == "__main__":
    main()
