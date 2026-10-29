import psutil
import time

found = False
for p in psutil.process_iter(['pid', 'name', 'cmdline', 'memory_info']):
    if 'fl64' in (p.info['name'] or '').lower():
        found = True
        print(f"FL64 is ALIVE! PID: {p.pid}, Memory: {p.info['memory_info'].rss/1024/1024:.1f} MB, Cmd: {p.info['cmdline']}")

if not found:
    print("FL64 is not running.")
