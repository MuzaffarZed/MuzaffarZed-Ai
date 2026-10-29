import subprocess
import numpy as np

sr = 44100
dur = 15.0

def load(path, start, d):
    cmd = ['ffmpeg', '-y', '-ss', str(start), '-t', str(d), '-i', path, '-ar', str(sr), '-ac', '2', '-f', 'f32le', '-']
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return np.frombuffer(p.stdout, dtype=np.float32).reshape(-1, 2)

orig = load(r"C:\Users\MuzaffarZed\Desktop\vakal minus\original_reference.mp3", 20.0, dur)
kara = load(r"C:\Users\MuzaffarZed\Desktop\vakal minus\minus\Mani izlab ovvora boʻlmang karaoke.mp3", 20.0 - 0.7715, dur)

# Align lengths
min_len = min(len(orig), len(kara))
orig = orig[:min_len]
kara = kara[:min_len]

# Find exact scale factor per channel
scale_L = np.dot(orig[:, 0], kara[:, 0]) / (np.dot(kara[:, 0], kara[:, 0]) + 1e-9)
scale_R = np.dot(orig[:, 1], kara[:, 1]) / (np.dot(kara[:, 1], kara[:, 1]) + 1e-9)

res = np.zeros_like(orig)
res[:, 0] = orig[:, 0] - scale_L * kara[:, 0]
res[:, 1] = orig[:, 1] - scale_R * kara[:, 1]

# Check RMS of residual in 0.1s steps from t=20.0 to 30.0
hop = int(0.1 * sr)
for i in range(0, len(res)-hop, hop):
    t_orig = 20.0 + i / sr
    t_kara = t_orig - 0.7715
    e = np.sqrt(np.mean(res[i:i+hop]**2))
    print(f"t_orig={t_orig:.2f}s (t_kara={t_kara:.2f}s): Vocal Residual RMS = {e:.4f}")
