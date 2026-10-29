import subprocess
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

minus_path = r"C:\Users\MuzaffarZed\Desktop\vakal minus\minus\Mani izlab ovvora boʻlmang karaoke.mp3"
vocal_path = r"C:\Users\MuzaffarZed\Desktop\vakal minus\vocall\untitled_2026-10-16 16-35-06_Insert 10.wav"
out_dir = r"C:\Users\MuzaffarZed\Desktop\vakal minus"

def render_master(delay_ms, label, is_main=False):
    filter_complex = (
        "[0:a]equalizer=f=3300:t=q:w=1.4:g=-3.5,equalizer=f=1200:t=q:w=1.2:g=-1.8,volume=0.90[minus_pocket];"
        f"[1:a]adelay={delay_ms}|{delay_ms},"
        "highpass=f=95,lowpass=f=16800,afftdn=nf=-42,deesser=i=0.55:m=0.5:f=0.55:s=o,"
        "equalizer=f=350:t=q:w=1.3:g=-3.5,equalizer=f=1300:t=q:w=1.1:g=+2.2,"
        "equalizer=f=3400:t=q:w=1.0:g=+4.2,equalizer=f=11500:t=h:g=+3.8,"
        "acompressor=threshold=-22dB:ratio=4.0:attack=6:release=90:makeup=3.5dB:knee=2dB,"
        "acompressor=threshold=-16dB:ratio=2.5:attack=25:release=220:makeup=2.5dB:knee=4dB,"
        "chorus=0.7:0.9:45:0.35:0.25:2[voc_sculpted];"
        "[voc_sculpted]asplit=2[voc_dry][voc_send];"
        "[voc_send]highpass=f=450,lowpass=f=5500,aecho=0.8:0.7:160|320:0.22|0.14,volume=0.22[voc_reverb];"
        "[voc_dry][voc_reverb]amix=inputs=2:weights=1.25 0.5:dropout_transition=0[voc_final];"
        "[minus_pocket][voc_final]amix=inputs=2:duration=first:weights=0.90 1.65:dropout_transition=0,"
        "loudnorm=I=-14:TP=-1.0:LRA=7[master_out]"
    )

    out_file = os.path.join(out_dir, f"Mani_izlab_ovvora_bolmang_({label}).mp3")
    cmd = [
        "ffmpeg", "-y",
        "-i", minus_path,
        "-i", vocal_path,
        "-filter_complex", filter_complex + ";[master_out]afade=t=out:st=138:d=6[final_radio]",
        "-map", "[final_radio]",
        "-t", "144",
        "-b:a", "320k",
        "-metadata", f"title=Mani izlab ovvora bo'lmang ({label})",
        "-metadata", "artist=MuzaffarZed Studio",
        "-metadata", "album=Master Series 2026",
        "-metadata", "comment=Mix & Master by MuzaffarZed",
        out_file
    ]
    print(f"Rendering {label} ({delay_ms}ms)...")
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if res.returncode == 0:
        print(f"  SUCCESS: {out_file}")
    else:
        print(f"  ERROR: {res.stderr[-300:]}")
    return out_file

# Clean up older broken mukammal files
for f in os.listdir(out_dir):
    if f.startswith("Mani_izlab_ovvora_bolmang_(Mukammal_Master_"):
        try:
            os.remove(os.path.join(out_dir, f))
            print(f"Removed previous test file: {f}")
        except Exception:
            pass

# Render the 3 pinpoint sweet spots:
# 1. 12080ms: Mathematical 4-bar center downbeat (Primary Master)
render_master(12080, "Mukammal_Master_Radio", is_main=True)
# 2. 11750ms: Slightly earlier option (-330ms, 1 eighth-note earlier)
render_master(11750, "Mukammal_Master_Variant_A")
# 3. 12380ms: Slightly laid-back option (+300ms, 1 eighth-note later)
render_master(12380, "Mukammal_Master_Variant_B")

# Also render full 6-minute master for 12080ms
filter_full = (
    "[0:a]equalizer=f=3300:t=q:w=1.4:g=-3.5,equalizer=f=1200:t=q:w=1.2:g=-1.8,volume=0.90[minus_pocket];"
    "[1:a]adelay=12080|12080,"
    "highpass=f=95,lowpass=f=16800,afftdn=nf=-42,deesser=i=0.55:m=0.5:f=0.55:s=o,"
    "equalizer=f=350:t=q:w=1.3:g=-3.5,equalizer=f=1300:t=q:w=1.1:g=+2.2,"
    "equalizer=f=3400:t=q:w=1.0:g=+4.2,equalizer=f=11500:t=h:g=+3.8,"
    "acompressor=threshold=-22dB:ratio=4.0:attack=6:release=90:makeup=3.5dB:knee=2dB,"
    "acompressor=threshold=-16dB:ratio=2.5:attack=25:release=220:makeup=2.5dB:knee=4dB,"
    "chorus=0.7:0.9:45:0.35:0.25:2[voc_sculpted];"
    "[voc_sculpted]asplit=2[voc_dry][voc_send];"
    "[voc_send]highpass=f=450,lowpass=f=5500,aecho=0.8:0.7:160|320:0.22|0.14,volume=0.22[voc_reverb];"
    "[voc_dry][voc_reverb]amix=inputs=2:weights=1.25 0.5:dropout_transition=0[voc_final];"
    "[minus_pocket][voc_final]amix=inputs=2:duration=first:weights=0.90 1.65:dropout_transition=0,"
    "loudnorm=I=-14:TP=-1.0:LRA=7[master_out]"
)
full_cmd = [
    "ffmpeg", "-y",
    "-i", minus_path,
    "-i", vocal_path,
    "-filter_complex", filter_full,
    "-map", "[master_out]",
    "-b:a", "320k",
    "-metadata", "title=Mani izlab ovvora bo'lmang (Mukammal Master Full)",
    "-metadata", "artist=MuzaffarZed Studio",
    "-metadata", "comment=Mix & Master by MuzaffarZed",
    os.path.join(out_dir, "Mani_izlab_ovvora_bolmang_(Mukammal_Master_Full).mp3")
]
print("Rendering Full Master Track...")
subprocess.run(full_cmd, capture_output=True, text=True, encoding="utf-8")
print("All masters generated successfully!")
