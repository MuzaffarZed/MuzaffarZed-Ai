import soundfile as sf
import numpy as np

m1_path = r"C:\Users\MuzaffarZed\Desktop\vakal minus\Mani_Izlab_Ovvora_Bolmang_(Haqiqiy_Studiya_Obrobotka_2026).wav"
m2_path = r"C:\Users\MuzaffarZed\Desktop\vakal minus\Mani_Izlab_Ovvora_Bolmang_(Variant_2_Pop_Air_Sheen_2026).wav"

d1, sr1 = sf.read(m1_path)
d2, sr2 = sf.read(m2_path)

def check(name, d):
    peak = np.max(np.abs(d))
    rms = np.sqrt(np.mean(d**2))
    peak_db = 20 * np.log10(peak)
    rms_db = 20 * np.log10(rms)
    print(f"[{name}]")
    print(f"  Duration: {len(d)/48000:.2f}s")
    print(f"  True Peak: {peak_db:.2f} dBFS")
    print(f"  RMS Loudness: {rms_db:.2f} dBFS")

check("Variant 1 (Lush Estrada Plate + Delay)", d1)
check("Variant 2 (Modern Pop + Air Sheen)", d2)
