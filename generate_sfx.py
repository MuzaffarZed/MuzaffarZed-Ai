import os
import math
import wave
import struct
import random

out_dir = r'C:\Users\MuzaffarZed\ai_workspace\sfx_pack'
os.makedirs(out_dir, exist_ok=True)
sample_rate = 44100

def write_wav(filename, samples):
    filepath = os.path.join(out_dir, filename)
    with wave.open(filepath, 'w') as wf:
        wf.setnchannels(1)  # mono
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        packed = b''.join(struct.pack('<h', max(-32767, min(32767, int(s * 32767)))) for s in samples)
        wf.writeframes(packed)
    print(f"Created: {filename} ({len(samples)} samples)")

# 1. Whoosh Fast (Frequency sweep with filtered noise)
duration = 0.35
num_samples = int(sample_rate * duration)
samples = []
for i in range(num_samples):
    t = i / sample_rate
    # envelope: peak at 60%
    env = math.sin(math.pi * (t / duration)) ** 3
    # frequency sweeps from 200Hz to 1200Hz then down to 300Hz
    freq = 200 + 1000 * math.sin(math.pi * (t / duration))
    noise = (random.random() * 2 - 1) * 0.4
    tone = math.sin(2 * math.pi * freq * t) * 0.6
    samples.append((tone + noise) * env * 0.8)
write_wav("01_Whoosh_Fast.wav", samples)

# 2. Whoosh Deep / Cinematic
duration = 0.55
num_samples = int(sample_rate * duration)
samples = []
for i in range(num_samples):
    t = i / sample_rate
    env = math.sin(math.pi * (t / duration)) ** 2
    freq = 80 + 350 * math.sin(math.pi * (t / duration))
    noise = (random.random() * 2 - 1) * 0.3
    tone = math.sin(2 * math.pi * freq * t) * 0.7
    samples.append((tone + noise) * env * 0.9)
write_wav("02_Whoosh_Cinematic.wav", samples)

# 3. Pop Clean (Bubble / Text popup)
duration = 0.12
num_samples = int(sample_rate * duration)
samples = []
for i in range(num_samples):
    t = i / sample_rate
    env = math.exp(-t * 40)
    # Pitch drops rapidly from 900Hz to 250Hz
    freq = 250 + 650 * math.exp(-t * 50)
    val = math.sin(2 * math.pi * freq * t) * env
    samples.append(val * 0.85)
write_wav("03_Pop_Text.wav", samples)

# 4. Ding / Crystal Chime (Important point)
duration = 0.8
num_samples = int(sample_rate * duration)
samples = []
for i in range(num_samples):
    t = i / sample_rate
    env = math.exp(-t * 6)
    # Bell harmonics: fundamental 1568Hz (G6) + 3136Hz
    val = 0.7 * math.sin(2 * math.pi * 1568 * t) + 0.3 * math.sin(2 * math.pi * 3136 * t)
    samples.append(val * env * 0.75)
write_wav("04_Ding_Chime.wav", samples)

# 5. Success / Achievement Chime (2 notes)
duration = 0.6
num_samples = int(sample_rate * duration)
samples = []
for i in range(num_samples):
    t = i / sample_rate
    if t < 0.15:
        # Note 1: E6 (1318 Hz)
        env = math.exp(-t * 12)
        val = math.sin(2 * math.pi * 1318 * t) * env
    else:
        # Note 2: A6 (1760 Hz)
        t2 = t - 0.15
        env = math.exp(-t2 * 7)
        val = math.sin(2 * math.pi * 1760 * t2) * env
    samples.append(val * 0.75)
write_wav("05_Success_Ding.wav", samples)

# 6. Camera Shutter Click
duration = 0.2
num_samples = int(sample_rate * duration)
samples = []
for i in range(num_samples):
    t = i / sample_rate
    # Click 1 at 0ms, Click 2 at 70ms
    val = 0.0
    if t < 0.05:
        val = (random.random() * 2 - 1) * math.exp(-t * 120) * 0.8
    elif 0.07 < t < 0.14:
        t2 = t - 0.07
        val = (random.random() * 2 - 1) * math.exp(-t2 * 90) * 0.7
    samples.append(val)
write_wav("06_Camera_Shutter.wav", samples)

# 7. Mouse UI Click
duration = 0.06
num_samples = int(sample_rate * duration)
samples = []
for i in range(num_samples):
    t = i / sample_rate
    env = math.exp(-t * 160)
    val = (math.sin(2 * math.pi * 2200 * t) * 0.5 + (random.random() * 2 - 1) * 0.5) * env
    samples.append(val * 0.8)
write_wav("07_Click_UI.wav", samples)

# 8. Keyboard Typing Click
duration = 0.08
num_samples = int(sample_rate * duration)
samples = []
for i in range(num_samples):
    t = i / sample_rate
    env = math.exp(-t * 100)
    freq = 600 + 400 * math.exp(-t * 80)
    val = (math.sin(2 * math.pi * freq * t) * 0.6 + (random.random() * 2 - 1) * 0.4) * env
    samples.append(val * 0.75)
write_wav("08_Keyboard_Tap.wav", samples)

# 9. Bass Impact / Hit (Transition hit)
duration = 0.6
num_samples = int(sample_rate * duration)
samples = []
for i in range(num_samples):
    t = i / sample_rate
    env = math.exp(-t * 7)
    # Bass pitch drop from 120Hz to 45Hz
    freq = 45 + 75 * math.exp(-t * 15)
    val = math.sin(2 * math.pi * freq * t) * env
    samples.append(val * 0.95)
write_wav("09_Bass_Impact.wav", samples)

# 10. Glitch / Cyber zap
duration = 0.18
num_samples = int(sample_rate * duration)
samples = []
for i in range(num_samples):
    t = i / sample_rate
    env = math.sin(math.pi * (t / duration))
    # Stepped harsh square-ish frequencies
    step = int(t * 80) % 4
    freq = [440, 880, 220, 1320][step]
    val = (1.0 if math.sin(2 * math.pi * freq * t) > 0 else -1.0) * 0.5 + (random.random() * 2 - 1) * 0.3
    samples.append(val * env * 0.7)
write_wav("10_Glitch_Transition.wav", samples)

print("SFX PACK COMPLETE!")
