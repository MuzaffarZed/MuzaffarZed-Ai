import numpy as np
import wave
import os

SAMPLE_RATE = 44100
OUT_DIR = r"C:\Users\MuzaffarZed\ai_workspace\sfx_pack"
os.makedirs(OUT_DIR, exist_ok=True)

def save_wav(filename, data):
    data = np.clip(data, -1.0, 1.0)
    int_data = (data * 32767).astype(np.int16)
    filepath = os.path.join(OUT_DIR, filename)
    with wave.open(filepath, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(int_data.tobytes())
    print(f"Created: {filename}")

# 11. Meme Laugh (Cartoon chuckle)
t = np.linspace(0, 1.2, int(SAMPLE_RATE * 1.2), False)
laugh = np.zeros_like(t)
for i in range(5):
    t_start = i * 0.22
    mask = (t >= t_start) & (t < t_start + 0.16)
    sub_t = t[mask] - t_start
    f = 450 + 80 * np.sin(2 * np.pi * 10 * sub_t)
    burst = np.sin(2 * np.pi * f * sub_t) * np.sin(np.pi * sub_t / 0.16)
    laugh[mask] += burst * 0.7
save_wav("11_Meme_Laugh.wav", laugh)

# 12. Applause / Crowd Clapping
t = np.linspace(0, 1.8, int(SAMPLE_RATE * 1.8), False)
np.random.seed(42)
applause = np.zeros_like(t)
# multiple random clap spikes
for _ in range(80):
    t_clap = np.random.uniform(0.05, 1.6)
    idx = int(t_clap * SAMPLE_RATE)
    if idx + 2000 < len(applause):
        spike = np.random.normal(0, 1, 2000) * np.exp(-np.linspace(0, 10, 2000))
        applause[idx:idx+2000] += spike * 0.15
envelope = np.minimum(t / 0.3, 1.0) * np.maximum(0.0, 1.0 - (t - 1.0) / 0.8)
save_wav("12_Applause_Crowd.wav", applause * envelope)

# 13. Dramatic Dun Dun Dun
t = np.linspace(0, 1.8, int(SAMPLE_RATE * 1.8), False)
dun = np.zeros_like(t)
# Note 1: 0 to 0.4s (Low G, 98Hz)
m1 = (t < 0.4)
dun[m1] += (np.sin(2 * np.pi * 98 * t[m1]) + 0.5 * np.sin(2 * np.pi * 196 * t[m1])) * np.exp(-t[m1] * 2.5)
# Note 2: 0.4 to 0.8s (Low G, 98Hz)
m2 = (t >= 0.4) & (t < 0.8)
dun[m2] += (np.sin(2 * np.pi * 98 * (t[m2]-0.4)) + 0.5 * np.sin(2 * np.pi * 196 * (t[m2]-0.4))) * np.exp(-(t[m2]-0.4) * 2.5)
# Note 3: 0.8 to 1.8s (Dramatic Eb, 77.7Hz with distortion)
m3 = (t >= 0.8)
t3 = t[m3] - 0.8
dun[m3] += (1.2 * np.sin(2 * np.pi * 77.78 * t3) + 0.7 * np.sin(2 * np.pi * 155.5 * t3) + 0.4 * np.sin(2 * np.pi * 233.1 * t3)) * np.exp(-t3 * 1.5)
save_wav("13_Dramatic_Dun_Dun.wav", dun * 0.8)

# 14. Error Buzzer
t = np.linspace(0, 0.45, int(SAMPLE_RATE * 0.45), False)
# Two dissonant low square waves
buzz = np.sign(np.sin(2 * np.pi * 140 * t)) * 0.5 + np.sign(np.sin(2 * np.pi * 148 * t)) * 0.5
env = np.exp(-t * 2)
save_wav("14_Error_Buzzer.wav", buzz * env * 0.6)

# 15. Correct Bell Ding
t = np.linspace(0, 0.8, int(SAMPLE_RATE * 0.8), False)
bell = (np.sin(2 * np.pi * 1046.5 * t) * 0.6 + 
        np.sin(2 * np.pi * 2093 * t) * 0.3 + 
        np.sin(2 * np.pi * 3136 * t) * 0.15) * np.exp(-t * 4.5)
save_wav("15_Correct_Bell_Ding.wav", bell)

# 16. Vinyl Scratch
t = np.linspace(0, 0.35, int(SAMPLE_RATE * 0.35), False)
mod_freq = 600 + 400 * np.sin(2 * np.pi * 8 * t)
noise = np.random.uniform(-0.5, 0.5, len(t))
scratch = np.sin(2 * np.pi * mod_freq * t) * 0.4 + noise * 0.6
scratch *= np.sin(np.pi * t / 0.35)
save_wav("16_Vinyl_Scratch.wav", scratch * 0.7)

# 17. Tape Rewind
t = np.linspace(0, 0.4, int(SAMPLE_RATE * 0.4), False)
chirp_freq = 800 + 4000 * (t / 0.4)**2
rewind = np.sin(2 * np.pi * chirp_freq * t) * np.sin(np.pi * t / 0.4)
save_wav("17_Tape_Rewind.wav", rewind * 0.7)

# 18. Telegram Notification
t = np.linspace(0, 0.35, int(SAMPLE_RATE * 0.35), False)
tg = np.zeros_like(t)
# Tone 1: 0 to 0.08s (880 Hz)
m1 = t < 0.08
tg[m1] = np.sin(2 * np.pi * 880 * t[m1]) * np.exp(-t[m1] * 15)
# Tone 2: 0.08 to 0.35s (1318.5 Hz, E6)
m2 = t >= 0.08
tg[m2] = np.sin(2 * np.pi * 1318.5 * (t[m2] - 0.08)) * np.exp(-(t[m2] - 0.08) * 12)
save_wav("18_Telegram_Notification.wav", tg * 0.8)

# 19. Punch Smash Impact
t = np.linspace(0, 0.3, int(SAMPLE_RATE * 0.3), False)
sub = np.sin(2 * np.pi * (80 - 40 * t/0.3) * t) * np.exp(-t * 12)
snap = np.random.uniform(-1, 1, len(t)) * np.exp(-t * 35)
save_wav("19_Punch_Smash.wav", (sub * 0.7 + snap * 0.6))

# 20. Tension Riser
t = np.linspace(0, 2.0, int(SAMPLE_RATE * 2.0), False)
riser_freq = 150 + 900 * (t / 2.0)**2
swell = (t / 2.0)**1.5
riser = (np.sin(2 * np.pi * riser_freq * t) + 0.3 * np.sin(2 * np.pi * riser_freq * 2 * t)) * swell
save_wav("20_Tension_Riser.wav", riser * 0.75)

# 21. Cinematic Sub Drop
t = np.linspace(0, 1.5, int(SAMPLE_RATE * 1.5), False)
drop_freq = 110 * np.exp(-t * 1.2)
drop = np.sin(2 * np.pi * drop_freq * t) * np.exp(-t * 1.5)
save_wav("21_Cinematic_Sub_Drop.wav", drop * 0.9)

# 22. Coin Collect (8-bit)
t = np.linspace(0, 0.35, int(SAMPLE_RATE * 0.35), False)
coin = np.zeros_like(t)
m1 = t < 0.07
coin[m1] = np.sin(2 * np.pi * 987.77 * t[m1])
m2 = t >= 0.07
coin[m2] = np.sin(2 * np.pi * 1318.5 * (t[m2] - 0.07)) * np.exp(-(t[m2] - 0.07) * 8)
save_wav("22_Coin_Collect.wav", coin * 0.7)

# 23. Clock Ticking
t = np.linspace(0, 0.15, int(SAMPLE_RATE * 0.15), False)
tick = (np.sin(2 * np.pi * 2200 * t) * 0.6 + np.random.uniform(-0.4, 0.4, len(t))) * np.exp(-t * 60)
save_wav("23_Clock_Ticking.wav", tick * 0.8)

# 24. Heartbeat Thump
t = np.linspace(0, 0.6, int(SAMPLE_RATE * 0.6), False)
hb = np.zeros_like(t)
# Lub
m1 = (t >= 0.05) & (t < 0.25)
t1 = t[m1] - 0.05
hb[m1] = np.sin(2 * np.pi * 55 * t1) * np.sin(np.pi * t1 / 0.2)
# Dub
m2 = (t >= 0.3) & (t < 0.5)
t2 = t[m2] - 0.3
hb[m2] = np.sin(2 * np.pi * 50 * t2) * np.sin(np.pi * t2 / 0.2) * 0.8
save_wav("24_Heartbeat_Thump.wav", hb * 0.9)

# 25. Swoosh High
t = np.linspace(0, 0.3, int(SAMPLE_RATE * 0.3), False)
swoosh_freq = 600 + 1200 * np.sin(np.pi * t / 0.3)
high_noise = np.random.normal(0, 0.6, len(t)) * np.sin(np.pi * t / 0.3)
swoosh = np.sin(2 * np.pi * swoosh_freq * t) * 0.4 + high_noise * 0.6
save_wav("25_Swoosh_High.wav", swoosh * 0.7)

print("All 15 expanded SFX successfully synthesized!")
