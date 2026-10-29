import subprocess

ps1 = """
Get-PnpDevice | Where-Object { $_.FriendlyName -like '*Samsung*' -or $_.FriendlyName -like '*Galaxy*' -or $_.Class -eq 'AndroidDevice' } | Select-Object Status, Class, FriendlyName, InstanceId | Format-Table -AutoSize
"""
with open(r"C:\Users\MuzaffarZed\ai_workspace\check_usb.ps1", "w", encoding="utf-8") as f:
    f.write(ps1)

res = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-File", r"C:\Users\MuzaffarZed\ai_workspace\check_usb.ps1"], capture_output=True, text=True)
print(res.stdout)
