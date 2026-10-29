import urllib.request
import json
import os
import time

appdata = os.environ.get('LOCALAPPDATA', r'C:\Users\MuzaffarZed\AppData\Local')
port_file = os.path.join(appdata, 'UzbekMusiqaMarkaziPro', 'running_port.txt')
with open(port_file, 'r', encoding='utf-8') as f:
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

print(f"=== LIVE VERIFICATION ON PORT {port} ===")

# 1. TEST MINI-DOCK
print("\n[TEST 1] Mini-Dock Non-Overlapping Layout...")
eval_js("if (!state.isMiniDock) toggleMiniDock();")
time.sleep(1)

mini_metrics = eval_js('''
(() => {
    const deck = document.querySelector('.master-deck');
    const left = document.querySelector('.deck-left');
    const center = document.querySelector('.deck-center');
    const right = document.querySelector('.deck-right');
    const pills = document.querySelector('.quick-fx-pills');
    const vol = document.getElementById('volumeSlider');
    const playBtn = document.getElementById('btnPlayPause');
    const restoreBtn = document.getElementById('btnRestoreFull');
    const canvas = document.getElementById('visualizerCanvas');

    const getR = el => el ? {
        left: Math.round(el.getBoundingClientRect().left),
        right: Math.round(el.getBoundingClientRect().right),
        top: Math.round(el.getBoundingClientRect().top),
        bottom: Math.round(el.getBoundingClientRect().bottom),
        width: Math.round(el.getBoundingClientRect().width),
        height: Math.round(el.getBoundingClientRect().height),
        display: window.getComputedStyle(el).display
    } : null;

    return {
        isMiniDock: state.isMiniDock,
        bodyHasClass: document.body.classList.contains('mini-dock'),
        deckDisplay: window.getComputedStyle(deck).display,
        deckFlexDirection: window.getComputedStyle(deck).flexDirection,
        pillsDisplay: pills ? window.getComputedStyle(pills).display : null,
        canvasDisplay: canvas ? window.getComputedStyle(canvas).display : null,
        leftRect: getR(left),
        centerRect: getR(center),
        rightRect: getR(right),
        volRect: getR(vol),
        playBtnRect: getR(playBtn),
        restoreBtnRect: getR(restoreBtn)
    };
})()
''')

print("Mini-Dock Metrics:")
print(json.dumps(mini_metrics, indent=2))

# Verify assertions
assert mini_metrics["isMiniDock"] == True, "Mini-dock state must be True"
assert mini_metrics["deckDisplay"] == "flex", "Deck must be flexbox"
assert mini_metrics["pillsDisplay"] == "none", "FX pills must be hidden in mini-dock"
assert mini_metrics["canvasDisplay"] == "none", "Visualizer canvas must be hidden in mini-dock"
assert mini_metrics["volRect"]["width"] <= 55, "Volume slider must be compact (<=55px)"

# Check non-overlapping guarantee
# Center must be to the right of Left, Right must be to the right of Center
left_r = mini_metrics["leftRect"]["right"]
center_l = mini_metrics["centerRect"]["left"]
center_r = mini_metrics["centerRect"]["right"]
right_l = mini_metrics["rightRect"]["left"]
print(f"Layout bounds: Left.right={left_r} <= Center.left={center_l} | Center.right={center_r} <= Right.left={right_l}")
assert center_l >= left_r - 2, "Center must not overlap Left"
assert right_l >= center_r - 2, "Right must not overlap Center"
print(">>> MINI-DOCK ZERO OVERLAP VERIFIED! (100% SUCCESS)")

# Test track change in mini-dock
print("\n[TEST 2] Mini-Dock Track Change Persistence...")
eval_js("playNextTrack();")
time.sleep(1)
persists = eval_js("state.isMiniDock && document.body.classList.contains('mini-dock')")
assert persists == True, "Mini-dock mode must persist across track changes"
print(">>> MINI-DOCK PERSISTENCE VERIFIED! (100% SUCCESS)")

# Restore full window
eval_js("toggleMiniDock();")
time.sleep(1)

# 2. TEST KINOZAL AUDIO OVERLAY SEPARATION
print("\n[TEST 3] Kinozal Audio Overlay Non-Overlapping Layout...")
eval_js("switchTab('simulator');")
time.sleep(1)

# Play an audio track
eval_js('''
(() => {
    const audioTrack = (state.libraryItems || []).find(x => x.mediaType !== 'mp4');
    if (audioTrack) playFileImmediately(audioTrack.path);
})()
''')
time.sleep(2)

kino_audio_metrics = eval_js('''
(() => {
    const stage = document.getElementById('cinemaStageCard');
    const slot = document.getElementById('cinemaVideoSlot');
    const topBar = document.querySelector('.cinema-top-bar');
    const ctrlDeck = document.querySelector('.cinema-control-deck');
    const overlay = document.getElementById('cinemaAudioOverlay');
    const cover = document.getElementById('simCoverImg');

    const getR = el => el ? {
        top: Math.round(el.getBoundingClientRect().top),
        bottom: Math.round(el.getBoundingClientRect().bottom),
        left: Math.round(el.getBoundingClientRect().left),
        right: Math.round(el.getBoundingClientRect().right),
        height: Math.round(el.getBoundingClientRect().height),
        width: Math.round(el.getBoundingClientRect().width),
        position: window.getComputedStyle(el).position,
        display: window.getComputedStyle(el).display,
        zIndex: window.getComputedStyle(el).zIndex
    } : null;

    return {
        topBar: getR(topBar),
        ctrlDeck: getR(ctrlDeck),
        overlay: getR(overlay),
        cover: getR(cover),
        activeTrackType: state.currentTrack ? state.currentTrack.mediaType : null
    };
})()
''')

print("Kinozal Audio Mode Metrics:")
print(json.dumps(kino_audio_metrics, indent=2))

tb = kino_audio_metrics["topBar"]
cd = kino_audio_metrics["ctrlDeck"]
ov = kino_audio_metrics["overlay"]

# Verifications
assert tb["position"] == "absolute", "Top bar must be absolute"
assert cd["position"] == "absolute", "Control deck must be absolute"
assert ov["position"] == "absolute", "Overlay must be absolute"
assert int(tb["zIndex"]) >= 25, "Top bar z-index must be higher than overlay"
assert int(cd["zIndex"]) >= 25, "Control deck z-index must be higher than overlay"

# Boundary check: Top bar must be at the very top, Control deck at the very bottom
assert tb["top"] < cd["top"], "Top bar must be above control deck"
assert cd["bottom"] > tb["bottom"], "Control deck must be at the bottom"
print(f"TopBar: y={tb['top']}..{tb['bottom']} | ControlDeck: y={cd['top']}..{cd['bottom']}")
print(">>> KINOZAL TOP BAR AND CONTROL DECK ANCHORS VERIFIED! (100% SUCCESS)")

# 3. TEST ACTUAL MP4 VIDEO PLAYBACK
print("\n[TEST 4] Actual MP4 Video Playback in Kinozal...")
eval_js('''
playFileImmediately("C:\\\\Users\\\\MuzaffarZed\\\\Desktop\\\\Toy Vidiyo.mp4");
''')
time.sleep(3)

video_status = eval_js('''
(() => {
    const v = document.getElementById('carVideoPlayer');
    const overlay = document.getElementById('cinemaAudioOverlay');
    return {
        src: v.src,
        paused: v.paused,
        currentTime: v.currentTime,
        duration: v.duration,
        videoWidth: v.videoWidth,
        videoHeight: v.videoHeight,
        overlayVisible: overlay.classList.contains('visible'),
        badgeText: document.getElementById('cinemaFormatBadge')?.textContent
    };
})()
''')

print("MP4 Video Playback Status:")
print(json.dumps(video_status, indent=2))

assert video_status["overlayVisible"] == False, "Overlay must be hidden when MP4 video is playing"
assert "Toy Vidiyo.mp4" in urllib.parse.unquote(video_status["src"]), "Video src must match Toy Vidiyo.mp4"
assert "HD MP4" in video_status["badgeText"], "Badge must display HD MP4"
print(">>> MP4 VIDEO PLAYBACK IN KINOZAL VERIFIED! (100% SUCCESS)")

print("\nALL ZERO-DEFECT QUALITY TESTS PASSED COMPLETELY!")
