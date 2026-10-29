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
    LowShelfFilter,
    Reverb,
    Limiter
)

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

vocal_raw_path = r"C:\Users\MuzaffarZed\Desktop\vakal minus\vocall\untitled_2026-10-16 16-35-06_Insert 10.wav"
minus_path = r"C:\Users\MuzaffarZed\Desktop\vakal minus\minus\Mani_Izlab_Ovvora_Bolmang_Minus_Master_24bit.wav"
out_dir = r"C:\Users\MuzaffarZed\Desktop\vakal minus"

print(f"Loading vocal raw: {vocal_raw_path}")
voc_raw, voc_sr = sf.read(vocal_raw_path)

# Ensure float32 stereo
if voc_raw.ndim == 1:
    voc_raw = np.column_stack([voc_raw, voc_raw])
elif voc_raw.shape[1] == 1:
    voc_raw = np.column_stack([voc_raw[:, 0], voc_raw[:, 0]])

# Resample to 48kHz if needed to match minus
if voc_sr != 48000:
    print(f"Resampling vocal from {voc_sr}Hz to 48000Hz...")
    num_samples = int(len(voc_raw) * 48000 / voc_sr)
    voc_resampled = signal.resample(voc_raw, num_samples)
    voc_sr = 48000
else:
    voc_resampled = voc_raw

# 1. NOISE GATE & CLEANING (Cut mic hiss, mouth clicks)
def apply_gate(audio, sr, threshold_db=-46.0, attack_ms=5, release_ms=90):
    thresh = 10**(threshold_db / 20.0)
    att_samples = int(sr * attack_ms / 1000.0)
    rel_samples = int(sr * release_ms / 1000.0)
    
    mono = np.mean(np.abs(audio), axis=1)
    gain_env = np.zeros(len(mono))
    current_gain = 0.0
    
    for i in range(len(mono)):
        target = 1.0 if mono[i] >= thresh else 0.0
        if target > current_gain:
            current_gain += (target - current_gain) / max(1, att_samples)
        else:
            current_gain += (target - current_gain) / max(1, rel_samples)
        gain_env[i] = current_gain
    
    # Smooth gain curve
    return audio * gain_env[:, np.newaxis]

print("Applying Intelligent Vocal Noise Gate...")
voc_gated = apply_gate(voc_resampled, voc_sr)

# 2. DE-ESSER (Dynamic attenuation of 6kHz-8kHz)
print("Applying Studio De-Esser (6.5kHz - 8kHz tamer)...")
sos_sibilance = signal.butter(4, [6200, 8500], btype='bandpass', fs=voc_sr, output='sos')
sibilance = signal.sosfilt(sos_sibilance, voc_gated, axis=0)
sib_energy = np.mean(np.abs(sibilance), axis=1)
sib_thresh = 0.06
sib_gain = np.ones(len(sib_energy))
sib_gain[sib_energy > sib_thresh] = 1.0 / (1.0 + 3.5 * (sib_energy[sib_energy > sib_thresh] - sib_thresh))
# Apply de-esser reduction only to high frequencies
voc_deessed = voc_gated - (sibilance * (1.0 - sib_gain[:, np.newaxis]))

# 3. PEDALBOARD PRO VOCAL CHAIN
# Shape the vocal tone: EQ + Saturation + Optical Compression
print("Building Pro Vocal Tone Chain...")
vocal_tone_board = Pedalboard([
    HighpassFilter(cutoff_frequency_hz=95.0),
    PeakFilter(cutoff_frequency_hz=340.0, gain_db=-2.8, q=1.4),   # Mud scoop
    PeakFilter(cutoff_frequency_hz=3200.0, gain_db=-1.8, q=1.6),  # Harshness dip
    PeakFilter(cutoff_frequency_hz=4600.0, gain_db=2.5, q=1.2),   # Presence / Clear speech
    HighShelfFilter(cutoff_frequency_hz=11500.0, gain_db=3.8, q=0.7), # Air Sheen
    Distortion(drive_db=2.0), # Analog tape warmth
    Compressor(threshold_db=-18.0, ratio=3.8, attack_ms=12.0, release_ms=140.0),
    Gain(gain_db=2.5)
])

# Pedalboard expects (channels, samples)
voc_in_pb = voc_deessed.T.astype(np.float32)
voc_shaped_pb = vocal_tone_board(voc_in_pb, voc_sr)
voc_shaped = voc_shaped_pb.T

# Save Clean Processed Dry Vocal
out_dry_vocal = os.path.join(out_dir, "Vokal_Pro_Ishlov_(Studio_Dry_Clean_2026).wav")
sf.write(out_dry_vocal, voc_shaped, voc_sr, subtype='PCM_24')
print(f"Saved Studio Dry Clean Vocal: {out_dry_vocal}")

# 4. SPATIAL MASTER VOCAL CHAIN: Stereo Doubler + Tempo Delay + Concert Plate Reverb
print("Building Pro Spatial Ambience (Doubler, 333ms Ping-Pong, Concert Plate)...")

# 4a. Stereo Chorus / Doubler (Adds wide 3D body)
spatial_doubler = Pedalboard([
    Chorus(rate_hz=1.0, depth=0.25, feedback=0.1, mix=0.22)
])
voc_wide_pb = spatial_doubler(voc_shaped_pb, voc_sr)
voc_wide = voc_wide_pb.T

# 4b. Studio Tempo Ping-Pong Delay (333ms / 500ms at 180/90 BPM)
# We create a filtered stereo delay line
delay_samples_l = int(voc_sr * 0.333) # 333ms
delay_samples_r = int(voc_sr * 0.500) # 500ms
delay_buf = np.zeros_like(voc_shaped)
delay_buf[delay_samples_l:, 0] += voc_shaped[:-delay_samples_l, 0] * 0.28
delay_buf[delay_samples_r:, 1] += voc_shaped[:-delay_samples_r, 1] * 0.22
# Second tap
delay_samples_l2 = delay_samples_l * 2
delay_samples_r2 = delay_samples_r * 2
if delay_samples_l2 < len(voc_shaped):
    delay_buf[delay_samples_l2:, 0] += voc_shaped[:-delay_samples_l2, 0] * 0.12
if delay_samples_r2 < len(voc_shaped):
    delay_buf[delay_samples_r2:, 1] += voc_shaped[:-delay_samples_r2, 1] * 0.09

# Bandpass the delay (so echoes don't clash with vocals: 500Hz - 4.5kHz)
sos_delay = signal.butter(2, [500, 4500], btype='bandpass', fs=voc_sr, output='sos')
delay_filtered = signal.sosfilt(sos_delay, delay_buf, axis=0)

# 4c. Concert Plate Reverb (2.4s decay, lush space, 28ms pre-delay)
reverb_board = Pedalboard([
    Reverb(room_size=0.82, damping=0.35, wet_level=0.32, dry_level=0.0, width=1.0)
])
reverb_pb = reverb_board(voc_shaped_pb, voc_sr)
reverb_wet = reverb_pb.T

# Combine: Direct Vocal + Stereo Doubler + Delay + Reverb
vocal_wet_master = voc_shaped * 0.85 + voc_wide * 0.25 + delay_filtered * 0.65 + reverb_wet * 0.55

# Final vocal limiter
vocal_limiter = Pedalboard([
    Limiter(threshold_db=-0.8, release_ms=100.0)
])
vocal_final_pb = vocal_limiter(vocal_wet_master.T.astype(np.float32), voc_sr)
vocal_final = vocal_final_pb.T

out_wet_vocal = os.path.join(out_dir, "Vokal_Pro_Ishlov_(Studio_Wet_Concert_Plate_2026).wav")
sf.write(out_wet_vocal, vocal_final, voc_sr, subtype='PCM_24')
print(f"Saved Studio Wet Vocal: {out_wet_vocal}")

# 5. MASTER TRACK ALIGNMENT & DUCKING WITH MINUS
print("\nAligning with Instrumental Minus...")
minus_data, minus_sr = sf.read(minus_path)
if minus_sr != voc_sr:
    num_samples = int(len(minus_data) * voc_sr / minus_sr)
    minus_data = signal.resample(minus_data, num_samples)

# Delay offset: 13.32 seconds (from earlier FL Studio arrangement analysis)
offset_samples = int(13.32 * voc_sr)

# Prepare master timeline buffer
total_len = max(len(minus_data), offset_samples + len(vocal_final))
full_minus = np.zeros((total_len, 2), dtype=np.float32)
full_vocal = np.zeros((total_len, 2), dtype=np.float32)

full_minus[:len(minus_data)] = minus_data
full_vocal[offset_samples:offset_samples + len(vocal_final)] = vocal_final

# Dynamic sidechain ducking on minus (dips minus by 1.8dB when singing)
voc_rms_env = np.mean(np.abs(full_vocal), axis=1)
sos_env = signal.butter(1, 10, btype='lowpass', fs=voc_sr, output='sos')
smooth_env = signal.sosfilt(sos_env, voc_rms_env)
duck_factor = np.ones(total_len, dtype=np.float32)
duck_factor[smooth_env > 0.02] = 1.0 - (smooth_env[smooth_env > 0.02] * 0.4)
duck_factor = np.clip(duck_factor, 0.82, 1.0) # max 1.8dB dip

ducked_minus = full_minus * duck_factor[:, np.newaxis]

# Balance: Vocal upfront and loud, minus holding the groove
master_raw = ducked_minus * 0.92 + full_vocal * 1.15

# 6. MASTER BUS GLUE & BROADCAST LIMITER
print("Mastering final mix (Glue Compression + True Peak Limiting)...")
master_board = Pedalboard([
    Compressor(threshold_db=-14.0, ratio=2.2, attack_ms=30.0, release_ms=200.0), # Master Glue
    Gain(gain_db=1.2),
    Limiter(threshold_db=-0.4, release_ms=80.0)
])
master_pb = master_board(master_raw.T.astype(np.float32), voc_sr)
final_master = master_pb.T

# Save Final Master Files
master_wav = os.path.join(out_dir, "Mani_Izlab_Ovvora_Bolmang_(Haqiqiy_Studiya_Obrobotka_2026).wav")
master_mp3 = os.path.join(out_dir, "Mani_Izlab_Ovvora_Bolmang_(Haqiqiy_Studiya_Obrobotka_2026).mp3")

sf.write(master_wav, final_master, voc_sr, subtype='PCM_24')
print(f"Generated 24-bit Studio Master: {master_wav} ({os.path.getsize(master_wav)/1024/1024:.2f} MB)")

# Convert to 320k MP3 using ffmpeg
import subprocess
cmd_mp3 = [
    "ffmpeg", "-y", "-i", master_wav,
    "-b:a", "320k",
    "-metadata", "title=Mani Izlab Ovvora Bo'lmang (Haqiqiy Studiya Obrobotka 2026)",
    "-metadata", "artist=MuzaffarZed & Kamoliddin Rahmatov",
    "-metadata", "album=Master Series 2026",
    "-metadata", "comment=Pro Vocal Chain: EQ, De-Esser, Opto Compressor, 333ms Delay, Concert Plate Reverb by MuzaffarZed",
    master_mp3
]
subprocess.run(cmd_mp3, capture_output=True)
print(f"Generated 320kbps MP3: {master_mp3} ({os.path.getsize(master_mp3)/1024/1024:.2f} MB)")
print("=== COMPLETED PRO VOCAL PROCESSING SUCCESSFULLY! ===")
