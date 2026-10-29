"""
senses/wake_listener.py — Always-On Resident Wake-Word Listener for J.A.R.V.I.S
Provides continuous 24/7 background audio perception. Detects wake words ('Jarvis', 'Salom Jarvis', 'Hey Jarvis')
and seamlessly bridges voice commands into the ReAct autonomous loop.
"""

from __future__ import annotations

import logging
import os
import sys
import threading
import time
from typing import Callable, List, Optional

try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
except ImportError:
    sr = None  # type: ignore
    SPEECH_AVAILABLE = False

try:
    import winsound
    WINSOUND_AVAILABLE = True
except ImportError:
    winsound = None  # type: ignore
    WINSOUND_AVAILABLE = False

logger = logging.getLogger("JARVIS.Senses.WakeListener")


class WakeListener:
    """Continuous background voice wake-word detector."""

    WAKE_WORDS: List[str] = [
        "jarvis",
        "salom jarvis",
        "hey jarvis",
        "ey jarvis",
        "jarvisjon",
        "salom",
    ]

    def __init__(
        self,
        on_wake: Optional[Callable[[str], None]] = None,
        language: str = "uz-UZ",
    ) -> None:
        self.on_wake = on_wake
        self.language = language
        self.running = False
        self._thread: Optional[threading.Thread] = None
        self.test_mode = os.getenv("JARVIS_TEST_MODE", "0") == "1"

        if SPEECH_AVAILABLE and not self.test_mode:
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 280
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 1.0
        else:
            self.recognizer = None

    def play_wake_chime(self) -> None:
        """Plays an acoustic chime to indicate JARVIS is actively listening."""
        if WINSOUND_AVAILABLE and not self.test_mode:
            try:
                # Pleasant high-pitch alert beep
                winsound.Beep(1200, 100)
                winsound.Beep(1800, 150)
            except Exception:
                pass

    def start_listening(self) -> None:
        """Starts the background listening loop in a dedicated thread."""
        if self.running:
            return
        self.running = True
        self._thread = threading.Thread(target=self._listen_loop, daemon=True, name="JarvisWakeListener")
        self._thread.start()
        logger.info("Always-on WakeListener started in background (language: %s)", self.language)

    def stop_listening(self) -> None:
        """Stops the background listener."""
        self.running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)
        logger.info("WakeListener stopped")

    def _listen_loop(self) -> None:
        """Core listener loop processing microphone audio streams."""
        if self.test_mode or not SPEECH_AVAILABLE or not self.recognizer:
            logger.info("TestMode/SpeechUnavailable: wake listener loop idle")
            while self.running:
                time.sleep(0.5)
            return

        try:
            with sr.Microphone() as source:
                logger.info("Adjusting microphone for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1.0)
                logger.info("Microphone calibrated. Listening for wake words: %s", self.WAKE_WORDS)

                while self.running:
                    try:
                        audio = self.recognizer.listen(source, timeout=3.0, phrase_time_limit=8.0)
                    except sr.WaitTimeoutError:
                        continue
                    except Exception as e:
                        logger.debug("Listen stream timeout/hiccup: %s", e)
                        continue

                    # Transcribe audio
                    try:
                        text = self.recognizer.recognize_google(audio, language=self.language).lower().strip()
                        logger.info("Audio recognized: '%s'", text)

                        # Check for wake words
                        matched_wake = any(w in text for w in self.WAKE_WORDS)
                        if matched_wake:
                            logger.info("WAKE WORD DETECTED: '%s'", text)
                            self.play_wake_chime()

                            # Extract command after wake word if present
                            clean_cmd = text
                            for w in self.WAKE_WORDS:
                                if w in clean_cmd:
                                    clean_cmd = clean_cmd.replace(w, "").strip()

                            if self.on_wake:
                                self.on_wake(clean_cmd)

                    except sr.UnknownValueError:
                        pass
                    except sr.RequestError as e:
                        logger.warning("Speech recognition API request error: %s", e)
                    except Exception as e:
                        logger.error("Error in audio recognition pipeline: %s", e)

        except Exception as e:
            logger.error("Microphone hardware failed to initialize: %s", e)
            self.running = False


_listener_instance: Optional[WakeListener] = None


def get_wake_listener(on_wake: Optional[Callable[[str], None]] = None) -> WakeListener:
    """Singleton getter for WakeListener."""
    global _listener_instance
    if _listener_instance is None:
        _listener_instance = WakeListener(on_wake=on_wake)
    return _listener_instance
