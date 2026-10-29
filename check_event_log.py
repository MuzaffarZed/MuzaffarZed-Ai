import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ps = """
Get-WinEvent -FilterHashtable @{LogName='Application'; ProviderName='.NET Runtime','Application Error'} -MaxEvents 5 | 
    Select-Object TimeCreated, ProviderName, Message | Format-List
"""

with open(r"C:\Users\MuzaffarZed\ai_workspace\get_events.ps1", "w", encoding="utf-8") as f:
    f.write(ps)

res = subprocess.run(
    ["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-File", r"C:\Users\MuzaffarZed\ai_workspace\get_events.ps1"],
    capture_output=True, text=True, errors='ignore'
)
print(res.stdout)
