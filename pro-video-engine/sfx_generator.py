"""
Pro-Cinema Engine: SFX Generator & Audio Ducking Studio
Author: MuzaffarZed
Standards:
- Synthesis of cinematic SFX: whoosh, riser, sub-bass impact, ui-click, typing
- Studio-grade Audio Ducking via FFmpeg sidechain compression
"""

import os
import sys
import math
import subprocess
import numpy as np
from scipy.io import wavfile

SAMPLE_RATE = 44100

def _save_wav(filepath: str, data: np.ndarray):
    """Normalize and write audio data to 16-bit PCM WAV."""
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    peak = np.max(np.abs(data))
    if peak > 0:
        data = data / peak * 0.95
    wavfile.write(filepath, SAMPLE_RATE, (data * 32767).astype(np.int16))
    print(f"[SFX] Generated: {filepath} ({len(data)/SAMPLE_RATE:.2f}s)")

def generate_whoosh(output_wav: str, duration: float = 0.75):
    """Cinematic air whoosh transition sound effect."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    # White noise base
    noise = np.random.normal(0, 1.0, len(t))
    # Frequency swept bandpass / envelope: ramp up to center then drop
    env = np.sin(np.pi * (t / duration)) ** 3
    # Sweeping tone underneath
    f_start, f_end = 120.0, 950.0
    freq_sweep = np.linspace(f_start, f_end, len(t))
    sweep_phase = 2 * np.pi * np.cumsum(freq_sweep) / SAMPLE_RATE
    carrier = np.sin(sweep_phase)
    # Combine noise and carrier
    audio = (0.7 * noise + 0.3 * carrier) * env
    # Soft low-pass smoothing
    kernel = np.ones(15) / 15
    audio = np.convolve(audio, kernel, mode='same')
    _save_wav(output_wav, audio)

def generate_riser(output_wav: str, duration: float = 2.5):
    """Rising tension buildup (riser/crescendo) for reveals."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    # Exponential frequency rise from 80Hz to 1800Hz
    freqs = 80.0 * ((1800.0 / 80.0) ** (t / duration))
    phase = 2 * np.pi * np.cumsum(freqs) / SAMPLE_RATE
    # Multiple harmonics + detuned chorus
    tone = (
        0.5 * np.sin(phase) +
        0.3 * np.sin(phase * 1.5 + 0.1) +
        0.2 * np.sin(phase * 2.0)
    )
    # Noise texture building up
    noise = np.random.normal(0, 0.4, len(t))
    # Exponential volume crescendo
    vol_env = (t / duration) ** 2.2
    audio = (tone + noise * vol_env) * vol_env
    _save_wav(output_wav, audio)

def generate_sub_bass_impact(output_wav: str, duration: float = 1.6):
    """Sub-bass cinematic impact boom / trailer drop."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    # Rapid pitch drop from 140Hz down to 32Hz
    freqs = 32.0 + 108.0 * np.exp(-t * 9.0)
    phase = 2 * np.pi * np.cumsum(freqs) / SAMPLE_RATE
    # Body tone + harmonic
    sub = 0.8 * np.sin(phase) + 0.25 * np.sin(phase * 2.0)
    # Punchy transient click at start (first 15ms)
    t_click = int(0.015 * SAMPLE_RATE)
    click = np.zeros(len(t))
    click[:t_click] = np.random.normal(0, 1.0, t_click) * np.linspace(1, 0, t_click)
    # Exponential decay envelope
    env = np.exp(-t * 2.5)
    # Mild saturation / soft clipping for warm analog weight
    raw = (sub * env) + (click * 0.4)
    audio = np.tanh(raw * 1.4)
    _save_wav(output_wav, audio)

def generate_ui_click(output_wav: str, duration: float = 0.08):
    """Crisp high-tech interface click/tap."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    # Dual resonant frequencies 1600Hz and 2800Hz with fast decay
    env = np.exp(-t * 80.0)
    audio = (0.7 * np.sin(2 * np.pi * 1600 * t) + 0.3 * np.sin(2 * np.pi * 2800 * t)) * env
    _save_wav(output_wav, audio)

def generate_typing(output_wav: str, num_clicks: int = 6, duration: float = 1.2):
    """Mechanical keyboard typing sound sequence."""
    total_samples = int(SAMPLE_RATE * duration)
    audio = np.zeros(total_samples)
    np.random.seed(42)
    # Click times distributed across duration
    click_times = np.sort(np.random.uniform(0.05, duration - 0.1, num_clicks))
    for ct in click_times:
        start_idx = int(ct * SAMPLE_RATE)
        click_len = int(0.04 * SAMPLE_RATE)
        t_c = np.linspace(0, 0.04, click_len, endpoint=False)
        pitch = np.random.uniform(1200, 2200)
        c_wave = np.sin(2 * np.pi * pitch * t_c) * np.exp(-t_c * 90.0)
        c_wave += np.random.normal(0, 0.3, click_len) * np.exp(-t_c * 120.0)
        end_idx = min(total_samples, start_idx + click_len)
        audio[start_idx:end_idx] += c_wave[:end_idx - start_idx]
    _save_wav(output_wav, audio)

def generate_all_sfx(output_dir: str):
    """Generate the full suite of cinema sound effects."""
    os.makedirs(output_dir, exist_ok=True)
    generate_whoosh(os.path.join(output_dir, "whoosh.wav"))
    generate_riser(os.path.join(output_dir, "riser.wav"))
    generate_sub_bass_impact(os.path.join(output_dir, "sub_bass_impact.wav"))
    generate_ui_click(os.path.join(output_dir, "ui_click.wav"))
    generate_typing(os.path.join(output_dir, "typing.wav"))
    print(f"[SFX] All 5 studio sound effects generated in: {output_dir}")

def mix_with_audio_ducking(
    voiceover_path: str,
    bgm_path: str,
    output_path: str,
    ducking_threshold: float = 0.06,
    ducking_ratio: float = 8.0,
    attack_ms: int = 120,
    release_ms: int = 600,
    bgm_volume: float = 0.35,
    voice_volume: float = 1.05
):
    """
    Studio-grade Audio Ducking using FFmpeg sidechaincompress:
    Automatically lowers background music volume whenever voiceover is active,
    and smoothly restores BGM during speaker pauses.
    """
    voice_p = os.path.abspath(voiceover_path)
    bgm_p = os.path.abspath(bgm_path)
    out_p = os.path.abspath(output_path)

    if not os.path.exists(voice_p):
        raise FileNotFoundError(f"Voiceover not found: {voice_p}")
    if not os.path.exists(bgm_p):
        raise FileNotFoundError(f"BGM not found: {bgm_p}")

    filter_complex = (
        f"[0:a]volume={voice_volume}[voice];"
        f"[1:a]volume={bgm_volume}[music];"
        f"[music][voice]sidechaincompress="
        f"threshold={ducking_threshold}:"
        f"ratio={ducking_ratio}:"
        f"attack={attack_ms}:"
        f"release={release_ms}[ducked_music];"
        f"[voice][ducked_music]amix=inputs=2:duration=first:dropout_transition=2[outa]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", voice_p,
        "-i", bgm_p,
        "-filter_complex", filter_complex,
        "-map", "[outa]",
        "-c:a", "aac",
        "-b:a", "256k",
        out_p
    ]

    print("[MASTERING] Running studio audio ducking mix...")
    subprocess.run(cmd, check=True)
    print(f"[MASTERING] Audio ducking master successfully created: {out_p}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sfx_dir = os.path.join(base_dir, "sfx")
    generate_all_sfx(sfx_dir)
