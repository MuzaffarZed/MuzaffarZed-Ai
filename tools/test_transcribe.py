import subprocess
import numpy as np
import json
from faster_whisper import WhisperModel

def main():
    audio_path = r"C:\Users\MuzaffarZed\ai_workspace\tools\voiceover.mp3"
    cmd = ['ffmpeg', '-v', 'error', '-i', audio_path, '-f', 'f32le', '-ar', '16000', '-ac', '1', '-']
    raw_audio = subprocess.check_output(cmd)
    audio_data = np.frombuffer(raw_audio, dtype=np.float32)

    model = WhisperModel('base', device='cpu', compute_type='int8')
    segments, info = model.transcribe(audio_data, word_timestamps=True, language="uz")
    words = []
    for s in segments:
        if s.words:
            for w in s.words:
                words.append({'word': w.word.strip(), 'start': round(w.start, 2), 'end': round(w.end, 2)})
    print(f"Success! Transcribed {len(words)} words:")
    with open(r"C:\Users\MuzaffarZed\ai_workspace\tools\words.json", "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=2)
    print("Saved words to words.json")

if __name__ == "__main__":
    main()
