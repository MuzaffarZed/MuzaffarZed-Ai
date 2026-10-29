import soundfile as sf
import numpy as np
import scipy.signal as signal
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

minus_path = r"C:\Users\MuzaffarZed\Desktop\vakal minus\minus\Mani_Izlab_Ovvora_Bolmang_Minus_Master_24bit.wav"
vocal_path = r"C:\Users\MuzaffarZed\Desktop\vakal minus\vocall\untitled_2026-10-16 16-35-06_Insert 10.wav"

data, sr = sf.read(minus_path)
if data.ndim > 1:
    data = np.mean(data, axis=1)

# Analyze chroma/key profile
# Chromagram via FFT filterbank
note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Standard frequencies for notes across octaves 2 to 6
chroma_energy = np.zeros(12)

# FFT over multiple windows
hop = int(sr * 0.5)
win = int(sr * 1.0)
for i in range(int(sr * 10), min(len(data) - win, int(sr * 80)), hop):
    chunk = data[i:i+win] * np.hanning(win)
    fft_mag = np.abs(np.fft.rfft(chunk))
    freqs = np.fft.rfftfreq(win, 1.0 / sr)
    for midi in range(36, 84): # C2 to B5
        f0 = 440.0 * (2.0 ** ((midi - 69) / 12.0))
        idx = np.argmin(np.abs(freqs - f0))
        note = midi % 12
        chroma_energy[note] += fft_mag[idx]

best_note_idx = np.argmax(chroma_energy)
sorted_notes = np.argsort(chroma_energy)[::-1]

print("Detected Key Profile in Minus:")
for idx in sorted_notes[:5]:
    print(f"  Note: {note_names[idx]} (energy: {chroma_energy[idx]:.1f})")

# Major and Minor profile correlation
major_profile = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
minor_profile = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])

best_corr = -1
detected_key = ""
for root in range(12):
    c_rolled = np.roll(chroma_energy, -root)
    corr_maj = np.corrcoef(c_rolled, major_profile)[0, 1]
    corr_min = np.corrcoef(c_rolled, minor_profile)[0, 1]
    if corr_maj > best_corr:
        best_corr = corr_maj
        detected_key = f"{note_names[root]} Major"
    if corr_min > best_corr:
        best_corr = corr_min
        detected_key = f"{note_names[root]} Minor"

print(f"\nEstimated Musical Key: {detected_key} (confidence: {best_corr:.2f})")
