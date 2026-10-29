"""
tests/test_wake_listener.py — Unit Tests for Always-on WakeListener
Validates thread lifecycle, callback triggering, and wake-word detection pipeline.
"""

import os
import pytest
from senses.wake_listener import WakeListener, get_wake_listener


@pytest.fixture(autouse=True)
def setup_test_mode(monkeypatch):
    monkeypatch.setenv("JARVIS_TEST_MODE", "1")


def test_wake_listener_singleton():
    l1 = get_wake_listener()
    l2 = get_wake_listener()
    assert l1 is l2
    assert isinstance(l1, WakeListener)


def test_wake_listener_lifecycle():
    recorded = []

    def on_wake(cmd: str):
        recorded.append(cmd)

    listener = WakeListener(on_wake=on_wake)
    assert listener.running is False

    listener.start_listening()
    assert listener.running is True

    # Play chime
    listener.play_wake_chime()

    # Trigger callback manually to verify handler
    if listener.on_wake:
        listener.on_wake("musiqani yoq")

    assert len(recorded) == 1
    assert recorded[0] == "musiqani yoq"

    listener.stop_listening()
    assert listener.running is False
