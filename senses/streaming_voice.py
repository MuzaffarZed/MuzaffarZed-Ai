"""senses/streaming_voice.py - Real-Time In-Memory Streaming Voice with Barge-In Interrupt.

Xususiyatlar:
1. Diskka hech qanday .mp3 fayl yozmasdan to'g'ridan-to'g'ri RAMda (io.BytesIO) edge-tts sintezi.
2. Background thread orqali pygame.mixer da oqimli ijro.
3. Barge-in (Interrupt) mexanizmi: foydalanuvchi gapira boshlaganda yoki klaviatura tugmasi
   bosilganda ovoz bir zumda to'xtatiladi (pygame.mixer.stop()).
4. Jonli HUD konsol status paneli: CPU, RAM, Gemini API va tsikl holatini ko'rsatish.
"""

from __future__ import annotations

import asyncio
import io
import logging
import msvcrt
import threading
import time
from typing import Any, Callable, Optional

import psutil
import pygame

logger = logging.getLogger("Jarvis.StreamingVoice")

# Sof aksentsiz O'zbek tili neyron ovozlari
VOICE_MADINA = "uz-UZ-MadinaNeural"  # Ayol ovozi (muloyim va ravon)
VOICE_SARDOR = "uz-UZ-SardorNeural"  # Erkak ovozi (jiddiy va professional)
DEFAULT_VOICE = VOICE_MADINA

AVAILABLE_VOICES = {
    "madina": VOICE_MADINA,
    "ayol": VOICE_MADINA,
    "sardor": VOICE_SARDOR,
    "erkak": VOICE_SARDOR,
}


class StreamingVoiceEngine:
    """Xotirada ishlovchi, to'xtatish (barge-in) imkoniyatiga ega ovoz dvigateli."""

    def __init__(
        self,
        voice: str = DEFAULT_VOICE,
        rate: str = "+5%",
        volume: str = "+0%",
        test_mode: bool = False,
    ) -> None:
        self.voice = voice
        self.rate = rate
        self.volume = volume
        self.test_mode = test_mode
        self._is_speaking = False
        self._interrupt_flag = threading.Event()
        self._current_thread: Optional[threading.Thread] = None

        if not self.test_mode:
            try:
                if not pygame.mixer.get_init():
                    pygame.mixer.init(frequency=24000, size=-16, channels=2, buffer=1024)
            except Exception as e:
                logger.warning("pygame.mixer ishga tushirishda ogohlantirish: %s", e)

    def set_voice(self, voice_name: str) -> bool:
        """Ovoz turini o'zgartiradi (Madina yoki Sardor)."""
        key = voice_name.lower().strip()
        if key in AVAILABLE_VOICES:
            self.voice = AVAILABLE_VOICES[key]
            logger.info("Ovoz muvaffaqiyatli almashtirildi: %s", self.voice)
            return True
        elif voice_name in (VOICE_MADINA, VOICE_SARDOR):
            self.voice = voice_name
            logger.info("Ovoz muvaffaqiyatli almashtirildi: %s", self.voice)
            return True
        logger.warning("Noma'lum ovoz nomi: %s. Mavjud ovozlar: Madina, Sardor", voice_name)
        return False

    def switch_to_male(self) -> str:
        """Sardor (erkak) ovoziga o'tkazadi."""
        self.set_voice(VOICE_SARDOR)
        return "Ovoz Sardor (erkak ovozi)ga o'zgartirildi, janob."

    def switch_to_female(self) -> str:
        """Madina (ayol) ovoziga o'tkazadi."""
        self.set_voice(VOICE_MADINA)
        return "Ovoz Madina (ayol ovozi)ga o'zgartirildi, janob."

    @property
    def current_voice_name(self) -> str:
        """Hozirgi faol ovoz nomini qaytaradi."""
        return "Sardor (Erkak)" if self.voice == VOICE_SARDOR else "Madina (Ayol)"

    @property
    def is_speaking(self) -> bool:
        """Hozirda ovoz yangrayotganligini bildiradi."""
        return self._is_speaking

    def interrupt(self) -> None:
        """Ovoz ijrosini darhol to'xtatadi (Barge-In)."""
        if self._is_speaking:
            logger.info("Barge-in: Ovoz ijrosi to'xtatildi!")
            self._interrupt_flag.set()
            try:
                if pygame.mixer.get_init():
                    pygame.mixer.stop()
            except Exception:
                pass
            self._is_speaking = False

    async def _synthesize_to_memory(self, text: str) -> bytes:
        """edge-tts orqali diskka yozmasdan xotirada (RAM) audio baytlarini oladi."""
        import edge_tts

        communicate = edge_tts.Communicate(text, self.voice, rate=self.rate, volume=self.volume)
        audio_stream = io.BytesIO()

        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_stream.write(chunk["data"])

        return audio_stream.getvalue()

    def speak(
        self,
        text: str,
        wait: bool = True,
        on_start: Optional[Callable[[], None]] = None,
        on_finish: Optional[Callable[[], None]] = None,
        listen_keyboard_interrupt: bool = True,
    ) -> bool:
        """Matnni xotirada generatsiya qilib ijro etadi.

        Barge-in yoqilgan bo'lsa, klaviatura tugmasi bosilishi ovozni to'xtatadi.
        """
        if not text or not text.strip():
            return False

        clean_text = text.strip()

        # Agar test rejimida bo'lsa
        if self.test_mode:
            logger.info("[TEST-VOICE] Gapirildi: %s", clean_text)
            if on_start:
                on_start()
            if on_finish:
                on_finish()
            return True

        # Avvalgi gapirishni to'xtatish
        self.interrupt()
        self._interrupt_flag.clear()

        def _play_worker() -> None:
            self._is_speaking = True
            if on_start:
                on_start()

            try:
                # Yangi asinxron hodisalar tsikli
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                audio_bytes = loop.run_until_complete(self._synthesize_to_memory(clean_text))
                loop.close()

                if self._interrupt_flag.is_set() or not audio_bytes:
                    self._is_speaking = False
                    return

                # Xotiradagi baytlarni pygame Sound obyektiga yuklash
                sound_io = io.BytesIO(audio_bytes)
                sound = pygame.mixer.Sound(sound_io)
                channel = sound.play()

                # Ijro davomida barge-in (klaviatura) nazorati
                while channel.get_busy() and not self._interrupt_flag.is_set():
                    if listen_keyboard_interrupt and msvcrt.kbhit():
                        # Klaviatura tugmasi bosildi - darhol to'xtatamiz
                        _ = msvcrt.getch()
                        logger.info("Foydalanuvchi klaviaturani bosdi: Ovoz to'xtatildi (Barge-in)")
                        self.interrupt()
                        break
                    time.sleep(0.05)

            except Exception as e:
                logger.error("Ovoz sintezi/ijrosida xatolik: %s", e)
            finally:
                self._is_speaking = False
                if on_finish:
                    on_finish()

        self._current_thread = threading.Thread(target=_play_worker, daemon=True)
        self._current_thread.start()

        if wait and self._current_thread:
            self._current_thread.join()

        return True

    # =========================================================================
    # JONLI HUD STATUS BAR
    # =========================================================================

    @staticmethod
    def get_hud_status(gemini_status: str = "GEMINI ONLINE", cycle_step: str = "Kutish") -> str:
        """Konsol uchun real vaqtli ixcham HUD satrini shakllantiradi."""
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory()
        ram_used = round(mem.used / (1024**3), 1)
        ram_total = round(mem.total / (1024**3), 1)

        # Holat belgisi
        if "ONLINE" in gemini_status.upper():
            status_icon = "●"
        elif "ERROR" in gemini_status.upper():
            status_icon = "▲"
        else:
            status_icon = "○"

        hud = f"[ CPU: {cpu:>4.1f}% | RAM: {ram_used:>3.1f}/{ram_total:>3.1f} GB | Holat: {status_icon} {gemini_status} | Tsikl: {cycle_step} ]"
        return hud


# Singleton
_streaming_voice: Optional[StreamingVoiceEngine] = None


def get_streaming_voice(test_mode: bool = False) -> StreamingVoiceEngine:
    """StreamingVoiceEngine yagona nusxasini qaytaradi."""
    global _streaming_voice
    if _streaming_voice is None:
        _streaming_voice = StreamingVoiceEngine(test_mode=test_mode)
    return _streaming_voice
