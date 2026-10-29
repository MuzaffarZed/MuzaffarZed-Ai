"""
bridge — J.A.R.V.I.S Windows & MCP Integration Bridge
Connects Antigravity and external autonomous clients directly to the Windows 10/11 operating system.
"""

from bridge.windows_controller import WindowsController, get_windows_controller

__all__ = ["WindowsController", "get_windows_controller"]
