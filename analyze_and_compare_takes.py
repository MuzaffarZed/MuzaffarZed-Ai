import soundfile as sf
import numpy as np
import scipy.signal as signal
import os
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

voc_dir = r"C:\Users\MuzaffarZed\Desktop\vakal minus\vocall"
minus_path = r"C:\Users\MuzaffarZed\Desktop\vakal minus\minus\Mani izlab ovvora boʻlmang karaoke.mp3"

t1_path = os.path.join(voc_dir, "Untitled project - 2026-Oct-16.wav")
t2_path = os.path.join(voc_dir, "untitled_2026-10-16 16-35-06_Insert 10.wav")

d1, sr1 = sf.read(t1_path)
d2, sr2 = sf.read(t2_path)

print(f"Take 1: shape={d1.shape}, sr={sr1}, duration={len(d1)/sr1:.2f}s, peak={np.max(np.abs(d1)):.3f}")
print(f"Take 2: shape={d2.shape}, sr={sr2}, duration={len(d2)/sr2:.2f}s, peak={np.max(np.abs(d2)):.3f}")

# Check correlation between Take 1 and Take 2
# Convert to mono
m1 = np.mean(d1, axis=1) if d1.ndim > 1 else d1
m2 = np.mean(d2, axis=1) if d2.ndim > 1 else d2

# Downsample to 8000Hz for fast cross-correlation
target_sr = 8000
step1 = sr1 // target_sr
m1_sub = m1[::step1]
m2_sub = m2[::step1]

corr = signal.correlate(m1_sub, m2_sub, mode='full')
lags = signal.correlation_lags(len(m1_sub), len(m2_sub), mode='full')
best_lag = lags[np.argmax(corr)]
best_offset_sec = best_lag / target_sr

print(f"Cross-correlation offset between Take 1 and Take 2: {best_offset_sec:.3f}s")
print(f"Correlation peak ratio: {np.max(corr) / (np.linalg.norm(m1_sub) * np.linalg.norm(m2_sub)):.3f}")
