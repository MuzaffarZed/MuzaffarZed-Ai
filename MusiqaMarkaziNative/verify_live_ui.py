import urllib.request
import json
import time
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

appdata = os.environ.get("LOCALAPPDATA", r"C:\Users\MuzaffarZed\AppData\Local")
port_file = os.path.join(appdata, "UzbekMusiqaMarkaziPro", "running_port.txt")
with open(port_file, "r", encoding="utf-8") as f:
    port = f.read().strip()

def eval_js(code):
    req = urllib.request.Request(
        f"http://127.0.0.1:{port}/api/native/action",
        data=json.dumps({"action": "evalJs", "code": code}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read().decode("utf-8"))
        raw = data.get("result", "")
        try:
            return json.loads(raw)
        except Exception:
            return raw

print(f"[Port {port}] Connecting to live UI...")

print("[1] Setting baseDir to Musiqa_Fleshka_2026 and scope to 'all'...")
eval_js("state.baseDir = 'C:\\\\Users\\\\MuzaffarZed\\\\Desktop\\\\Musiqa_Fleshka_2026';")
eval_js("setLibraryScope('all');")
time.sleep(2)

info = eval_js("""
({
    itemsCount: state.libraryItems ? state.libraryItems.length : 0,
    mp4Count: state.libraryItems ? state.libraryItems.filter(x => x.mediaType === 'mp4').length : 0,
    mp3Count: state.libraryItems ? state.libraryItems.filter(x => x.mediaType !== 'mp4').length : 0,
    folderDrawerBadge: document.getElementById('folderDrawerBadge')?.textContent,
    folderPillsCount: document.querySelectorAll('#libraryFolderPills .cat-pill').length
})
""")
print("Standard Library Scan:", info)

print("[2] Testing Collapsible Folder Drawer (Tepaga / Pastga ko'tarib tushirish)...")
eval_js("toggleFolderDrawer();")
drawer_collapsed = eval_js("document.getElementById('libraryFolderDrawer')?.classList.contains('collapsed')")
btn_text = eval_js("document.getElementById('folderDrawerToggleText')?.textContent")
print("Drawer collapsed state:", drawer_collapsed, "| Button text:", btn_text)

eval_js("toggleFolderDrawer();")
drawer_opened = eval_js("document.getElementById('libraryFolderDrawer')?.classList.contains('collapsed')")
print("Drawer reopened state (not collapsed):", not drawer_opened)

print("[3] Testing 'Whole PC' Music Scan (🖥️ Butun Kompyuter)...")
eval_js("setLibraryScope('whole_pc');")
time.sleep(3)

whole_pc_info = eval_js("""
({
    totalItems: state.libraryItems ? state.libraryItems.length : 0,
    folderPillsCount: document.querySelectorAll('#libraryFolderPills .cat-pill').length,
    drawerBadge: document.getElementById('folderDrawerBadge')?.textContent
})
""")
print("Whole PC scan results:", whole_pc_info)

print("[4] Testing Kinozal MP4 video clip playback and non-overlapping controls...")
eval_js("switchTab('simulator');")
time.sleep(1)

# Play first MP4 clip
eval_js("""
(() => {
    const mp4 = state.libraryItems.find(x => x.mediaType === 'mp4');
    if (mp4) playFileImmediately(mp4.path);
})()
""")
time.sleep(3)

kinozal_status = eval_js("""
(() => {
    const v = document.getElementById('carVideoPlayer');
    const topBar = document.querySelector('.cinema-top-bar');
    const ctrlDeck = document.querySelector('.cinema-control-deck');
    const vp = document.querySelector('.cinema-video-viewport');
    return {
        paused: v ? v.paused : true,
        currentTime: v ? v.currentTime : 0,
        readyState: v ? v.readyState : 0,
        videoWidth: v ? v.videoWidth : 0,
        videoHeight: v ? v.videoHeight : 0,
        topBarPosition: topBar ? window.getComputedStyle(topBar).position : null,
        topBarTop: topBar ? window.getComputedStyle(topBar).top : null,
        ctrlDeckPosition: ctrlDeck ? window.getComputedStyle(ctrlDeck).position : null,
        ctrlDeckBottom: ctrlDeck ? window.getComputedStyle(ctrlDeck).bottom : null
    };
})()
""")
print("Kinozal video playback status:", kinozal_status)

print("[5] Testing Mini-Dock (Kichraytirish) persistence...")
eval_js("toggleMiniDock();")
time.sleep(1)

mini_status = eval_js("""
({
    isMiniDockState: state.isMiniDock,
    bodyHasMiniDockClass: document.body.classList.contains('mini-dock'),
    appShellDisplay: window.getComputedStyle(document.querySelector('.app-shell')).display,
    masterDeckDisplay: window.getComputedStyle(document.querySelector('.master-deck')).display
})
""")
print("Mini-Dock state:", mini_status)

# Now play next track while in mini-dock: must NOT exit mini-dock!
eval_js("playNextTrack();")
time.sleep(1)

mini_after_next = eval_js("""
({
    isMiniDockState: state.isMiniDock,
    bodyHasMiniDockClass: document.body.classList.contains('mini-dock'),
    currentTitle: document.getElementById('deckTrackTitle')?.textContent
})
""")
print("Mini-Dock state after next track:", mini_after_next)

# Restore full window
eval_js("toggleMiniDock();")
time.sleep(1)
restored_status = eval_js("document.body.classList.contains('mini-dock')")
print("Mini-Dock restored (has class):", restored_status)
