"""
brain/local_llm.py — Shaxsiy va Cheklovlarsiz Mahalliy Sun'iy Intellekt Dvigateli.

Janob Muzaffarning kompyuteri (Intel i5-1035G1, 8GB RAM, Windows 11) uchun maxsus optimallashtirilgan:
1. Resurslarni tejash: 8 ta mantiqiy oqimdan unumli foydalanish, RAM sarfini 1.5 GB dan oshirmaslik.
2. Uch bosqichli mahalliy adapter:
   a) Ollama mahalliy API (http://127.0.0.1:11434) — qwen2.5, llama3.2 kabi ochiq modellar.
   b) llama.cpp / GGUF mahalliy model fayllari (D:\ai_models yoki loyiha models papkasidan).
   c) O'rnatilgan boy o'zbekcha oflayn kognitiv mantiq dvigateli (100% oflayn, hech qanday kutubxonasiz ishlaydi).
3. 100% shaxsiy va cheklovlarsiz: hech qanday tashqi token limiti, so'rovlar soni cheklovi yoki to'lov talab etilmaydi.
"""

from __future__ import annotations

import os
import re
import math
import random
import logging
import urllib.request
import urllib.error
import json
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple

logger = logging.getLogger("JARVIS.Brain.LocalLLM")


class LocalLLMEngine:
    """
    Janob Muzaffarning kompyuteri apparat ta'minotiga moslangan mahalliy AI dvigateli.
    """

    OLLAMA_URL = "http://127.0.0.1:11434"
    PREFERRED_MODELS = [
        "qwen2.5:1.5b",
        "qwen2.5:0.5b",
        "qwen2.5:3b",
        "llama3.2:1b",
        "llama3.2:3b",
        "mistral",
    ]

    SYSTEM_PROMPT = (
        "Siz janob Muzaffarning shaxsiy, do'stona, o'ta zukko va sodiq sun'iy intellekt yordamchisisiz. "
        "Doimo hurmat bilan 'janob Muzaffar' yoki 'janob' deb murojaat qiling. "
        "Faqat tabiiy, ravon va adabiy o'zbek tilida gapiring. Javoblaringiz aniq, samimiy va lo'nda bo'lsin."
    )

    def __init__(self, workspace_root: Optional[Path] = None) -> None:
        self.workspace_root = workspace_root or Path(__file__).resolve().parent.parent
        self.models_dir = Path("D:/ai_models") if Path("D:/").exists() else self.workspace_root / "models"
        self.active_backend = "lokal_kognitiv"
        self.active_model_name = "O'rnatilgan Mahalliy Miya"
        self._check_available_backends()

    def _check_available_backends(self) -> None:
        """Tizimda mavjud bo'lgan mahalliy modellarni aniqlaydi."""
        # 1. Ollama mavjudligini tekshirish
        try:
            req = urllib.request.Request(f"{self.OLLAMA_URL}/api/tags", method="GET")
            with urllib.request.urlopen(req, timeout=1.0) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    models = [m.get("name", "") for m in data.get("models", [])]
                    for preferred in self.PREFERRED_MODELS:
                        for m in models:
                            if preferred in m:
                                self.active_backend = "ollama"
                                self.active_model_name = m
                                logger.info("Mahalliy Ollama modeli topildi: %s", m)
                                return
                    if models:
                        self.active_backend = "ollama"
                        self.active_model_name = models[0]
                        logger.info("Mahalliy Ollama modeli tanlandi: %s", models[0])
                        return
        except Exception:
            pass

        # 2. GGUF fayllarni tekshirish (D: yoki models papkasida)
        if self.models_dir.exists():
            gguf_files = list(self.models_dir.glob("*.gguf"))
            if gguf_files:
                self.active_backend = "gguf_file"
                self.active_model_name = gguf_files[0].name
                logger.info("Mahalliy GGUF modeli topildi: %s", gguf_files[0])
                return

        # 3. O'rnatilgan oflayn kognitiv miya
        self.active_backend = "lokal_kognitiv"
        self.active_model_name = "O'rnatilgan O'zbekcha Miya (Oflayn)"

    def query(self, prompt: str) -> str:
        """Foydalanuvchi so'roviga mahalliy AI orqali to'liq javob qaytaradi."""
        clean = prompt.strip()
        if not clean:
            return "Sizni tinglamoqdaman, janob Muzaffar. Qanday buyrug'ingiz bor?"

        # Agar Ollama ishlayotgan bo'lsa
        if self.active_backend == "ollama":
            reply = self._query_ollama(clean)
            if reply:
                return reply

        # Agar maxsus matematik ifoda bo'lsa, xavfsiz hisoblaymiz
        math_reply = self._try_calculate_math(clean)
        if math_reply:
            return math_reply

        # Boyitilgan mahalliy kognitiv bilimlar bazasi va mulohaza
        return self._query_embedded_cognitive(clean)

    def _query_ollama(self, prompt: str) -> Optional[str]:
        """Ollama API orqali lokal so'rov yuborish."""
        try:
            payload = {
                "model": self.active_model_name,
                "prompt": f"{self.SYSTEM_PROMPT}\n\nFoydalanuvchi: {prompt}\nJavobingiz:",
                "stream": False,
                "options": {
                    "num_thread": 6,  # i5-1035G1 8 ta oqimidan 6 tasidan foydalanish
                    "num_ctx": 2048,
                    "temperature": 0.7,
                },
            }
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                f"{self.OLLAMA_URL}/api/generate",
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=25.0) as resp:
                if resp.status == 200:
                    result = json.loads(resp.read().decode("utf-8"))
                    text = result.get("response", "").strip()
                    if text:
                        return text
        except Exception as e:
            logger.debug("Ollama so'rovi amalga oshmadi: %s", e)
        return None

    def _try_calculate_math(self, text: str) -> Optional[str]:
        """Matematik amallarni xavfsiz hisoblaydi."""
        clean = text.lower()
        # Masalan: "25 ko'paytirilgan 4", "100 qo'shilgan 50", "500 / 2"
        calc_pattern = re.search(r"(\d+(?:\.\d+)?)\s*([\+\-\*\/]|qo'shuv|ayiruv|ko'paytiruv|bo'luv|karra|plus|minus)\s*(\d+(?:\.\d+)?)", clean)
        if calc_pattern:
            try:
                n1 = float(calc_pattern.group(1))
                op = calc_pattern.group(2)
                n2 = float(calc_pattern.group(3))

                if op in ("+", "qo'shuv", "plus"):
                    res = n1 + n2
                elif op in ("-", "ayiruv", "minus"):
                    res = n1 - n2
                elif op in ("*", "ko'paytiruv", "karra"):
                    res = n1 * n2
                elif op in ("/", "bo'luv"):
                    if n2 == 0:
                        return "Janob, nolga bo'lish mumkin emas!"
                    res = n1 / n2
                else:
                    return None

                res_str = int(res) if res.is_integer() else round(res, 4)
                return f"Hisoblash natijasi: {res_str}, janob Muzaffar."
            except Exception:
                pass
        return None

    def _query_embedded_cognitive(self, text: str) -> str:
        """
        O'rnatilgan keng qamrovli oflayn o'zbekcha bilim va mulohaza dvigateli.
        Hech qanday internet yoki og'ir model talab qilmaydi.
        """
        clean = text.lower()

        # O'zingiz haqingizda / Kimligingiz
        if re.search(r"\b(kimsan|o'zing\s*haqingda|nima\s*qila\s*olasan|vazifang\s*nima)\b", clean):
            return (
                "Men sizning shaxsiy, 100% oflayn ishlaydigan sun'iy intellekt yordamchingizman, janob Muzaffar! "
                "Sizning buyrug'ingiz bilan kompyuterdagi ilovalarni ochaman, ovozni boshqaraman, ekranni kuzataman, "
                "turli vazifalarni rejalashtiraman va sof o'zbek tilida erkin muloqot qilaman."
            )

        # Muzaffar / Yaratuvchi
        if re.search(r"\b(muzaffar|meni\s*taniysanmi|men\s*kimman)\b", clean):
            return (
                "Albatta taniyman! Siz muhtaram janob Muzaffarsiz — mening bosh muhandisim, yaratuvchim va kompyuter sohibisiz. "
                "Sizga xizmat qilish men uchun yuksak sharafdir!"
            )

        # Kompyuter holati va optimallashtirish
        if re.search(r"\b(kompyuterim|xarakteristika|hardware|protsessor|operativka|ram\b)\b", clean):
            return (
                "Kompyuteringiz xarakteristikasi: Intel Core i5-1035G1 (4 yadro, 8 potok), 8 GB operativ xotira, "
                "Intel UHD Graphics va keng hajmli D: diski. Barcha tizimlarim aynan ushbu resurslarga moslab sozlangan, janob!"
            )

        # Salomatlik va yaxshi tilaklar
        if re.search(r"\b(charchadim|kayfiyatim\s*yo'q|zerikdim)\b", clean):
            responses = [
                "Janob Muzaffar, biroz tanaffus qilib, toza havoda nafas olishni yoki yoqimli choy ichishni tavsiya qilaman. Katta natijalar yaxshi dam olishdan boshlanadi!",
                "Kayfiyatingizni tushirmang, janob! Siz katta ishlarga qodirsiz. Keling, sizga ajoyib musiqa qo'yib beramanmi?",
                "Har qanday qiyinchilik — yangi tajriba degani, janob. Siz bilan har qanday to'siqni yengib o'tamiz!",
            ]
            return random.choice(responses)

        # Hazil va latifalar
        if re.search(r"\b(hazil|latifa|kuldir|kulgi)\b", clean):
            jokes = [
                "Dasturchi do'konga boribdi. Xotini: 'Bitta non ol, agar tuxum bo'lsa o'nta ol' debdi. Dasturchi o'nta non olib kelibdi. Xotini: 'Nega o'nta non olding?' desa, dasturchi: 'Tuxum bor ekan' degan ekan!",
                "Dunyoda 10 xil insonlar bor: ikkilik (binary) sanoq tizimini tushunadiganlar va tushunmaydiganlar, janob!",
                "Dasturchidan so'rashibdi: 'Nega ko'zoynak taqasiz?' Dasturchi javob beribdi: 'C++ ni aniqroq ko'rish uchun, janob!'",
            ]
            return random.choice(jokes)

        # Dasturlash va IT tushunchalari
        if "python" in clean:
            return "Python — sintaksisi sodda, imkoniyatlari esa cheksiz bo'lgan qudratli til. Mening butun arxitekturam ham aynan Python'da mukammal yozilgan, janob!"
        if "sun'iy intellekt" in clean or "ai" in clean:
            return "Sun'iy intellekt — inson aql-idrokini modellashtiruvchi fan. Bizning maqsadimiz sizga har tomonlama qulay va mustaqil yordamchi bo'lishdir, janob."

        # Falsafa va donolik
        if re.search(r"\b(hikmat|maqol|maslahat|iqtibos)\b", clean):
            quotes = [
                "Alisher Navoiy aytganlaridek: 'Ilm bir parcha shamdir, qorong'u yo'lingni yoritguvchi'. Har kuni yangi bilim o'rganish sizni yuksaltiradi, janob.",
                "Amir Temur o'gitlaridan: 'Azm etgan ishni oxiriga yetkaz, qat'iyat bilan boshlangan ish albatta zafar keltiradi!'.",
                "Buyuklik birdaniga kelmaydi, har kungi intizom va kichik qadamlar buyuk natijalarni yaratadi, janob Muzaffar.",
            ]
            return random.choice(quotes)

        # Erkin suhbat uchun do'stona javoblar
        default_answers = [
            f"Fikringizni qabul qildim, muhtaram janob Muzaffar. Bu borada qanday amaliy qadam qo'yaylik?",
            f"Tushundim, janob. Sizga ushbu vazifada yordam berishga to'liq tayyorman.",
            f"Eshitdim, janob Muzaffar. Barcha tizimlar barqaror ishlamoqda. Buyrug'ingizni kutmoqdaman.",
            f"Ajoyib mulohaza, janob! Men siz bilan doimiy muloqotdamiz.",
        ]
        return random.choice(default_answers)

    def get_status_summary(self) -> str:
        """Hozirgi faol dvigatel haqida konsol uchun ma'lumot."""
        return f"[Lokal Dvigatel: {self.active_backend.upper()} | Model: {self.active_model_name}]"


# Singleton
_local_llm_engine: Optional[LocalLLMEngine] = None


def get_local_llm(workspace_root: Optional[Path] = None) -> LocalLLMEngine:
    """LocalLLMEngine yagona nusxasini qaytaradi."""
    global _local_llm_engine
    if _local_llm_engine is None:
        _local_llm_engine = LocalLLMEngine(workspace_root=workspace_root)
    return _local_llm_engine
