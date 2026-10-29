import requests
import json
import os

port_file = os.path.expandvars(r"%LOCALAPPDATA%\UzbekMusiqaMarkaziPro\running_port.txt")
with open(port_file, "r") as f:
    port = int(f.read().strip())

js = """
(() => {
    const c = document.querySelector(".media-card");
    const acts = c ? c.querySelector(".card-actions") : null;
    const main = acts ? acts.querySelector(".btn-card-turbo") : null;
    const subs = acts ? Array.from(acts.querySelectorAll(".card-sub-actions .btn")) : [];
    return {
        cardW: c ? c.getBoundingClientRect().width : 0,
        actsW: acts ? acts.getBoundingClientRect().width : 0,
        mainBtn: main ? {
            text: main.textContent.trim(),
            w: main.getBoundingClientRect().width,
            scrollW: main.scrollWidth,
            overflow: main.scrollWidth > (main.clientWidth + 1)
        } : null,
        subs: subs.map(s => ({
            text: s.textContent.trim(),
            w: s.getBoundingClientRect().width,
            scrollW: s.scrollWidth,
            overflow: s.scrollWidth > (s.clientWidth + 1)
        }))
    };
})()
"""

res = requests.post(f"http://127.0.0.1:{port}/api/native/action", json={"action": "evalJs", "code": js}).json()
raw = res.get("result", "")
try:
    data = json.loads(raw)
except Exception:
    data = raw
print("METRICS:", json.dumps(data, indent=2))
