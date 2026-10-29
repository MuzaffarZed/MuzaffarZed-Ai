"""
Configuration Manager for Brightness Sync.
Foydalanuvchi sozlamalarini boshqarish (config.json).
"""

import json
import os
from typing import Any, Dict

DEFAULT_CONFIG: Dict[str, Any] = {
    "sync_enabled": True,
    "interval": 0.5,  # Zaxira tekshiruv intervali (soniya)
    "min_change": 1,
    "mode": "mirror",  # "mirror" (1:1), "offset", "scale"
    "offset": 0,  # e.g. +5 or -10
    "scale": 1.0,  # e.g. 1.0, 1.1
    "min_brightness": 0,  # 1:1 to'liq diapazon (0% gacha)
    "max_brightness": 100,
    "remap_range": False,  # 1:1 to'g'ridan-to'g'ri moslash
    "deep_dimming": True,  # Chuqur qorong'ulik (past darajada noutbuk kabi to'liq xiralashish)
    "smooth_transition": False,
    "smooth_step": 4,
    "smooth_delay": 0.02,
    "hotkeys_enabled": True,
}


class ConfigManager:
    """Sozlamalarni yuklash, saqlash va boshqarish klassi."""

    def __init__(self, config_path: str):
        self.config_path = config_path
        self._data: Dict[str, Any] = dict(DEFAULT_CONFIG)
        self.load()

    def load(self) -> Dict[str, Any]:
        """Fayldan sozlamalarni yuklaydi, yo'q bo'lsa yangi yaratadi."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    self._data = {**DEFAULT_CONFIG, **loaded}
            except Exception:
                self._data = dict(DEFAULT_CONFIG)
        else:
            self.save()
        return self._data

    def save(self):
        """Sozlamalarni config.json fayliga saqlaydi."""
        try:
            os.makedirs(os.path.dirname(os.path.abspath(self.config_path)), exist_ok=True)
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=4, ensure_ascii=False)
        except Exception:
            pass

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def set(self, key: str, value: Any):
        self._data[key] = value
        self.save()

    def calculate_external(self, laptop_brightness: int) -> int:
        """Noutbuk yorug'ligi asosida tashqi monitor uchun mos yorug'likni hisoblaydi."""
        target = float(laptop_brightness)
        min_b = max(0, min(100, int(self.get("min_brightness", 0))))
        max_b = max(min_b, min(100, int(self.get("max_brightness", 100))))
        remap = bool(self.get("remap_range", False))

        if remap and max_b > min_b:
            normalized = max(0.0, min(100.0, target)) / 100.0
            remapped = min_b + normalized * (max_b - min_b)
            return int(round(remapped))

        mode = self.get("mode", "mirror")
        if mode == "offset":
            target += float(self.get("offset", 0))
        elif mode == "scale":
            target = target * float(self.get("scale", 1.0)) + float(self.get("offset", 0))

        final_val = int(round(target))
        return max(min_b, min(max_b, final_val))

    def calculate_contrast(self, laptop_brightness: int) -> int:
        """
        Chuqur qorong'ulik rejimi (Deep Dimming).
        Noutbuk 40% dan pastga tushganda, tashqi monitor ham noutbuk kabi
        chuqur va qorong'i bo'lishi uchun kontrastni 50 dan 10 gacha yumshoq pasaytiradi.
        """
        if not bool(self.get("deep_dimming", True)):
            return 50

        if laptop_brightness >= 40:
            return 50

        # laptop_brightness 0..40 oralig'ida: contrast 10..50
        ratio = max(0.0, min(40.0, float(laptop_brightness))) / 40.0
        contrast = 10.0 + ratio * 40.0
        return int(round(contrast))
