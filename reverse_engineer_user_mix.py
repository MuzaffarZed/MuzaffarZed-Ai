import soundfile as sf
import numpy as np
import scipy.signal as signal
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

user_mix_path = r"C:\Users\MuzaffarZed\Desktop\shag'zod aka.mp3"
minus_path = r"C:\Users\MuzaffarZed\Desktop\vakal minus\minus\Mani izlab ovvora boʻlmang karaoke.mp3"

user_mix, sr_u = sf.read(user_mix_path)
minus, sr_m = sf.read(minus_path)

print(f"User mix: {user_mix.shape}, sr={sr_u}, dur={len(user_mix)/sr_u:.2f}s")
print(f"Minus: {minus.shape}, sr={sr_m}, dur={len(minus)/sr_m:.2f}s")

# Let's align minus with user_mix to extract the ISOLATED VOCAL with all effects!
# In user_mix, user_mix = minus * k + vocal_processed
# If we phase-invert minus, we can isolate the exact processed vocal with reverb and delay!

# Resample minus to match user_mix
if sr_m != sr_u:
    num_samples = int(len(minus) * sr_u / sr_m)
    minus = signal.resample(minus, num_samples)

# Align the intro
u_mono = np.mean(user_mix[:sr_u*20], axis=1) # first 20s intro (pure minus)
m_mono = np.mean(minus[:sr_u*20], axis=1)

corr = signal.correlate(u_mono, m_mono, mode='full')
lags = signal.correlation_lags(len(u_mono), len(m_mono), mode='full')
best_lag = lags[np.argmax(corr)]
best_offset = best_lag / sr_u
print(f"Minus alignment offset: {best_offset:.4f}s ({best_lag} samples)")

# Gain ratio
k_gain = np.dot(u_mono, m_mono) / np.dot(m_mono, m_mono)
print(f"Minus gain in user mix: {k_gain:.3f}")

# Extract isolated processed vocal
aligned_minus = np.zeros_like(user_mix)
if best_lag >= 0:
    end = min(len(user_mix), best_lag + len(minus))
    m_len = end - best_lag
    aligned_minus[best_lag:end] = minus[:m_len] * k_gain
else:
    start_m = -best_lag
    m_len = min(len(user_mix), len(minus) - start_m)
    aligned_minus[:m_len] = minus[start_m:start_m + m_len] * k_gain

isolated_vocal = user_mix - aligned_minus

out_iso = r"C:\Users\MuzaffarZed\ai_workspace\user_isolated_vocal_fx.wav"
sf.write(out_iso, isolated_vocal, sr_u)
print(f"Isolated user's processed vocal with FX saved to: {out_iso}")
