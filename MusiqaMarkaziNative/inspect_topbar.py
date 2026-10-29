import requests
import json
import os

port_file = os.path.expandvars(r"%LOCALAPPDATA%\UzbekMusiqaMarkaziPro\running_port.txt")
with open(port_file, "r") as f:
    port = int(f.read().strip())

def eval_js(code):
    url = f"http://127.0.0.1:{port}/api/native/action"
    res = requests.post(url, json={"action": "evalJs", "code": code})
    raw = res.json().get("result", "")
    try:
        return json.loads(raw)
    except Exception:
        return raw

data = eval_js("""
(() => {
    const tb = document.querySelector(".stage-topbar");
    const controls = document.querySelector(".topbar-controls");
    const tbChildren = Array.from(tb.children).map(c => ({
        tag: c.tagName,
        id: c.id,
        className: c.className,
        width: c.getBoundingClientRect().width,
        left: c.getBoundingClientRect().left,
        right: c.getBoundingClientRect().right
    }));
    
    const ctrlChildren = Array.from(controls ? controls.children : []).map(c => ({
        tag: c.tagName,
        id: c.id,
        className: c.className,
        text: c.textContent.trim().substring(0, 15),
        width: c.getBoundingClientRect().width,
        left: c.getBoundingClientRect().left,
        right: c.getBoundingClientRect().right
    }));

    return {
        windowWidth: window.innerWidth,
        tbWidth: tb ? tb.getBoundingClientRect().width : 0,
        tbRight: tb ? tb.getBoundingClientRect().right : 0,
        tbChildren,
        ctrlWidth: controls ? controls.getBoundingClientRect().width : 0,
        ctrlRight: controls ? controls.getBoundingClientRect().right : 0,
        ctrlChildren
    };
})()
""")

print("Window innerWidth:", data["windowWidth"])
print("Stage Topbar Width:", data["tbWidth"], "| Right edge:", data["tbRight"])
print("Topbar Direct Children:")
for c in data["tbChildren"]:
    print(f"  [{c['tag']} #{c['id']} .{c['className']}] width={c['width']:.1f}, left={c['left']:.1f}, right={c['right']:.1f}")

print("\nTopbar Controls Total Width:", data["ctrlWidth"], "| Right edge:", data["ctrlRight"])
print("Controls Items:")
for c in data["ctrlChildren"]:
    print(f"  '{c['text']}' [{c['tag']} #{c['id']}] width={c['width']:.1f}, left={c['left']:.1f}, right={c['right']:.1f}")
