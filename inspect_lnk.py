import win32com.client
import os

shell = win32com.client.Dispatch("WScript.Shell")
lnk_path = r"C:\Users\MuzaffarZed\Desktop\Mani Izlab - FL Studio Loyihasi.lnk"

if os.path.exists(lnk_path):
    shortcut = shell.CreateShortcut(lnk_path)
    print("Shortcut exists:")
    print("Target:", shortcut.TargetPath)
    print("Arguments:", shortcut.Arguments)
    print("WorkingDir:", shortcut.WorkingDirectory)
    print("IconLocation:", shortcut.IconLocation)
else:
    print("Shortcut does not exist at:", lnk_path)
