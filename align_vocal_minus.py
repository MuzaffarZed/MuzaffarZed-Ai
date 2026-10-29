import soundfile as sf
import numpy as np
import os
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

minus_path = r"C:\Users\MuzaffarZed\Desktop\vakal minus\minus\Mani_Izlab_Ovvora_Bolmang_Minus_Master_24bit.wav"
vocal1_path = r"C:\Users\MuzaffarZed\Desktop\vakal minus\vocall\Untitled project - 2026-Oct-16.wav"
vocal2_path = r"C:\Users\MuzaffarZed\Desktop\vakal minus\vocall\untitled_2026-10-16 16-35-06_Insert 10.wav"

minus_data, minus_sr = sf.read(minus_path)
v1_data, v1_sr = sf.read(vocal1_path)
v2_data, v2_sr = sf.read(vocal2_path)

print(f"Minus: shape={minus_data.shape}, sr={minus_sr}, dur={len(minus_data)/minus_sr:.2f}s")
print(f"Vocal 1 (Untitled): shape={v1_data.shape}, sr={v1_sr}, dur={len(v1_data)/v1_sr:.2f}s")
print(f"Vocal 2 (Insert 10): shape={v2_data.shape}, sr={v2_sr}, dur={len(v2_data)/v2_sr:.2f}s")

# Let's find where voice energy starts in Vocal 1 and Vocal 2
def find_onset(data, sr, thresh_db=-35):
    if data.ndim > 1:
        mono = np.mean(data, axis=1)
    else:
        mono = data
    mono = np.abs(mono)
    thresh = 10**(thresh_db / 20)
    # 50ms window
    win = int(sr * 0.05)
    for i in range(0, len(mono) - win, win):
        if np.max(mono[i:i+win]) > thresh:
            return i / sr
    return 0

print("Vocal 1 first singing onset:", find_onset(v1_data, v1_sr), "seconds")
print("Vocal 2 first singing onset:", find_onset(v2_data, v2_sr), "seconds")
