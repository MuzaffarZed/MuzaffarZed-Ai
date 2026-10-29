import json
import os
import sys
import wave
import subprocess
import numpy as np
from pathlib import Path

# Force UTF-8 on Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ENGINE_DIR = Path(r"C:\Users\MuzaffarZed\ai_workspace\pro-video-engine")
TEMP = ENGINE_DIR / "temp_comedy_v2"
SFX_DIR = ENGINE_DIR / "sfx"

TIMINGS_FILE = TEMP / "timings.json"
MASTER_WAV = TEMP / "master_audio.wav"

def load_audio_ffmpeg(path, sr=44100):
    cmd = [
        "ffmpeg", "-y", "-i", str(path),
        "-f", "s16le", "-acodec", "pcm_s16le",
        "-ar", str(sr), "-ac", "1", "-"
    ]
    raw = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0

def main():
    print("🎚️ Master audioni 88.6 soniyaga 100% aniqlik bilan sintezlash...")
    with open(TIMINGS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    sr = 44100
    total_duration = data["total_duration"]
    total_samples = int(total_duration * sr)
    print(f"Total duration: {total_duration:.2f}s ({total_samples} samples)")

    # 1. Speech track
    speech_track = np.zeros(total_samples, dtype=np.float32)
    speech_mask = np.zeros(total_samples, dtype=np.float32)

    for sc in data["scenes"]:
        sc_file = sc["file"]
        sc_start = sc["start"]
        samples = load_audio_ffmpeg(sc_file, sr=sr)
        start_idx = int(sc_start * sr)
        end_idx = min(total_samples, start_idx + len(samples))
        actual_len = end_idx - start_idx
        speech_track[start_idx:end_idx] += samples[:actual_len]
        # Envelope for ducking
        env = np.abs(samples[:actual_len])
        speech_mask[start_idx:end_idx] = np.maximum(speech_mask[start_idx:end_idx], env)

    # Smooth the speech mask for ducking (attack 50ms, release 300ms)
    smooth_mask = np.zeros_like(speech_mask)
    current_val = 0.0
    attack_coeff = 1.0 / (0.05 * sr)
    release_coeff = 1.0 / (0.35 * sr)
    for i in range(total_samples):
        target = min(1.0, speech_mask[i] * 3.5)
        if target > current_val:
            current_val = min(1.0, current_val + attack_coeff)
        else:
            current_val = max(0.0, current_val - release_coeff)
        smooth_mask[i] = current_val

    # 2. BGM track
    bgm_file = TEMP / "bgm.wav"
    bgm_samples = load_audio_ffmpeg(bgm_file, sr=sr)
    bgm_track = np.zeros(total_samples, dtype=np.float32)
    bgm_len = min(total_samples, len(bgm_samples))
    bgm_track[:bgm_len] = bgm_samples[:bgm_len]

    # Apply ducking: when speech is loud, reduce BGM to 20% (-14dB), else 100%
    duck_gain = 1.0 - (smooth_mask * 0.78)
    ducked_bgm = bgm_track * duck_gain

    # 3. SFX track
    sfx_track = np.zeros(total_samples, dtype=np.float32)

    def add_sfx(sfx_path, at_sec, vol=1.0):
        if not os.path.exists(sfx_path):
            return
        s = load_audio_ffmpeg(sfx_path, sr=sr) * vol
        s_idx = int(at_sec * sr)
        e_idx = min(total_samples, s_idx + len(s))
        sfx_track[s_idx:e_idx] += s[:e_idx - s_idx]

    sfx_subbass = SFX_DIR / "sub_bass_impact.wav"
    sfx_whoosh = SFX_DIR / "whoosh.wav"
    sfx_click = SFX_DIR / "ui_click.wav"
    sfx_typing = SFX_DIR / "typing.wav"
    sfx_riser = SFX_DIR / "riser.wav"

    # Add SFX at each scene transition
    add_sfx(sfx_subbass, 0.0, 1.2)
    add_sfx(sfx_typing, 1.0, 0.8)

    # Scene 2 (disaster at 17.02s)
    s2 = data["scenes"][1]["start"]
    add_sfx(sfx_riser, max(0, s2 - 1.2), 0.7)
    add_sfx(sfx_subbass, s2, 1.3)

    # Scene 3 (phone ring at 29.47s)
    s3 = data["scenes"][2]["start"]
    add_sfx(sfx_whoosh, s3, 0.9)
    add_sfx(sfx_click, s3 + 0.4, 1.3)
    add_sfx(sfx_click, s3 + 0.8, 1.3)

    # Scene 4 (Stackoverflow at 45.53s)
    s4 = data["scenes"][3]["start"]
    add_sfx(sfx_whoosh, s4, 0.9)
    add_sfx(sfx_typing, s4 + 0.6, 0.9)

    # Scene 5 (Rocket launch / force push at 61.87s)
    s5 = data["scenes"][4]["start"]
    add_sfx(sfx_riser, max(0, s5 - 1.2), 0.8)
    add_sfx(sfx_subbass, s5, 1.3)

    # Scene 6 (Victory at 74.30s)
    s6 = data["scenes"][5]["start"]
    add_sfx(sfx_whoosh, s6, 1.0)
    add_sfx(sfx_subbass, s6 + 0.8, 1.2)

    # 4. Final Master Mix: Speech (1.0) + Ducked BGM (0.6) + SFX (0.75)
    final_mix = speech_track * 1.05 + ducked_bgm * 0.6 + sfx_track * 0.75

    # Outro fade
    fade_len = int(1.5 * sr)
    final_mix[-fade_len:] *= np.linspace(1, 0, fade_len)

    # Limiter / normalize
    max_peak = np.max(np.abs(final_mix))
    if max_peak > 0.98:
        final_mix = final_mix / max_peak * 0.96

    int_mix = (final_mix * 32767).astype(np.int16)

    with wave.open(str(MASTER_WAV), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(int_mix.tobytes())

    print(f"✅ Mukammal Master Audio tayyor ({total_duration:.2f}s): {MASTER_WAV}")

if __name__ == "__main__":
    main()
