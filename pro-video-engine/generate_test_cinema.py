#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_test_cinema.py
Pro-Cinema Master Pipeline: 20 soniyalik 60 FPS 3D Neyron tarmoq videosini
100% avtonom ravishda yaratadi.
Dasturchi: MuzaffarZed
"""

import os
import sys
import json
import wave
import asyncio
import subprocess
import numpy as np
from pathlib import Path

# Windows console UTF-8 handling
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ENGINE_DIR = Path(r"C:\Users\MuzaffarZed\ai_workspace\pro-video-engine")
WORKSPACE = Path(r"C:\Users\MuzaffarZed\ai_workspace")
FINAL_OUTPUT = WORKSPACE / "test_cinema_output.mp4"
TEMP_DIR = ENGINE_DIR / "temp_render"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# 1. Matn va Ovoz (20 soniyalik optimal ssenariy)
SSENARIY = (
    "Sun'iy intellekt qanday ishlaydi? "
    "Neyron tarmoqlarda kiruvchi ma'lumotlar ko'p qatlamli tugunlar orqali tahlil qilinadi. "
    "Har bir sinaps o'z vazniga ega bo'lib, murakkab signallarni qayta ishlaydi "
    "va eng optimal yechimni hosil qiladi!"
)

async def create_voiceover(text, out_mp3):
    import edge_tts
    print(f"🎙️ Edge-TTS ovozi yozilmoqda: {out_mp3.name}...")
    communicate = edge_tts.Communicate(text, "uz-UZ-MadinaNeural", rate="+5%")
    await communicate.save(str(out_mp3))
    print("✅ Voiceover tayyor!")

def load_audio_ffmpeg(path, sr=16000):
    cmd = [
        "ffmpeg", "-y", "-i", str(path),
        "-f", "s16le", "-acodec", "pcm_s16le",
        "-ar", str(sr), "-ac", "1", "-"
    ]
    raw = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0

def transcribe_and_build_ass(audio_path, out_ass):
    print("📝 Faster-Whisper orqali so'zma-so'z taymkodlar olinmoqda...")
    from faster_whisper import WhisperModel
    model = WhisperModel("base", device="cpu", compute_type="int8")
    audio_arr = load_audio_ffmpeg(audio_path)
    segments, info = model.transcribe(audio_arr, word_timestamps=True)

    header = """[Script Info]
Title: Pro-Cinema Subtitles
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Inter Black,52,&H00FFFFFF,&H0000FFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,3.5,1.5,2,40,40,90,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    def fmt(sec):
        h = int(sec // 3600)
        m = int((sec % 3600) // 60)
        s = sec % 60
        return f"{h:01d}:{m:02d}:{s:05.2f}"

    for seg in segments:
        if hasattr(seg, "words") and seg.words:
            # So'zma-so'z dinamik ko'rsatish
            chunk_size = 3
            words = seg.words
            for i in range(0, len(words), chunk_size):
                chunk = words[i:i + chunk_size]
                c_start = chunk[0].start
                c_end = chunk[-1].end
                c_text = " ".join([w.word.strip() for w in chunk])
                events.append(f"Dialogue: 0,{fmt(c_start)},{fmt(c_end)},Default,,0,0,0,,{c_text}")
        else:
            events.append(f"Dialogue: 0,{fmt(seg.start)},{fmt(seg.end)},Default,,0,0,0,,{seg.text.strip()}")

    with open(out_ass, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events))
    print(f"✅ ASS subtitri yaratildi: {len(events)} ta ibora")

def generate_ambient_music(duration=20.0, sample_rate=44100):
    """Kinematik chuqur kosmik ambient fon musiqasi."""
    out_wav = TEMP_DIR / "ambient_music.wav"
    t = np.linspace(0, duration, int(sample_rate * duration))
    # 3 ta garmonik qatlam (A minor / Space pad)
    base = 110.0 # A2
    pad1 = np.sin(2 * np.pi * base * t) * 0.25
    pad2 = np.sin(2 * np.pi * (base * 1.5) * t + 0.5) * 0.18 # Fifth
    pad3 = np.sin(2 * np.pi * (base * 1.2) * t + 1.0) * 0.15 # Minor third
    sub = np.sin(2 * np.pi * (base * 0.5) * t) * 0.35 # Sub 55Hz
    
    # Silliq fade-in va fade-out
    env = np.ones_like(t)
    fade_len = int(sample_rate * 2.0)
    env[:fade_len] = np.linspace(0, 1, fade_len)
    env[-fade_len:] = np.linspace(1, 0, fade_len)

    music = (pad1 + pad2 + pad3 + sub) * env * 0.4
    int_music = (np.clip(music, -1.0, 1.0) * 32767).astype(np.int16)

    with wave.open(str(out_wav), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(int_music.tobytes())
    return out_wav

def master_audio(voice_mp3, ambient_wav, out_master_wav):
    print("🎚️ Audio Ducking va SFX mikslash jarayoni...")
    sfx_dir = ENGINE_DIR / "sfx"
    sub_bass = sfx_dir / "sub_bass_impact.wav"
    whoosh = sfx_dir / "whoosh.wav"
    ui_click = sfx_dir / "ui_click.wav"

    # FFmpeg filtergraph:
    # 0:a = voiceover
    # 1:a = ambient music
    # 2:a = sub-bass (at 0s)
    # 3:a = whoosh (at 6.5s)
    # 4:a = whoosh (at 13.5s)
    # 5:a = click (at 3.5s)
    # 6:a = click (at 10.0s)
    filter_complex = (
        "[1:a][0:a]sidechaincompress=threshold=0.04:ratio=4:attack=50:release=300[ducked_music];"
        "[2:a]adelay=0|0,volume=1.2[sfx_impact];"
        "[3:a]adelay=6500|6500,volume=0.8[sfx_w1];"
        "[4:a]adelay=13500|13500,volume=0.8[sfx_w2];"
        "[5:a]adelay=3500|3500,volume=0.6[sfx_c1];"
        "[6:a]adelay=10000|10000,volume=0.6[sfx_c2];"
        "[ducked_music][sfx_impact][sfx_w1][sfx_w2][sfx_c1][sfx_c2]amix=inputs=6:duration=first:dropout_transition=2[sfx_and_music];"
        "[0:a][sfx_and_music]amix=inputs=2:duration=longest[master_out]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", str(voice_mp3),
        "-i", str(ambient_wav),
        "-i", str(sub_bass),
        "-i", str(whoosh),
        "-i", str(whoosh),
        "-i", str(ui_click),
        "-i", str(ui_click),
        "-filter_complex", filter_complex,
        "-map", "[master_out]",
        "-t", "20.0",
        "-c:a", "pcm_s16le",
        str(out_master_wav)
    ]
    subprocess.run(cmd, capture_output=True, check=True)
    print("✅ Master audio muvaffaqiyatli mikslandi!")

def render_3d_video(out_raw_video):
    print("🚀 Remotion 3D Neural Network sahnasi render qilinmoqda (1200 kadr @ 60 FPS)...")
    cmd = [
        "npx.cmd", "remotion", "render",
        "src/index.ts", "NeuralNetwork1080p",
        str(out_raw_video),
        "--codec=h264",
        "--gl=angle"
    ]
    res = subprocess.run(cmd, cwd=str(ENGINE_DIR), capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        raise RuntimeError(f"Remotion render xatosi: {res.stderr}")
    print("✅ Remotion 3D render muvaffaqiyatli yakunlandi!")

def assemble_final_cinema_mp4(raw_video, master_audio_wav, ass_subtitles, final_mp4):
    print("🎬 Yakuniy Pro-Cinema MP4 videoni yig'ish va subtitrni yopishtirish...")
    escaped_ass = str(ass_subtitles).replace("\\", "/").replace(":", "\\:")
    cmd = [
        "ffmpeg", "-y",
        "-i", str(raw_video),
        "-i", str(master_audio_wav),
        "-vf", f"ass='{escaped_ass}'",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "256k",
        "-t", "20.0",
        str(final_mp4)
    ]
    subprocess.run(cmd, capture_output=True, check=True)
    print("🎉 MUKAMMAL PRO-CINEMA VIDEO TAYYOR:", final_mp4)

def main():
    print("=" * 60)
    print("🎬 PRO-CINEMA ENGINE: 20 SONIYALIK 3D TEST VIDEOSI")
    print("=" * 60)

    voice_mp3 = TEMP_DIR / "voiceover.mp3"
    ass_subs = TEMP_DIR / "subtitles.ass"
    ambient_wav = generate_ambient_music(duration=20.0)
    master_audio_wav = TEMP_DIR / "audio_master.wav"
    raw_video = TEMP_DIR / "neural_raw.mp4"

    # 1. Voiceover
    asyncio.run(create_voiceover(SSENARIY, voice_mp3))

    # 2. Whisper Timestamps
    transcribe_and_build_ass(voice_mp3, ass_subs)

    # 3. Audio Ducking & SFX Mastering
    master_audio(voice_mp3, ambient_wav, master_audio_wav)

    # 4. Remotion 3D 60 FPS Render
    render_3d_video(raw_video)

    # 5. Final Assembly
    assemble_final_cinema_mp4(raw_video, master_audio_wav, ass_subs, FINAL_OUTPUT)

    # 6. Verification
    file_size_mb = os.path.getsize(FINAL_OUTPUT) / (1024 * 1024)
    print(f"📊 Fayl hajmi: {file_size_mb:.2f} MB")
    print(f"📍 Manzil: {FINAL_OUTPUT}")
    print("=" * 60)

if __name__ == "__main__":
    main()
