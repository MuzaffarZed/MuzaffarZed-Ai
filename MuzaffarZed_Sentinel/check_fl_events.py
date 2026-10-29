import subprocess

ps_code = """
$events = Get-WinEvent -FilterHashtable @{LogName='Application'; Level=1,2,3; StartTime=(Get-Date).AddMinutes(-15)} -ErrorAction SilentlyContinue
foreach ($e in $events) {
    if ($e.Message -like "*FL64*" -or $e.Message -like "*Image-Line*") {
        Write-Output "TIME: $($e.TimeCreated)"
        Write-Output "PROVIDER: $($e.ProviderName)"
        Write-Output "MESSAGE: $($e.Message)"
        Write-Output "------------------------"
    }
}
"""

p = subprocess.run(
    ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_code],
    capture_output=True,
    text=True
)
print("Event log search results:")
print(p.stdout if p.stdout.strip() else "Zero crash events found in Application log.")
