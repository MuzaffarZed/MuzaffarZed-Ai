import soundfile as sf
import numpy as np

p1 = r"C:\Users\MuzaffarZed\Desktop\vakal minus\vocall\Untitled project - 2026-Oct-16.wav"
p2 = r"C:\Users\MuzaffarZed\Desktop\vakal minus\vocall\untitled_2026-10-16 16-35-06_Insert 10.wav"

d1, sr1 = sf.read(p1)
d2, sr2 = sf.read(p2)

def stats(name, d, sr):
    mono = np.mean(d, axis=1) if d.ndim > 1 else d
    peak = np.max(np.abs(mono))
    rms = np.sqrt(np.mean(mono**2))
    # Silence vs active ratio
    active = mono[np.abs(mono) > (peak * 0.1)]
    active_rms = np.sqrt(np.mean(active**2)) if len(active) > 0 else 0
    silence = mono[np.abs(mono) < (peak * 0.02)]
    noise_floor = np.sqrt(np.mean(silence**2)) if len(silence) > 0 else 1e-6
    snr = 20 * np.log10((active_rms + 1e-6) / (noise_floor + 1e-6))
    print(f"[{name}]")
    print(f"  Duration: {len(d)/sr:.2f}s | Sample Rate: {sr} Hz")
    print(f"  Peak: {peak:.3f} ({20*np.log10(peak+1e-6):.1f} dBFS)")
    print(f"  RMS: {rms:.4f} ({20*np.log10(rms+1e-6):.1f} dBFS)")
    print(f"  Active Vocal RMS: {active_rms:.4f} ({20*np.log10(active_rms+1e-6):.1f} dBFS)")
    print(f"  Estimated SNR: {snr:.1f} dB")

stats("Take 1: Untitled project - 2026-Oct-16.wav", d1, sr1)
stats("Take 2: untitled_2026-10-16 16-35-06_Insert 10.wav", d2, sr2)
