"""
Unit tests for Senses Subsystem (VoiceEngine)
"""

import os
import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

os.environ["JARVIS_TEST_MODE"] = "1"

from senses.voice import VoiceEngine, get_voice_engine


def test_voice_engine_init():
    voice = VoiceEngine()
    assert voice is not None
    assert voice.test_mode is True
    assert voice.voice_name == "uz-UZ-MadinaNeural"


def test_voice_speak_test_mode():
    voice = VoiceEngine()
    res = voice.speak("Salom, janob!")
    assert res is True

    res_offline = voice.speak_offline("Offline sinov")
    assert res_offline is True


def test_voice_cues():
    voice = VoiceEngine()
    # In test mode, cues execute without making sound
    voice.play_cue("listen_start")
    voice.play_cue("command_recognized")
    voice.play_cue("done")
    voice.play_cue("error")


def test_voice_singleton():
    v1 = get_voice_engine()
    v2 = get_voice_engine()
    assert v1 is v2
