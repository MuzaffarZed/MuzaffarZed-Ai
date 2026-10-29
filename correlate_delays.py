import subprocess
import numpy as np
import isolate_vocal

sr = 44100
# Isolated vocal from original_reference is in isolate_vocal.res (starting at orig t=20.0s, kara t=19.2285s)
# Let's extract mono vocal from 23.0s to 33.0s in original reference (which is 22.23s to 32.23s in karaoke)
orig_voc_mono = np.mean(isolate_vocal.res, axis=1)

# In isolate_vocal, t=0 corresponds to t_orig = 20.0s, so t_kara = 19.2285s
# We want the window in karaoke from 23.5s to 33.5s:
s_idx = int((23.5 - 19.2285) * sr)
e_idx = int((33.5 - 19.2285) * sr)
orig_segment = orig_voc_mono[s_idx:e_idx]

# Now for each delay in test_mixes, load the vocal track placed at that delay
vocal_path = r"C:\Users\MuzaffarZed\Desktop\vakal minus\vocall\untitled_2026-10-16 16-35-06_Insert 10.wav"

delays = [10200, 10400, 10600, 10750, 10900, 11100]
print("Correlating test delays with original vocal:")

# Search finest offset
for d_ms in range(10200, 11200, 100):
    d_sec = d_ms / 1000.0
    # In karaoke timeline, window is 23.5s to 33.5s
    # In Insert 10 timeline, that corresponds to (23.5 - d_sec) to (33.5 - d_sec)
    ins_start = 23.5 - d_sec
    cmd = ['ffmpeg', '-y', '-ss', str(ins_start), '-t', '10.0', '-i', vocal_path, '-ar', str(sr), '-ac', '1', '-f', 'f32le', '-']
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ins_segment = np.frombuffer(p.stdout, dtype=np.float32)
    
    min_l = min(len(orig_segment), len(ins_segment))
    c = np.corrcoef(np.abs(orig_segment[:min_l]), np.abs(ins_segment[:min_l]))[0, 1]
    # Energy correlation (rhythmic envelope alignment)
    print(f"Delay {d_ms}ms: Envelope Correlation = {c:.4f}")
