import speech_recognition as sr
import subprocess
import os

r = sr.Recognizer()
voc_dir = r"C:\Users\MuzaffarZed\Desktop\vakal minus\vocall"

files = [
    "untitled_2026-10-16 16-35-06_Insert 10.wav",
    "Untitled project - 2026-Oct-16.wav"
]

for f in files:
    fp = os.path.join(voc_dir, f)
    # Convert first 30s to 16kHz mono wav for speech recognition
    tmp_wav = os.path.join(r"C:\Users\MuzaffarZed\ai_workspace", f"tmp_{f[:10]}.wav")
    cmd = ["ffmpeg", "-y", "-i", fp, "-ss", "10", "-t", "30", "-ar", "16000", "-ac", "1", tmp_wav]
    subprocess.run(cmd, capture_output=True)
    try:
        with sr.AudioFile(tmp_wav) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language="uz-UZ")
            print(f"Recognized from {f}: '{text}'")
    except Exception as e:
        print(f"Could not recognize from {f}: {e}")
    finally:
        if os.path.exists(tmp_wav):
            os.remove(tmp_wav)
