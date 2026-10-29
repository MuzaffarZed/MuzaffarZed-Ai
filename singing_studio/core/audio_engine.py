"""
JARVIS AI Singing Studio - Professional Audio Engine
Master Architect: janob Muzaffar uchun professional darajadagi audio ishlovchi dvigatel.
FFmpeg asosidagi to'liq spektrli studiya mikseri, pitch-shift, reverb va mastering vositalari.
"""

import json
import logging
import math
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

logger = logging.getLogger("AudioEngine")
logger.setLevel(logging.INFO)


class AudioEngineError(Exception):
    """Audio dvigatelida yuz beradigan xatoliklar uchun maxsus istisno."""
    pass


class AudioEngine:
    """
    Professional darajadagi audio tahrirlash, vokal va minusovkani miks qilish,
    ovoz effektlari (Reverb, EQ, Delay) va mastering tizimi.
    """

    def __init__(self, ffmpeg_path: Optional[str] = None):
        self.ffmpeg = ffmpeg_path or shutil.which("ffmpeg") or "ffmpeg"
        self.ffprobe = shutil.which("ffprobe") or "ffprobe"
        self._verify_binaries()

    def _verify_binaries(self) -> None:
        """FFmpeg va FFprobe dasturlari mavjudligini tekshiradi."""
        try:
            res = subprocess.run(
                [self.ffmpeg, "-version"],
                capture_output=True,
                text=True,
                check=False
            )
            if res.returncode != 0:
                raise AudioEngineError(f"FFmpeg ishga tushmadi: {res.stderr}")
        except FileNotFoundError:
            raise AudioEngineError(
                "FFmpeg tizimda topilmadi. Iltimos, ffmpeg o'rnatilganligini va PATH ga qo'shilganligini tekshiring."
            )

    def get_audio_info(self, file_path: str | Path) -> Dict[str, Any]:
        """
        Audio fayl haqida to'liq texnik ma'lumotlarni qaytaradi (davomiylik, chastota, kanallar).
        """
        path = Path(file_path).resolve()
        if not path.exists():
            raise AudioEngineError(f"Audio fayl topilmadi: {path}")

        cmd = [
            self.ffprobe,
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            str(path)
        ]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(res.stdout)
            
            duration = float(data.get("format", {}).get("duration", 0.0))
            bitrate = int(data.get("format", {}).get("bit_rate", 0))
            
            # Birinchi audio oqimni topamiz
            sample_rate = 44100
            channels = 2
            codec_name = "unknown"
            for stream in data.get("streams", []):
                if stream.get("codec_type") == "audio":
                    sample_rate = int(stream.get("sample_rate", 44100))
                    channels = int(stream.get("channels", 2))
                    codec_name = stream.get("codec_name", "unknown")
                    break

            return {
                "file_path": str(path),
                "duration": duration,
                "duration_formatted": f"{int(duration // 60):02d}:{int(duration % 60):02d}",
                "sample_rate": sample_rate,
                "channels": channels,
                "codec": codec_name,
                "bitrate": bitrate
            }
        except Exception as e:
            logger.warning(f"ffprobe orqali o'qishda xatolik: {e}. Standart qiymatlar olinmoqda.")
            return {
                "file_path": str(path),
                "duration": 0.0,
                "duration_formatted": "00:00",
                "sample_rate": 44100,
                "channels": 2,
                "codec": "unknown",
                "bitrate": 0
            }

    def convert_format(
        self,
        input_path: str | Path,
        output_path: str | Path,
        sample_rate: int = 44100,
        channels: int = 2,
        bitrate: str = "320k"
    ) -> Path:
        """
        Audio formatini yuqori sifatda WAV yoki MP3 ga o'giradi.
        """
        in_p = Path(input_path).resolve()
        out_p = Path(output_path).resolve()
        out_p.parent.mkdir(parents=True, exist_ok=True)

        if not in_p.exists():
            raise AudioEngineError(f"Kirish audio fayli mavjud emas: {in_p}")

        cmd = [
            self.ffmpeg, "-y",
            "-i", str(in_p),
            "-ar", str(sample_rate),
            "-ac", str(channels)
        ]

        if out_p.suffix.lower() == ".mp3":
            cmd.extend(["-b:a", bitrate, "-c:a", "libmp3lame"])
        elif out_p.suffix.lower() == ".wav":
            cmd.extend(["-c:a", "pcm_s16le"])

        cmd.append(str(out_p))

        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise AudioEngineError(f"Format konvertatsiyasida xatolik: {res.stderr}")

        return out_p

    def shift_pitch(
        self,
        input_path: str | Path,
        output_path: str | Path,
        semitones: float
    ) -> Path:
        """
        Audioning sur'atini (tempo) o'zgartirmasdan, faqat notalarini (pitch) balandlatadi yoki pastlatadi.
        semitones: -12 dan +12 gacha (masalan: +2 semiton baland, -12 bir oktava past).
        """
        in_p = Path(input_path).resolve()
        out_p = Path(output_path).resolve()
        out_p.parent.mkdir(parents=True, exist_ok=True)

        if not in_p.exists():
            raise AudioEngineError(f"Audio topilmadi: {in_p}")

        if abs(semitones) < 0.01:
            # O'zgarish bo'lmasa to'g'ridan-to'g'ri nusxalaymiz
            shutil.copyfile(in_p, out_p)
            return out_p

        # Semiton bo'yicha ko'paytiruvchi omil
        factor = math.pow(2.0, semitones / 12.0)
        tempo_factor = 1.0 / factor

        # Audio ma'lumotidan chastotani olamiz
        info = self.get_audio_info(in_p)
        base_rate = info.get("sample_rate", 44100)
        target_rate = int(round(base_rate * factor))

        # atempo filtri 0.5 dan 2.0 gacha bo'lishi kerak.
        # Agar kerak bo'lsa, bir nechta atempo zanjirini tuzamiz
        atempo_filters = []
        rem_tempo = tempo_factor
        while rem_tempo > 2.0:
            atempo_filters.append("atempo=2.0")
            rem_tempo /= 2.0
        while rem_tempo < 0.5:
            atempo_filters.append("atempo=0.5")
            rem_tempo /= 0.5
        atempo_filters.append(f"atempo={rem_tempo:.5f}")

        atempo_str = ",".join(atempo_filters)
        filter_str = f"asetrate={target_rate},{atempo_str},aresample={base_rate}"

        cmd = [
            self.ffmpeg, "-y",
            "-i", str(in_p),
            "-af", filter_str,
            str(out_p)
        ]

        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise AudioEngineError(f"Pitch shift xatosi: {res.stderr}")

        return out_p

    def apply_vocal_chain(
        self,
        input_path: str | Path,
        output_path: str | Path,
        reverb_level: float = 0.25,
        echo_level: float = 0.0,
        highpass_hz: int = 80,
        presence_boost: float = 2.0
    ) -> Path:
        """
        Vokalga professional studiya effektlarini (reverb, studio echo, EQ) qo'llaydi.
        - highpass_hz: pastki xiralik va shovqinlarni kesish (80Hz)
        - presence_boost: vokal tiniqligini oshirish (+2dB at 3.5kHz)
        - reverb_level: aks-sado darajasi (0.0 dan 1.0 gacha)
        - echo_level: kechikish effekti (0.0 dan 1.0 gacha)
        """
        in_p = Path(input_path).resolve()
        out_p = Path(output_path).resolve()
        out_p.parent.mkdir(parents=True, exist_ok=True)

        filters = []
        
        # 1. Pastki xira shovqinlarni kesish
        if highpass_hz > 20:
            filters.append(f"highpass=f={highpass_hz}")

        # 2. Vokal tiniqligi (Presence)
        if abs(presence_boost) > 0.1:
            filters.append(f"equalizer=f=3500:width_type=h:width=1200:g={presence_boost:.1f}")

        # 3. Studiya Reverberatsiyasi (Aks-sado)
        if reverb_level > 0.05:
            # aecho yordamida chuqur va mayin studiya reverbi
            in_gain = 1.0
            out_gain = min(1.0, 0.7 + reverb_level * 0.3)
            delays = "40|80|120"
            decays = f"{reverb_level * 0.35:.2f}|{reverb_level * 0.25:.2f}|{reverb_level * 0.15:.2f}"
            filters.append(f"aecho={in_gain}:{out_gain}:{delays}:{decays}")

        # 4. Studiya Echo / Delay
        if echo_level > 0.05:
            filters.append(f"aecho=0.8:0.88:350:{echo_level * 0.4:.2f}")

        filter_chain = ",".join(filters) if filters else "anull"

        cmd = [
            self.ffmpeg, "-y",
            "-i", str(in_p),
            "-af", filter_chain,
            str(out_p)
        ]

        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise AudioEngineError(f"Vokal effektlarini qo'llashda xatolik: {res.stderr}")

        return out_p

    def clean_voice_sample(
        self,
        input_path: str | Path,
        output_path: str | Path,
        noise_reduction: bool = True,
        trim_silence: bool = True
    ) -> Path:
        """
        Ovoz namunasini shovqinlardan tozalaydi, jimliklarni qirqadi va model uchun tayyorlaydi.
        """
        in_p = Path(input_path).resolve()
        out_p = Path(output_path).resolve()
        out_p.parent.mkdir(parents=True, exist_ok=True)

        filters = []
        if noise_reduction:
            filters.append("afftdn=nf=-24")
        if trim_silence:
            filters.append("silenceremove=start_periods=1:start_duration=0.1:start_threshold=-50dB:detection=peak")
        filters.append("highpass=f=75,lowpass=f=15000")

        filter_chain = ",".join(filters)

        cmd = [
            self.ffmpeg, "-y",
            "-i", str(in_p),
            "-af", filter_chain,
            "-ar", "44100",
            "-ac", "1",  # Ovoz modeli uchun toza mono audio
            str(out_p)
        ]

        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise AudioEngineError(f"Ovozni tozalashda xatolik: {res.stderr}")

        return out_p

    def mix_song(
        self,
        vocal_path: str | Path,
        minus_path: str | Path,
        output_path: str | Path,
        vocal_vol: float = 1.0,
        minus_vol: float = 1.0,
        apply_mastering: bool = True
    ) -> Path:
        """
        Vokal va Minusovkani professional tarzda sinxronlashtirib aralashtiradi.
        - vocal_vol: Vokal ovoz balandligi ko'paytiruvchisi (masalan: 1.15 = +15%)
        - minus_vol: Fon musiqasi balandligi (masalan: 0.9 = 90%)
        - apply_mastering: EBU R128 (Spotify/Apple Music) balandlik standartida master qilish (-14 LUFS)
        """
        voc_p = Path(vocal_path).resolve()
        min_p = Path(minus_path).resolve()
        out_p = Path(output_path).resolve()
        out_p.parent.mkdir(parents=True, exist_ok=True)

        if not voc_p.exists():
            raise AudioEngineError(f"Vokal fayli topilmadi: {voc_p}")
        if not min_p.exists():
            raise AudioEngineError(f"Minusovka fayli topilmadi: {min_p}")

        # Murakkab filtr zanjiri:
        # 1. Vokal hajmi
        # 2. Minusovka hajmi
        # 3. amix orqali qo'shish
        # 4. loudnorm orqali ovoz balandligini professional studiya darajasiga tekislash
        filter_complex = (
            f"[0:a]volume={vocal_vol:.2f}[v];"
            f"[1:a]volume={minus_vol:.2f}[m];"
            f"[v][m]amix=inputs=2:duration=longest:dropout_transition=2[mixed]"
        )

        if apply_mastering:
            filter_complex += ";[mixed]loudnorm=I=-14:TP=-1.5:LRA=11[out]"
            output_map = "[out]"
        else:
            output_map = "[mixed]"

        cmd = [
            self.ffmpeg, "-y",
            "-i", str(voc_p),
            "-i", str(min_p),
            "-filter_complex", filter_complex,
            "-map", output_map,
            "-b:a", "320k",
            str(out_p)
        ]

        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise AudioEngineError(f"Qo'shiqni miks qilishda xatolik: {res.stderr}")

        return out_p

    def generate_test_audio(
        self,
        output_path: str | Path,
        duration: float = 3.0,
        frequency: int = 440,
        sample_rate: int = 44100
    ) -> Path:
        """
        Sinovlar va kalibrlash uchun toza sinusoial audio yaratadi.
        """
        out_p = Path(output_path).resolve()
        out_p.parent.mkdir(parents=True, exist_ok=True)

        cmd = [
            self.ffmpeg, "-y",
            "-f", "lavfi",
            "-i", f"sine=frequency={frequency}:duration={duration}",
            "-ar", str(sample_rate),
            str(out_p)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise AudioEngineError(f"Sinov audio yaratishda xatolik: {res.stderr}")
        return out_p
