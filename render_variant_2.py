import os
import sys
import soundfile as sf
import numpy as np
import scipy.signal as signal
from pedalboard import (
    Pedalboard,
    Chorus,
    Compressor,
    Delay,
    Distortion,
    Gain,
    HighpassFilter,
    LowpassFilter,
    PeakFilter,
    HighShelfFilter,
    Reverb,
    Limiter
)

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

vocal_raw_path = r"C:\Users\MuzaffarZed\Desktop\vakal minus\vocall\untitled_2026-10-16 16-35-06_Insert 10.wav"
minus_path = r"C:\Users\MuzaffarZed\Desktop\vakal minus\minus\Mani_Izlab_Ovvora_Bolmang_Minus_Master_24bit.wav"
out_dir = r"C:\Users\MuzaffarZed\Desktop\vakal minus"

print("Loading raw vocal for Variant 2 (Modern Pop & Bright Air Sheen)...")
voc_raw, voc_sr = sf.read(vocal_raw_path)

if voc_raw.ndim == 1:
    voc_raw = np.column_stack([voc_raw, voc_raw])
elif voc_raw.shape[1] == 1:
    voc_raw = np.column_stack([voc_raw[:, 0], voc_raw[:, 0]])

if voc_sr != 48000:
    num_samples = int(len(voc_raw) * 48000 / voc_sr)
    voc_resampled = signal.resample(voc_raw, num_samples)
    voc_sr = 48000
else:
    voc_resampled = voc_raw

# 1. Noise gate
mono = np.mean(np.abs(voc_resampled), axis=1)
thresh = 10**(-48.0 / 20.0)
gain_env = np.ones(len(mono))
gain_env[mono < thresh] = 0.0
sos_g = signal.butter(1, 20, btype='lowpass', fs=voc_sr, output='sos')
smooth_gain = signal.sosfilt(sos_g, gain_env)
voc_gated = voc_resampled * smooth_gain[:, np.newaxis]

# 2. Modern Pop Vocal Tone Chain (Extra Presence & Bright Air Sheen)
pop_tone = Pedalboard([
    HighpassFilter(cutoff_frequency_hz=105.0), # Crisp low cut
    PeakFilter(cutoff_frequency_hz=350.0, gain_db=-3.5, q=1.5),   # Deep mud scoop
    PeakFilter(cutoff_frequency_hz=2800.0, gain_db=3.2, q=1.3),   # Super presence
    PeakFilter(cutoff_frequency_hz=5200.0, gain_db=2.0, q=1.5),   # Clarity
    HighShelfFilter(cutoff_frequency_hz=10500.0, gain_db=5.2, q=0.7), # Bright Modern Air Sheen
    Distortion(drive_db=1.5), # Tube warmth
    Compressor(threshold_db=-20.0, ratio=4.5, attack_ms=8.0, release_ms=100.0), # Fast Pop Leveler
    Gain(gain_db=3.0)
])

voc_in_pb = voc_gated.T.astype(np.float32)
voc_pop_pb = pop_tone(voc_in_pb, voc_sr)
voc_pop = voc_pop_pb.T

# 3. Stereo Spatial Doubler + Ping-Pong Delay + Shimmering Reverb
pop_spatial = Pedalboard([
    Chorus(rate_hz=1.2, depth=0.35, feedback=0.15, mix=0.28), # Wider stereo field
    Delay(delay_seconds=0.333, feedback=0.25, mix=0.20),      # Tempo delay (333ms)
    Reverb(room_size=0.88, damping=0.25, wet_level=0.35, dry_level=0.85, width=1.0) # Shimmering Plate
])

voc_spatial_pb = pop_spatial(voc_pop.T.astype(np.float32), voc_sr)
voc_spatial = voc_spatial_pb.T

# Limiter for vocal
vocal_lim = Pedalboard([Limiter(threshold_db=-0.5, release_ms=60.0)])
vocal_final_pb = vocal_lim(voc_spatial.T.astype(np.float32), voc_sr)
vocal_final = vocal_final_pb.T

# Save Variant 2 Wet Vocal
out_pop_vocal = os.path.join(out_dir, "Vokal_Pro_Ishlov_(Variant_2_Pop_Air_Sheen_Wet).wav")
sf.write(out_pop_vocal, vocal_final, voc_sr, subtype='PCM_24')

# 4. Align with Minus
minus_data, minus_sr = sf.read(minus_path)
if minus_sr != voc_sr:
    num_samples = int(len(minus_data) * voc_sr / minus_sr)
    minus_data = signal.resample(minus_data, num_samples)

offset_samples = int(13.32 * voc_sr)
total_len = max(len(minus_data), offset_samples + len(vocal_final))
full_minus = np.zeros((total_len, 2), dtype=np.float32)
full_vocal = np.zeros((total_len, 2), dtype=np.float32)

full_minus[:len(minus_data)] = minus_data
full_vocal[offset_samples:offset_samples + len(vocal_final)] = vocal_final

# Dynamic sidechain ducking (-2.0 dB)
voc_env = np.mean(np.abs(full_vocal), axis=1)
sos_env = signal.butter(1, 10, btype='lowpass', fs=voc_sr, output='sos')
smooth_env = signal.sosfilt(sos_env, voc_env)
duck = np.ones(total_len, dtype=np.float32)
duck[smooth_env > 0.02] = 1.0 - (smooth_env[smooth_env > 0.02] * 0.45)
duck = np.clip(duck, 0.79, 1.0)

ducked_minus = full_minus * duck[:, np.newaxis]
master_raw = ducked_minus * 0.90 + full_vocal * 1.25

# 5. Master Bus Glue
master_board = Pedalboard([
    Compressor(threshold_db=-15.0, ratio=2.5, attack_ms=25.0, release_ms=180.0),
    Gain(gain_db=1.5),
    Limiter(threshold_db=-0.3, release_ms=70.0)
])
final_master_pb = master_board(master_raw.T.astype(np.float32), voc_sr)
final_master = final_master_pb.T

master_wav = os.path.join(out_dir, "Mani_Izlab_Ovvora_Bolmang_(Variant_2_Pop_Air_Sheen_2026).wav")
master_mp3 = os.path.join(out_dir, "Mani_Izlab_Ovvora_Bolmang_(Variant_2_Pop_Air_Sheen_2026).mp3")

sf.write(master_wav, final_master, voc_sr, subtype='PCM_24')

import subprocess
cmd_mp3 = [
    "ffmpeg", "-y", "-i", master_wav,
    "-b:a", "320k",
    "-metadata", "title=Mani Izlab Ovvora Bo'lmang (Variant 2 Pop Air Sheen 2026)",
    "-metadata", "artist=MuzaffarZed & Kamoliddin Rahmatov",
    "-metadata", "album=Master Series 2026",
    master_mp3
]
subprocess.run(cmd_mp3, capture_output=True)
print(f"Variant 2 WAV created: {master_wav}")
print(f"Variant 2 MP3 created: {master_mp3}")
