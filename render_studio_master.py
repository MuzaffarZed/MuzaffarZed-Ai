import subprocess
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

minus_path = r"C:\Users\MuzaffarZed\Desktop\vakal minus\minus\Mani izlab ovvora boʻlmang karaoke.mp3"
vocal_path = r"C:\Users\MuzaffarZed\Desktop\vakal minus\vocall\untitled_2026-10-16 16-35-06_Insert 10.wav"
out_dir = r"C:\Users\MuzaffarZed\Desktop\vakal minus"

# Delay needed:
# Singing in Insert 10 starts at 11.28s
# Target start in karaoke is 24.60s
# Delay = 24.60 - 11.28 = 13.32s = 13320 ms
delay_ms = 13320

print(f"Starting Studio Mix & Master with vocal delay: {delay_ms}ms...")

# Filtergraph:
# [0:a] is minus
# [1:a] is vocal
filter_complex = (
    # 1. Prepare minus: apply gentle carving EQ in vocal range
    "[0:a]equalizer=f=2800:t=q:w=1.5:g=-1.8,volume=0.92[minus_sc];"
    # 2. Vocal chain:
    # Highpass 80Hz, Lowpass 16.5kHz, gentle denoise, de-esser, presence EQ, warmth EQ
    "[1:a]highpass=f=80,lowpass=f=16500,afftdn=nf=-45,deesser=i=0.5:m=0.5:f=0.5,"
    "equalizer=f=320:t=q:w=1.2:g=-2.2,equalizer=f=3300:t=q:w=1.0:g=+2.2,equalizer=f=10500:t=q:w=1.5:g=+1.8,"
    "acompressor=threshold=-19dB:ratio=3.5:attack=12:release=130:makeup=3dB[vocal_proc];"
    # 3. Create spatial reverb & delay for vocal
    "[vocal_proc]adelay={delay_ms}|{delay_ms}[vocal_delayed];"
    "[vocal_delayed]asplit=2[voc_dry][voc_fx_in];"
    "[voc_fx_in]aecho=0.8:0.7:120|240:0.25|0.18,lowpass=f=6000,volume=0.22[voc_reverb];"
    "[voc_dry][voc_reverb]amix=inputs=2:weights=1.0 0.8:dropout_transition=0[vocal_mastered];"
    # 4. Mix minus and vocal together
    "[minus_sc][vocal_mastered]amix=inputs=2:duration=first:weights=1.0 1.15:dropout_transition=0,"
    # 5. Broadcast Mastering (LUFS -14, True Peak -1.0)
    "loudnorm=I=-14:TP=-1.0:LRA=7[out]"
).format(delay_ms=delay_ms)

# 1. Output Radio Edit (~2m 25s with smooth fade-out at end of solo)
radio_out_mp3 = os.path.join(out_dir, "Mani_izlab_ovvora_bolmang_(Master_Radio_Edit).mp3")
cmd_radio = [
    "ffmpeg", "-y",
    "-i", minus_path,
    "-i", vocal_path,
    "-filter_complex", filter_complex + ";[out]afade=t=out:st=138:d=6[final_radio]",
    "-map", "[final_radio]",
    "-t", "144",
    "-b:a", "320k",
    "-metadata", "title=Mani izlab ovvora bo'lmang (Master Radio Edit)",
    "-metadata", "artist=MuzaffarZed Studio",
    "-metadata", "album=Studio Masters",
    "-metadata", "comment=Mix & Master by MuzaffarZed",
    radio_out_mp3
]

print("Rendering Radio Edit (320kbps MP3)...")
res_radio = subprocess.run(cmd_radio, capture_output=True, text=True, encoding="utf-8")
if res_radio.returncode == 0:
    print(f"Successfully created: {radio_out_mp3}")
else:
    print(f"Error creating Radio Edit: {res_radio.stderr[-500:]}")

# 2. Output Full Track (Full minus duration)
full_out_mp3 = os.path.join(out_dir, "Mani_izlab_ovvora_bolmang_(Master_Full_Track).mp3")
cmd_full = [
    "ffmpeg", "-y",
    "-i", minus_path,
    "-i", vocal_path,
    "-filter_complex", filter_complex,
    "-map", "[out]",
    "-b:a", "320k",
    "-metadata", "title=Mani izlab ovvora bo'lmang (Master Full Track)",
    "-metadata", "artist=MuzaffarZed Studio",
    "-metadata", "album=Studio Masters",
    "-metadata", "comment=Mix & Master by MuzaffarZed",
    full_out_mp3
]

print("Rendering Full Track (320kbps MP3)...")
res_full = subprocess.run(cmd_full, capture_output=True, text=True, encoding="utf-8")
if res_full.returncode == 0:
    print(f"Successfully created: {full_out_mp3}")
else:
    print(f"Error creating Full Track: {res_full.stderr[-500:]}")

# 3. Output Hi-Res Studio WAV (24-bit 44.1kHz Studio Master)
studio_wav = os.path.join(out_dir, "Mani_izlab_ovvora_bolmang_(Studio_Master_24bit).wav")
cmd_wav = [
    "ffmpeg", "-y",
    "-i", minus_path,
    "-i", vocal_path,
    "-filter_complex", filter_complex + ";[out]afade=t=out:st=138:d=6[final_wav]",
    "-map", "[final_wav]",
    "-t", "144",
    "-c:a", "pcm_s24le",
    studio_wav
]

print("Rendering Studio Master WAV (24-bit)...")
res_wav = subprocess.run(cmd_wav, capture_output=True, text=True, encoding="utf-8")
if res_wav.returncode == 0:
    print(f"Successfully created: {studio_wav}")
else:
    print(f"Error creating Studio WAV: {res_wav.stderr[-500:]}")
