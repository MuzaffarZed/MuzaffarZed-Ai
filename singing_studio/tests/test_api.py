"""
Integration and API tests for JARVIS AI Singing Studio FastAPI backend.
"""

from fastapi.testclient import TestClient
import pytest
from pathlib import Path

from singing_studio.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_home_page_served(client):
    """Bosh sahifa HTML formatida to'g'ri qaytarilishi kerak."""
    response = client.get("/")
    assert response.status_code == 200
    assert "JARVIS AI Singing Studio" in response.text
    assert "Janob Muzaffar" in response.text


def test_api_status(client):
    """Tizim holati va tayyorlik ma'lumotlari."""
    response = client.get("/api/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["ffmpeg_ready"] is True
    assert "dataset_stats" in data


def test_api_models_list(client):
    """Mavjud modellar ro'yxati."""
    response = client.get("/api/voice/models")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
    assert len(data["models"]) >= 1
