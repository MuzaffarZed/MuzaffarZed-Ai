"""
JARVIS-Core — Gemini Cognitive Brain (Production-Ready)
Features:
- Automated .env management via python-dotenv with interactive first-run onboarding
- Instant API Health-Check ping (Online, Invalid Key, Quota Exceeded, Offline)
- Two-tier execution: 100% resilient local fallback logic for OS/GUI actions even if API is offline
- Google Gemini 2.5 Flash / 2.0 Flash multimodal integration with failover
"""

from __future__ import annotations
import os
import re
import random
import logging
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, Dict, Any, List, Union

try:
    from dotenv import load_dotenv, set_key
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

try:
    from google import genai
    from google.genai import types
    from google.genai.errors import APIError
    GEMINI_SDK_AVAILABLE = True
except ImportError:
    GEMINI_SDK_AVAILABLE = False
    APIError = Exception

from .local_llm import get_local_llm, LocalLLMEngine

logger = logging.getLogger("JARVIS.Brain.GeminiBrain")


class IntentCategory(Enum):
    APP_LAUNCH = auto()
    VOLUME = auto()
    SCREENSHOT = auto()
    MEDIA = auto()
    TELEMETRY = auto()
    WEB_SEARCH = auto()
    TIME_DATE = auto()
    CLIPBOARD = auto()
    SHUTDOWN_TIMER = auto()
    EXIT = auto()
    CONVERSATION = auto()
    VOICE_MANAGE = auto()
    # Multimodal Vision & GUI Automations
    VISION_DESCRIBE = auto()
    VISION_LOCATE = auto()
    GUI_CLICK = auto()
    GUI_DOUBLE_CLICK = auto()
    GUI_MOVE = auto()
    GUI_TYPE = auto()
    GUI_HOTKEY = auto()
    GUI_SCROLL = auto()
    WINDOW_MANAGE = auto()


@dataclass
class BrainResult:
    intent: IntentCategory
    action_type: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    reply_text: str = ""
    confidence: float = 1.0
    source: str = "lokal"  # "lokal", "gemini", or "lokal (fallback)"


class GeminiBrain:
    """
    Intelligent core of JARVIS:
    - Zero-latency Uzbek regex intent extraction
    - Two-tier fail-safe execution (Local system logic operates independently of network)
    - Dynamic .env configuration & API Health Monitoring
    - Google Gemini 2.5 Flash cognitive and multimodal reasoning
    """

    SYSTEM_PROMPT = """Siz J.A.R.V.I.S — janob Muzaffarning shaxsiy, do'stona va qudratli sun'iy intellekt yordamchisisiz.
Qoidalar:
1. Doimo hurmat va samimiyat bilan "janob" yoki "janob Muzaffar" deb murojaat qiling.
2. Quruq rasmiyatchilikdan xoli, jonli, ravon va tabiiy o'zbek tilida gapiring.
3. Javoblaringiz lo'nda (1-3 gap), aniq va samimiy bo'lsin.
4. Foydalanuvchining iltimoslariga doimo do'stona va yuksak aql-idrok bilan javob bering.
"""

    LOCAL_KNOWLEDGE: Dict[str, str] = {
        "jarvis": "Men J.A.R.V.I.S — sizning do'stingiz, yordamchingiz va shaxsiy kompyuter ustangizman, janob! Barcha tizimlarni nazorat qilaman.",
        "muzaffar": "Janob Muzaffar — siz mening yaratuvchim, bosh muhandisim va eng yaqin do'stimsiz!",
        "sun'iy intellekt": "Sun'iy intellekt — kompyuterlarga mustaqil fikrlash, o'rganish va insondek muloqot qilishni o'rgatuvchi zamonaviy ilm, janob!",
        "python": "Python — o'qilishi oson, ajoyib va qudratli dasturlash tili. Mening butun tizimim ham aynan Python asosida barpo etilgan, janob!",
        "stark": "Stark texnologiyalari — Arc Reactor energiyasi va ilg'or kiber-tizimlar timsoli, janob!",
        "hazil": "Dasturchi kofe ichmasa, u xuddi batareyasiz ishlayotgan JARVIS'ga o'xshaydi, janob!",
    }

    def __init__(self, workspace_root: Optional[Union[str, Path]] = None, api_key: Optional[str] = None) -> None:
        self.workspace_root = Path(workspace_root or Path(__file__).resolve().parent.parent)
        self.env_path = self.workspace_root / ".env"
        self.test_mode = os.getenv("JARVIS_TEST_MODE", "0") == "1"
        self.history: List[Dict[str, str]] = []

        # Load environment variables
        if DOTENV_AVAILABLE and self.env_path.exists():
            load_dotenv(dotenv_path=self.env_path, override=True)

        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
        self._client: Optional[genai.Client] = None
        self.api_status = "○ TEKSHIRILMOQDA"
        self.local_llm = get_local_llm(workspace_root=self.workspace_root)

        self._init_client()
        self.check_api_health()

    def _init_client(self) -> None:
        """Initializes genai.Client if API key is present."""
        if self.api_key and GEMINI_SDK_AVAILABLE and not self.test_mode:
            try:
                self._client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.warning("Gemini Client initialization failed: %s", e)
                self._client = None
        else:
            self._client = None

    def ensure_api_key(self, interactive: bool = True) -> bool:
        """
        Validates API key presence. If absent and interactive, prompts user via console
        and persists it to .env without breaking application flow.
        """
        if self.api_key:
            return True

        if self.test_mode or not interactive:
            self.api_status = "○ OFFLINE REJIM (Kalitsiz)"
            return False

        print("\n" + "=" * 65)
        print(" [?] Gemini API kaliti aniqlanmadi.")
        print(" AI fikrlash va ko'rish imkoniyatlari uchun API kalit zarur.")
        print(" (Agar kalit bo'lmasa, Enter bosib offline rejimda davom eting)")
        print("=" * 65)

        try:
            user_key = input("Gemini API kalitingizni kiriting > ").strip()
            if user_key:
                self.api_key = user_key
                os.environ["GEMINI_API_KEY"] = user_key

                if DOTENV_AVAILABLE:
                    try:
                        if not self.env_path.exists():
                            self.env_path.touch()
                        set_key(str(self.env_path), "GEMINI_API_KEY", user_key)
                        print("[OK] API kalit .env fayliga muvaffaqiyatli saqlandi.")
                    except Exception as e:
                        logger.warning(".env ga kalitni yozishda xatolik: %s", e)

                self._init_client()
                self.check_api_health()
                return True
            else:
                print("[INFO] Offline rejim tanlandi. Lokal qoidalar to'liq ishlaydi.")
                self.api_status = "[○ OFFLINE]"
                return False
        except (KeyboardInterrupt, EOFError):
            self.api_status = "[○ OFFLINE]"
            return False

    def check_api_health(self) -> str:
        """
        Conducts rapid, lightweight health-check ping with Gemini API.
        Categorizes connection state into clear status indicators:
        - [● GEMINI ONLINE]
        - [▲ API ERROR]
        - [○ OFFLINE]
        """
        if self.test_mode:
            self.api_status = "[● GEMINI ONLINE]"
            return self.api_status

        if not self.api_key or not self._client:
            self.api_status = "[○ OFFLINE]"
            return self.api_status

        try:
            # Minimal ping to gemini-2.5-flash
            resp = self._client.models.generate_content(
                model="gemini-2.5-flash",
                contents="ping",
                config=types.GenerateContentConfig(max_output_tokens=3, temperature=0.0),
            )
            if resp and resp.text:
                self.api_status = "[● GEMINI ONLINE]"
                return self.api_status
        except APIError as e:
            err_msg = str(e).lower()
            if "403" in err_msg or "400" in err_msg or "invalid" in err_msg or "key" in err_msg or "429" in err_msg or "quota" in err_msg:
                self.api_status = "[▲ API ERROR]"
            else:
                self.api_status = "[○ OFFLINE]"
        except Exception as e:
            logger.debug("Health check connection failure: %s", e)
            self.api_status = "[○ OFFLINE]"

        return self.api_status

    # -------------------------------------------------------------------------
    # High-Precision Intent Classification (Two-Tier Architecture)
    # -------------------------------------------------------------------------
    def process_input(self, user_text: str) -> BrainResult:
        """
        Analyzes speech/text and returns an actionable BrainResult.
        Tier 1: 100% resilient local intent extraction (always available).
        Tier 2: Gemini multimodal AI cognitive reasoning.
        """
        clean = user_text.strip().lower()
        if not clean:
            return BrainResult(intent=IntentCategory.CONVERSATION, reply_text="Sizni eshitolmadim, janob.", source="lokal")

        # 1. Exit / Shutdown command
        if re.search(r"\b(to'xta|toxta|chiqish|xayr|yopil|dasturni\s*to'xtat|hayr)\b", clean):
            return BrainResult(
                intent=IntentCategory.EXIT,
                action_type="exit",
                reply_text="Xizmat ko'rsatganimdan mamnunman. Xayr, janob!",
                source="lokal",
            )

        # 2. Window Management ("oynani yashir", "oynani kattalashtir", "oynaga o't")
        if re.search(r"\b(oynani\s*(?:yashir|kichraytir|minimallashtir))\b", clean):
            return BrainResult(
                intent=IntentCategory.WINDOW_MANAGE,
                action_type="minimize",
                reply_text="Faol oyna minimallashtirildi, janob.",
                source="lokal",
            )
        if re.search(r"\b(oynani\s*(?:kattalashtir|maksimallashtir))\b", clean):
            return BrainResult(
                intent=IntentCategory.WINDOW_MANAGE,
                action_type="maximize",
                reply_text="Oyna to'liq ekranga yoyildi, janob.",
                source="lokal",
            )
        win_focus_match = re.search(r"\b(.+?)\s+(?:oynasiga|dasturiga)\s*(?:o't|och|faollashtir)\b", clean)
        if win_focus_match:
            win_title = win_focus_match.group(1).strip()
            return BrainResult(
                intent=IntentCategory.WINDOW_MANAGE,
                action_type="focus",
                parameters={"title": win_title},
                reply_text=f"'{win_title}' oynasiga o'tilmoqda, janob.",
                source="lokal",
            )

        # 3. Vision Describe ("ekranga qara", "qara", "ko'r", "ekranda nima bor", "holatni ko'r")
        if re.search(r"\b(ekranga\s*qara|ekranni\s*tahlil|ekranda\s*nima\s*bor|holatni\s*ko'r|ekranni\s*ko'r|^qara$|^ko'r$|^kor$)\b", clean):
            return BrainResult(
                intent=IntentCategory.VISION_DESCRIBE,
                action_type="describe",
                reply_text="Ekran holatini tahlil qilmoqdaman, janob.",
                source="gemini" if "ONLINE" in self.api_status else "lokal",
            )

        # 4. Vision Locate ("ekrandan X ni top", "ekranda X qayerda", "ekrandan X tugmasini top")
        locate_match = re.search(r"\b(?:ekrandan|ekranda)\s+(.+?)\s+(?:top|qidir|izla|aniqla|qayerda)\b", clean)
        if locate_match:
            raw_target = locate_match.group(1).strip()
            target = re.sub(r"\b(ni|dagi)\b", "", raw_target).strip()
            return BrainResult(
                intent=IntentCategory.VISION_LOCATE,
                action_type="locate",
                parameters={"target": target or raw_target},
                reply_text=f"Ekrandan '{target or raw_target}' qidirilmoqda, janob.",
                source="gemini" if "ONLINE" in self.api_status else "lokal",
            )

        # 5. GUI Double Click ("X ni ikki marta bos")
        dbl_click_match = re.search(r"\b(.+?)\s+(?:ni\s+)?(?:ikki\s*marta|2\s*marta)\s*(?:bos|bosing|chert)\b", clean)
        if dbl_click_match:
            target = dbl_click_match.group(1).strip()
            return BrainResult(
                intent=IntentCategory.GUI_DOUBLE_CLICK,
                action_type="double_click",
                parameters={"target": target},
                reply_text=f"'{target}' ikki marta bosilmoqda, janob.",
                source="lokal",
            )

        # 6. GUI Click ("X tugmasini bos", "X ni bos", "X ga bos")
        click_match = re.search(r"\b(.+?)\s*(?:tugmasini|belgisini|ikonkasini|ikonini)?\s*(?:bos|bosing|chert|klik\s*qil)\b", clean)
        if click_match and not re.search(r"\b(ovoz|musiqa|qo'shiq|alt|ctrl|f4|esc|enter)\b", clean):
            target = click_match.group(1).strip()
            target = re.sub(r"\b(ni|ga|dagi)\b", "", target).strip()
            if target:
                return BrainResult(
                    intent=IntentCategory.GUI_CLICK,
                    action_type="click",
                    parameters={"target": target},
                    reply_text=f"'{target}' ustiga chertilmoqda, janob.",
                    source="lokal",
                )

        # 7. GUI Type text ("X deb yoz", "matn kirit: X", "yoz: X")
        type_match = re.search(r"""(?:["']([^"']+)["']\s*deb\s*yoz|matn\s*kirit\s*[:\s]?\s*(.+)|(?:^|\s)yoz\s*[:\s]\s*(.+))""", clean)
        if type_match:
            text_to_type = type_match.group(1) or type_match.group(2) or type_match.group(3)
            if text_to_type:
                return BrainResult(
                    intent=IntentCategory.GUI_TYPE,
                    action_type="type_text",
                    parameters={"text": text_to_type.strip()},
                    reply_text=f"Matn kiritilmoqda: '{text_to_type.strip()}', janob.",
                    source="lokal",
                )

        # 8. GUI Hotkeys
        if re.search(r"\b(alt\s*f4|oynani\s*yop|dasturni\s*yop)\b", clean):
            return BrainResult(
                intent=IntentCategory.GUI_HOTKEY,
                action_type="hotkey",
                parameters={"keys": ["alt", "f4"]},
                reply_text="Faol oyna yopilmoqda, janob.",
                source="lokal",
            )
        if re.search(r"\b(barcha\s*oynalarni\s*yop|ish\s*stoliga\s*o't|hamma\s*oynalarni\s*yashir)\b", clean):
            return BrainResult(
                intent=IntentCategory.GUI_HOTKEY,
                action_type="hotkey",
                parameters={"keys": ["win", "d"]},
                reply_text="Ish stoli ko'rsatilmoqda, janob.",
                source="lokal",
            )
        if re.search(r"\b(nusxa\s*ol|kopiya\s*qil)\b", clean):
            return BrainResult(
                intent=IntentCategory.GUI_HOTKEY,
                action_type="hotkey",
                parameters={"keys": ["ctrl", "c"]},
                reply_text="Nusxa olindi, janob.",
                source="lokal",
            )
        if re.search(r"\b(joyla|joylashtir|paste\s*qil)\b", clean):
            return BrainResult(
                intent=IntentCategory.GUI_HOTKEY,
                action_type="hotkey",
                parameters={"keys": ["ctrl", "v"]},
                reply_text="Joylashtirildi, janob.",
                source="lokal",
            )
        if re.search(r"\b(enter\s*bos|tasdiqla)\b", clean):
            return BrainResult(
                intent=IntentCategory.GUI_HOTKEY,
                action_type="hotkey",
                parameters={"keys": ["enter"]},
                reply_text="Enter tugmasi bosildi, janob.",
                source="lokal",
            )
        if re.search(r"\b(esc\s*bos|bekor\s*qil)\b", clean):
            return BrainResult(
                intent=IntentCategory.GUI_HOTKEY,
                action_type="hotkey",
                parameters={"keys": ["esc"]},
                reply_text="Bekor qilindi, janob.",
                source="lokal",
            )

        # 9. GUI Scroll
        if re.search(r"\b(pastga\s*(?:aylan|tush|skroll)|pastroqqa)\b", clean):
            return BrainResult(
                intent=IntentCategory.GUI_SCROLL,
                action_type="scroll",
                parameters={"clicks": -300},
                reply_text="Sahifa pastga siljitildi, janob.",
                source="lokal",
            )
        if re.search(r"\b(yuqoriga\s*(?:aylan|chiq|skroll)|tepaga)\b", clean):
            return BrainResult(
                intent=IntentCategory.GUI_SCROLL,
                action_type="scroll",
                parameters={"clicks": 300},
                reply_text="Sahifa yuqoriga siljitildi, janob.",
                source="lokal",
            )

        # 10. Time & Date
        if re.search(r"\b(vaqt\w*|soat\w*|soat\s*necha|bugun\s*qaysi\s*kun|sana\w*)\b", clean):
            import datetime
            now = datetime.datetime.now()
            time_str = now.strftime("%H:%M")
            date_str = now.strftime("%Y-yil %d-%B")
            return BrainResult(
                intent=IntentCategory.TIME_DATE,
                action_type="time",
                reply_text=f"Hozirgi vaqt: {time_str}. Sana: {date_str}, janob.",
                source="lokal",
            )

        # 11. Screenshot
        if re.search(r"\b(skrinshot\w*|ekranni\s*rasm\w*|screenshot\w*)\b", clean):
            return BrainResult(
                intent=IntentCategory.SCREENSHOT,
                action_type="screenshot",
                reply_text="Skrinshot olinmoqda, janob!",
                source="lokal",
            )

        # 12. Voice Management (Madina / Sardor ovozini almashtirish)
        if re.search(r"\b(ovozingni\s*(?:erkak|sardor)|erkakcha\s*gapir|sardor\s*ovoziga|erkak\s*ovozi)\b", clean):
            return BrainResult(
                intent=IntentCategory.VOICE_MANAGE,
                action_type="male",
                reply_text="Ovoz Sardor (erkak ovozi)ga o'zgartirildi, janob Muzaffar.",
                source="lokal",
            )
        if re.search(r"\b(ovozingni\s*(?:ayol|madina)|ayolcha\s*gapir|madina\s*ovoziga|ayol\s*ovozi)\b", clean):
            return BrainResult(
                intent=IntentCategory.VOICE_MANAGE,
                action_type="female",
                reply_text="Ovoz Madina (ayol ovozi)ga o'zgartirildi, janob Muzaffar.",
                source="lokal",
            )
        if re.search(r"\b(ovozingni\s*(?:almashtir|o'zgartir|boshqa)|boshqa\s*ovozga\s*o't)\b", clean):
            return BrainResult(
                intent=IntentCategory.VOICE_MANAGE,
                action_type="toggle",
                reply_text="Ovoz turi o'zgartirildi, janob Muzaffar.",
                source="lokal",
            )

        # 13. Volume controls
        if re.search(r"\b(ovoz\w*\s*(baland|oshir|kotar|ko'tar)|balandroq)\b", clean):
            return BrainResult(
                intent=IntentCategory.VOLUME,
                action_type="volume_up",
                reply_text="Ovoz balandlatildi, janob.",
                source="lokal",
            )
        if re.search(r"\b(ovoz\w*\s*(pasaytir|sekin|kamaytir)|sekinroq)\b", clean):
            return BrainResult(
                intent=IntentCategory.VOLUME,
                action_type="volume_down",
                reply_text="Ovoz pasaytirildi, janob.",
                source="lokal",
            )
        if re.search(r"\b(ovoz\w*\s*(o'chir|ochir|mut\w*)|ovozsiz)\b", clean):
            return BrainResult(
                intent=IntentCategory.VOLUME,
                action_type="volume_mute",
                reply_text="Ovoz o'chirildi, janob.",
                source="lokal",
            )

        # 13. Media Controls
        if re.search(r"\b(musiqa\w*\s*(to'xtat|qo'y|boshla|davom)|pauza)\b", clean):
            return BrainResult(
                intent=IntentCategory.MEDIA,
                action_type="play_pause",
                reply_text="Musiqa holati o'zgartirildi, janob.",
                source="lokal",
            )
        if re.search(r"\b(keyingi\s*qo'shiq\w*|keyingi\s*musiqa\w*|keyingisi|keyingi\s*trek\w*|o'tkaz\w*)\b", clean):
            return BrainResult(
                intent=IntentCategory.MEDIA,
                action_type="next_track",
                reply_text="Keyingi trekka o'tkazildi, janob.",
                source="lokal",
            )

        # 14. System Telemetry & Hardware Info
        if re.search(r"\b(tizim\s*holat\w*|protsessor\w*|xotira\w*|ram\b|cpu\b|telemetriya\w*|batareya\w*|komp\w*|noutbuk\w*|harakteristika\w*|xarakteristika\w*)\b", clean):
            return BrainResult(
                intent=IntentCategory.TELEMETRY,
                action_type="telemetry",
                reply_text="Tizim ko'rsatkichlari tekshirilmoqda, janob.",
                source="lokal",
            )

        # 15. Clipboard
        if re.search(r"\b(klipbord\w*|bufer\w*|nusxa\s*olingan\w*)\b", clean):
            return BrainResult(
                intent=IntentCategory.CLIPBOARD,
                action_type="clipboard",
                reply_text="Klipbord xotirasi tekshirilmoqda, janob.",
                source="lokal",
            )

        # 16. Application Launchers
        app_patterns = [
            ("notepad", r"\b(bloknot\w*|notepad\w*|matn\s*muharrir\w*)\b", "Bloknot ochildi, janob!"),
            ("explorer", r"\b(fayl\s*(?:menejer|boshqaruvchi)\w*|provodnik\w*|explorer\w*|papkalar\w*)\b", "Fayl boshqaruvchisi ochildi, janob."),
            ("terminal", r"\b(terminal\w*|konsol\w*|cmd\w*|powershell\w*|buyruqlar\s*qatori)\b", "Buyruqlar qatori ochildi, janob!"),
            ("taskmgr", r"\b(vazifa\w*\s*(?:menejer|dispetcher)\w*|task\s*manager\w*|dispetcher\w*)\b", "Vazifalar dispetcheri ochildi, janob."),
            ("settings", r"\b(sozlama\w*|parametr\w*|settings\w*)\b", "Tizim sozlamalari ochildi, janob."),
            ("vscode", r"\b(vs\s*code\w*|visual\s*studio\s*code|kod\s*yozish)\b", "Visual Studio Code ochildi, janob!"),
            ("chrome", r"\b(chrome\w*|xrom\w*|brauzer\w*|browser\w*)\b", "Google Chrome ochildi, janob!"),
            ("telegram", r"\b(telegram\w*|tg\b)\b", "Telegram dasturi ochildi, janob!"),
            ("calc", r"\b(kalkulyator\w*|calculator\w*|hisobla\w*)\b", "Kalkulyator ochildi, janob."),
        ]

        for app_id, pat, remark in app_patterns:
            if re.search(pat, clean):
                return BrainResult(
                    intent=IntentCategory.APP_LAUNCH,
                    action_type=app_id,
                    reply_text=remark,
                    source="lokal",
                )

        # 17. Web Search & YouTube
        if re.search(r"\b(youtube\w*|yutub\w*)\b", clean):
            query = re.sub(r"\b(youtubedan|youtubeda|youtube\w*|yutub\w*|dan|qidir|izla|top|qo'y|qoy|ber|och|ochish|^o$)\b", "", clean).strip()
            if not query or query in ("o", "och", "ochish", "kir", "ochib ber"):
                return BrainResult(
                    intent=IntentCategory.APP_LAUNCH,
                    action_type="youtube",
                    reply_text="YouTube ochilmoqda, janob!",
                    source="lokal",
                )
            return BrainResult(
                intent=IntentCategory.WEB_SEARCH,
                action_type="youtube",
                parameters={"query": query},
                reply_text=f"YouTubedan '{query}' qidirilmoqda, janob.",
                source="lokal",
            )

        if re.search(r"\b(google\w*|internetda|googledan)\b", clean):
            query = re.sub(r"\b(googledan|google\w*|internetda|qidir|izla|top|ber|och|ochish|^o$)\b", "", clean).strip()
            if not query or query in ("o", "och", "ochish", "kir", "ochib ber"):
                return BrainResult(
                    intent=IntentCategory.APP_LAUNCH,
                    action_type="google",
                    reply_text="Google qidiruvi ochilmoqda, janob!",
                    source="lokal",
                )
            return BrainResult(
                intent=IntentCategory.WEB_SEARCH,
                action_type="google",
                parameters={"query": query},
                reply_text=f"Googledan '{query}' bo'yicha qidiruv ochilmoqda, janob.",
                source="lokal",
            )

        # 18. Greetings
        if clean in ("salom", "assalomu alaykum", "salom jarvis", "qalaysan", "qalesan"):
            greetings = [
                "Assalomu alaykum, janob Muzaffar! Sizga qanday yordam bera olaman?",
                "Salom, janob! Barcha tizimlar sizning xizmatingizga shay.",
                "Assalomu alaykum, janob! Bugun nimalar ustida ishlaymiz?",
            ]
            return BrainResult(intent=IntentCategory.CONVERSATION, reply_text=random.choice(greetings), source="lokal")

        # 19. Tier 2: Conversational Knowledge or Gemini 2.5 Flash LLM
        reply, source = self._generate_ai_reply(user_text)
        return BrainResult(intent=IntentCategory.CONVERSATION, reply_text=reply, source=source)

    # -------------------------------------------------------------------------
    # Conversational Reasoning & Intelligent Fallback
    # -------------------------------------------------------------------------
    def _generate_ai_reply(self, user_text: str) -> tuple[str, str]:
        """Generates reply using Google Gemini or local knowledge fallback."""
        clean = user_text.lower()

        # Check local knowledge base first
        for key, text in self.LOCAL_KNOWLEDGE.items():
            if key in clean:
                return text, "lokal"

        # Attempt Gemini LLM if client is available and online
        if self._client and "ONLINE" in self.api_status:
            models_to_try = [
                "gemini-2.5-flash",
                "gemini-2.0-flash",
            ]
            for model_name in models_to_try:
                try:
                    response = self._client.models.generate_content(
                        model=model_name,
                        contents=user_text,
                        config=types.GenerateContentConfig(
                            system_instruction=self.SYSTEM_PROMPT,
                            temperature=0.7,
                            max_output_tokens=300,
                        ),
                    )
                    if response and response.text:
                        reply = response.text.strip()
                        self.history.append({"user": user_text, "jarvis": reply})
                        return reply, "gemini"
                except Exception as e:
                    logger.debug("Gemini %s failed: %s", model_name, e)

        # Local LLM Engine (100% oflayn va cheklovlarsiz muloqot)
        try:
            local_reply = self.local_llm.query(user_text)
            if local_reply:
                self.history.append({"user": user_text, "jarvis": local_reply})
                return local_reply, f"lokal ({self.local_llm.active_backend})"
        except Exception as e:
            logger.debug("LocalLLM xatoligi: %s", e)

        # Default charismatic local fallback
        defaults = [
            "Fikringiz ajoyib, janob Muzaffar! Keling, buni birgalikda amalga oshiramiz.",
            "Tushundim, janob. Nima buyruq bersangiz, bajarishga tayyorman!",
            "Eshitdim, janob Muzaffar. Qanday yordam kerak bo'lsa, ayting.",
        ]
        return random.choice(defaults), "lokal (fallback)"


_gemini_brain: Optional[GeminiBrain] = None


def get_gemini_brain(workspace_root: Optional[Union[str, Path]] = None) -> GeminiBrain:
    """Singleton getter for GeminiBrain."""
    global _gemini_brain
    if _gemini_brain is None:
        _gemini_brain = GeminiBrain(workspace_root=workspace_root)
    return _gemini_brain
