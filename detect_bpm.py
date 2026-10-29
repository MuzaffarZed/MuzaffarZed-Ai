import soundfile as sf
import numpy as np
import scipy.signal as signal

minus_path = r"C:\Users\MuzaffarZed\Desktop\vakal minus\minus\Mani_Izlab_Ovvora_Bolmang_Minus_Master_24bit.wav"
data, sr = sf.read(minus_path)
if data.ndim > 1:
    data = np.mean(data, axis=1)

# Downsample to 1000Hz envelope
target_sr = 1000
step = sr // target_sr
sub = data[::step]

# Highpass to keep percussion transients
b, a = signal.butter(2, 50 / (target_sr / 2), btype='high')
env = np.abs(signal.lfilter(b, a, sub))

# Autocorrelation of envelope for lag 60 BPM to 180 BPM
# BPM = 60 * target_sr / lag
min_lag = int(60 * target_sr / 180) # 180 BPM
max_lag = int(60 * target_sr / 65)  # 65 BPM

corr = signal.correlate(env, env, mode='full')
lags = signal.correlation_lags(len(env), len(env), mode='full')
pos_idx = lags >= min_lag
valid_lags = lags[pos_idx & (lags <= max_lag)]
valid_corr = corr[pos_idx & (lags <= max_lag)]

best_lag = valid_lags[np.argmax(valid_corr)]
detected_bpm = 60 * target_sr / best_lag

print(f"Detected BPM: {detected_bpm:.1f} (lag: {best_lag})")
