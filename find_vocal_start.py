import subprocess
import speech_recognition as sr
import os
import tempfile
import sys

sys.stdout.reconfigure(encoding='utf-8')
r = sr.Recognizer()

vocal_dir = r"C:\Users\MuzaffarZed\Desktop\vakal minus\vocall"

candidates = [
    "untitled_2026-10-16 16-35-06_Insert 10.wav",
    "Untitled project - 2026-Oct-16.wav",
    "Untitled project - 2026-Oct-16_2.wav"
]

for f in candidates:
    p = os.path.join(vocal_dir, f)
    print(f"Checking {f}...")
    found = False
    for t_int in range(0, 350, 10):
        t = t_int / 10.0
        tmp = tempfile.mktemp(suffix=".wav")
        subprocess.run(["ffmpeg", "-y", "-ss", str(t), "-t", "3.0", "-i", p, "-ar", "16000", "-ac", "1", tmp], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        txt = ""
        try:
            with sr.AudioFile(tmp) as source:
                audio = r.record(source)
                txt = r.recognize_google(audio, language="uz-UZ")
        except Exception:
            pass
        if os.path.exists(tmp):
            os.remove(tmp)
        if txt and any(k in txt.lower() for k in ["meni", "mani", "izlab", "ovora", "ovvora"]):
            print(f"   FOUND START at [{t:.1f}s]: \"{txt}\"")
            found = True
            break
    if not found:
        print("   Not found in first 35 seconds")
