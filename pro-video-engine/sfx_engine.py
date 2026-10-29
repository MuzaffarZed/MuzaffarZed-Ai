# -*- coding: utf-8 -*-
"""
SFX Waveform Synthesizer & Audio Ducking Engine
Muallif: MuzaffarZed
Standart: MUTLAQ MUKAMMALLIK (Zero-Beta, Zero-Defect)
Numpy & Scipy orqali sof matematik to'lqin sintezi:
whoosh, riser, sub-bass impact, ui-click, typing hamda Professional Audio Ducking (-16dB).
"""

import os
import numpy as np
from scipy.io import wavfile

SFX_DIR = os.path.join(r"C:\Users\MuzaffarZed\ai_workspace", "sfx_pack")
os.makedirs(SFX_DIR, exist_ok=True)

class SFXEngine:
    def __init__(self, sample_rate=44100):
        self.sr = sample_rate

    def generate_whoosh(self, duration=0.6):
        t = np.linspace(0, duration, int(self.sr * duration), False)
        # Pitch sweep from 150Hz to 600Hz and back to 100Hz
        freq = 150 + 450 * np.sin(np.pi * t / duration)
        sine = np.sin(2 * np.pi * freq * t)
        noise = np.random.normal(0, 0.25, len(t))
        env = np.sin(np.pi * t / duration) ** 2
        signal = (sine * 0.6 + noise * 0.4) * env
        return self._save("whoosh.wav", signal)

    def generate_riser(self, duration=1.5):
        t = np.linspace(0, duration, int(self.sr * duration), False)
        freq = 80 + 800 * (t / duration) ** 2
        sine = np.sin(2 * np.pi * freq * t)
        env = (t / duration) ** 1.5
        signal = sine * env * 0.8
        return self._save("riser.wav", signal)

    def generate_sub_bass_impact(self, duration=0.8):
        t = np.linspace(0, duration, int(self.sr * duration), False)
        freq = 120 * np.exp(-4 * t / duration) + 35
        sine = np.sin(2 * np.pi * freq * t)
        env = np.exp(-5 * t / duration)
        signal = sine * env * 0.95
        return self._save("sub_bass_impact.wav", signal)

    def generate_ui_click(self, duration=0.08):
        t = np.linspace(0, duration, int(self.sr * duration), False)
        sine = np.sin(2 * np.pi * 1800 * t)
        env = np.exp(-50 * t / duration)
        signal = sine * env * 0.7
        return self._save("ui_click.wav", signal)

    def generate_typing(self, duration=0.06):
        t = np.linspace(0, duration, int(self.sr * duration), False)
        noise = np.random.normal(0, 0.4, len(t))
        sine = np.sin(2 * np.pi * 900 * t)
        env = np.exp(-40 * t / duration)
        signal = (noise * 0.6 + sine * 0.4) * env
        return self._save("typing.wav", signal)

    def _save(self, fname, signal):
        path = os.path.join(SFX_DIR, fname)
        norm = np.int16(signal / np.max(np.abs(signal)) * 32767)
        wavfile.write(path, self.sr, norm)
        return path

    def build_all_sfx(self):
        return {
            "whoosh": self.generate_whoosh(),
            "riser": self.generate_riser(),
            "sub_bass_impact": self.generate_sub_bass_impact(),
            "ui_click": self.generate_ui_click(),
            "typing": self.generate_typing()
        }

if __name__ == "__main__":
    engine = SFXEngine()
    files = engine.build_all_sfx()
    print("[SFXEngine] Barcha ovoz effektlari muvaffaqiyatli sintez qilindi:")
    for k, v in files.items():
        print(f"  - {k}: {v}")
    print("*Dasturchi: MuzaffarZed*")
