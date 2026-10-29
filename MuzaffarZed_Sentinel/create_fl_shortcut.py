import os
import win32com.client

wsh = win32com.client.Dispatch('WScript.Shell')
s_path = os.path.expanduser(r'~\Desktop\Mani Izlab - FL Studio Loyihasi.lnk')
fl_exe = r'C:\Program Files\Image-Line\FL Studio 2025\FL64.exe'
flp = os.path.expanduser(r'~\Desktop\vakal minus\Mani_Izlab_Ovvora_Bolmang_Studio_Project.flp')

sc = wsh.CreateShortcut(s_path)
sc.TargetPath = fl_exe
sc.Arguments = f'"{flp}"'
sc.WorkingDirectory = os.path.expanduser(r'~\Documents\Image-Line')
sc.IconLocation = f"{fl_exe},0"
sc.Description = "Mani Izlab Ovvora Bo'lmang - FL Studio 2025 Studiya Loyihasi"
sc.Save()
print("Created Desktop Shortcut:", s_path)
