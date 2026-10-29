"""
JARVIS AI Singing Studio - Voice Dataset & Model Manager
Master Architect: janob Muzaffar uchun shaxsiy ovoz namunalari va AI modellarini boshqarish moduli.
"""

import json
import logging
import os
import shutil
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional

from .audio_engine import AudioEngine

logger = logging.getLogger("VoiceManager")


class VoiceManager:
    """
    Foydalanuvchining ovoz namunalarini to'plash, tozalash, tahlil qilish,
    Colab uchun dataset arxivini tayyorlash va o'qitilgan RVC modellarini saqlash.
    """

    def __init__(self, data_root: Optional[str | Path] = None):
        self.root = Path(data_root or Path(__file__).resolve().parent.parent / "data")
        self.voices_dir = self.root / "voices"
        self.cleaned_dir = self.root / "voices" / "cleaned"
        self.models_dir = self.root / "models"
        self.output_dir = self.root / "output"

        # Barcha kerakli papkalarni yaratamiz
        self.voices_dir.mkdir(parents=True, exist_ok=True)
        self.cleaned_dir.mkdir(parents=True, exist_ok=True)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.audio_engine = AudioEngine()

    def add_voice_sample(self, file_path: str | Path, custom_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Yangi ovoz namunasini qabul qiladi, tozalaydi va saqlaydi.
        """
        src = Path(file_path).resolve()
        if not src.exists():
            raise FileNotFoundError(f"Ovoz fayli topilmadi: {src}")

        name = custom_name or src.name
        # Formatni WAV ga keltiramiz
        target_raw = self.voices_dir / f"raw_{name}"
        target_clean = self.cleaned_dir / f"clean_{Path(name).stem}.wav"

        shutil.copyfile(src, target_raw)

        # Ovozni shovqindan tozalash va tayyorlash
        self.audio_engine.clean_voice_sample(target_raw, target_clean)

        info = self.audio_engine.get_audio_info(target_clean)
        return {
            "filename": target_clean.name,
            "raw_filename": target_raw.name,
            "duration": info["duration"],
            "duration_formatted": info["duration_formatted"],
            "clean_path": str(target_clean)
        }

    def list_voice_samples(self) -> List[Dict[str, Any]]:
        """
        Mavjud tozalangan ovoz namunalarining ro'yxati va umumiy davomiyligini qaytaradi.
        """
        samples = []
        for file in sorted(self.cleaned_dir.glob("*.wav")):
            info = self.audio_engine.get_audio_info(file)
            samples.append({
                "filename": file.name,
                "size_bytes": file.stat().st_size,
                "duration": info["duration"],
                "duration_formatted": info["duration_formatted"],
                "path": str(file)
            })
        return samples

    def get_dataset_statistics(self) -> Dict[str, Any]:
        """
        Dataset haqida umumiy xulosa (nechta audio, umumiy davomiylik, model uchun tayyorlik darajasi).
        """
        samples = self.list_voice_samples()
        total_seconds = sum(s["duration"] for s in samples)
        count = len(samples)

        # RVC modeli uchun kamida 3-5 daqiqa (180 - 300 soniya) yaxshi natija beradi
        recommended_seconds = 300.0
        readiness_pct = min(100, int((total_seconds / recommended_seconds) * 100))

        status_text = "Boshlang'ich (Yana ovoz yozing)"
        if readiness_pct >= 100:
            status_text = "A'lo darajada tayyor (100%)"
        elif readiness_pct >= 60:
            status_text = "Yetarli (Model yaxshi o'rganadi)"
        elif readiness_pct >= 30:
            status_text = "O'rtacha (Yana biroz yozish tavsiya etiladi)"

        return {
            "sample_count": count,
            "total_seconds": round(total_seconds, 2),
            "total_formatted": f"{int(total_seconds // 60):02d}:{int(total_seconds % 60):02d}",
            "readiness_percent": readiness_pct,
            "readiness_status": status_text
        }

    def package_dataset_zip(self, output_zip_path: Optional[str | Path] = None) -> Path:
        """
        Google Colab yoki tashqi GPU trenirovkasi uchun barcha tozalangan audio namunalarni
        bitta 'muzaffar_voice_dataset.zip' fayliga arxivlaydi.
        """
        out_zip = Path(output_zip_path or self.root / "muzaffar_voice_dataset.zip").resolve()
        samples = list(self.cleaned_dir.glob("*.wav"))
        if not samples:
            raise ValueError("Arxivlash uchun tozalangan ovoz namunalari mavjud emas!")

        with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
            for s in samples:
                zipf.write(s, arcname=f"dataset/{s.name}")

        return out_zip

    def add_model(self, model_file: str | Path, index_file: Optional[str | Path] = None, model_name: Optional[str] = None) -> Dict[str, Any]:
        """
        O'qitilgan RVC modelini (.pth va ixtiyoriy .index) tizimga qo'shadi.
        """
        mod_p = Path(model_file).resolve()
        if not mod_p.exists():
            raise FileNotFoundError(f"Model fayli topilmadi: {mod_p}")

        m_name = model_name or mod_p.stem
        target_model = self.models_dir / f"{m_name}.pth"
        shutil.copyfile(mod_p, target_model)

        target_index = None
        if index_file and Path(index_file).exists():
            target_index = self.models_dir / f"{m_name}.index"
            shutil.copyfile(Path(index_file), target_index)

        return {
            "name": m_name,
            "model_path": str(target_model),
            "index_path": str(target_index) if target_index else None
        }

    def list_models(self) -> List[Dict[str, Any]]:
        """
        Mavjud barcha AI ovoz modellarini ro'yxatini qaytaradi.
        """
        models = []
        for pth in sorted(self.models_dir.glob("*.pth")):
            idx = pth.with_suffix(".index")
            models.append({
                "name": pth.stem,
                "model_path": str(pth),
                "index_path": str(idx) if idx.exists() else None,
                "size_mb": round(pth.stat().st_size / (1024 * 1024), 2)
            })

        # Agar hali tayyor model yuklanmagan bo'lsa, "Janob Muzaffar (Asosiy Vokal)" virtual profilini ko'rsatamiz
        if not models:
            models.append({
                "name": "Muzaffar (Standart Vokal Profili)",
                "model_path": "default",
                "index_path": None,
                "size_mb": 0.0,
                "is_default": True
            })

        return models

    def delete_sample(self, filename: str) -> bool:
        """Ovoz namunasini o'chiradi."""
        clean_target = self.cleaned_dir / filename
        raw_target = self.voices_dir / f"raw_{filename}"
        deleted = False
        if clean_target.exists():
            clean_target.unlink()
            deleted = True
        if raw_target.exists():
            raw_target.unlink()
            deleted = True
        return deleted
