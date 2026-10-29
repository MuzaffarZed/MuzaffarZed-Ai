import subprocess

adb = r"C:\Users\MuzaffarZed\AppData\Local\Android\Sdk\platform-tools\adb.exe"

def run_adb(args):
    r = subprocess.run([adb] + args, capture_output=True, text=True, errors="replace")
    return r.stdout.strip()

print("=== /storage ===")
print(run_adb(["shell", "ls", "-la", "/storage"]))

print("\n=== MOUNTS ===")
mounts = run_adb(["shell", "mount"]).splitlines()
for m in mounts:
    if any(k in m.lower() for k in ["sd", "vfat", "fat", "media", "fuse", "storage"]):
        print(m)

print("\n=== LOGCAT ERRORS (gamebox or boxui) ===")
print(run_adb(["shell", "logcat", "-d", "-s", "gamebox", "GameBox", "BOXUI", "BoxUI", "VMedia"]))
