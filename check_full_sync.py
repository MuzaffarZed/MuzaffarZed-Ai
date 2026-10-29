import subprocess
import numpy as np

# Load minus drums
# Measure drum beats across the song at:
# Verse 1: 24s - 45s
# Chorus: 45s - 75s
# Outro of verse: 75s - 105s

sr = 22050
def load(path, s, d):
    cmd = ['ffmpeg', '-y', '-ss', str(s), '-t', str(d), '-i', path, '-ar', str(sr), '-ac', '1', '-f', 'f32le', '-']
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return np.frombuffer(p.stdout, dtype=np.float32)

kara = load(r"C:\Users\MuzaffarZed\Desktop\vakal minus\minus\Mani izlab ovvora boʻlmang karaoke.mp3", 20.0, 90.0)
vocal = load(r"C:\Users\MuzaffarZed\Desktop\vakal minus\vocall\untitled_2026-10-16 16-35-06_Insert 10.wav", 0.0, 103.0)

delay_sec = 10.80
print(f"Karaoke length: {len(kara)/sr:.1f}s, Vocal length: {len(vocal)/sr:.1f}s, Delay: {delay_sec}s")
