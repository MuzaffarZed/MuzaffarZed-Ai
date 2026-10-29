import os
import sys
import re
import winreg
import win32com.client

sys.stdout.reconfigure(encoding='utf-8')

def fix_all():
    print("==================================================")
    print("STARTING COMPREHENSIVE ZERO-DEFECT OVERLAY REMOVAL")
    print("==================================================")

    # -------------------------------------------------------------------------
    # 1. FIX DGVOODOO WATERMARKS ACROSS ALL GAMES
    # -------------------------------------------------------------------------
    d_games = r"D:\KANPIYUTER O'YINLARI"
    fixed_confs = 0
    if os.path.exists(d_games):
        for root, dirs, files in os.walk(d_games):
            for f in files:
                if f.lower() == 'dgvoodoo.conf':
                    conf_path = os.path.join(root, f)
                    try:
                        with open(conf_path, 'r', encoding='utf-8', errors='ignore') as fp:
                            content = fp.read()

                        # Disable dgVoodooWatermark, 3DfxWatermark, 3DfxSplashScreen
                        new_content = re.sub(r'(?i)^\s*dgVoodooWatermark\s*=.*$', 'dgVoodooWatermark                   = false', content, flags=re.MULTILINE)
                        new_content = re.sub(r'(?i)^\s*3DfxWatermark\s*=.*$', '3DfxWatermark                       = false', new_content, flags=re.MULTILINE)
                        new_content = re.sub(r'(?i)^\s*3DfxSplashScreen\s*=.*$', '3DfxSplashScreen                    = false', new_content, flags=re.MULTILINE)

                        with open(conf_path, 'w', encoding='utf-8') as fp:
                            fp.write(new_content)
                        print(f"[+] Fixed dgVoodoo watermark in: {conf_path}")
                        fixed_confs += 1
                    except Exception as e:
                        print(f"[-] Error fixing {conf_path}: {e}")

    print(f"Total dgVoodoo configs cleaned: {fixed_confs}")

    # -------------------------------------------------------------------------
    # 2. DISABLE WINDOWS GAME BAR "PRESS WIN+G" & GAMEDVR POPUPS IN REGISTRY
    # -------------------------------------------------------------------------
    print("\n--- Disabling Windows Game Bar & Game Mode popups in Registry ---")
    try:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\GameBar") as key:
            winreg.SetValueEx(key, "ShowStartupPanel", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key, "UseNexusForGameBarEnabled", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key, "AutoGameModeEnabled", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key, "AllowAutoGameMode", 0, winreg.REG_DWORD, 0)
        print("[+] Disabled GameBar ShowStartupPanel (Press Win+G prompt removed)")
    except Exception as e:
        print("[-] Error updating Software\\Microsoft\\GameBar:", e)

    try:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"System\GameConfigStore") as key:
            winreg.SetValueEx(key, "GameDVR_Enabled", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key, "GameDVR_FSEBehaviorMode", 0, winreg.REG_DWORD, 2)
            winreg.SetValueEx(key, "GameDVR_HonorUserFSEBehaviorMode", 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, "GameDVR_DXGIHonorFSEWindowsCompatible", 0, winreg.REG_DWORD, 1)
        print("[+] Disabled GameDVR in GameConfigStore")
    except Exception as e:
        print("[-] Error updating System\\GameConfigStore:", e)

    try:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\GameDVR") as key:
            winreg.SetValueEx(key, "AppCaptureEnabled", 0, winreg.REG_DWORD, 0)
        print("[+] Disabled GameDVR AppCaptureEnabled")
    except Exception as e:
        print("[-] Error updating GameDVR:", e)

    # -------------------------------------------------------------------------
    # 3. SILENT WINDOWLESS LAUNCH FOR CYBER ARENA & GAMEPAD STUDIO
    # -------------------------------------------------------------------------
    print("\n--- Configuring Silent Windowless Launch for Cyber Arena ---")
    game_dir = r"C:\Users\MuzaffarZed\ai_workspace\CyberArena_MuzaffarZed"
    cyber_arena_py = os.path.join(game_dir, "cyber_arena.py")
    
    # Hide Pygame support prompt in python code
    if os.path.exists(cyber_arena_py):
        with open(cyber_arena_py, 'r', encoding='utf-8') as f:
            code = f.read()
        if "PYGAME_HIDE_SUPPORT_PROMPT" not in code:
            code = 'import os\nos.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"\n' + code
            with open(cyber_arena_py, 'w', encoding='utf-8') as f:
                f.write(code)
            print("[+] Added PYGAME_HIDE_SUPPORT_PROMPT to cyber_arena.py")

    # Create silent VBScript launcher
    vbs_path = os.path.join(game_dir, "run_cyber_arena.vbs")
    vbs_code = '''Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\\Users\\MuzaffarZed\\ai_workspace\\CyberArena_MuzaffarZed"
WshShell.Run """C:\\Users\\MuzaffarZed\\ai_workspace\\venv\\Scripts\\pythonw.exe"" ""C:\\Users\\MuzaffarZed\\ai_workspace\\CyberArena_MuzaffarZed\\cyber_arena.py""", 0, False
'''
    with open(vbs_path, 'w', encoding='utf-8') as f:
        f.write(vbs_code)
    print(f"[+] Created silent launcher: {vbs_path}")

    # Update Desktop Shortcut for Cyber Arena
    wscript = win32com.client.Dispatch('WScript.Shell')
    desktop = r"C:\Users\MuzaffarZed\Desktop"
    shortcut_path = os.path.join(desktop, "Cyber Arena - 2x Jostik Oyini.lnk")
    shortcut = wscript.CreateShortcut(shortcut_path)
    shortcut.TargetPath = vbs_path
    shortcut.WorkingDirectory = game_dir
    shortcut.Description = "Cyber Arena: 2x Jostik uchun Mukammal Jang Oyini (by MuzaffarZed)"
    shortcut.IconLocation = r"C:\Windows\System32\shell32.dll,24"
    shortcut.WindowStyle = 7 # Minimized / Silent
    shortcut.Save()
    print(f"[+] Updated Cyber Arena desktop shortcut: {shortcut_path}")

    # Update Desktop Shortcut for 2x Jostik Boshqaruv Markazi
    studio_lnk = os.path.join(desktop, "2x Jostik Boshqaruv Markazi.lnk")
    if os.path.exists(studio_lnk):
        s = wscript.CreateShortcut(studio_lnk)
        s.TargetPath = r"C:\Users\MuzaffarZed\AppData\Local\Programs\Python\Python312\pythonw.exe"
        s.Arguments = r'"C:\Users\MuzaffarZed\ai_workspace\MuzaffarZed_Twin_Gamepad_Studio.py"'
        s.WorkingDirectory = r"C:\Users\MuzaffarZed\ai_workspace"
        s.IconLocation = r"C:\Windows\System32\shell32.dll,24"
        s.Save()
        print(f"[+] Updated 2x Jostik Boshqaruv Markazi shortcut to pythonw.exe")

    print("\n[SUCCESS] All game entry white text, console popups, and watermarks eliminated!")

if __name__ == '__main__':
    fix_all()
