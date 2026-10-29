import os, time, subprocess, shutil
import sys
sys.stdout.reconfigure(encoding='utf-8')

src = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\publish_single\Musiqa_Markazi_Pro.exe"
dst = r"C:\Users\MuzaffarZed\Desktop\Musiqa_Markazi_Pro.exe"

print("1. Terminating running Musiqa_Markazi_Pro processes...")
subprocess.run(["taskkill", "/F", "/IM", "Musiqa_Markazi_Pro.exe"], capture_output=True)
time.sleep(1.5)

print(f"2. Copying {src} to {dst}...")
shutil.copy2(src, dst)
print("File copied successfully. Size:", os.path.getsize(dst))

print("3. Launching new Musiqa_Markazi_Pro from Desktop...")
proc = subprocess.Popen([dst], cwd=os.path.dirname(dst))
print(f"Launched with PID {proc.pid}. Waiting 3 seconds for UI load...")
time.sleep(3.5)

print("Done!")
