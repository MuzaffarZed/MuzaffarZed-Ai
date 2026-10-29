import subprocess, time, shutil, os

src = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\publish_single\Musiqa_Markazi_Pro.exe"
dst = r"C:\Users\MuzaffarZed\Desktop\Musiqa_Markazi_Pro.exe"

print("1. Terminating running Musiqa_Markazi_Pro.exe...")
subprocess.run(["taskkill", "/F", "/IM", "Musiqa_Markazi_Pro.exe"], capture_output=True)
time.sleep(1.5)

print(f"2. Copying {src} -> {dst}...")
shutil.copy2(src, dst)
print("Copied successfully! File size:", os.path.getsize(dst))
