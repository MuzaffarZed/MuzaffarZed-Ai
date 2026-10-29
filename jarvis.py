"""
jarvis.py — Janob Muzaffarning Shaxsiy Ovozli AI Yordamchisi (Oflayn & Cheklovlarsiz).

Ushbu skript to'liq ovozli muloqot rejimini ishga tushiradi:
- Intel i5-1035G1 va 8GB RAM ga moslangan yengil va tezkor hisoblash.
- Sof va aksentsiz O'zbek tili neyron ovozi (uz-UZ-MadinaNeural / uz-UZ-SardorNeural).
- Xotirada (RAM) audio oqimi va shovqinga chidamli nutqni tanish.
- Oflayn mahalliy kognitiv miya va Windows tizimini boshqarish.
"""

from __future__ import annotations

import sys
import os
from pathlib import Path

# Windows konsolida UTF-8 ni to'g'ri ko'rsatish
if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        ctypes.windll.kernel32.SetConsoleCP(65001)
    except Exception:
        pass
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

# Loyiha ildiz papkasini sys.path ga qo'shish
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from main import JarvisCore


def run_jarvis_voice() -> None:
    """Ovozli yordamchini ishga tushiradi."""
    print("=" * 70)
    print("   J.A.R.V.I.S — JANOB MUZAFFARNING SHAXSIY OVOZLI YORDAMCHISI")
    print("   100% O'zbekcha • Sof Aksentsiz Neyron Ovoz • Cheklovlarsiz Miya")
    print("=" * 70)
    
    app = JarvisCore()
    app.run_voice_loop()


if __name__ == "__main__":
    run_jarvis_voice()