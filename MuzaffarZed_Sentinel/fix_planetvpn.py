import os
import subprocess
import win32com.client

install_dir = r"C:\Program Files\WindowsApps\FreeVPNPlanet.PlanetVPN_2.10.113.0_x64__b2qrq2z57ppd2"
ps_cmd = f"Get-ChildItem -Path '{install_dir}' -Recurse -Filter '*.ico' | Select-Object -ExpandProperty FullName"

p = subprocess.run(
    ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_cmd],
    capture_output=True,
    text=True
)

icons = [line.strip() for line in p.stdout.splitlines() if line.strip().endswith('.ico')]
print("Found icons:", icons)

if icons:
    best_icon = icons[0]
    shortcut_path = os.path.expanduser(r"~\Desktop\PlanetVPN.lnk")
    wsh = win32com.client.Dispatch("WScript.Shell")
    sc = wsh.CreateShortcut(shortcut_path)
    sc.IconLocation = f"{best_icon},0"
    sc.Save()
    print("Successfully set PlanetVPN icon to:", best_icon)
else:
    # If no .ico found, look for .png or assets
    ps_png = f"Get-ChildItem -Path '{install_dir}' -Recurse -Filter '*.png' | Select-Object -ExpandProperty FullName"
    p2 = subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_png],
        capture_output=True,
        text=True
    )
    pngs = [line.strip() for line in p2.stdout.splitlines() if "logo" in line.lower() or "app" in line.lower()]
    print("Found PNGs:", pngs[:5])
