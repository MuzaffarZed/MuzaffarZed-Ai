"""
daemon/elevated_server.py — High-Integrity Resident Background Daemon for J.A.R.V.I.S
Runs locally on 127.0.0.1:8765 to execute high-privilege and background OS operations,
bypassing standard user UAC constraints and providing 24/7 autonomous availability.
"""

from __future__ import annotations

import ctypes
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import psutil
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Ensure project root is in sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from bridge.windows_controller import get_windows_controller

# Windows console UTF-8 config
if sys.platform == "win32":
    try:
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        ctypes.windll.kernel32.SetConsoleCP(65001)
    except Exception:
        pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("JARVIS.Daemon.ElevatedServer")

app = FastAPI(
    title="JARVIS Elevated OS Daemon",
    description="High-Integrity Local Service for Universal Windows Control",
    version="3.0.0",
)

controller = get_windows_controller()


def is_admin() -> bool:
    """Checks whether the daemon is running with elevated administrator privileges."""
    if sys.platform != "win32":
        return False
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


# Request Models
class CommandRequest(BaseModel):
    command: str
    timeout: int = 30


class LaunchRequest(BaseModel):
    target: str


class HotkeyRequest(BaseModel):
    keys: List[str]


class ClickRequest(BaseModel):
    x: int
    y: int
    button: str = "left"
    clicks: int = 1


class TypeRequest(BaseModel):
    text: str


class FocusRequest(BaseModel):
    query: str


# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.get("/health")
def health_check() -> Dict[str, Any]:
    """Returns daemon health status and administrator elevation level."""
    return {
        "status": "online",
        "service": "JARVIS_OMNI_DAEMON",
        "is_admin": is_admin(),
        "pid": os.getpid(),
        "python": sys.version.split()[0],
    }


@app.get("/telemetry")
def get_telemetry() -> Dict[str, Any]:
    """Retrieves hardware and system telemetry."""
    return controller.get_system_telemetry()


@app.get("/windows")
def list_windows(include_invisible: bool = False) -> List[Dict[str, Any]]:
    """Lists desktop windows."""
    return [w.to_dict() for w in controller.list_windows(include_invisible=include_invisible)]


@app.post("/focus")
def focus_window(req: FocusRequest) -> Dict[str, Any]:
    """Focuses a desktop window."""
    ok = controller.focus_window(req.query)
    return {"success": ok, "query": req.query}


@app.post("/exec")
def execute_command(req: CommandRequest) -> Dict[str, Any]:
    """Executes a PowerShell command with elevated daemon privileges."""
    res = controller.run_powershell(req.command, timeout=req.timeout)
    return res


@app.post("/launch")
def launch_application(req: LaunchRequest) -> Dict[str, Any]:
    """Launches an application or URL."""
    ok = controller.launch_app(req.target)
    return {"success": ok, "target": req.target}


@app.post("/click")
def mouse_click(req: ClickRequest) -> Dict[str, Any]:
    """Performs mouse click at coordinates (x, y)."""
    ok = controller.mouse_click(x=req.x, y=req.y, button=req.button, clicks=req.clicks)
    return {"success": ok, "x": req.x, "y": req.y}


@app.post("/type")
def type_text(req: TypeRequest) -> Dict[str, Any]:
    """Types text safely."""
    ok = controller.type_text(req.text)
    return {"success": ok}


@app.post("/hotkey")
def press_hotkey(req: HotkeyRequest) -> Dict[str, Any]:
    """Presses key combination."""
    ok = controller.press_hotkey(*req.keys)
    return {"success": ok, "keys": req.keys}


@app.get("/screenshot")
def take_screenshot() -> Dict[str, Any]:
    """Takes a screenshot and returns base64 and file path."""
    return controller.capture_screen()


def start_daemon(host: str = "127.0.0.1", port: int = 8765) -> None:
    """Starts the Uvicorn web server."""
    import uvicorn
    logger.info("Starting JARVIS Elevated Daemon on http://%s:%d (Admin: %s)", host, port, is_admin())
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    start_daemon()
