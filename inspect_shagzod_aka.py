import soundfile as sf
import numpy as np
import subprocess
import json
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

p = r"C:\Users\MuzaffarZed\Desktop\shag'zod aka.mp3"
print(f"Inspecting: {p}")

cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", "-show_format", p]
res = subprocess.run(cmd, capture_output=True, text=True)
info = json.loads(res.stdout)
fmt = info.get("format", {})
print("Tags:", fmt.get("tags", {}))
print("Bitrate:", int(fmt.get("bit_rate", 0)) // 1000, "kbps")
print("Duration:", float(fmt.get("duration", 0)), "seconds")

data, sr = sf.read(p)
print(f"Data shape: {data.shape}, Sample rate: {sr}")
peak = np.max(np.abs(data))
rms = np.sqrt(np.mean(data**2))
print(f"Peak: {peak:.3f} ({20*np.log10(peak):.2f} dBFS)")
print(f"RMS: {rms:.4f} ({20*np.log10(rms):.2f} dBFS)")
