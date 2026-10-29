import json
import os
import subprocess
import time
import urllib.parse
import urllib.request
from pathlib import Path
import pytest


DESKTOP_EXE = Path(r"C:\Users\MuzaffarZed\Desktop\JARVIS_Pro.exe")
PUBLISH_EXE = Path(r"C:\Users\MuzaffarZed\ai_workspace\JarvisNativePro\publish\JARVIS_Pro.exe")
PORT_FILE = Path(os.environ["LOCALAPPDATA"]) / "JarvisNativePro" / "running_port.txt"


@pytest.fixture(scope="module")
def jarvis_server_url():
    assert DESKTOP_EXE.exists(), "Desktop JARVIS_Pro.exe topilmadi"
    assert PUBLISH_EXE.exists(), "Publish JARVIS_Pro.exe topilmadi"

    if PORT_FILE.exists():
        try:
            PORT_FILE.unlink()
        except Exception:
            pass

    proc = subprocess.Popen([str(DESKTOP_EXE)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for _ in range(30):
        if PORT_FILE.exists() and PORT_FILE.stat().st_size > 0:
            break
        time.sleep(0.3)

    assert PORT_FILE.exists(), "running_port.txt yaratilmadi"
    port = int(PORT_FILE.read_text(encoding="utf-8").strip())
    base_url = f"http://127.0.0.1:{port}"

    # Wait until server responds
    ready = False
    for _ in range(20):
        try:
            with urllib.request.urlopen(f"{base_url}/api/telemetry", timeout=3) as r:
                if r.status == 200:
                    ready = True
                    break
        except Exception:
            time.sleep(0.4)

    assert ready, "JARVIS LocalServer javob bermadi"
    try:
        yield base_url
    finally:
        try:
            proc.terminate()
        except Exception:
            pass


def http_get_json(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=15) as r:
        assert r.status == 200
        return json.loads(r.read().decode("utf-8"))


def http_post_json(url: str, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=20) as r:
        assert r.status == 200
        return json.loads(r.read().decode("utf-8"))


def test_ui_assets_and_5_themes(jarvis_server_url):
    with urllib.request.urlopen(f"{jarvis_server_url}/", timeout=5) as r:
        html = r.read().decode("utf-8")
    assert "J.A.R.V.I.S PRO NATIVE" in html
    assert "v12.0 QUANTUM-APEX" in html
    assert "arcReactorCanvas" in html
    assert "commandPaletteOverlay" in html
    for tab in ("tab-cockpit", "tab-apps", "tab-vault", "tab-missions", "tab-system", "tab-vision", "tab-files", "tab-settings"):
        assert tab in html

    with urllib.request.urlopen(f"{jarvis_server_url}/styles.css", timeout=5) as r:
        css = r.read().decode("utf-8")
    for skin in ("onyx", "gold", "emerald", "sport", "crystal"):
        assert f'[data-skin="{skin}"]' in css

    with urllib.request.urlopen(f"{jarvis_server_url}/app.js", timeout=5) as r:
        js = r.read().decode("utf-8")
    assert "startArcReactorAnimation" in js
    assert "ensureAudioContext" in js
    assert "renderAppsHub" in js
    assert "exportStudioTtsMp3" in js
    assert "openCommandPalette" in js
    assert "changeFocusAmbience" in js
    assert "renderVaultList" in js


def test_bootstrap_and_live_telemetry(jarvis_server_url):
    boot = http_get_json(f"{jarvis_server_url}/api/bootstrap")
    assert boot["ok"] is True
    assert "state" in boot
    assert "telemetry" in boot
    assert "apps" in boot
    assert "vault" in boot
    assert "folderAudit" in boot
    assert len(boot["apps"]) >= 5
    assert len(boot["vault"]) >= 3
    assert len(boot["folderAudit"]) >= 3

    tel = boot["telemetry"]
    assert tel["ramTotalGb"] > 0
    assert 0 <= tel["cpuPercent"] <= 100
    assert 0 <= tel["healthScore"] <= 100
    assert len(tel["drives"]) >= 1
    assert "autoRamGuard" in tel


def test_desktop_apps_hub_endpoint(jarvis_server_url):
    apps_res = http_get_json(f"{jarvis_server_url}/api/apps")
    assert apps_res["ok"] is True
    assert len(apps_res["apps"]) >= 5
    categories = {a["category"] for a in apps_res["apps"]}
    assert bool(categories.intersection({"studio", "ai", "office", "system"}))


def test_smart_vault_and_anti_clutter_organizer(jarvis_server_url):
    # 1. GET /api/vault
    v_res = http_get_json(f"{jarvis_server_url}/api/vault")
    assert v_res["ok"] is True
    assert len(v_res["vault"]) >= 3
    assert len(v_res["folderAudit"]) >= 3

    # 2. Add Vault Item
    add_res = http_post_json(
        f"{jarvis_server_url}/api/vault",
        {
            "action": "add",
            "title": "Pytest Quantum Snippet",
            "category": "snippet",
            "content": "dotnet publish -c Release",
            "isPinned": True
        }
    )
    assert add_res["ok"] is True
    added_item = next((i for i in add_res["vault"] if i["title"] == "Pytest Quantum Snippet"), None)
    assert added_item is not None
    new_id = added_item["id"]

    # 3. Toggle Pin Vault Item
    pin_res = http_post_json(f"{jarvis_server_url}/api/vault", {"action": "togglePin", "id": new_id})
    assert pin_res["ok"] is True

    # 4. Delete Vault Item
    del_res = http_post_json(f"{jarvis_server_url}/api/vault", {"action": "delete", "id": new_id})
    assert del_res["ok"] is True
    assert not any(i["id"] == new_id for i in del_res["vault"])

    # 5. Organize Downloads
    org_res = http_post_json(f"{jarvis_server_url}/api/macro", {"macroId": "organize_downloads"})
    assert org_res["ok"] is True
    assert "movedCount" in org_res
    assert len(org_res["audit"]) >= 3


def test_ai_brain_commands_and_math(jarvis_server_url):
    # 1. Greeting
    res1 = http_post_json(f"{jarvis_server_url}/api/command", {"text": "Assalomu alaykum Jarvis"})
    assert res1["ok"] is True
    assert "janob" in res1["message"]["text"].lower()

    # 2. Math calculation
    res2 = http_post_json(f"{jarvis_server_url}/api/command", {"text": "125 * 8"})
    assert res2["ok"] is True
    assert "1000" in res2["message"]["text"]

    # 3. Telemetry command
    res3 = http_post_json(f"{jarvis_server_url}/api/command", {"text": "Tizim holati va telemetriya"})
    assert res3["ok"] is True
    assert "RAM" in res3["message"]["text"] or "CPU" in res3["message"]["text"]


def test_autonomous_macros_super_boost_and_vision(jarvis_server_url):
    # 1. RAM Turbo Optimizer
    ram_res = http_post_json(f"{jarvis_server_url}/api/macro", {"macroId": "ram_turbo"})
    assert ram_res["ok"] is True
    assert ram_res["trimmedProcesses"] > 0
    assert ram_res["freedMb"] > 0

    # 2. PC Manager Super-Boost 3-in-1 (RAM + Temp + DNS)
    boost_res = http_post_json(f"{jarvis_server_url}/api/macro", {"macroId": "super_boost"})
    assert boost_res["ok"] is True
    assert boost_res["freedRamMb"] > 0
    assert "Super-Boost" in boost_res["message"]

    # 3. Screenshot capture
    shot_res = http_post_json(f"{jarvis_server_url}/api/macro", {"macroId": "take_screenshot"})
    assert shot_res["ok"] is True
    assert Path(shot_res["screenshot"]["fullPath"]).exists()

    # 4. Hybrid Vision analysis
    vis_res = http_post_json(f"{jarvis_server_url}/api/macro", {"macroId": "vision_analyze"})
    assert vis_res["ok"] is True
    assert len(vis_res["analysis"]) > 20

    # 5. PowerShell execution
    ps_res = http_post_json(f"{jarvis_server_url}/api/macro", {"macroId": "run_powershell", "command": "Write-Output 'JARVIS_OK_2026'"})
    assert ps_res["ok"] is True
    assert "JARVIS_OK_2026" in ps_res["output"]


def test_windows_processes_and_instant_files(jarvis_server_url):
    wins = http_get_json(f"{jarvis_server_url}/api/windows")
    assert wins["ok"] is True
    assert len(wins["windows"]) >= 1

    procs = http_get_json(f"{jarvis_server_url}/api/processes?limit=30")
    assert procs["ok"] is True
    assert len(procs["processes"]) >= 5

    files = http_get_json(f"{jarvis_server_url}/api/files?q=jarvis&ext=all&max=25")
    assert files["ok"] is True
    assert len(files["files"]) >= 1


def test_neural_uzbek_tts_synthesis_and_mp3_export(jarvis_server_url):
    text = urllib.parse.quote("Salom muhtaram janob Muzaffar")
    url = f"{jarvis_server_url}/api/tts?text={text}&voice=uz-UZ-MadinaNeural"
    with urllib.request.urlopen(url, timeout=15) as r:
        assert r.status == 200
        audio_bytes = r.read()
        assert len(audio_bytes) > 1000

    # Test Neural TTS MP3 Export to Desktop
    exp_res = http_post_json(
        f"{jarvis_server_url}/api/macro",
        {
            "macroId": "export_tts_mp3",
            "text": "Salom janob Muzaffar, Jarvis diktor ovozi tayyor.",
            "voice": "uz-UZ-MadinaNeural"
        }
    )
    assert exp_res["ok"] is True
    assert Path(exp_res["filePath"]).exists()
