import sys
import os
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from gradio_client import Client, handle_file

# Paths
source_vocal = Path("singing_studio/data/songs/vocal_20260921_161740.mp3").resolve()
ref_voice = Path("singing_studio/data/voices/cleaned/clean_rec_20260921_161108.wav").resolve()

# First, extract 20 seconds of vocal to test
snippet_vocal = Path("singing_studio/data/temp/test_snippet.wav").resolve()
snippet_vocal.parent.mkdir(parents=True, exist_ok=True)

import subprocess
subprocess.run([
    "ffmpeg", "-y",
    "-ss", "40", "-t", "20",
    "-i", str(source_vocal),
    "-ar", "44100",
    str(snippet_vocal)
], check=True)

print(f"[OK] Snippet extracted: {snippet_vocal}")
print(f"[OK] Reference voice: {ref_voice}")

print("Connecting to Plachta/Seed-VC...")
client = Client("Plachta/Seed-VC")

print("Running Voice Conversion to Janob Muzaffar's voice...")
result = client.predict(
    source_audio=handle_file(str(snippet_vocal)),
    reference_audio=handle_file(str(ref_voice)),
    diffusion_steps=25,
    length_adjust=1.0,
    inference_cfg_rate=0.7,
    use_f0_conditioned_model=True,
    auto_f0_adjust=True,
    pitch_shift=0,
    api_name="/predict_1"
)

print("[OK] Conversion Result:", result)
