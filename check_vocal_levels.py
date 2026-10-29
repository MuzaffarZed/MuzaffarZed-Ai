import subprocess
import os
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

voc_dir = r"C:\Users\MuzaffarZed\Desktop\vakal minus\vocall"
for f in os.listdir(voc_dir):
    if f.endswith('.wav'):
        fp = os.path.join(voc_dir, f)
        # Run ffmpeg volumedetect
        cmd = ["ffmpeg", "-i", fp, "-af", "volumedetect", "-f", "null", "-"]
        p = subprocess.run(cmd, capture_output=True, text=True)
        lines = [line for line in p.stderr.split('\n') if 'mean_volume' in line or 'max_volume' in line]
        print(f"File: {f}")
        for l in lines:
            print(" ", l.strip())
