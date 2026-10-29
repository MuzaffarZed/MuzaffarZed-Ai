"""
JARVIS AI Singing Studio - Stem Separator (Vokal va Minus Ajratuvchi)
Master Architect: janob Muzaffar uchun to'liq qo'shiqdan vokal va minusovkani ajratish moduli.
"""

import logging
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from .audio_engine import AudioEngine, AudioEngineError

logger = logging.getLogger("StemSeparator")


class StemSeparator:
    """
    To'liq qo'shiqdan Vokal (Acapella) va Musiqiy Fon (Minusovka)ni ajratuvchi modul.
    """

    def __init__(self, data_root: Optional[str | Path] = None):
        self.root = Path(data_root or Path(__file__).resolve().parent.parent / "data")
        self.songs_dir = self.root / "songs"
        self.songs_dir.mkdir(parents=True, exist_ok=True)
        self.audio_engine = AudioEngine()

    def separate_song(
        self,
        song_path: str | Path,
        song_id: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Original to'liq qo'shiqni vokal va minusovkaga ajratadi.
        Natijada ikkita fayl qaytariladi:
        - 'vocals': Ajratilgan vokal yo'li
        - 'instrumental': Toza minusovka yo'li
        """
        src = Path(song_path).resolve()
        if not src.exists():
            raise FileNotFoundError(f"Qo'shiq fayli topilmadi: {src}")

        prefix = song_id or src.stem
        out_vocal = self.songs_dir / f"{prefix}_vocals.wav"
        out_minus = self.songs_dir / f"{prefix}_instrumental.wav"

        # Minusovka yaratish: O'rta vokal kanalini fazaviy susaytirish va pastki/yuqori chastotalarni saqlash
        # FFmpeg filter: stereotools / o'rta-yon kanallar bilan professional minusovka filtri
        minus_filter = (
            "stereotools=mlev=0.01:slev=1.2:sbal=0:mpan=0,"
            "equalizer=f=2500:width_type=h:width=2000:g=-16,"
            "equalizer=f=120:width_type=h:width=100:g=3"
        )
        cmd_minus = [
            self.audio_engine.ffmpeg, "-y",
            "-i", str(src),
            "-af", minus_filter,
            "-ar", "44100",
            str(out_minus)
        ]
        res_m = subprocess.run(cmd_minus, capture_output=True, text=True)
        if res_m.returncode != 0:
            logger.warning(f"Minusovka ajratishda xatolik: {res_m.stderr}")

        # Vokalni ajratish: O'rtadagi vokal chastotalarini kuchaytirish va chekka asboblarni bosish
        vocal_filter = (
            "pan=mono|c0=0.5*c0+0.5*c1,"
            "highpass=f=120,lowpass=f=9000,"
            "equalizer=f=3000:width_type=h:width=2500:g=6"
        )
        cmd_vocal = [
            self.audio_engine.ffmpeg, "-y",
            "-i", str(src),
            "-af", vocal_filter,
            "-ar", "44100",
            str(out_vocal)
        ]
        res_v = subprocess.run(cmd_vocal, capture_output=True, text=True)
        if res_v.returncode != 0:
            logger.warning(f"Vokal ajratishda xatolik: {res_v.stderr}")

        return {
            "vocals": str(out_vocal),
            "instrumental": str(out_minus)
        }
