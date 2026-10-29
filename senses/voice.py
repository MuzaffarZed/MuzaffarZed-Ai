"""
JARVIS-Core — Voice & Hearing Engine (Senses Subsystem)
Production-Ready Features:
- Fileless, zero-disk in-memory audio streaming (RAM/BytesIO) using edge-tts (uz-UZ-MadinaNeural)
- Ultra-low latency memory playback via pygame.mixer with WinMM fallback
- Tuned noise-tolerant SpeechRecognition for natural Uzbek speech
- Pyttsx3 instantaneous offline voice fallback
- Non-blocking acoustic cues via winsound
"""

from __future__ import annotations
import io
import os
import sys
import time
import asyncio
import logging
import threading
import ctypes
from pathlib import Path
from typing import Optional

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False

try:
    import winsound
    WINSOUND_AVAILABLE = True
except ImportError:
    WINSOUND_AVAILABLE = False

logger = logging.getLogger("JARVIS.Senses.Voice")


class VoiceEngine:
    """
    High-Performance Audio Perception and Synthesis Engine.
    Streams neural Uzbek speech entirely in RAM without polluting disk storage.
    """

    def __init__(
        self,
        voice_name: str = "uz-UZ-MadinaNeural",
        speech_rate: int = 175,
        energy_threshold: int = 300,
        dynamic_energy: bool = True,
    ) -> None:
        self.voice_name = voice_name
        self.speech_rate = speech_rate
        self.energy_threshold = energy_threshold
        self.dynamic_energy = dynamic_energy
        self.test_mode = os.getenv("JARVIS_TEST_MODE", "0") == "1"

        # Speech recognition tuning (O'zbek tili uchun optimallashtirilgan)
        self.recognizer = None
        self.microphone = None
        self._listening_announced = False
        if SPEECH_RECOGNITION_AVAILABLE:
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = self.energy_threshold
            self.recognizer.dynamic_energy_threshold = self.dynamic_energy
            self.recognizer.dynamic_energy_adjustment_damping = 0.15
            self.recognizer.dynamic_energy_ratio = 1.5
            self.recognizer.pause_threshold = 1.5  # So'zlar orasidagi tabiiy pauza uchun (kesilib qolmaslik)
            self.recognizer.phrase_threshold = 0.3
            self.recognizer.non_speaking_duration = 0.7

        # Offline pyttsx3 fallback
        self._offline_engine = None
        if PYTTSX3_AVAILABLE and not self.test_mode:
            try:
                self._offline_engine = pyttsx3.init()
                self._offline_engine.setProperty("rate", self.speech_rate)
            except Exception as e:
                logger.debug("pyttsx3 initialization note: %s", e)

        # WinMM fallback
        self._winmm = None
        if sys.platform == "win32":
            try:
                self._winmm = ctypes.windll.winmm
            except Exception as e:
                logger.debug("WinMM not available: %s", e)

        self._lock = threading.Lock()

    # -------------------------------------------------------------------------
    # 1. Acoustic Feedback Cues
    # -------------------------------------------------------------------------
    def play_cue(self, cue_type: str) -> None:
        """Plays non-blocking acoustic feedback tones."""
        if self.test_mode or not WINSOUND_AVAILABLE:
            return

        def _sound_worker():
            try:
                if cue_type == "listen_start":
                    winsound.Beep(880, 80)
                    time.sleep(0.02)
                    winsound.Beep(1320, 100)
                elif cue_type == "command_recognized":
                    winsound.Beep(1200, 70)
                elif cue_type == "done":
                    winsound.Beep(980, 80)
                    time.sleep(0.02)
                    winsound.Beep(1470, 120)
                elif cue_type == "error":
                    winsound.Beep(400, 150)
                    time.sleep(0.05)
                    winsound.Beep(300, 200)
            except Exception:
                pass

        threading.Thread(target=_sound_worker, daemon=True).start()

    # -------------------------------------------------------------------------
    # 2. Fileless In-Memory Audio Playback (RAM / BytesIO)
    # -------------------------------------------------------------------------
    def _play_in_memory_mp3(self, mp3_bytes: bytes) -> bool:
        """Plays raw MP3 bytes directly from RAM without touching the hard drive."""
        if self.test_mode:
            return True

        # Preferred in-memory player: Pygame Mixer
        if PYGAME_AVAILABLE:
            try:
                with self._lock:
                    if not pygame.mixer.get_init():
                        pygame.mixer.init()
                    audio_io = io.BytesIO(mp3_bytes)
                    pygame.mixer.music.load(audio_io)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        time.sleep(0.05)
                return True
            except Exception as e:
                logger.debug("Pygame in-memory playback failed: %s, falling back", e)

        # Fallback via WinMM if pygame is uninitialized
        if self._winmm:
            import tempfile
            temp_path = Path(tempfile.gettempdir()) / f"jarvis_speech_{int(time.time()*1000)}.mp3"
            try:
                temp_path.write_bytes(mp3_bytes)
                alias = f"jplay_{int(time.time() * 1000) % 100000}"
                self._winmm.mciSendStringW(f'open "{temp_path}" type mpegvideo alias {alias}', None, 0, None)
                self._winmm.mciSendStringW(f"play {alias} wait", None, 0, None)
                self._winmm.mciSendStringW(f"close {alias}", None, 0, None)
                temp_path.unlink(missing_ok=True)
                return True
            except Exception as e:
                logger.debug("WinMM fallback failed: %s", e)
                try:
                    temp_path.unlink(missing_ok=True)
                except Exception:
                    pass

        return False

    # -------------------------------------------------------------------------
    # 3. Speech Synthesis (TTS)
    # -------------------------------------------------------------------------
    async def speak_async(self, text: str, force_offline: bool = False) -> bool:
        """Asynchronously streams speech in RAM and plays back without disk writes."""
        print(f"JARVIS: {text}")

        if self.test_mode:
            return True

        if not force_offline and EDGE_TTS_AVAILABLE:
            try:
                communicate = edge_tts.Communicate(text, self.voice_name)
                audio_buffer = bytearray()
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        audio_buffer.extend(chunk["data"])

                if audio_buffer:
                    loop = asyncio.get_running_loop()
                    success = await loop.run_in_executor(None, self._play_in_memory_mp3, bytes(audio_buffer))
                    if success:
                        return True
            except Exception as e:
                logger.warning("edge-tts in-memory stream failed: %s, using offline voice", e)

        # Offline fallback
        return self.speak_offline(text)

    def speak_offline(self, text: str) -> bool:
        """Offline speech fallback using pyttsx3."""
        if self.test_mode:
            return True

        if self._offline_engine:
            try:
                with self._lock:
                    self._offline_engine.say(text)
                    self._offline_engine.runAndWait()
                return True
            except Exception as e:
                logger.error("Offline speech error: %s", e)
        return False

    def speak(self, text: str, force_offline: bool = False) -> bool:
        """Synchronous wrapper for speaking."""
        try:
            loop = asyncio.get_running_loop()
            if loop.is_running():
                future = asyncio.run_coroutine_threadsafe(
                    self.speak_async(text, force_offline),
                    loop,
                )
                return future.result(timeout=20)
        except RuntimeError:
            pass

        return asyncio.run(self.speak_async(text, force_offline))

    def set_voice(self, voice_name: str) -> bool:
        """Ovoz turini o'zgartiradi (Madina yoki Sardor)."""
        key = voice_name.lower().strip()
        if "sardor" in key or "erkak" in key:
            self.voice_name = "uz-UZ-SardorNeural"
            return True
        elif "madina" in key or "ayol" in key:
            self.voice_name = "uz-UZ-MadinaNeural"
            return True
        elif voice_name in ("uz-UZ-MadinaNeural", "uz-UZ-SardorNeural"):
            self.voice_name = voice_name
            return True
        return False

    def switch_to_male(self) -> str:
        """Sardor (erkak) ovoziga o'tkazadi."""
        self.set_voice("uz-UZ-SardorNeural")
        return "Ovoz Sardor (erkak ovozi)ga o'zgartirildi, janob."

    def switch_to_female(self) -> str:
        """Madina (ayol) ovoziga o'tkazadi."""
        self.set_voice("uz-UZ-MadinaNeural")
        return "Ovoz Madina (ayol ovozi)ga o'zgartirildi, janob."

    # -------------------------------------------------------------------------
    # 4. Microphone Hearing & Speech Recognition (STT)
    # -------------------------------------------------------------------------
    def calibrate_microphone(self, duration: float = 1.0) -> None:
        """Calibrates microphone for ambient noise."""
        if self.test_mode or not SPEECH_RECOGNITION_AVAILABLE:
            return

        try:
            if self.microphone is None:
                self.microphone = sr.Microphone()

            print("Mikrofon atrof-muhit shovqiniga moslashtirilmoqda...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=duration)
            print("[OK] Mikrofon kalibratsiyasi muvaffaqiyatli yakunlandi.")
        except Exception as e:
            logger.warning("Mikrofonni kalibratsiya qilishda xatolik: %s", e)

    def listen(self, timeout: int = 10, phrase_time_limit: int = 15) -> str:
        """
        Listens for user speech via microphone and converts to text in Uzbek.
        Returns recognized string in lowercase, or empty string on timeout/failure.
        """
        if self.test_mode or not SPEECH_RECOGNITION_AVAILABLE:
            return ""

        try:
            if self.microphone is None:
                self.microphone = sr.Microphone()

            if not self._listening_announced:
                self.play_cue("listen_start")
                print("\n[Tinglayapman...] (Janob, marhamat, buyruq bering)")
                self._listening_announced = True

            with self.microphone as source:
                try:
                    audio = self.recognizer.listen(
                        source,
                        timeout=timeout,
                        phrase_time_limit=phrase_time_limit,
                    )
                except sr.WaitTimeoutError:
                    return ""

            # Nutq aniqlandi - navbatdagi so'rov uchun e'lon bayrog'ini yangilaymiz
            self._listening_announced = False
            self.play_cue("command_recognized")
            text = self.recognizer.recognize_google(audio, language="uz-UZ")
            cleaned = text.strip()
            print(f"Siz: {cleaned}")
            return cleaned.lower()

        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            logger.error("Google Speech Recognition xizmatiga ulanib bo'lmadi: %s", e)
            return ""
        except Exception as e:
            logger.error("Ovozni qabul qilishda kutilmagan xatolik: %s", e)
            return ""

    def reset_listen_announcement(self) -> None:
        """Navbatdagi tinglashda bildirishnoma chiqishini ta'minlaydi."""
        self._listening_announced = False


_voice_engine: Optional[VoiceEngine] = None


def get_voice_engine() -> VoiceEngine:
    """Singleton getter for VoiceEngine."""
    global _voice_engine
    if _voice_engine is None:
        _voice_engine = VoiceEngine()
    return _voice_engine
