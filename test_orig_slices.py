import subprocess
import speech_recognition as sr
import os
import tempfile
import sys

sys.stdout.reconfigure(encoding='utf-8')
r = sr.Recognizer()
path = r"C:\Users\MuzaffarZed\Desktop\vakal minus\original_reference.mp3"

for s in [24.0, 24.3, 24.5, 24.7, 24.9, 25.1, 25.3]:
    tmp = tempfile.mktemp(suffix=".wav")
    subprocess.run(["ffmpeg", "-y", "-ss", str(s), "-t", "2.0", "-i", path, "-ar", "16000", "-ac", "1", tmp], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    txt = ""
    try:
        with sr.AudioFile(tmp) as sf:
            txt = r.recognize_google(r.record(sf), language="uz-UZ")
    except Exception:
        pass
    if os.path.exists(tmp):
        os.remove(tmp)
    print(f"Original at {s:.1f}s: \"{txt}\"")
