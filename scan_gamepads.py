import subprocess
import json
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ps_script = """
Get-PnpDevice -PresentOnly | Select-Object FriendlyName, InstanceId, Class, Status, Problem | ConvertTo-Json -Depth 2
"""

with open(r"C:\Users\MuzaffarZed\ai_workspace\get_pnp.ps1", "w", encoding="utf-8") as f:
    f.write(ps_script)

res = subprocess.run(
    ["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-File", r"C:\Users\MuzaffarZed\ai_workspace\get_pnp.ps1"],
    capture_output=True, text=True, errors='ignore'
)

try:
    devices = json.loads(res.stdout)
    if isinstance(devices, dict):
        devices = [devices]
    
    print(f"Total present devices: {len(devices)}")
    print("=" * 60)
    for d in devices:
        name = d.get('FriendlyName') or ''
        cid = d.get('Class') or ''
        inst = d.get('InstanceId') or ''
        status = d.get('Status') or ''
        
        # Check for Gamepad / Joystick / USB / HID devices
        is_relevant = any(k in name.lower() for k in ['game', 'joy', 'controller', 'twin', 'shanwan', 'usb', 'hid', 'wireless', 'composite', 'xinput', 'xbox'])
        if is_relevant or cid in ['HIDClass', 'USB', 'XboxComposite', 'XnaComposite']:
            print(f"[{cid}] {name} | Status: {status} | ID: {inst}")
except Exception as e:
    print(f"Error parsing JSON: {e}")
    print("Raw output sample:", res.stdout[:1000])
