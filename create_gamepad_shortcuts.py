import os
import sys
import win32com.client

desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
shell = win32com.client.Dispatch("WScript.Shell")

# 1. Twin Gamepad Studio
sc1_path = os.path.join(desktop, "2x Jostik Boshqaruv Markazi.lnk")
sc1 = shell.CreateShortCut(sc1_path)
sc1.TargetPath = sys.executable
sc1.Arguments = r'"C:\Users\MuzaffarZed\ai_workspace\MuzaffarZed_Twin_Gamepad_Studio.py"'
sc1.WorkingDirectory = r"C:\Users\MuzaffarZed\ai_workspace"
sc1.Description = "Twin USB Gamepad 2x Jostik Boshqaruv Markazi by MuzaffarZed"
sc1.IconLocation = r"C:\Windows\System32\shell32.dll,24"
sc1.save()
print("Created:", sc1_path)

# 2. XOutput Shortcut
sc2_path = os.path.join(desktop, "XOutput (Xbox 360 Emulyator).lnk")
sc2 = shell.CreateShortCut(sc2_path)
sc2.TargetPath = r"C:\Users\MuzaffarZed\ai_workspace\XOutput\XOutput.exe"
sc2.WorkingDirectory = r"C:\Users\MuzaffarZed\ai_workspace\XOutput"
sc2.Description = "XOutput DirectInput to XInput Controller Bridge"
sc2.save()
print("Created:", sc2_path)

# 3. x360ce Shortcut
sc3_path = os.path.join(desktop, "x360ce Pro (Jostik Sozlagich).lnk")
sc3 = shell.CreateShortCut(sc3_path)
sc3.TargetPath = r"C:\Users\MuzaffarZed\ai_workspace\x360ce\x360ce.exe"
sc3.WorkingDirectory = r"C:\Users\MuzaffarZed\ai_workspace\x360ce"
sc3.Description = "x360ce Xbox 360 Controller Emulator"
sc3.save()
print("Created:", sc3_path)
