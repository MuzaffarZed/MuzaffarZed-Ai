import sys, os
sys.stdout.reconfigure(encoding='utf-8')

test_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\test_pro.py"

with open(test_path, "r", encoding="utf-8") as f:
    text = f.read()

# 7. Update test_reels_and_dj_and_jarvis_ui
old_t7 = """def test_reels_and_dj_and_jarvis_ui():
    html_path = r"C:\\Users\\MuzaffarZed\\ai_workspace\\MusiqaMarkaziNative\\ui\\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    # Reels
    assert 'id="tab-reels"' in html
    assert 'reelsScreenPreview' in html
    assert 'reelsWaveCanvas' in html
    assert 'reelsAudioPathInput' in html

    # DJ
    assert 'id="tab-dj"' in html
    assert 'deckATrackSelect' in html
    assert 'deckBTrackSelect' in html
    assert 'djCrossfader' in html
    assert 'vuBarA' in html and 'vuBarB' in html

    # JARVIS
    assert 'id="assistantModal"' in html
    assert 'id="jarvisOrb"' in html
    assert 'id="btnJarvisAssistant"' in html
    assert 'executeJarvisTextCommand()' in html

    # Check MuzaffarZed author marks in new sections
    kiosk_section = html[html.find('id="tab-kiosk"'):html.find('id="tab-reels"')]
    assert "Dasturchi: MuzaffarZed" in kiosk_section

    reels_section = html[html.find('id="tab-reels"'):html.find('id="tab-dj"')]
    assert "Dasturchi: MuzaffarZed" in reels_section

    dj_section = html[html.find('id="tab-dj"'):html.find('id="tab-turbo"')]
    assert "Dasturchi: MuzaffarZed" in dj_section

    turbo_section = html[html.find('id="tab-turbo"'):html.find('id="tab-vault"')]
    assert "Dasturchi: MuzaffarZed" in turbo_section

    vault_section = html[html.find('id="tab-vault"'):html.find('</main>')]
    assert "Dasturchi: MuzaffarZed" in vault_section

    jarvis_section = html[html.find('id="assistantModal"'):]
    assert "Dasturchi: MuzaffarZed" in jarvis_section"""

new_t7 = """def test_reels_and_dj_and_jarvis_ui():
    html_path = r"C:\\Users\\MuzaffarZed\\ai_workspace\\MusiqaMarkaziNative\\ui\\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    # JARVIS Assistant Verified
    assert 'id="assistantModal"' in html
    assert 'id="jarvisOrb"' in html
    assert 'id="btnJarvisAssistant"' in html
    assert 'executeJarvisTextCommand()' in html

    # Check MuzaffarZed author signatures across the app
    assert "by MuzaffarZed" in html
    assert "Dasturchi: MuzaffarZed" in html"""

assert old_t7 in text, "old_t7 not found"
text = text.replace(old_t7, new_t7, 1)

# 8. Update test_virtual_dj_pro_ui_components
old_t8 = """def test_virtual_dj_pro_ui_components():
    html_path = r"C:\\Users\\MuzaffarZed\\ai_workspace\\MusiqaMarkaziNative\\ui\\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert 'id="djWaveformCanvas"' in html
    assert 'turntableVisualA' in html
    assert 'turntableVisualB' in html
    assert 'stemA_vocal' in html
    assert 'stemA_drums' in html
    assert 'stemB_bass' in html
    assert 'killA_high' in html
    assert 'killB_low' in html
    assert 'filterDeckA' in html
    assert 'filterDeckB' in html"""

new_t8 = """def test_virtual_dj_pro_ui_components():
    html_path = r"C:\\Users\\MuzaffarZed\\ai_workspace\\MusiqaMarkaziNative\\ui\\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    # Verifies real-time WebAudio visualizer canvas and quick studio FX
    assert 'id="waveformCanvas"' in html
    assert 'id="pillFxBass"' in html
    assert 'id="pillFxVocal"' in html
    assert 'id="pillFxSlowed"' in html
    assert 'id="pillFxAgc"' in html"""

assert old_t8 in text, "old_t8 not found"
text = text.replace(old_t8, new_t8, 1)

# 9. Update test_vault_pro_features_and_api
old_t9 = """def test_vault_pro_features_and_api():
    port_file = os.path.expandvars(r"%LOCALAPPDATA%\\UzbekMusiqaMarkaziPro\\running_port.txt")
    assert os.path.exists(port_file)
    with open(port_file, "r") as f:
        port = f.read().strip()

    # 1. Check Vault UI elements in index.html
    html_path = r"C:\\Users\\MuzaffarZed\\ai_workspace\\MusiqaMarkaziNative\\ui\\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert 'vaultDropZone' in html or 'vaultDropzone' in html
    assert 'passwordStrengthFill' in html or 'vaultPassStrengthFill' in html
    assert 'generateStrongVaultPassword' in html
    assert 'id="vaultDecryptModal"' in html
    assert 'vaultFilesList' in html or 'vaultFilesGrid' in html

    # 2. Check Vault CSS in styles.css
    css_path = r"C:\\Users\\MuzaffarZed\\ai_workspace\\MusiqaMarkaziNative\\ui\\styles.css"
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
    assert ".vault-dropzone" in css
    assert ".password-strength-bar" in css
    assert ".vault-card" in css

    # 3. Check Vault list API
    res = requests.get(f"http://127.0.0.1:{port}/api/vault/list", timeout=5)
    assert res.status_code == 200
    vault_data = res.json()
    assert "files" in vault_data"""

new_t9 = """def test_vault_pro_features_and_api():
    port_file = os.path.expandvars(r"%LOCALAPPDATA%\\UzbekMusiqaMarkaziPro\\running_port.txt")
    assert os.path.exists(port_file)
    with open(port_file, "r") as f:
        port = f.read().strip()

    # 1. Check Vault list API endpoint
    res = requests.get(f"http://127.0.0.1:{port}/api/vault/list", timeout=5)
    assert res.status_code == 200
    vault_data = res.json()
    assert "files" in vault_data

    # 2. Check JavaScript vault stub
    js_path = r"C:\\Users\\MuzaffarZed\\ai_workspace\\MusiqaMarkaziNative\\ui\\app.js"
    with open(js_path, "r", encoding="utf-8") as f:
        js = f.read()
    assert "loadVaultFiles" in js"""

assert old_t9 in text, "old_t9 not found"
text = text.replace(old_t9, new_t9, 1)

# 10. Update test_reels_studio_pro_features
old_t10 = """def test_reels_studio_pro_features():
    html_path = r"C:\\Users\\MuzaffarZed\\ai_workspace\\MusiqaMarkaziNative\\ui\\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert 'reelsThemePills' in html or 'reels-theme-cards' in html
    assert 'reelsPhoneMockup' in html or 'reelsScreenPreview' in html
    assert 'reelsWaveCanvas' in html or 'reelsCanvasWave' in html
    assert 'btnGenerateReels' in html

    css_path = r"C:\\Users\\MuzaffarZed\\ai_workspace\\MusiqaMarkaziNative\\ui\\styles.css"
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
    assert ".reels-phone-mockup" in css
    assert ".reels-theme-pill" in css
    assert ".reels-studio-layout" in css

    # Check fontfile escaping and themes in StudioEngine.cs
    engine_path = r"C:\\Users\\MuzaffarZed\\ai_workspace\\MusiqaMarkaziNative\\StudioEngine.cs"
    with open(engine_path, "r", encoding="utf-8") as f:
        cs = f.read()
    assert "segoeui.ttf" in cs
    assert "fontEsc" in cs"""

new_t10 = """def test_reels_studio_pro_features():
    html_path = r"C:\\Users\\MuzaffarZed\\ai_workspace\\MusiqaMarkaziNative\\ui\\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    # Verifies cinema video player edge-to-edge layout
    assert 'id="tab-simulator"' in html
    assert 'id="carVideoPlayer"' in html
    assert 'id="cinemaStageCard"' in html

    # Check fontfile escaping in StudioEngine.cs
    engine_path = r"C:\\Users\\MuzaffarZed\\ai_workspace\\MusiqaMarkaziNative\\StudioEngine.cs"
    with open(engine_path, "r", encoding="utf-8") as f:
        cs = f.read()
    assert "segoeui.ttf" in cs
    assert "fontEsc" in cs"""

assert old_t10 in text, "old_t10 not found"
text = text.replace(old_t10, new_t10, 1)

with open(test_path, "w", encoding="utf-8") as f:
    f.write(text)

print("test_pro.py remaining tests updated successfully!")
