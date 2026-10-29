import speech_recognition as sr
import subprocess
import os
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

r = sr.Recognizer()
voc_dir = r"C:\Users\MuzaffarZed\Desktop\vakal minus\vocall"

takes = {
    "Take 1 (Untitled)": os.path.join(voc_dir, "Untitled project - 2026-Oct-16.wav"),
    "Take 2 (Insert 10)": os.path.join(voc_dir, "untitled_2026-10-16 16-35-06_Insert 10.wav"),
}

for name, path in takes.items():
    print(f"\n--- {name} ---")
    # Transcribe in 3 chunks: 0-30s, 30-60s, 60-90s
    for start_s in [0, 25, 55, 80]:
        tmp_wav = os.path.join(r"C:\Users\MuzaffarZed\ai_workspace", f"chunk_{start_s}.wav")
        cmd = ["ffmpeg", "-y", "-i", path, "-ss", str(start_s), "-t", "25", "-ar", "16000", "-ac", "1", tmp_wav]
        subprocess.run(cmd, capture_output=True)
        try:
            with sr.AudioFile(tmp_wav) as src:
                audio = r.record(src)
                text = r.recognize_google(audio, language="uz-UZ")
                print(f"[{start_s}s - {start_s+25}s]: {text}")
        except Exception as e:
            print(f"[{start_s}s - {start_s+25}s]: (no clear speech or {e})")
        finally:
            if os.path.exists(tmp_wav):
                os.remove(tmp_wav)
