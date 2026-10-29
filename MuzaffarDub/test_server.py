"""
MuzaffarDub Server Unit Tests v1.1
Dasturchi: MuzaffarZed
"""

import sys
from pathlib import Path
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).parent.resolve()))
from server import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["developer"] == "MuzaffarZed"
    print("\n[OK] Health check muvaffaqiyatli o'tdi!")

def test_translate():
    response = client.get("/translate?text=Hello%20world")
    assert response.status_code == 200
    data = response.json()
    assert len(data["translated"]) > 0
    print(f"\n[OK] Tarjima testi muvaffaqiyatli: '{data['original']}' -> '{data['translated']}'")

def test_dub_endpoint():
    response = client.get("/dub?text=Welcome%20to%20our%20channel&voice=madina&rate=%2B10%25")
    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/mpeg"
    assert len(response.content) > 1000
    print(f"\n[OK] Dublyaj testi muvaffaqiyatli: {len(response.content)} bayt MP3 olindi!")

if __name__ == "__main__":
    test_health()
    test_translate()
    test_dub_endpoint()
    print("\n==========================================")
    print("BARCHA TESTLAR 100% BENUQSON YAKUNLANDI!")
    print("Dasturchi: MuzaffarZed")
    print("==========================================")
