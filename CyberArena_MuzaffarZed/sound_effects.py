import pygame
import numpy as np

SAMPLE_RATE = 44100

def init_audio():
    try:
        pygame.mixer.init(SAMPLE_RATE, -16, 2, 512)
        return True
    except Exception as e:
        print(f"Mixer init error: {e}")
        return False

def make_stereo(mono_array):
    audio16 = (np.clip(mono_array, -1.0, 1.0) * 32767).astype(np.int16)
    return np.column_stack((audio16, audio16))

class SoundFX:
    def __init__(self):
        self.sounds = {}
        if not pygame.mixer.get_init():
            init_audio()
        self.generate_all()

    def generate_all(self):
        try:
            # 1. Laser Blast (Fast sweep down)
            dur = 0.12
            t = np.linspace(0, dur, int(SAMPLE_RATE * dur), False)
            freq = np.linspace(1100, 220, len(t))
            env = np.exp(-t * 25)
            wave = np.sin(2 * np.pi * freq * t) * env * 0.4
            self.sounds['laser'] = pygame.sndarray.make_sound(make_stereo(wave))

            # 2. Heavy Plasma Cannon (Deep crunch)
            dur = 0.22
            t = np.linspace(0, dur, int(SAMPLE_RATE * dur), False)
            freq = np.linspace(420, 70, len(t))
            noise = (np.random.rand(len(t)) * 2 - 1) * 0.3
            env = np.exp(-t * 14)
            wave = (np.sin(2 * np.pi * freq * t) * 0.7 + noise) * env * 0.5
            self.sounds['plasma'] = pygame.sndarray.make_sound(make_stereo(wave))

            # 3. Missile Launch (Whoosh + tone)
            dur = 0.3
            t = np.linspace(0, dur, int(SAMPLE_RATE * dur), False)
            freq = np.linspace(250, 700, len(t))
            noise = (np.random.rand(len(t)) * 2 - 1) * 0.25
            env = np.sin(np.pi * (t / dur))
            wave = (np.sin(2 * np.pi * freq * t) * 0.5 + noise) * env * 0.45
            self.sounds['missile'] = pygame.sndarray.make_sound(make_stereo(wave))

            # 4. Explosion (Sub-bass thump + pink noise decay)
            dur = 0.45
            t = np.linspace(0, dur, int(SAMPLE_RATE * dur), False)
            noise = (np.random.rand(len(t)) * 2 - 1)
            env = np.exp(-t * 7.5)
            sub = np.sin(2 * np.pi * 55 * t) * np.exp(-t * 9)
            wave = (noise * 0.6 + sub * 0.7) * env * 0.6
            self.sounds['explosion'] = pygame.sndarray.make_sound(make_stereo(wave))

            # 5. Dash / Blink (High speed air sweep)
            dur = 0.16
            t = np.linspace(0, dur, int(SAMPLE_RATE * dur), False)
            freq = np.linspace(600, 1500, len(t))
            noise = (np.random.rand(len(t)) * 2 - 1) * 0.4
            env = np.sin(np.pi * (t / dur)) ** 2
            wave = (np.sin(2 * np.pi * freq * t) * 0.4 + noise) * env * 0.4
            self.sounds['dash'] = pygame.sndarray.make_sound(make_stereo(wave))

            # 6. Shield Hit (Metallic ping + resonance)
            dur = 0.18
            t = np.linspace(0, dur, int(SAMPLE_RATE * dur), False)
            env = np.exp(-t * 22)
            wave = (np.sin(2 * np.pi * 1400 * t) * 0.5 + np.sin(2 * np.pi * 2200 * t) * 0.3) * env * 0.4
            self.sounds['shield'] = pygame.sndarray.make_sound(make_stereo(wave))

            # 7. Powerup Pickup (Rising magical arpeggio)
            notes = [523.25, 659.25, 783.99, 1046.50] # C5, E5, G5, C6
            chunk_len = int(SAMPLE_RATE * 0.06)
            wave_chunks = []
            for n in notes:
                ct = np.linspace(0, 0.06, chunk_len, False)
                chunk = np.sin(2 * np.pi * n * ct) * np.exp(-ct * 12) * 0.35
                wave_chunks.append(chunk)
            wave = np.concatenate(wave_chunks)
            self.sounds['powerup'] = pygame.sndarray.make_sound(make_stereo(wave))

            # 8. KO / Round Win Fanfare
            chord_notes = [440, 554.37, 659.25, 880]
            dur = 0.7
            t = np.linspace(0, dur, int(SAMPLE_RATE * dur), False)
            env = np.exp(-t * 4)
            wave = sum(np.sin(2 * np.pi * n * t) for n in chord_notes) * 0.2 * env
            self.sounds['ko'] = pygame.sndarray.make_sound(make_stereo(wave))

            # 9. Menu Beep / Select
            dur = 0.05
            t = np.linspace(0, dur, int(SAMPLE_RATE * dur), False)
            wave = np.sin(2 * np.pi * 880 * t) * np.exp(-t * 30) * 0.25
            self.sounds['beep'] = pygame.sndarray.make_sound(make_stereo(wave))

            print(f"[+] Successfully generated {len(self.sounds)} procedural sound effects!")
        except Exception as e:
            print(f"[-] Error synthesizing sounds: {e}")

    def play(self, name):
        if name in self.sounds:
            try:
                self.sounds[name].play()
            except Exception:
                pass
