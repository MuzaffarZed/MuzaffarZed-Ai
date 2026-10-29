import os
import subprocess

ps_code = """
$WshShell = New-Object -ComObject WScript.Shell
$Desktop = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $Desktop "🎮 M8 PRO va O'yinlar Markazi.lnk"
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "pythonw.exe"
$Shortcut.Arguments = '\"C:\\Users\\MuzaffarZed\\ai_workspace\\MuzaffarZed_Game_Center.pyw\"'
$Shortcut.WorkingDirectory = "C:\\Users\\MuzaffarZed\\ai_workspace"
$Shortcut.Description = "M8 PRO Mini & Kompyuter O'yinlar Markazi (by MuzaffarZed)"
$Shortcut.IconLocation = "shell32.dll,24"
$Shortcut.Save()
Write-Host "Shortcut created at $ShortcutPath"
"""

with open("create_shortcut.ps1", "w", encoding="utf-8") as f:
    f.write(ps_code)

res = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-File", "create_shortcut.ps1"], capture_output=True, text=True)
print(res.stdout)
