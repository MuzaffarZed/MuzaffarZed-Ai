import os
from win32com.client import Dispatch

desktop = os.path.join(os.path.expanduser("~"), "Desktop")
path = os.path.join(desktop, "MuzaffarDub - YouTube Dublyaj.lnk")
target = r"C:\Users\MuzaffarZed\ai_workspace\MuzaffarDub\Start_MuzaffarDub.bat"
wDir = r"C:\Users\MuzaffarZed\ai_workspace\MuzaffarDub"

shell = Dispatch('WScript.Shell')
shortcut = shell.CreateShortCut(path)
shortcut.Targetpath = target
shortcut.WorkingDirectory = wDir
shortcut.Description = "YouTube jonli o'zbekcha dublyaj serveri - Dasturchi MuzaffarZed"
shortcut.save()
print("Shortcut created successfully at:", path)
