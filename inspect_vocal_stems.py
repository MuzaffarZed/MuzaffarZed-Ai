import os
import wave
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

p = r"C:\Users\MuzaffarZed\Desktop\vakal minus"
for root, dirs, files in os.walk(p):
    for f in files:
        if f.endswith('.wav') or f.endswith('.mp3'):
            fp = os.path.join(root, f)
            if f.endswith('.wav'):
                try:
                    with wave.open(fp, 'rb') as w:
                        ch = w.getnchannels()
                        rate = w.getframerate()
                        frames = w.getnframes()
                        dur = frames / rate
                        bits = w.getsampwidth() * 8
                        print(f"WAV: {f} | {dur:.2f}s | {rate}Hz | {bits}-bit | {ch}ch | {os.path.getsize(fp)/1024/1024:.2f}MB")
                except Exception as e:
                    print(f"WAV Error {f}: {e}")
            else:
                print(f"MP3: {f} | {os.path.getsize(fp)/1024/1024:.2f}MB")
