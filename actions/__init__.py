"""
JARVIS-Core — Actions Subsystem
Provides operating system control, GUI automation (mouse/keyboard), application launching, media management, and telemetry.
"""

from .system_actions import SystemActions, get_system_actions
from .gui_actions import GuiActions, get_gui_actions

__all__ = [
    "SystemActions",
    "get_system_actions",
    "GuiActions",
    "get_gui_actions",
]
