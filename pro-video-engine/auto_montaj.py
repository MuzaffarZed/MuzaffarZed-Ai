#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auto_montaj.py
0.4s dan uzun pauzalarni avtomatik kesuvchi va ovozga mos so'zma-so'z
Inter Black subtitrini yopishtiruvchi professional avto-montaj tizimi.
Dasturchi: MuzaffarZed
"""

import os
import sys
import re
import json
import subprocess
from pathlib import Path

def extract_audio(video_path, output_audio_path):
    cmd = [
        "ffmpeg", "-y", "-i", str(video_path),
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        str(output_audio_path)
    ]
    subprocess.run(cmd, capture_output=True, check=True)
    return output_audio_path

def detect_silence_intervals(audio_path, noise_threshold_db=-30, min_silence_sec=0.4):
    cmd = [
        "ffmpeg", "-i", str(audio_path),
        "-af", f"silencedetect=noise={noise_threshold_db}dB:d={min_silence_sec}",
        "-f", "null", "-"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    silences = []
    start = None
    for line in res.stderr.splitlines():
        if "silence_start:" in line:
            m = re.search(r"silence_start:\s*([0-9.]+)", line)
            if m:
                start = float(m.group(1))
        elif "silence_end:" in line and start is not None:
            m = re.search(r"silence_end:\s*([0-9.]+)", line)
            if m:
                end = float(m.group(1))
                silences.append((start, end))
                start = None
    return silences

def build_cut_segments(total_duration, silences):
    segments = []
    cur = 0.0
    for s_start, s_end in silences:
        if s_start > cur + 0.1:
            segments.append((cur, s_start))
        cur = max(cur, s_end)
    if cur < total_duration:
        segments.append((cur, total_duration))
    return segments

def get_video_duration(video_path):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def generate_subtitles_whisper(audio_path, output_ass_path):
    """faster-whisper orqali so'zma-so'z Inter Black subtitr yaratish."""
    from faster_whisper import WhisperModel
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, info = model.transcribe(str(audio_path), word_timestamps=True)

    header = """[Script Info]
Title: Auto Montaj Subtitles
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Inter Black,54,&H00FFFFFF,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,1,2,60,60,80,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    def fmt_time(sec):
        h = int(sec // 3600)
        m = int((sec % 3600) // 60)
        s = sec % 60
        return f"{h:01d}:{m:02d}:{s:05.2f}"

    for seg in segments:
        if hasattr(seg, "words") and seg.words:
            for w in seg.words:
                events.append(f"Dialogue: 0,{fmt_time(w.start)},{fmt_time(w.end)},Default,,0,0,0,,{w.word.strip()}")
        else:
            events.append(f"Dialogue: 0,{fmt_time(seg.start)},{fmt_time(seg.end)},Default,,0,0,0,,{seg.text.strip()}")

    with open(output_ass_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events))
    return output_ass_path

def run_auto_montaj(video_path, output_path, cut_pauses=True):
    video_path = Path(video_path).resolve()
    output_path = Path(output_path).resolve()
    temp_dir = output_path.parent / "temp_montaj"
    temp_dir.mkdir(parents=True, exist_ok=True)

    audio_path = temp_dir / "extracted_audio.wav"
    extract_audio(video_path, audio_path)

    total_dur = get_video_duration(video_path)
    cut_video = temp_dir / "cut_video.mp4"

    if cut_pauses:
        silences = detect_silence_intervals(audio_path, min_silence_sec=0.4)
        segments = build_cut_segments(total_dur, silences)
        if segments:
            filter_select = "+".join([f"between(t,{s},{e})" for s, e in segments])
            cmd = [
                "ffmpeg", "-y", "-i", str(video_path),
                "-vf", f"select='{filter_select}',setpts=N/FRAME_RATE/TB",
                "-af", f"aselect='{filter_select}',asetpts=N/SR/TB",
                "-c:v", "libx264", "-c:a", "aac", str(cut_video)
            ]
            subprocess.run(cmd, capture_output=True, check=True)
            cut_audio = temp_dir / "cut_audio.wav"
            extract_audio(cut_video, cut_audio)
            sub_audio = cut_audio
            target_video = cut_video
        else:
            target_video = video_path
            sub_audio = audio_path
    else:
        target_video = video_path
        sub_audio = audio_path

    ass_path = temp_dir / "subs.ass"
    try:
        generate_subtitles_whisper(sub_audio, ass_path)
        has_subs = True
    except Exception as e:
        print("Whisper subtitr xatosi (subtitrsiz davom etiladi):", e)
        has_subs = False

    # Yakuniy video
    if has_subs:
        escaped_ass = str(ass_path).replace("\\", "/").replace(":", "\\:")
        cmd_final = [
            "ffmpeg", "-y", "-i", str(target_video),
            "-vf", f"ass='{escaped_ass}'",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", str(output_path)
        ]
    else:
        cmd_final = [
            "ffmpeg", "-y", "-i", str(target_video),
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", str(output_path)
        ]
    subprocess.run(cmd_final, capture_output=True, check=True)
    print("Auto Montaj muvaffaqiyatli yakunlandi:", output_path)
    return output_path

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_auto_montaj(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "output_montaj.mp4")
    else:
        print("Foydalanish: python auto_montaj.py input.mp4 [output.mp4]")
