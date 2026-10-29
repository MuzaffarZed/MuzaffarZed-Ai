import subprocess
import os
import json
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

voc_dir = r"C:\Users\MuzaffarZed\Desktop\vakal minus\vocall"
for f in os.listdir(voc_dir):
    fp = os.path.join(voc_dir, f)
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_streams", "-show_format", fp
    ]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode == 0:
        info = json.loads(p.stdout)
        fmt = info.get("format", {})
        streams = info.get("streams", [{}])
        dur = float(fmt.get("duration", 0))
        rate = streams[0].get("sample_rate", "N/A")
        ch = streams[0].get("channels", "N/A")
        codec = streams[0].get("codec_name", "N/A")
        print(f"File: {f}")
        print(f"  Duration: {dur:.2f}s | Rate: {rate}Hz | Ch: {ch} | Codec: {codec} | Size: {os.path.getsize(fp)/1024/1024:.2f} MB")
