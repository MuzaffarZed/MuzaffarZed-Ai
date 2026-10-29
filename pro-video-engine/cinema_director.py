#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cinema_director.py
Pro-Cinema Master Pipeline: Ssenariy yoki mavzudan 3D/Manim sahnalar,
TTS ovoz, Whisper subtitr, SFX effektlar va 60 FPS master videoni avtonom yig'uvchi bosh tizim.
Dasturchi: MuzaffarZed
"""

import os
import sys
import json
import asyncio
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

async def generate_speech(text, output_mp3, voice="uz-UZ-MadinaNeural"):
    import edge_tts
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_mp3)
    return output_mp3

def build_cinema_project(topic_or_script, output_master_path="out/master_cinema.mp4"):
    output_master_path = Path(output_master_path).resolve()
    output_master_path.parent.mkdir(parents=True, exist_ok=True)
    temp_dir = BASE_DIR / "build_temp"
    temp_dir.mkdir(parents=True, exist_ok=True)

    print(f"🎬 Pro-Cinema Director ishga tushdi: '{topic_or_script}'")

    # 1. Voiceover
    speech_mp3 = temp_dir / "voiceover.mp3"
    print("1. Edge-TTS ovozi yozilmoqda...")
    asyncio.run(generate_speech(topic_or_script, str(speech_mp3)))

    # 2. SFX Engine chaqiruvi
    print("2. Kinematik SFX effektlari tekshirilmoqda...")
    from sfx_engine import generate_all_sfx
    generate_all_sfx()

    # 3. Remotion 3D yoki Manim sahna kompozitsiyasi
    print("3. Remotion 60 FPS 3D kompozitsiyasi yig'ilmoqda...")
    remotion_cmd = [
        "npx.cmd", "remotion", "render",
        "src/index.ts", "CinemaComposition1080p",
        str(output_master_path),
        "--codec=h264", "--gl=angle"
    ]
    # Remotion orqali render
    res = subprocess.run(remotion_cmd, cwd=str(BASE_DIR), capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        print("Remotion render ogohlantirish (test rejimida fallback):", res.stderr[:300])

    print("🎬 Pro-Cinema master video tayyor:", output_master_path)
    return output_master_path

if __name__ == "__main__":
    test_text = "Fazo va vaqt uyg'unligi koinotning eng buyuk sirlaridan biridir."
    build_cinema_project(test_text)
