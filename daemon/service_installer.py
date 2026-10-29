"""
daemon/service_installer.py — Windows Task Scheduler Service Installer
Registers JARVIS Elevated Daemon to run with highest administrator privileges on system logon.
"""

from __future__ import annotations

import logging
import os
import subprocess
import sys
from pathlib import Path

# UTF-8 console output
if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        ctypes.windll.kernel32.SetConsoleCP(65001)
    except Exception:
        pass

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")
logger = logging.getLogger("JARVIS.ServiceInstaller")

TASK_NAME = "JARVIS_OMNI_DAEMON"


def get_paths() -> tuple[Path, Path]:
    workspace_root = Path(__file__).resolve().parent.parent
    python_exe = workspace_root / "venv" / "Scripts" / "python.exe"
    script_path = workspace_root / "daemon" / "elevated_server.py"
    return python_exe, script_path


def install_scheduled_task() -> bool:
    """Registers the daemon in Windows Task Scheduler with highest privileges."""
    python_exe, script_path = get_paths()

    if not python_exe.exists():
        logger.error("Python executable not found at: %s", python_exe)
        return False

    if not script_path.exists():
        logger.error("Daemon script not found at: %s", script_path)
        return False

    # schtasks command to create elevated logon task
    cmd = [
        "schtasks.exe",
        "/create",
        "/tn", TASK_NAME,
        "/tr", f'"{python_exe}" "{script_path}"',
        "/sc", "onlogon",
        "/rl", "highest",
        "/f",
    ]

    try:
        logger.info("Registering '%s' in Windows Task Scheduler...", TASK_NAME)
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if res.returncode == 0:
            logger.info("Successfully registered task: %s", res.stdout.strip())
            return True
        else:
            logger.error("Failed to register task: %s", res.stderr.strip())
            return False
    except Exception as e:
        logger.error("Exception while registering task: %s", e)
        return False


def start_scheduled_task() -> bool:
    """Triggers the scheduled task immediately."""
    cmd = ["schtasks.exe", "/run", "/tn", TASK_NAME]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if res.returncode == 0:
            logger.info("Successfully started task '%s'", TASK_NAME)
            return True
        else:
            logger.warning("Could not start task '%s': %s", TASK_NAME, res.stderr.strip())
            return False
    except Exception as e:
        logger.error("Exception starting task: %s", e)
        return False


def stop_scheduled_task() -> bool:
    """Stops the running scheduled task."""
    cmd = ["schtasks.exe", "/end", "/tn", TASK_NAME]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        return res.returncode == 0
    except Exception:
        return False


def uninstall_scheduled_task() -> bool:
    """Deletes the scheduled task from Windows Task Scheduler."""
    cmd = ["schtasks.exe", "/delete", "/tn", TASK_NAME, "/f"]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        return res.returncode == 0
    except Exception:
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "uninstall":
        uninstall_scheduled_task()
    elif len(sys.argv) > 1 and sys.argv[1] == "start":
        start_scheduled_task()
    elif len(sys.argv) > 1 and sys.argv[1] == "stop":
        stop_scheduled_task()
    else:
        success = install_scheduled_task()
        if success:
            start_scheduled_task()
