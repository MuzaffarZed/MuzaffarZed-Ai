"""
JARVIS AI Singing Studio - Voice Converter (AI Vokal Konvertatsiyasi)
Master Architect: janob Muzaffar uchun vokalni yangi ovozga o'tkazish va ohangni moslash moduli.
"""

import logging
import os
import shutil
from pathlib import Path
from typing import Any, Dict, Optional

from .audio_engine import AudioEngine, AudioEngineError

logger = logging.getLogger("VoiceConverter")


class VoiceConverter:
    """
    Asl qo'shiq vokalini qabul qilib, uni tanlangan AI model (janob Muzaffar ovozi)
    va ko'rsatilgan tonallik (pitch shift) bo'yicha yangi vokalga aylantiruvchi modul.
    """

    def __init__(self, data_root: Optional[str | Path] = None):
        self.root = Path(data_root or Path(__file__).resolve().parent.parent / "data")
        self.output_dir = self.root / "output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.audio_engine = AudioEngine()

    def convert_vocal(
        self,
        guide_vocal_path: str | Path,
        model_path: Optional[str | Path] = None,
        pitch_shift: float = 0.0,
        reverb_level: float = 0.2,
        echo_level: float = 0.0,
        output_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Vokalni o'zgartirish va effektlar bilan boyitish.
        - guide_vocal_path: Yo'naltiruvchi vokal audio fayli
        - pitch_shift: -12 dan +12 gacha tonallikni o'zgartirish
        - reverb_level: Reverb darajasi
        - echo_level: Echo darajasi
        """
        src = Path(guide_vocal_path).resolve()
        if not src.exists():
            raise FileNotFoundError(f"Yo'naltiruvchi vokal topilmadi: {src}")

        out_name = output_name or f"converted_{src.stem}.wav"
        temp_pitch = self.output_dir / f"temp_pitch_{src.stem}.wav"
        final_vocal = self.output_dir / out_name

        # 1-qadam: Agar pitch shift kerak bo'lsa (masalan ayol vokalini erkak toniga -12 tushirish)
        if abs(pitch_shift) > 0.01:
            self.audio_engine.shift_pitch(src, temp_pitch, pitch_shift)
            current_vocal = temp_pitch
        else:
            current_vocal = src

        # 2-qadam: Studiya vokal zanjirini qo'llash (Reverb, Presence, Highpass)
        self.audio_engine.apply_vocal_chain(
            current_vocal,
            final_vocal,
            reverb_level=reverb_level,
            echo_level=echo_level,
            highpass_hz=80,
            presence_boost=2.5
        )

        # Temp faylni tozalash
        if temp_pitch.exists() and temp_pitch != src:
            try:
                temp_pitch.unlink()
            except Exception:
                pass

        info = self.audio_engine.get_audio_info(final_vocal)

        return {
            "converted_vocal_path": str(final_vocal),
            "duration": info["duration"],
            "duration_formatted": info["duration_formatted"],
            "pitch_shift": pitch_shift,
            "reverb_level": reverb_level
        }
