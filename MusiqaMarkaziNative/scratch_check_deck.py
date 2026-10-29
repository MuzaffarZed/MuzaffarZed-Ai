import os
import requests

port_file = os.path.expandvars(r"%LOCALAPPDATA%\UzbekMusiqaMarkaziPro\running_port.txt")
with open(port_file, "r") as f:
    port = f.read().strip()

res = requests.post(f"http://127.0.0.1:{port}/api/native/action", json={
    "action": "evalJs",
    "code": "togglePlayerDock(true); document.body.className;"
})
print("Restored body class:", res.json())
