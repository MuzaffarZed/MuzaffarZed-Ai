import json
import os
import sys
import subprocess
import numpy as np
from pathlib import Path

# Force UTF-8 on Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

TEMP = Path(r"C:\Users\MuzaffarZed\ai_workspace\pro-video-engine\temp_comedy_v2")
TIMINGS_FILE = TEMP / "timings.json"

def load_audio_ffmpeg(path, sr=16000):
    cmd = [
        "ffmpeg", "-y", "-i", str(path),
        "-f", "s16le", "-acodec", "pcm_s16le",
        "-ar", str(sr), "-ac", "1", "-"
    ]
    raw = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0

def fmt(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h:01d}:{m:02d}:{s:05.2f}"

def main():
    print("📝 Faster-Whisper orqali 6 ta epizodning so'zma-so'z subtitrlari olinmoqda...")
    from faster_whisper import WhisperModel
    model = WhisperModel("base", device="cpu", compute_type="int8")

    with open(TIMINGS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    header = """[Script Info]
Title: Comedy Video Subtitles V2
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Inter Black,54,&H00FFFFFF,&H0000FFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,3.5,1.5,2,40,40,85,1
Style: Boss,Inter Black,54,&H004DF8FF,&H0000FFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,3.5,1.5,2,40,40,85,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []

    for sc in data["scenes"]:
        sc_id = sc["id"]
        sc_offset = sc["start"]
        sc_file = sc["file"]
        is_boss = (sc_id == "scene3")
        style = "Boss" if is_boss else "Default"

        audio_arr = load_audio_ffmpeg(sc_file)
        segments, _ = model.transcribe(audio_arr, word_timestamps=True)

        for seg in segments:
            if hasattr(seg, "words") and seg.words:
                chunk_size = 3
                words = seg.words
                for i in range(0, len(words), chunk_size):
                    chunk = words[i:i + chunk_size]
                    c_start = sc_offset + chunk[0].start
                    c_end = sc_offset + chunk[-1].end
                    c_text = " ".join([w.word.strip() for w in chunk])
                    events.append(f"Dialogue: 0,{fmt(c_start)},{fmt(c_end)},{style},,0,0,0,,{c_text}")
            else:
                c_start = sc_offset + seg.start
                c_end = sc_offset + seg.end
                events.append(f"Dialogue: 0,{fmt(c_start)},{fmt(c_end)},{style},,0,0,0,,{seg.text.strip()}")

    out_ass = TEMP / "subtitles.ass"
    with open(out_ass, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events))
    print(f"✅ Subtitr fayli tayyor ({len(events)} ta ibora): {out_ass}")

if __name__ == "__main__":
    main()
