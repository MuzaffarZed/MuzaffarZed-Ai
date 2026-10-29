import subprocess
import numpy as np

sr = 44100
path = r"C:\Users\MuzaffarZed\Desktop\vakal minus\vocall\untitled_2026-10-16 16-35-06_Insert 10.wav"

cmd = ['ffmpeg', '-ss', '12.0', '-t', '4.0', '-i', path, '-ar', str(sr), '-ac', '1', '-f', 'f32le', '-']
p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
audio = np.frombuffer(p.stdout, dtype=np.float32)

hop = int(0.05 * sr)
for i in range(0, len(audio)-hop, hop):
    t = 12.0 + i / sr
    e = np.sqrt(np.mean(audio[i:i+hop]**2))
    print(f"t={t:.2f}s: Insert 10 RMS = {e:.4f}")
