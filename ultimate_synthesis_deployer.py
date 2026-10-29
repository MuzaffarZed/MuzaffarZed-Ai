import subprocess
import sys
import os
import urllib.request
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ADB_PATH = r"C:\platform-tools\adb.exe"

def run_adb(cmd):
    full_cmd = [ADB_PATH] + cmd
    res = subprocess.run(full_cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    return res.stdout.strip()

def get_latest_github_apk(repo, name_filter, exclude_filter=None):
    api_url = f"https://api.github.com/repos/{repo}/releases/latest"
    req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())
        for asset in data.get("assets", []):
            name = asset.get("name", "")
            if name.endswith(".apk") and name_filter in name:
                if exclude_filter and exclude_filter in name:
                    continue
                return asset.get("browser_download_url"), name
    return None, None

def download_and_install(url, filename, desc):
    print(f"\n[*] Processing: {desc}")
    target_path = os.path.join(os.environ["TEMP"], filename)
    print(f"    [+] Downloading from: {url} ...")
    try:
        urllib.request.urlretrieve(url, target_path)
        print("    [+] Installing via ADB...")
        res = run_adb(["install", "-r", "-d", target_path])
        print(f"    [+] Result: {res}")
        if os.path.exists(target_path):
            os.remove(target_path)
        return "Success" in res
    except Exception as e:
        print(f"    [-] Error: {e}")
        return False

def main():
    print("=== DEPLOYING THE UNIVERSAL OS SYNTHESIS ON JANOB MUZAFFAR'S TABLET ===")
    
    # 1. LINUX ENGINE: Termux (ARM64)
    print("\n=======================================================")
    print("PHASE 1: LINUX ENGINE (Termux)")
    print("=======================================================")
    termux_url, t_name = get_latest_github_apk("termux/termux-app", "arm64-v8a", "apt-android-7")
    if not termux_url:
        termux_url, t_name = get_latest_github_apk("termux/termux-app", "universal")
    if termux_url:
        download_and_install(termux_url, t_name, "Termux Linux Engine")
    else:
        print("    [-] Termux release not found via GitHub API.")

    # 2. WINDOWS & TABLET LINK: LocalSend (Universal Clipboard & AirDrop)
    print("\n=======================================================")
    print("PHASE 2: WINDOWS & TABLET LINK (LocalSend)")
    print("=======================================================")
    localsend_url, ls_name = get_latest_github_apk("localsend/localsend", "apk")
    if localsend_url:
        download_and_install(localsend_url, ls_name, "LocalSend Universal Hub")
    else:
        print("    [-] LocalSend release not found via GitHub API.")

    # 3. GRAPHENEOS FIREWALL: NetGuard
    print("\n=======================================================")
    print("PHASE 3: GRAPHENEOS FIREWALL (NetGuard)")
    print("=======================================================")
    netguard_url, ng_name = get_latest_github_apk("M66B/NetGuard", "netguard")
    if netguard_url:
        download_and_install(netguard_url, ng_name, "NetGuard Network Firewall")
    else:
        print("    [-] NetGuard release not found via GitHub API.")
        
    print("\n=======================================================")
    print("PHASE 4: VERIFICATION")
    print("=======================================================")
    pkgs = run_adb(["shell", "pm", "list", "packages"]).splitlines()
    installed = [p.replace("package:", "").strip() for p in pkgs]
    
    modules = {
        "Linux Engine (Termux)": "com.termux",
        "Universal Clipboard & AirDrop (LocalSend)": "org.localsend.localsend_app",
        "GrapheneOS Firewall (NetGuard)": "eu.faircode.netguard"
    }
    
    for name, pkg in modules.items():
        status = "INSTALLED & READY" if pkg in installed else "PENDING"
        print(f"    [+] {name}: {status}")

if __name__ == "__main__":
    main()
