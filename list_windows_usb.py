import subprocess

ps_script = """
Get-PnpDevice -PresentOnly | Where-Object { $_.Class -in @('HIDClass', 'USB') } | Select-Object FriendlyName, InstanceId | Format-Table -Wrap
"""

with open("C:/Users/MuzaffarZed/ai_workspace/list_usb.ps1", "w", encoding="utf-8") as f:
    f.write(ps_script)

r = subprocess.run([
    "powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
    "-File", "C:/Users/MuzaffarZed/ai_workspace/list_usb.ps1"
], capture_output=True, text=True)

print(r.stdout)
