import subprocess

adb = r"C:\Users\MuzaffarZed\AppData\Local\Android\Sdk\platform-tools\adb.exe"

def run_adb(args):
    r = subprocess.run([adb] + args, capture_output=True, text=True, errors="replace")
    return r.stdout.strip()

print("Model:", run_adb(["shell", "getprop", "ro.product.model"]))
print("Brand:", run_adb(["shell", "getprop", "ro.product.brand"]))
print("Android Version:", run_adb(["shell", "getprop", "ro.build.version.release"]))
print("Hardware:", run_adb(["shell", "getprop", "ro.hardware"]))
print("\n=== STORAGE (df -h) ===")
print(run_adb(["shell", "df", "-h"]))
print("\n=== RUNNING PACKAGES / APPS ===")
print(run_adb(["shell", "dumpsys", "window", "windows"]))
