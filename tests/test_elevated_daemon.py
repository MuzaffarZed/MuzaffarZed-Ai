"""
tests/test_elevated_daemon.py — Integration & Unit Tests for JARVIS Elevated Daemon
Validates all REST API endpoints for remote and resident Windows control.
"""

import os
import pytest
from starlette.testclient import TestClient

os.environ["JARVIS_TEST_MODE"] = "1"

from daemon.elevated_server import app


@pytest.fixture
def client():
    return TestClient(app)


def test_daemon_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "online"
    assert data["service"] == "JARVIS_OMNI_DAEMON"
    assert "is_admin" in data
    assert "pid" in data


def test_daemon_telemetry(client):
    res = client.get("/telemetry")
    assert res.status_code == 200
    data = res.json()
    assert "cpu_percent" in data
    assert "ram_percent" in data


def test_daemon_windows(client):
    res = client.get("/windows")
    assert res.status_code == 200
    windows = res.json()
    assert len(windows) >= 1


def test_daemon_actions(client):
    # Focus
    foc_res = client.post("/focus", json={"query": "Code"})
    assert foc_res.status_code == 200
    assert foc_res.json()["success"] is True

    # Launch
    lnch_res = client.post("/launch", json={"target": "notepad"})
    assert lnch_res.status_code == 200
    assert lnch_res.json()["success"] is True

    # Click
    clk_res = client.post("/click", json={"x": 500, "y": 500, "button": "left", "clicks": 1})
    assert clk_res.status_code == 200
    assert clk_res.json()["success"] is True

    # Type
    typ_res = client.post("/type", json={"text": "Salom JARVIS"})
    assert typ_res.status_code == 200
    assert typ_res.json()["success"] is True

    # Hotkey
    htk_res = client.post("/hotkey", json={"keys": ["ctrl", "c"]})
    assert htk_res.status_code == 200
    assert htk_res.json()["success"] is True

    # Exec
    exc_res = client.post("/exec", json={"command": "Get-Date"})
    assert exc_res.status_code == 200
    assert exc_res.json()["success"] is True

    # Screenshot
    scr_res = client.get("/screenshot")
    assert scr_res.status_code == 200
    assert scr_res.json()["success"] is True
