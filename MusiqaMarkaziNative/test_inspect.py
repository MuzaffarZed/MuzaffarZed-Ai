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

eval_js('switchTab("simulator");')
time.sleep(1)

res = eval_js('''
(() => {
    const stage = document.getElementById('cinemaStageCard');
    const slot = document.getElementById('cinemaVideoSlot');
    const topBar = document.querySelector('.cinema-top-bar');
    const ctrlDeck = document.querySelector('.cinema-control-deck');
    const overlay = document.getElementById('cinemaAudioOverlay');
    const getRect = el => {
        if (!el) return null;
        const r = el.getBoundingClientRect();
        return {
            x: Math.round(r.x),
            y: Math.round(r.y),
            top: Math.round(r.top),
            bottom: Math.round(r.bottom),
            height: Math.round(r.height),
            width: Math.round(r.width),
            computedPos: window.getComputedStyle(el).position,
            computedDisplay: window.getComputedStyle(el).display,
            computedTop: window.getComputedStyle(el).top,
            computedBottom: window.getComputedStyle(el).bottom
        };
    };
    return {
        stage: getRect(stage),
        slot: getRect(slot),
        topBar: getRect(topBar),
        ctrlDeck: getRect(ctrlDeck),
        overlay: getRect(overlay)
    };
})()
''')
print('Cinema Rects (Active Tab):')
print(json.dumps(res, indent=2))
