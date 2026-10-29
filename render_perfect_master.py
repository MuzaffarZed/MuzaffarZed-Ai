import subprocess
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

minus_path = r"C:\Users\MuzaffarZed\Desktop\vakal minus\minus\Mani izlab ovvora boʻlmang karaoke.mp3"
vocal_path = r"C:\Users\MuzaffarZed\Desktop\vakal minus\vocall\untitled_2026-10-16 16-35-06_Insert 10.wav"
out_dir = r"C:\Users\MuzaffarZed\Desktop\vakal minus"

delay_ms = 10800
print(f"Rendering Ultra-Studio Master with delay: {delay_ms}ms...")

filter_complex = (
    # 1. Minus pocket carving (carve space in mid-frequencies for the lead vocal)
    "[0:a]equalizer=f=3300:t=q:w=1.4:g=-3.5,"
    "equalizer=f=1200:t=q:w=1.2:g=-1.8,"
    "volume=0.90[minus_pocket];"

    # 2. Lead vocal chain:
    # Timing sync, Sub-bass cut, Top-end cleanup, Gentle Denoise, De-Esser,
    # 4-Band Studio EQ (Cut mud, add body, forward presence bite, silky air shelf),
    # 2-Stage Compression (Fast peak FET + Smooth Opto Leveler)
    "[1:a]adelay={delay_ms}|{delay_ms},"
    "highpass=f=95,lowpass=f=16800,"
    "afftdn=nf=-42,"
    "deesser=i=0.55:m=0.5:f=0.55:s=o,"
    "equalizer=f=350:t=q:w=1.3:g=-3.5,"
    "equalizer=f=1300:t=q:w=1.1:g=+2.2,"
    "equalizer=f=3400:t=q:w=1.0:g=+4.2,"
    "equalizer=f=11500:t=h:g=+3.8,"
    "acompressor=threshold=-22dB:ratio=4.0:attack=6:release=90:makeup=3.5dB:knee=2dB,"
    "acompressor=threshold=-16dB:ratio=2.5:attack=25:release=220:makeup=2.5dB:knee=4dB,"
    "chorus=0.7:0.9:45:0.35:0.25:2[voc_sculpted];"

    # 3. Spatial Reverb & Stereo Delay (Abbey Road filter: 450Hz - 5.5kHz)
    "[voc_sculpted]asplit=2[voc_dry][voc_send];"
    "[voc_send]highpass=f=450,lowpass=f=5500,"
    "aecho=0.8:0.7:160|320:0.22|0.14,"
    "volume=0.22[voc_reverb];"
    "[voc_dry][voc_reverb]amix=inputs=2:weights=1.25 0.5:dropout_transition=0[voc_final];"

    # 4. Mix Minus + Upfront Lead Vocal (High Vocal Prominence 1.65x)
    "[minus_pocket][voc_final]amix=inputs=2:duration=first:weights=0.90 1.65:dropout_transition=0,"
    # 5. Broadcast EBU R128 Loudness Normalization & True Peak Limiter
    "loudnorm=I=-14:TP=-1.0:LRA=7[master_out]"
).format(delay_ms=delay_ms)

# 1. Output Radio Edit (~2m 24s)
out_radio = os.path.join(out_dir, "Mani_izlab_ovvora_bolmang_(Mukammal_Master_Radio).mp3")
cmd_radio = [
    "ffmpeg", "-y",
    "-i", minus_path,
    "-i", vocal_path,
    "-filter_complex", filter_complex + ";[master_out]afade=t=out:st=138:d=6[final_radio]",
    "-map", "[final_radio]",
    "-t", "144",
    "-b:a", "320k",
    "-metadata", "title=Mani izlab ovvora bo'lmang (Mukammal Master)",
    "-metadata", "artist=MuzaffarZed Studio",
    "-metadata", "album=Master Series 2026",
    "-metadata", "comment=Mix & Master by MuzaffarZed",
    out_radio
]

print("Rendering Mukammal Master Radio Edit (320kbps MP3)...")
r_rad = subprocess.run(cmd_radio, capture_output=True, text=True, encoding="utf-8")
if r_rad.returncode == 0:
    print(f"SUCCESS: {out_radio}")
else:
    print(f"ERROR: {r_rad.stderr[-600:]}")

# 2. Output Full Track (Full minus duration: 6m 48s)
out_full = os.path.join(out_dir, "Mani_izlab_ovvora_bolmang_(Mukammal_Master_Full).mp3")
cmd_full = [
    "ffmpeg", "-y",
    "-i", minus_path,
    "-i", vocal_path,
    "-filter_complex", filter_complex,
    "-map", "[master_out]",
    "-b:a", "320k",
    "-metadata", "title=Mani izlab ovvora bo'lmang (Mukammal Master Full)",
    "-metadata", "artist=MuzaffarZed Studio",
    "-metadata", "album=Master Series 2026",
    "-metadata", "comment=Mix & Master by MuzaffarZed",
    out_full
]

print("Rendering Mukammal Master Full Track (320kbps MP3)...")
r_full = subprocess.run(cmd_full, capture_output=True, text=True, encoding="utf-8")
if r_full.returncode == 0:
    print(f"SUCCESS: {out_full}")
else:
    print(f"ERROR: {r_full.stderr[-600:]}")

# 3. Output Hi-Res 24-bit Studio Master WAV (Lossless)
out_wav = os.path.join(out_dir, "Mani_izlab_ovvora_bolmang_(Mukammal_Master_24bit).wav")
cmd_wav = [
    "ffmpeg", "-y",
    "-i", minus_path,
    "-i", vocal_path,
    "-filter_complex", filter_complex + ";[master_out]afade=t=out:st=138:d=6[final_wav]",
    "-map", "[final_wav]",
    "-t", "144",
    "-c:a", "pcm_s24le",
    out_wav
]

print("Rendering Mukammal Studio Master WAV (24-bit)...")
r_wav = subprocess.run(cmd_wav, capture_output=True, text=True, encoding="utf-8")
if r_wav.returncode == 0:
    print(f"SUCCESS: {out_wav}")
else:
    print(f"ERROR: {r_wav.stderr[-600:]}")
