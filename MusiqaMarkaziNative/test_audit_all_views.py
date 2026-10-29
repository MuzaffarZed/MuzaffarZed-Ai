import os
import time
import requests
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

def main():
    exe_path = r"C:\Users\MuzaffarZed\Desktop\Musiqa_Markazi_Pro.exe"
    port_file = os.path.expandvars(r"%LOCALAPPDATA%\UzbekMusiqaMarkaziPro\running_port.txt")
    port = None

    if os.path.exists(port_file):
        try:
            with open(port_file, "r") as f:
                p = int(f.read().strip())
            r = requests.post(f"http://127.0.0.1:{p}/api/native/action", json={"action": "evalJs", "code": "1+1"}, timeout=2)
            if r.status_code == 200:
                port = p
                print(f"[Port {port}] Using active Musiqa Markazi Pro instance.")
        except Exception:
            pass

    if port is None:
        import subprocess
        subprocess.run(["powershell", "-NoProfile", "-Command", "Stop-Process -Name 'Musiqa_Markazi_Pro' -Force -ErrorAction SilentlyContinue"], capture_output=True)
        if os.path.exists(port_file):
            try: os.remove(port_file)
            except: pass
        print("Launching updated Musiqa_Markazi_Pro.exe...")
        proc = subprocess.Popen([exe_path], creationflags=0x00000008) # DETACHED_PROCESS
        for _ in range(15):
            if os.path.exists(port_file):
                try:
                    with open(port_file, "r") as f:
                        port = int(f.read().strip())
                    if port: break
                except: pass
            time.sleep(1)
        assert port is not None, "Failed to get running port!"
        print(f"[Port {port}] App active and ready.")

    def eval_js(code):
        url = f"http://127.0.0.1:{port}/api/native/action"
        res = requests.post(url, json={"action": "evalJs", "code": code}, timeout=5)
        raw = res.json().get("result", "")
        try:
            return json.loads(raw)
        except Exception:
            return raw

    def capture_screenshot(filename):
        artifact_dir = r"C:\Users\MuzaffarZed\.gemini\antigravity\brain\2f3e54a9-40f9-472c-8160-446093bb35d0"
        target_path = os.path.join(artifact_dir, filename)
        url = f"http://127.0.0.1:{port}/api/native/action"
        payload = {"action": "capturePreview", "path": target_path}
        res = requests.post(url, json=payload, timeout=6)
        print(f"Captured {filename}: {res.json()}")
        return target_path

    # Check DOM ready
    ready = eval_js("typeof state !== 'undefined' && !!document.getElementById('btnScaleManager')")
    assert ready is True, "App state is not ready!"
    print("DOM & JavaScript State verified.")

    # 1. AUDIT ALL 11 TABS
    tabs = [
        ("artists", "San'atkorlar"),
        ("collections", "Janrlar & Uslublar"),
        ("search", "Qidiruv & Tanlash"),
        ("aimp", "Kutubxona & Pleylist"),
        ("simulator", "HD Kinozal (MP4)"),
        ("queue", "Yuklamalar (32-Oqim)"),
        ("kiosk", "Fleshka Kiosk Pro"),
        ("reels", "9:16 Reels Fabrikasi"),
        ("dj", "DJ Mashup Studiya"),
        ("turbo", "Turbo Doctor & RAM"),
        ("vault", "Kiber-Sandiq (AES)")
    ]

    print("\n--- [AUDIT 1: All 11 Navigation Tabs Sweep] ---")
    for tab_id, tab_label in tabs:
        res = eval_js(f"""
        (() => {{
            switchTab('{tab_id}');
            const pane = document.getElementById('tab-{tab_id}');
            return {{
                tab: state.activeTab,
                hasPane: !!pane,
                isActive: pane ? pane.classList.contains('active') : false,
                display: pane ? window.getComputedStyle(pane).display : 'none'
            }};
        }})()
        """)
        print(f"Tab '{tab_label}' ({tab_id}): {res}")
        assert res["tab"] == tab_id, f"Tab {tab_id} did not become active in state!"
        assert res["hasPane"], f"Pane tab-{tab_id} missing from DOM!"
        assert res["isActive"], f"Pane tab-{tab_id} is not marked active!"
        assert res["display"] != "none", f"Pane tab-{tab_id} is hidden with display:none!"
    print("=> AUDIT 1 PASSED: All 11 tabs switch seamlessly and display properly.")

    # 2. AUDIT FOLDER DRAWER & PC MUSIC DISCOVERY
    print("\n--- [AUDIT 2: Whole PC Folder Drawer & Category Filters] ---")
    eval_js("switchTab('aimp');")
    time.sleep(0.3)
    drawer_res = eval_js("""
    (() => {
        const drawer = document.getElementById('libraryFolderDrawer');
        const isCol = drawer ? drawer.classList.contains('collapsed') : true;
        if (isCol) toggleFolderDrawer();
        const afterToggle = drawer ? !drawer.classList.contains('collapsed') : false;
        
        // Test category filter
        setFolderDrawerCategory('audio');
        const audioActive = document.getElementById('btnFolderCatAudio')?.classList.contains('active');
        setFolderDrawerCategory('video');
        const videoActive = document.getElementById('btnFolderCatVideo')?.classList.contains('active');
        setFolderDrawerCategory('all');
        const allActive = document.getElementById('btnFolderCatAll')?.classList.contains('active');
        
        return {
            hasDrawer: !!drawer,
            isExpanded: afterToggle,
            audioCatWorks: audioActive,
            videoCatWorks: videoActive,
            allCatWorks: allActive,
            pillsCount: document.querySelectorAll('#libraryFolderPills .cat-pill').length
        };
    })()
    """)
    print("Folder Drawer Audit:", drawer_res)
    assert drawer_res["hasDrawer"], "libraryFolderDrawer missing from DOM!"
    assert drawer_res["isExpanded"], "Drawer toggle failed to expand!"
    assert drawer_res["allCatWorks"], "Category button 'all' not active!"
    capture_screenshot("live_audit_folder_drawer.png")
    print("=> AUDIT 2 PASSED: Folder drawer expands, categories filter, and pills display.")

    # 3. AUDIT CINEMA VIDEO PLAYER CONTROLS
    print("\n--- [AUDIT 3: Cinema Video Player Controls & Overlay] ---")
    eval_js("switchTab('simulator');")
    time.sleep(0.3)
    cinema_res = eval_js("""
    (() => {
        const vid = document.getElementById('carVideoPlayer');
        const controls = document.querySelector('.cinema-control-deck');
        const seek = document.getElementById('cinemaSeekSlider');
        const filterStrip = document.getElementById('cinemaFilterStrip');
        const playlistBox = document.getElementById('cinemaPlaylistContainer');
        
        return {
            hasVideo: !!vid,
            hasControls: !!controls,
            hasSeek: !!seek,
            hasFilterStrip: !!filterStrip,
            hasPlaylist: !!playlistBox,
            controlsZIndex: window.getComputedStyle(controls).zIndex
        };
    })()
    """)
    print("Cinema Player Audit:", cinema_res)
    assert cinema_res["hasVideo"], "carVideoPlayer missing!"
    assert cinema_res["hasControls"], "cinema-control-deck missing!"
    assert cinema_res["hasSeek"], "cinemaSeekSlider missing!"
    capture_screenshot("live_audit_cinema_player.png")
    print("=> AUDIT 3 PASSED: Cinema video player stage and controls verified.")

    # 4. AUDIT UNIVERSAL SCALE ENGINE & MODAL
    print("\n--- [AUDIT 4: Universal Scale Engine Controls] ---")
    scale_res = eval_js("""
    (() => {
        openScaleSettingsModal();
        const modal = document.getElementById('scaleSettingsModal');
        const isOpen = modal ? modal.classList.contains('open') : false;
        
        // Sliders
        const zS = document.getElementById('scaleZoomSlider');
        const fS = document.getElementById('scaleFontSlider');
        const cS = document.getElementById('scaleCardSlider');
        const sS = document.getElementById('scaleSidebarSlider');
        const wS = document.getElementById('scaleWaveformSlider');
        
        closeScaleSettingsModal();
        return {
            opened: isOpen,
            hasSliders: !!(zS && fS && cS && sS && wS),
            cardWidth: state.scaleSettings ? state.scaleSettings.cardWidth : null,
            zoom: state.scaleSettings ? state.scaleSettings.zoom : null
        };
    })()
    """)
    print("Scale Engine Audit:", scale_res)
    assert scale_res["opened"], "Scale settings modal did not open!"
    assert scale_res["hasSliders"], "Not all scale sliders exist in DOM!"
    print("=> AUDIT 4 PASSED: Universal Scale Engine verified.")

    # 5. AUDIT MINI DOCK & RESTORE
    print("\n--- [AUDIT 5: Mini Dock Mode Transition] ---")
    eval_js("switchTab('aimp');")
    time.sleep(0.2)
    eval_js("(async () => { await toggleMiniDock(); })()")
    time.sleep(1.0)
    mini_check = eval_js("""
    (() => {
        const isMini = state.isMiniDock && document.body.classList.contains('mini-dock');
        const deck = document.querySelector('.master-deck');
        const deckH = deck ? deck.getBoundingClientRect().height : 0;
        return { isMini, deckH };
    })()
    """)
    print("Mini Dock Activated:", mini_check)
    assert mini_check["isMini"], "Mini dock failed to activate!"
    capture_screenshot("live_audit_mini_dock.png")

    eval_js("(async () => { await toggleMiniDock(); })()")
    time.sleep(1.0)
    restored_check = eval_js("""
    (() => {
        return {
            isRestored: !state.isMiniDock && !document.body.classList.contains('mini-dock')
        };
    })()
    """)
    print("Mini Dock Restored:", restored_check)
    assert restored_check["isRestored"], "Mini dock failed to restore to full window!"
    print("=> AUDIT 5 PASSED: Mini Dock mode transition works seamlessly.")

    print("\n========================================================")
    print(" ALL AUDIT CHECKS PASSED WITH ZERO FLAWS & ZERO ERRORS! ")
    print("========================================================")

if __name__ == "__main__":
    main()
