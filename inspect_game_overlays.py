import os
import sys
import psutil
import win32com.client
import winreg

def inspect():
    wscript = win32com.client.Dispatch('WScript.Shell')
    desktop = r'C:\Users\MuzaffarZed\Desktop'

    print("=== DESKTOP SHORTCUT TARGETS ===")
    for item in os.listdir(desktop):
        if item.endswith('.lnk'):
            try:
                p = os.path.join(desktop, item)
                s = wscript.CreateShortcut(p)
                if any(x in item.lower() for x in ['jostik', 'cyber', 'm8', 'gta', 'flatout', 'counter', 'nfs', 'mafia', 'firewatch', 'blur']):
                    print(f"{item} -> {s.TargetPath} ({s.Arguments})")
            except Exception as e:
                pass

    print("\n=== RUNNING PROCESSES (OVERLAY / GAME / OSD / XBOX) ===")
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            n = proc.info['name'].lower()
            if any(k in n for k in ['game', 'bar', 'xbox', 'overlay', 'rtss', 'afterburner', 'nvidia', 'geforce', 'steam', 'discord', 'lenovo', 'vantage', 'osd', 'cmd', 'conhost']):
                print(f"{proc.info['pid']}: {proc.info['name']}")
        except Exception:
            pass

    print("\n=== GAMEBAR & GAMEDVR REGISTRY SETTINGS ===")
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\GameBar") as k:
            for i in range(winreg.QueryInfoKey(k)[1]):
                name, val, _ = winreg.EnumValue(k, i)
                print(f"HKCU\\Software\\Microsoft\\GameBar\\{name} = {val}")
    except Exception as e:
        print("GameBar key error:", e)

    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"System\GameConfigStore") as k:
            for i in range(winreg.QueryInfoKey(k)[1]):
                name, val, _ = winreg.EnumValue(k, i)
                print(f"HKCU\\System\\GameConfigStore\\{name} = {val}")
    except Exception as e:
        print("GameConfigStore key error:", e)

if __name__ == '__main__':
    inspect()
