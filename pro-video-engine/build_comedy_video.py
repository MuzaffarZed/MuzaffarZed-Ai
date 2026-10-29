#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_comedy_video.py
Janob Muzaffar uchun ajoyib kulguli IT rolik:
"Dasturchining oddiy bir kuni: Bitta kichik o'zgarish!"
Dasturchi: MuzaffarZed
"""

import os
import sys
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
FINAL_OUTPUT = WORKSPACE / "kulguli_dasturchi_video.mp4"
TEMP_DIR = ENGINE_DIR / "temp_comedy"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

SSENARIY = (
    "Kechki soat sakkiz. Dasturchi: 'Bo'ldi, bitta kichik o'zgarish kiritaman-u uxlayman' dedi. "
    "Soat tungi to'rt. Kompyuter ventilyatori samolyotdek uvillab, koinotga uchishga tayyorlanyapti! "
    "To'rt soat qidirilgan buyuk xato: qayerdadir bitta ortiqcha nuqta ekan! "
    "O'chirgandi... yana o'n ikkita yangi xato chiqdi! Mana bu haqiqiy dasturlash!"
)

async def create_voiceover(text, out_mp3):
    import edge_tts
    print(f"🎙️ Sardor ovozida kulguli ssenariy yozilmoqda: {out_mp3.name}...")
    communicate = edge_tts.Communicate(text, "uz-UZ-SardorNeural", rate="+10%", pitch="+2Hz")
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
Title: Comedy Subtitles
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Inter Black,56,&H00FFFFFF,&H0000FFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,3.5,1.5,2,40,40,90,1

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
    print(f"✅ Inter Black so'zma-so'z subtitri tayyorlandi ({len(events)} ta ibora)")

def generate_upbeat_comedy_music(duration=18.0, sample_rate=44100):
    """Qiziqarli va dinamik sintezatorli ritmik komediya foni."""
    out_wav = TEMP_DIR / "comedy_bgm.wav"
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # 128 BPM ritmik bassline + staccato akkordlar
    tempo = 128
    beat_dur = 60.0 / tempo
    beats = int(duration / beat_dur)

    music = np.zeros_like(t)

    # Ritmik zarbalar va melodik arpejio
    for b in range(beats):
        b_start = b * beat_dur
        idx_start = int(b_start * sample_rate)
        idx_end = int(min(duration, b_start + 0.35) * sample_rate)
        sub_t = t[idx_start:idx_end] - b_start
        
        # Bass akkordlar (C - G - Am - F progression)
        chord_root = [130.81, 196.00, 220.00, 174.61][(b // 4) % 4]
        bass = np.sin(2 * np.pi * chord_root * sub_t) * np.exp(-sub_t * 6.0)
        synth = np.sin(2 * np.pi * (chord_root * 2) * sub_t) * 0.3 * np.exp(-sub_t * 8.0)
        
        music[idx_start:idx_end] += (bass * 0.5 + synth)

    # Shovqinli hi-hat
    for b in range(beats * 2):
        b_start = b * (beat_dur / 2)
        idx_start = int(b_start * sample_rate)
        idx_end = int(min(duration, b_start + 0.05) * sample_rate)
        sub_t = t[idx_start:idx_end] - b_start
        hat = np.random.uniform(-0.15, 0.15, len(sub_t)) * np.exp(-sub_t * 40.0)
        music[idx_start:idx_end] += hat

    # Silliq master fade-out
    fade_len = int(sample_rate * 1.5)
    music[-fade_len:] *= np.linspace(1, 0, fade_len)

    final_music = np.clip(music * 0.45, -1.0, 1.0)
    int_music = (final_music * 32767).astype(np.int16)

    with wave.open(str(out_wav), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(int_music.tobytes())
    return out_wav

def master_comedy_audio(voice_mp3, bgm_wav, out_master_wav):
    print("🎚️ Komediya ovozi va SFX effektlarini mikslash (Audio Ducking)...")
    sfx_dir = ENGINE_DIR / "sfx"
    sub_bass = sfx_dir / "sub_bass_impact.wav"
    whoosh = sfx_dir / "whoosh.wav"
    typing = sfx_dir / "typing.wav"
    riser = sfx_dir / "riser.wav"
    ui_click = sfx_dir / "ui_click.wav"

    # FFmpeg sidechaincompress Audio Ducking:
    # 0:a = Voiceover
    # 1:a = Background Music
    # 2:a = Sub-bass at 0s
    # 3:a = Typing at 0.8s
    # 4:a = Whoosh at 4.3s
    # 5:a = Riser at 6.0s
    # 6:a = Whoosh at 9.0s
    # 7:a = Click at 11.0s
    # 8:a = Sub-bass at 13.5s
    filter_complex = (
        "[1:a][0:a]sidechaincompress=threshold=0.04:ratio=4:attack=50:release=300[ducked_music];"
        "[2:a]adelay=0|0,volume=1.1[sfx_sb1];"
        "[3:a]adelay=800|800,volume=0.9[sfx_type];"
        "[4:a]adelay=4300|4300,volume=0.8[sfx_w1];"
        "[5:a]adelay=6000|6000,volume=0.6[sfx_rise];"
        "[6:a]adelay=9000|9000,volume=0.8[sfx_w2];"
        "[7:a]adelay=11000|11000,volume=0.7[sfx_clk];"
        "[8:a]adelay=13500|13500,volume=1.2[sfx_sb2];"
        "[ducked_music][sfx_sb1][sfx_type][sfx_w1][sfx_rise][sfx_w2][sfx_clk][sfx_sb2]amix=inputs=8:duration=first:dropout_transition=2[sfx_and_music];"
        "[0:a][sfx_and_music]amix=inputs=2:duration=longest[master_out]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", str(voice_mp3),
        "-i", str(bgm_wav),
        "-i", str(sub_bass),
        "-i", str(typing),
        "-i", str(whoosh),
        "-i", str(riser),
        "-i", str(whoosh),
        "-i", str(ui_click),
        "-i", str(sub_bass),
        "-filter_complex", filter_complex,
        "-map", "[master_out]",
        "-t", "18.0",
        "-c:a", "pcm_s16le",
        str(out_master_wav)
    ]
    subprocess.run(cmd, capture_output=True, check=True)
    print("✅ Komediya master audio tayyor!")

def render_remotion_comedy(out_raw_video):
    print("🚀 Remotion 60 FPS Komediya sahnasi render qilinmoqda (1080 kadr)...")
    cmd = [
        "npx.cmd", "remotion", "render",
        "src/index.ts", "ComedyVideo1080p",
        str(out_raw_video),
        "--codec=h264",
        "--concurrency=4"
    ]
    res = subprocess.run(cmd, cwd=str(ENGINE_DIR), capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        raise RuntimeError(f"Remotion render xatosi: {res.stderr}")
    print("✅ Remotion 60 FPS render muvaffaqiyatli yakunlandi!")

def assemble_final_comedy_video(raw_video, master_audio, ass_subs, final_mp4):
    print("🎬 Subtitrlarni yopishtirish va yakuniy MP4 video yig'ish...")
    escaped_ass = str(ass_subs).replace("\\", "/").replace(":", "\\:")
    cmd = [
        "ffmpeg", "-y",
        "-i", str(raw_video),
        "-i", str(master_audio),
        "-vf", f"ass='{escaped_ass}'",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "256k",
        "-t", "18.0",
        str(final_mp4)
    ]
    subprocess.run(cmd, capture_output=True, check=True)
    print("🎉 KULGULI VIDEO 100% TAYYOR:", final_mp4)

def main():
    print("=" * 60)
    print("🎬 DASTURCHINING ODDIY KUNI: KULGULI VIDEO ISHLAB CHIQARISH")
    print("=" * 60)

    voice_mp3 = TEMP_DIR / "comedy_voice.mp3"
    ass_subs = TEMP_DIR / "comedy_subs.ass"
    bgm_wav = generate_upbeat_comedy_music(duration=18.0)
    master_audio_wav = TEMP_DIR / "comedy_audio_master.wav"
    raw_video = TEMP_DIR / "comedy_raw.mp4"

    # 1. Voiceover
    asyncio.run(create_voiceover(SSENARIY, voice_mp3))

    # 2. Whisper Timestamps & Subtitles
    transcribe_and_build_ass(voice_mp3, ass_subs)

    # 3. SFX & Ducking Mastering
    master_comedy_audio(voice_mp3, bgm_wav, master_audio_wav)

    # 4. Remotion 60 FPS Render
    render_remotion_comedy(raw_video)

    # 5. Final Assembly
    assemble_final_comedy_video(raw_video, master_audio_wav, ass_subs, FINAL_OUTPUT)

    size_mb = os.path.getsize(FINAL_OUTPUT) / (1024 * 1024)
    print(f"📊 Yakuniy Fayl Hajmi: {size_mb:.2f} MB")
    print(f"📍 Manzil: {FINAL_OUTPUT}")
    print("=" * 60)

if __name__ == "__main__":
    main()
