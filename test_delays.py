import subprocess
import os

minus = r"C:\Users\MuzaffarZed\Desktop\vakal minus\minus\Mani izlab ovvora boʻlmang karaoke.mp3"
vocal = r"C:\Users\MuzaffarZed\Desktop\vakal minus\vocall\untitled_2026-10-16 16-35-06_Insert 10.wav"
out_dir = r"C:\Users\MuzaffarZed\ai_workspace\test_mixes"
os.makedirs(out_dir, exist_ok=True)

# Test delays: 10400ms, 10600ms, 10750ms, 10900ms
delays = [10400, 10600, 10750, 10900]

for d in delays:
    out_file = os.path.join(out_dir, f"test_delay_{d}ms.mp3")
    fc = (
        f"[1:a]adelay={d}|{d},volume=1.5[v];"
        f"[0:a][v]amix=inputs=2:weights=1.0 1.2:dropout_transition=0"
    )
    cmd = [
        "ffmpeg", "-y",
        "-ss", "20",
        "-t", "25",
        "-i", minus,
        "-i", vocal,
        "-filter_complex", fc,
        "-b:a", "192k",
        out_file
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Rendered test snippet for {d}ms: {out_file}")
