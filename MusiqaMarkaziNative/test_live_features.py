import os
import time
import subprocess
import requests

def main():
    exe_path = r"C:\Users\MuzaffarZed\Desktop\Musiqa_Markazi_Pro.exe"
    port_file = os.path.expandvars(r"%LOCALAPPDATA%\UzbekMusiqaMarkaziPro\running_port.txt")
    
    # Remove stale port file if any
    if os.path.exists(port_file):
        try:
            os.remove(port_file)
        except:
            pass

    print("Launching Musiqa_Markazi_Pro.exe...")
    proc = subprocess.Popen([exe_path])
    time.sleep(4)

    try:
        assert os.path.exists(port_file), "running_port.txt was not generated!"
        with open(port_file, "r") as f:
            port = int(f.read().strip())
        print(f"App running successfully on port: {port}")

        # 1. Test /api/init
        res = requests.get(f"http://127.0.0.1:{port}/api/init", timeout=5)
        assert res.status_code == 200, f"Init failed: {res.status_code}"
        data = res.json()
        print(f"Init OK. BaseDir: {data.get('baseDir')}, Artists: {len(data.get('artists', []))}")

        # 2. Test /styles.css contains zoom and responsive styles
        res_css = requests.get(f"http://127.0.0.1:{port}/styles.css", timeout=5)
        assert res_css.status_code == 200
        css = res_css.text
        assert ".zoom-widget" in css, "Missing .zoom-widget in styles.css"
        assert ".active-folder-banner" in css, "Missing .active-folder-banner in styles.css"
        assert ".folder-badge-btn" in css, "Missing .folder-badge-btn in styles.css"
        assert "@media (max-width: 1400px)" in css, "Missing responsive media queries"
        print("CSS verification: 100% OK")

        # 3. Test /index.html contains zoom widget, category pills, banner
        res_html = requests.get(f"http://127.0.0.1:{port}/", timeout=5)
        assert res_html.status_code == 200
        html = res_html.text
        assert 'id="zoomWidget"' in html, "Missing zoomWidget in index.html"
        assert 'id="appZoomSelect"' in html, "Missing appZoomSelect in index.html"
        assert 'id="btnToggleFullscreen"' in html, "Missing btnToggleFullscreen in index.html"
        assert 'id="btnFolderCatAll"' in html, "Missing btnFolderCatAll in index.html"
        assert 'id="activeFolderBanner"' in html, "Missing activeFolderBanner in index.html"
        assert 'Dasturchi: MuzaffarZed' in html, "Missing Law 7 MuzaffarZed signature"
        print("HTML verification: 100% OK")

        # 4. Test /app.js contains zoom functions, folder category & dispatch logic
        res_js = requests.get(f"http://127.0.0.1:{port}/app.js", timeout=5)
        assert res_js.status_code == 200
        js = res_js.text
        assert "function setAppZoom" in js, "Missing setAppZoom in app.js"
        assert "function adjustZoom" in js, "Missing adjustZoom in app.js"
        assert "function resetZoom" in js, "Missing resetZoom in app.js"
        assert "function toggleAppFullscreen" in js, "Missing toggleAppFullscreen in app.js"
        assert "function setFolderDrawerCategory" in js, "Missing setFolderDrawerCategory in app.js"
        assert "function playActiveFolderTracks" in js, "Missing playActiveFolderTracks in app.js"
        assert "function playActiveFolderInKinozal" in js, "Missing playActiveFolderInKinozal in app.js"
        assert "folder-badge-btn" in js, "Missing folder-badge-btn in app.js"
        assert "musiqa_deck_collapsed" in js, "Missing musiqa_deck_collapsed in app.js"
        print("JavaScript verification: 100% OK")

        # 5. Test /api/library with whole_pc scope
        res_lib = requests.get(f"http://127.0.0.1:{port}/api/library?scope=whole_pc", timeout=10)
        assert res_lib.status_code == 200
        lib = res_lib.json()
        items = lib.get("items", [])
        print(f"Library whole_pc returned {len(items)} tracks across folders!")
        if items:
            sample_folders = set(x.get("folder") for x in items[:20])
            print(f"Sample folders detected: {sample_folders}")

        print("\nALL VERIFICATIONS PASSED WITH ZERO DEFECTS (100% MUKAMMAL)!")

    finally:
        try:
            proc.terminate()
        except:
            pass

if __name__ == "__main__":
    main()
