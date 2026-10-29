"""
Unit tests for GUI Actions Subsystem (GuiActions)
"""

import os
import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

os.environ["JARVIS_TEST_MODE"] = "1"

from actions.gui_actions import GuiActions, get_gui_actions


def test_gui_actions_mouse_operations():
    gui = GuiActions(screen_width=1920, screen_height=1080)
    assert gui.screen_size == (1920, 1080)

    # Mouse moves
    assert gui.move_to(500, 500) is True
    # Clamping out-of-bounds coordinates
    assert gui.move_to(5000, -100) is True

    # Clicks
    assert gui.click(100, 200) is True
    assert gui.double_click(300, 400) is True
    assert gui.right_click(500, 600) is True

    # Drag and Scroll
    assert gui.drag_to(800, 800) is True
    assert gui.scroll(-300) is True
    assert gui.scroll(300, x=500, y=500) is True


def test_gui_actions_keyboard_and_unicode_typing():
    gui = GuiActions()

    # Unicode typing (Uzbek letters)
    assert gui.type_text("Assalomu alaykum, O‘zbekiston!") is True
    assert gui.type_text("Go'zal shahar — Toshkent") is True

    # Hotkeys
    assert gui.press_hotkey("ctrl", "c") is True
    assert gui.press_hotkey("alt", "f4") is True
    assert gui.press_key("enter") is True
    assert gui.press_key("esc") is True


def test_gui_actions_window_management():
    gui = GuiActions()

    title = gui.get_active_window_title()
    assert len(title) > 0

    assert gui.focus_window("Visual Studio Code") is True
    assert gui.minimize_active_window() is True
    assert gui.maximize_active_window() is True


def test_gui_actions_singleton():
    g1 = get_gui_actions()
    g2 = get_gui_actions()
    assert g1 is g2
