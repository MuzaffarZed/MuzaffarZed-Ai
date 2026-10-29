"""tests/test_streaming_voice.py - Unit tests for StreamingVoiceEngine with Barge-In."""

import pytest
from senses.streaming_voice import StreamingVoiceEngine, get_streaming_voice


def test_streaming_voice_singleton():
    v1 = get_streaming_voice(test_mode=True)
    v2 = get_streaming_voice(test_mode=True)
    assert v1 is v2
    assert isinstance(v1, StreamingVoiceEngine)


def test_streaming_voice_speak_test_mode():
    v = StreamingVoiceEngine(test_mode=True)
    started = False
    finished = False

    def on_s():
        nonlocal started
        started = True

    def on_f():
        nonlocal finished
        finished = True

    res = v.speak("Salom Muzaffar janoblari", on_start=on_s, on_finish=on_f)
    assert res is True
    assert started is True
    assert finished is True


def test_streaming_voice_interrupt():
    v = StreamingVoiceEngine(test_mode=True)
    v.interrupt()
    assert v.is_speaking is False


def test_streaming_voice_hud_status():
    hud = StreamingVoiceEngine.get_hud_status("GEMINI ONLINE", "ReAct Tsikl")
    assert "CPU:" in hud
    assert "RAM:" in hud
    assert "● GEMINI ONLINE" in hud
    assert "Tsikl: ReAct Tsikl" in hud
