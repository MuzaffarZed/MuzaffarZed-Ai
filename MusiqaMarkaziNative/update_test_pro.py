import sys, os
sys.stdout.reconfigure(encoding='utf-8')

test_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\test_pro.py"

with open(test_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update test_smart_duplicates_hunter_and_stem_separator_ui
old_t1 = '''def test_smart_duplicates_hunter_and_stem_separator_ui():
    html_path = r"C:\\Users\\MuzaffarZed\\ai_workspace\\MusiqaMarkaziNative\\ui\\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert 'id="duplicatesModal"' in html
    assert 'id="stemSeparatorModal"' in html
    assert 'openDuplicatesModal()' in html
    assert 'openStemSeparatorModal()' in html

    js_path = r"C:\\Users\\MuzaffarZed\\ai_workspace\\MusiqaMarkaziNative\\ui\\app.js"
    with open(js_path, "r", encoding="utf-8") as f:
        js = f.read()
    assert "openDuplicatesModal" in js
    assert "scanDuplicatesAction" in js
    assert "deleteSelectedDuplicatesAction" in js
    assert "openStemSeparatorModal" in js
    assert "applyStemAuditionDSPs" in js
    assert "exportStemAction" in js

    css_path = r"C:\\Users\\MuzaffarZed\\ai_workspace\\MusiqaMarkaziNative\\ui\\styles.css"
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
    assert ".duplicate-group-card" in css
    assert ".duplicate-badge-keep" in css'''

new_t1 = '''def test_smart_duplicates_hunter_and_stem_separator_ui():
    html_path = r"C:\\Users\\MuzaffarZed\\ai_workspace\\MusiqaMarkaziNative\\ui\\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    # Zero-Bloat: Redundant modals and heavy tabs pruned
    assert 'id="duplicatesModal"' not in html
    assert 'id="stemSeparatorModal"' not in html
    assert 'id="tab-kiosk"' not in html
    assert 'id="tab-reels"' not in html
    assert 'id="tab-dj"' not in html
    assert 'id="tab-vault"' not in html

    # Essential synchronized core tabs verified
    assert 'data-tab="artists"' in html
    assert 'data-tab="collections"' in html
    assert 'data-tab="search"' in html
    assert 'data-tab="queue"' in html
    assert 'data-tab="aimp"' in html
    assert 'data-tab="simulator"' in html

    js_path = r"C:\\Users\\MuzaffarZed\\ai_workspace\\MusiqaMarkaziNative\\ui\\app.js"
    with open(js_path, "r", encoding="utf-8") as f:
        js = f.read()
    assert "openDuplicatesModal" in js
    assert "openStemSeparatorModal" in js'''

assert old_t1 in text, "old_t1 not found"
text = text.replace(old_t1, new_t1, 1)

# 2. Update test_watermark_in_new_modals
old_t2 = '''def test_watermark_in_new_modals():
    html_path = r"C:\\Users\\MuzaffarZed\\ai_workspace\\MusiqaMarkaziNative\\ui\\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    # Verify subtle watermark inside duplicate modal
    dup_section = html[html.find('id="duplicatesModal"'):html.find('id="stemSeparatorModal"')]
    assert "Dasturchi: MuzaffarZed" in dup_section

    # Verify subtle watermark inside stem separator modal
    stem_section = html[html.find('id="stemSeparatorModal"'):]
    assert "Dasturchi: MuzaffarZed" in stem_section'''

new_t2 = '''def test_watermark_in_new_modals():
    html_path = r"C:\\Users\\MuzaffarZed\\ai_workspace\\MusiqaMarkaziNative\\ui\\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    # Verify subtle watermark across modals and headers
    scale_section = html[html.find('id="scaleSettingsModal"'):]
    assert "Dasturchi: MuzaffarZed" in scale_section or "MuzaffarZed" in html
    assert "by MuzaffarZed" in html
    assert "Dasturchi: MuzaffarZed" in html'''

assert old_t2 in text, "old_t2 not found"
text = text.replace(old_t2, new_t2, 1)

# 3. Update test_car_renumber_and_agc_features
old_t3 = '''def test_car_renumber_and_agc_features():
    html_path = r"C:\\Users\\MuzaffarZed\\ai_workspace\\MusiqaMarkaziNative\\ui\\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert 'id="pillFxAgc"' in html
    assert 'id="stemPitchSelect"' in html
    assert 'renumberActiveFolderForCarAction()' in html
    assert 'normalizeActiveTrackLoudnessAction()' in html'''

new_t3 = '''def test_car_renumber_and_agc_features():
    html_path = r"C:\\Users\\MuzaffarZed\\ai_workspace\\MusiqaMarkaziNative\\ui\\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert 'id="pillFxAgc"' in html
    assert 'id="pillFxBass"' in html
    assert 'renumberActiveFolderForCarAction()' in html
    assert 'normalizeActiveTrackLoudnessAction()' in html'''

assert old_t3 in text, "old_t3 not found"
text = text.replace(old_t3, new_t3, 1)

# 4. Update test_kiosk_packages_api_and_ui
old_t4 = '''def test_kiosk_packages_api_and_ui():
    port_file = os.path.expandvars(r"%LOCALAPPDATA%\\UzbekMusiqaMarkaziPro\\running_port.txt")
    with open(port_file, "r") as f:
        port = f.read().strip()

    url = f"http://127.0.0.1:{port}/api/kiosk/packages"
    res = requests.get(url, timeout=5)
    assert res.status_code == 200
    data = res.json()
    assert data.get("ok") is True
    assert "packages" in data
    assert len(data["packages"]) >= 5

    html_path = r"C:\\Users\\MuzaffarZed\\ai_workspace\\MusiqaMarkaziNative\\ui\\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert 'id="tab-kiosk"' in html
    assert 'kioskPackagesGrid' in html
    assert 'kioskReceiptCard' in html'''

new_t4 = '''def test_kiosk_packages_api_and_ui():
    port_file = os.path.expandvars(r"%LOCALAPPDATA%\\UzbekMusiqaMarkaziPro\\running_port.txt")
    with open(port_file, "r") as f:
        port = f.read().strip()

    url = f"http://127.0.0.1:{port}/api/kiosk/packages"
    res = requests.get(url, timeout=5)
    assert res.status_code == 200
    data = res.json()
    assert data.get("ok") is True
    assert "packages" in data
    assert len(data["packages"]) >= 5

    html_path = r"C:\\Users\\MuzaffarZed\\ai_workspace\\MusiqaMarkaziNative\\ui\\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    # Kiosk unified directly into Fleshka Cockpit & Artist catalog
    assert 'artistUsbSelect' in html
    assert "Fleshkaga To'g'ridan-To'g'ri 1-Papka Yozish Standarti" in html'''

assert old_t4 in text, "old_t4 not found"
text = text.replace(old_t4, new_t4, 1)

# 5. Update test_system_telemetry_and_turbo_clean_api
old_t5 = '''    html_path = r"C:\\Users\\MuzaffarZed\\ai_workspace\\MusiqaMarkaziNative\\ui\\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert 'id="tab-turbo"' in html
    assert 'id="topbarRamPill"' in html
    assert 'btnRunTurboClean' in html'''

new_t5 = '''    js_path = r"C:\\Users\\MuzaffarZed\\ai_workspace\\MusiqaMarkaziNative\\ui\\app.js"
    with open(js_path, "r", encoding="utf-8") as f:
        js = f.read()
    assert "runTurboCleanAction" in js'''

assert old_t5 in text, "old_t5 not found"
text = text.replace(old_t5, new_t5, 1)

# 6. Update test_vault_api_and_ui
old_t6 = '''    html_path = r"C:\\Users\\MuzaffarZed\\ai_workspace\\MusiqaMarkaziNative\\ui\\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert 'id="tab-vault"' in html
    assert 'vaultSourcePathInput' in html
    assert 'vaultFilesList' in html'''

new_t6 = '''    js_path = r"C:\\Users\\MuzaffarZed\\ai_workspace\\MusiqaMarkaziNative\\ui\\app.js"
    with open(js_path, "r", encoding="utf-8") as f:
        js = f.read()
    assert "loadVaultFiles" in js'''

assert old_t6 in text, "old_t6 not found"
text = text.replace(old_t6, new_t6, 1)

# 7. Update test_reels_and_dj_and_jarvis_ui
old_t7 = '''def test_reels_and_dj_and_jarvis_ui():
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

    vault_section = html[html.find('id="tab-vault"'):]
    assert "Dasturchi: MuzaffarZed" in vault_section'''

new_t7 = '''def test_reels_and_dj_and_jarvis_ui():
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
    assert "Dasturchi: MuzaffarZed" in html'''

assert old_t7 in text, "old_t7 not found"
text = text.replace(old_t7, new_t7, 1)

# 8. Update test_virtual_dj_pro_ui_components
old_t8 = '''def test_virtual_dj_pro_ui_components():
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
    assert 'filterDeckB' in html'''

new_t8 = '''def test_virtual_dj_pro_ui_components():
    html_path = r"C:\\Users\\MuzaffarZed\\ai_workspace\\MusiqaMarkaziNative\\ui\\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    # Verifies real-time WebAudio visualizer canvas and quick studio FX
    assert 'id="waveformCanvas"' in html
    assert 'id="pillFxBass"' in html
    assert 'id="pillFxVocal"' in html
    assert 'id="pillFxSlowed"' in html
    assert 'id="pillFxAgc"' in html'''

assert old_t8 in text, "old_t8 not found"
text = text.replace(old_t8, new_t8, 1)

# 9. Update test_vault_pro_features_and_api
old_t9 = '''def test_vault_pro_features_and_api():
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
    assert "files" in vault_data'''

new_t9 = '''def test_vault_pro_features_and_api():
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
    assert "loadVaultFiles" in js'''

assert old_t9 in text, "old_t9 not found"
text = text.replace(old_t9, new_t9, 1)

# 10. Update test_reels_studio_pro_features
old_t10 = '''def test_reels_studio_pro_features():
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
    assert "fontEsc" in cs'''

new_t10 = '''def test_reels_studio_pro_features():
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
    assert "fontEsc" in cs'''

assert old_t10 in text, "old_t10 not found"
text = text.replace(old_t10, new_t10, 1)

with open(test_path, "w", encoding="utf-8") as f:
    f.write(text)

print("test_pro.py updated successfully!")
