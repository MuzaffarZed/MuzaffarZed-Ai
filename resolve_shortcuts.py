import os
import subprocess

ps_script = """
$wsh = New-Object -ComObject WScript.Shell
$desktop = [Environment]::GetFolderPath("Desktop")
Get-ChildItem $desktop -Filter "*.lnk" | ForEach-Object {
    $target = $wsh.CreateShortcut($_.FullName).TargetPath
    Write-Host "$($_.Name) -> $target"
}
"""

with open("resolve_lnk.ps1", "w", encoding="utf-8") as f:
    f.write(ps_script)

res = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-File", "resolve_lnk.ps1"], capture_output=True, text=True)
print(res.stdout)
