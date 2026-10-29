import subprocess
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

vocal_insert10 = r"C:\Users\MuzaffarZed\Desktop\vakal minus\vocall\untitled_2026-10-16 16-35-06_Insert 10.wav"
vocal_project = r"C:\Users\MuzaffarZed\Desktop\vakal minus\vocall\Untitled project - 2026-Oct-16.wav"
out_dir = r"C:\Users\MuzaffarZed\Desktop\vakal minus"

print("Starting Professional Studio Vocal Stem Processing...")

# 1. DRY STUDIO VOCAL (EQ + De-Ess + 1176/LA2A Compressor + MicroShift Width - No Reverb)
# Ideal for producers who want a dry, upfront vocal to add their own FL Studio reverb/delay
filter_dry = (
    "highpass=f=90,lowpass=f=17500,"
    "afftdn=nf=-42,"
    "deesser=i=0.55:m=0.5:f=0.55:s=o,"
    "equalizer=f=340:t=q:w=1.3:g=-3.5,"
    "equalizer=f=850:t=q:w=1.2:g=+1.0,"
    "equalizer=f=1400:t=q:w=1.1:g=+2.2,"
    "equalizer=f=3500:t=q:w=1.0:g=+4.2,"
    "equalizer=f=11500:t=h:g=+3.8,"
    "acompressor=threshold=-22dB:ratio=4.0:attack=5:release=80:makeup=3.5dB:knee=2dB,"
    "acompressor=threshold=-16dB:ratio=2.5:attack=25:release=220:makeup=2.5dB:knee=4dB,"
    "chorus=0.7:0.9:45:0.35:0.25:2,"
    "alimiter=limit=-0.5dB"
)

# 2. WET STUDIO VOCAL (Full Studio Chain with Abbey Road Lush Hall Reverb & Stereo Delay)
filter_wet = (
    "highpass=f=90,lowpass=f=17500,"
    "afftdn=nf=-42,"
    "deesser=i=0.55:m=0.5:f=0.55:s=o,"
    "equalizer=f=340:t=q:w=1.3:g=-3.5,"
    "equalizer=f=850:t=q:w=1.2:g=+1.0,"
    "equalizer=f=1400:t=q:w=1.1:g=+2.2,"
    "equalizer=f=3500:t=q:w=1.0:g=+4.2,"
    "equalizer=f=11500:t=h:g=+3.8,"
    "acompressor=threshold=-22dB:ratio=4.0:attack=5:release=80:makeup=3.5dB:knee=2dB,"
    "acompressor=threshold=-16dB:ratio=2.5:attack=25:release=220:makeup=2.5dB:knee=4dB,"
    "chorus=0.7:0.9:45:0.35:0.25:2[v_dry];"
    "[v_dry]asplit=2[v_center][v_send];"
    "[v_send]highpass=f=450,lowpass=f=5500,aecho=0.8:0.7:160|320:0.22|0.14,volume=0.25[v_rev];"
    "[v_center][v_rev]amix=inputs=2:weights=1.2 0.5:dropout_transition=0,"
    "alimiter=limit=-0.5dB"
)

# Render Target 1: Vokal Pro Wet (24-bit WAV - Lossless Studio Master)
out_wav_wet = os.path.join(out_dir, "Vokal_Pro_Ishlov_(Wet_Reverb_24bit).wav")
cmd_wav_wet = [
    "ffmpeg", "-y",
    "-i", vocal_insert10,
    "-filter_complex", filter_wet,
    "-c:a", "pcm_s24le",
    out_wav_wet
]
print("Rendering Vokal Pro Wet 24-bit WAV...")
subprocess.run(cmd_wav_wet, capture_output=True, text=True, encoding="utf-8")

# Render Target 2: Vokal Pro Dry (24-bit WAV - Lossless Dry Studio Master)
out_wav_dry = os.path.join(out_dir, "Vokal_Pro_Ishlov_(Dry_Studio_24bit).wav")
cmd_wav_dry = [
    "ffmpeg", "-y",
    "-i", vocal_insert10,
    "-af", filter_dry,
    "-c:a", "pcm_s24le",
    out_wav_dry
]
print("Rendering Vokal Pro Dry 24-bit WAV...")
subprocess.run(cmd_wav_dry, capture_output=True, text=True, encoding="utf-8")

# Render Target 3: Vokal Pro Wet MP3 (320kbps)
out_mp3_wet = os.path.join(out_dir, "Vokal_Pro_Ishlov_(Wet_Reverb_320k).mp3")
cmd_mp3_wet = [
    "ffmpeg", "-y",
    "-i", vocal_insert10,
    "-filter_complex", filter_wet,
    "-b:a", "320k",
    "-metadata", "title=Mani izlab ovvora bo'lmang (Processed Vocal Wet)",
    "-metadata", "artist=MuzaffarZed Studio",
    out_mp3_wet
]
print("Rendering Vokal Pro Wet MP3...")
subprocess.run(cmd_mp3_wet, capture_output=True, text=True, encoding="utf-8")

# Render Target 4: Vokal Pro Dry MP3 (320kbps)
out_mp3_dry = os.path.join(out_dir, "Vokal_Pro_Ishlov_(Dry_Studio_320k).mp3")
cmd_mp3_dry = [
    "ffmpeg", "-y",
    "-i", vocal_insert10,
    "-af", filter_dry,
    "-b:a", "320k",
    "-metadata", "title=Mani izlab ovvora bo'lmang (Processed Vocal Dry)",
    "-metadata", "artist=MuzaffarZed Studio",
    out_mp3_dry
]
print("Rendering Vokal Pro Dry MP3...")
subprocess.run(cmd_mp3_dry, capture_output=True, text=True, encoding="utf-8")

# Clean up older test mixes to avoid clutter
for f in os.listdir(out_dir):
    if f.startswith("Mani_izlab_ovvora_bolmang_("):
        try:
            os.remove(os.path.join(out_dir, f))
            print(f"Cleaned up old mix: {f}")
        except Exception:
            pass

print("ALL PROCESSED VOCAL STEMS CREATED SUCCESSFULLY!")
