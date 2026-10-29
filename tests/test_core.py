"""
Unit tests for Core Orchestrator (JarvisCore)
"""

import os
import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

os.environ["JARVIS_TEST_MODE"] = "1"

from main import JarvisCore


def test_jarvis_core_lifecycle():
    core = JarvisCore()
    assert core.voice is not None
    assert core.brain is not None
    assert core.actions is not None
    assert core.gui is not None
    assert core.vision is not None

    # Test processing time command
    keep_running = core.process_command("Vaqt necha bo'ldi?")
    assert keep_running is True

    # Test Vision Describe command
    assert core.process_command("Ekranga qara") is True

    # Test Vision Locate command
    assert core.process_command("Ekrandan Start tugmasini top") is True

    # Test GUI Click command (uses Vision + GUI Actions)
    assert core.process_command("Start tugmasini bos") is True

    # Test GUI Type command
    assert core.process_command("Matn kirit: Salom janob Muzaffar") is True

    # Test GUI Hotkey command
    assert core.process_command("Alt F4 bos") is True

    # Test exit command
    should_stop = core.process_command("Dasturni to'xtat")
    assert should_stop is False
    assert core.running is False
