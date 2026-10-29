"""
JARVIS-Core — Screen Analyzer (Vision Subsystem)
Hybrid Vision Architecture:
- Multimodal perception via Google Gemini 2.5 Flash / 2.0 Flash
- Windows OS UI context fusion (active foreground window, window titles, and topologies via Win32)
- High-precision coordinate detection [0..1000] for mouse automation
"""

from __future__ import annotations
import os
import sys
import re
import json
import logging
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Union

try:
    from PIL import Image
except ImportError:
    Image = None

try:
    import win32gui
    import win32process
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

try:
    import pygetwindow as gw
    PYGETWINDOW_AVAILABLE = True
except ImportError:
    PYGETWINDOW_AVAILABLE = False

try:
    from google import genai
    from google.genai import types
    GEMINI_SDK_AVAILABLE = True
except ImportError:
    GEMINI_SDK_AVAILABLE = False

logger = logging.getLogger("JARVIS.Vision.ScreenAnalyzer")


@dataclass
class UIElementLocation:
    found: bool
    target: str
    box_2d: List[int] = field(default_factory=lambda: [0, 0, 0, 0])  # [ymin, xmin, ymax, xmax] in 0..1000
    point: List[int] = field(default_factory=lambda: [0, 0])          # [y, x] in 0..1000
    confidence: float = 0.0
    description: str = ""


class ScreenAnalyzer:
    """
    Hybrid Multimodal Visual Reasoning Engine.
    Combines direct pixel vision with native Windows OS window metadata.
    """

    SYSTEM_PROMPT = """Siz Windows 10/11 ish stoli va ilovalari ekranini tahlil qiluvchi yuqori aniqlikdagi J.A.R.V.I.S vizual tahlilchisisiz.
Sizga skrinshot bilan birgalikda tizimdagi ochiq oynalar va ularning holati taqdim etiladi.
Vazifangiz:
1. Ekrandagi oynalar, dasturlar, tugmalar, ikonalar, qidiruv maydonlari va matnlarni aniq ko'rish.
2. Foydalanuvchi so'ragan elementning koordinatalarini 0 dan 1000 gacha bo'lgan normallashtirilgan shkalada (box_2d: [ymin, xmin, ymax, xmax] yoki point: [y, x]) aniqlash.
3. Javoblarni hurmat bilan, lutf ila o'zbek tilida bayon qilish.
"""

    def __init__(self, api_key: Optional[str] = None) -> None:
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
        self.test_mode = os.getenv("JARVIS_TEST_MODE", "0") == "1"
        self._client: Optional[genai.Client] = None

        if self.api_key and GEMINI_SDK_AVAILABLE and not self.test_mode:
            try:
                self._client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.warning("Gemini Client initialization failed in ScreenAnalyzer: %s", e)

    # -------------------------------------------------------------------------
    # Hybrid Vision: Windows OS Window Topology Context
    # -------------------------------------------------------------------------
    def get_window_context(self) -> str:
        """
        Gathers list of visible desktop windows and the active foreground window.
        Returns formatted context string to guide the multimodal model.
        """
        if self.test_mode or sys.platform != "win32":
            return "Faol oyna: Visual Studio Code, Ochiq oynalar: Google Chrome, Bloknot"

        windows_info = []
        active_title = ""

        try:
            if WIN32_AVAILABLE:
                fg_hwnd = win32gui.GetForegroundWindow()
                if fg_hwnd:
                    active_title = win32gui.GetWindowText(fg_hwnd).strip()

                def _enum_cb(hwnd, _):
                    if win32gui.IsWindowVisible(hwnd):
                        txt = win32gui.GetWindowText(hwnd).strip()
                        if txt and txt not in ("Default IME", "MSCTFIME UI", "Program Manager"):
                            rect = win32gui.GetWindowRect(hwnd)
                            w = rect[2] - rect[0]
                            h = rect[3] - rect[1]
                            if w > 100 and h > 100:
                                is_active = " [FAOL]" if hwnd == fg_hwnd else ""
                                windows_info.append(f"- \"{txt}\"{is_active} (O'lcham: {w}x{h})")
                    return True

                win32gui.EnumWindows(_enum_cb, None)

            elif PYGETWINDOW_AVAILABLE:
                for w in gw.getAllWindows():
                    if w.visible and w.title.strip() and w.width > 100 and w.height > 100:
                        is_active = " [FAOL]" if w.isActive else ""
                        windows_info.append(f"- \"{w.title}\"{is_active}")
        except Exception as e:
            logger.debug("Oynalar holatini olishda xatolik: %s", e)

        if not windows_info:
            return "Oynalar haqida ma'lumot mavjud emas."

        summary = "Joriy ekrandagi ochiq dasturlar va oynalar:\n" + "\n".join(windows_info[:10])
        return summary

    # -------------------------------------------------------------------------
    # Screen Description & QA
    # -------------------------------------------------------------------------
    def describe_screen(self, image: Union["Image.Image", bytes, str], custom_query: Optional[str] = None) -> str:
        """
        Provides a concise, intelligent Uzbek summary of the current desktop/window visual state.
        Leverages hybrid visual + window metadata context.
        """
        if self.test_mode:
            return "Ekranda dasturlar faol holatda ko'rinmoqda, janob."

        if not self._client:
            return "Vizual tahlil uchun Gemini API kaliti sozlanmagan, janob."

        pil_img = self._ensure_pil_image(image)
        if pil_img is None:
            return "Ekran tasvirini yuklashda xatolik yuz berdi, janob."

        window_ctx = self.get_window_context()
        base_prompt = custom_query or (
            "Ushbu skrinshotga va tizim oynalari kontekstiga qarang. Ekranda qaysi dasturlar ochiq, "
            "nima ish bajarilayotganini janob Muzaffarga 2-3 ta lo'nda va chiroyli o'zbekcha gap bilan aytib bering."
        )
        full_prompt = f"{window_ctx}\n\nTopshiriq: {base_prompt}"

        models = ["gemini-2.5-flash", "gemini-2.0-flash"]
        for model in models:
            try:
                response = self._client.models.generate_content(
                    model=model,
                    contents=[pil_img, full_prompt],
                    config=types.GenerateContentConfig(
                        system_instruction=self.SYSTEM_PROMPT,
                        temperature=0.3,
                        max_output_tokens=300,
                    ),
                )
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                logger.debug("Model %s failed on describe_screen: %s", model, e)

        return "Ekran tasvirini tahlil qilishda tarmoq xatoligi yuz berdi, janob."

    # -------------------------------------------------------------------------
    # Target UI Element Localization
    # -------------------------------------------------------------------------
    def locate_element(self, image: Union["Image.Image", bytes, str], target_description: str) -> UIElementLocation:
        """
        Pinpoints the bounding box and center coordinate of target GUI element.
        Returns normalized coordinates in [0..1000] scale.
        """
        if self.test_mode:
            return UIElementLocation(
                found=True,
                target=target_description,
                box_2d=[100, 100, 200, 300],
                point=[150, 200],
                confidence=0.95,
                description=f"Sinov rejimida aniqlangan element: {target_description}",
            )

        if not self._client:
            return UIElementLocation(
                found=False,
                target=target_description,
                description="Gemini API kaliti mavjud emas.",
            )

        pil_img = self._ensure_pil_image(image)
        if pil_img is None:
            return UIElementLocation(
                found=False,
                target=target_description,
                description="Tasvirni o'qib bo'lmadi.",
            )

        window_ctx = self.get_window_context()
        prompt = f"""{window_ctx}

Skrinshotdagi quyidagi elementni toping: "{target_description}".
Element koordinatalarini 0 dan 1000 gacha bo'lgan normallashtirilgan shkalada (0 - eng yuqori/chap, 1000 - eng quyi/o'ng) aniqlang.
Qat'iy ravishda faqat quyidagi JSON formatida javob bering, boshqa hech qanday so'z yoki belgi qo'shmang:
{{
  "found": true,
  "target": "{target_description}",
  "box_2d": [ymin, xmin, ymax, xmax],
  "point": [y, x],
  "confidence": 0.95,
  "description": "element haqida qisqacha ma'lumot"
}}
Agar element ekranda umuman mavjud bo'lmasa:
{{
  "found": false,
  "target": "{target_description}",
  "box_2d": [0, 0, 0, 0],
  "point": [0, 0],
  "confidence": 0.0,
  "description": "Element topilmadi"
}}
"""
        models = ["gemini-2.5-flash", "gemini-2.0-flash"]
        for model in models:
            try:
                response = self._client.models.generate_content(
                    model=model,
                    contents=[pil_img, prompt],
                    config=types.GenerateContentConfig(
                        system_instruction=self.SYSTEM_PROMPT,
                        temperature=0.1,
                        response_mime_type="application/json",
                    ),
                )
                if response and response.text:
                    parsed = self._parse_json_response(response.text)
                    if parsed:
                        return UIElementLocation(
                            found=bool(parsed.get("found", False)),
                            target=str(parsed.get("target", target_description)),
                            box_2d=list(parsed.get("box_2d", [0, 0, 0, 0])),
                            point=list(parsed.get("point", [0, 0])),
                            confidence=float(parsed.get("confidence", 0.0)),
                            description=str(parsed.get("description", "")),
                        )
            except Exception as e:
                logger.debug("Model %s failed on locate_element: %s", model, e)

        return UIElementLocation(
            found=False,
            target=target_description,
            description="Elementni qidirishda xatolik yuz berdi.",
        )

    def _ensure_pil_image(self, image: Union["Image.Image", bytes, str]) -> Optional["Image.Image"]:
        """Converts diverse image formats (path, bytes, PIL) into a valid PIL Image."""
        if not Image:
            return None
        try:
            if isinstance(image, Image.Image):
                return image
            elif isinstance(image, (str, os.PathLike)):
                return Image.open(str(image))
            elif isinstance(image, (bytes, bytearray)):
                import io
                return Image.open(io.BytesIO(image))
        except Exception as e:
            logger.error("Tasvirni konvertatsiya qilishda xatolik: %s", e)
        return None

    def _parse_json_response(self, text: str) -> Optional[Dict[str, Any]]:
        """Parses clean or markdown-wrapped JSON response."""
        try:
            cleaned = text.strip()
            if cleaned.startswith("```"):
                cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
                cleaned = re.sub(r"\s*```$", "", cleaned)
            return json.loads(cleaned)
        except Exception as e:
            logger.warning("JSON parse error: %s from text: %s", e, text[:100])
            return None
