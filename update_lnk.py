import win32com.client
import os

shell = win32com.client.Dispatch("WScript.Shell")
lnk_path = r"C:\Users\MuzaffarZed\Desktop\Mani Izlab - FL Studio Loyihasi.lnk"

shortcut = shell.CreateShortcut(lnk_path)
shortcut.TargetPath = r"C:\Program Files\Image-Line\FL Studio 2025\FL64.exe"
shortcut.Arguments = r'"C:\Users\MuzaffarZed\Desktop\vakal minus\Mani_Izlab_Ovvora_Bolmang_Studio_Project.flp"'
shortcut.WorkingDirectory = r"C:\Program Files\Image-Line\FL Studio 2025"
shortcut.IconLocation = r"C:\Program Files\Image-Line\FL Studio 2025\FL64.exe,0"
shortcut.Description = "Mani Izlab Ovvora Bolmang - FL Studio Professional Studio Project"
shortcut.Save()

print("Shortcut updated successfully with correct WorkingDirectory!")
