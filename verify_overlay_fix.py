import winreg

print("=== VERIFYING REGISTRY ===")
with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\GameBar") as k:
    v, _ = winreg.QueryValueEx(k, "ShowStartupPanel")
    print(f"GameBar ShowStartupPanel = {v} (0 means disabled)")

with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"System\GameConfigStore") as k:
    v, _ = winreg.QueryValueEx(k, "GameDVR_Enabled")
    print(f"GameConfigStore GameDVR_Enabled = {v} (0 means disabled)")

print("\n=== VERIFYING DGVOODOO CONF ===")
for p in [r"D:\KANPIYUTER O'YINLARI\Alien Shooter\dgVoodoo.conf", r"D:\KANPIYUTER O'YINLARI\FlatOut2\dgVoodoo.conf"]:
    print(f"Path: {p}")
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if 'watermark' in line.lower():
                print(" ", line.strip())
