"""
JARVIS-Core — Central Orchestrator & Peak-Level Autonomous Multimodal System (v3.0)
Integrates:
1. ReAct Multi-Step Autonomous Agent Loop (Perceive -> Plan -> Act -> Verify)
2. 3-Layer Universal OS Control (UI Automation + PowerShell API + Multimodal Vision)
3. Hybrid Vision (DPI-Aware 100/125/150%, Window Topology & Cursor Coordinates)
4. Streaming Neural Voice (In-Memory RAM synthesis with Barge-in interrupt)
5. Live Telemetry HUD Monitoring Bar & Fail-Safe Security
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
import time
from pathlib import Path
from typing import Optional

import psutil

# Windows console UTF-8 configuration
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

# Ensure project root is in sys.path
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from actions.gui_actions import GuiActions, get_gui_actions
from actions.omni_control import OmniControl, get_omni_controller
from actions.system_actions import SystemActions, get_system_actions
from brain.agent_loop import AgentLoop, TaskResult, get_agent_loop
from brain.gemini_brain import BrainResult, GeminiBrain, IntentCategory, get_gemini_brain
from senses.streaming_voice import StreamingVoiceEngine, get_streaming_voice
from senses.voice import VoiceEngine, get_voice_engine
from vision.hybrid_vision import HybridVisionEngine, get_hybrid_vision
from vision.vision_engine import VisionEngine, get_vision_engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("JARVIS.Core")


class JarvisCore:
    """Central Coordinator for the JARVIS Peak-Level Autonomous Desktop Assistant.

    Features ReAct multi-step autonomous loops, 3-tier OS control, hybrid vision,
    in-memory streaming voice with barge-in, and real-time telemetry HUD.
    """

    BANNER = r"""
================================================================================
          J.A.R.V.I.S — PEAK-LEVEL AUTONOMOUS MULTIMODAL AGENT (v3.0)           
      ReAct Loop • 3-Tier OS Control • Hybrid Vision • Streaming Barge-In       
                 Bosh Muhandis: Janob Muzaffar | ai_workspace                   
================================================================================
"""

    def __init__(
        self,
        brain: Optional[GeminiBrain] = None,
        omni: Optional[OmniControl] = None,
        hybrid_vision: Optional[HybridVisionEngine] = None,
        streaming_voice: Optional[StreamingVoiceEngine] = None,
        agent_loop: Optional[AgentLoop] = None,
        voice: Optional[VoiceEngine] = None,
        actions: Optional[SystemActions] = None,
        gui: Optional[GuiActions] = None,
        vision: Optional[VisionEngine] = None,
    ) -> None:
        self.workspace_root = Path(__file__).resolve().parent
        self.brain = brain or get_gemini_brain(workspace_root=self.workspace_root)
        self.omni = omni or get_omni_controller()
        self.hybrid_vision = hybrid_vision or get_hybrid_vision()
        self.streaming_voice = streaming_voice or get_streaming_voice()
        self.agent_loop = agent_loop or get_agent_loop()

        # Legacy adapters for backward compatibility
        self.voice = voice or get_voice_engine()
        self.actions = actions or get_system_actions(workspace_root=str(self.workspace_root))
        self.gui = gui or get_gui_actions()
        self.vision = vision or get_vision_engine()

        self.running = False

    def get_hud_status(self, cycle_step: str = "Kutish") -> str:
        """Constructs a real-time HUD monitoring status string."""
        return self.streaming_voice.get_hud_status(
            gemini_status=self.brain.api_status,
            cycle_step=cycle_step,
        )

    def startup(self, interactive: bool = True) -> None:
        """Initializes hardware interfaces, validates API key, and prepares speech."""
        print(self.BANNER)

        # Check / Prompt API key if needed
        self.brain.ensure_api_key(interactive=interactive)

        print(f"\n>>> Tizim Tayyor! {self.get_hud_status()}\n")
        self.voice.play_cue("done")
        ready_message = "Assalomu alaykum, muhtaram janob Muzaffar! Peak-Level ReAct avtonom tizimi shay, xizmatingizdaman."
        self.streaming_voice.speak(ready_message)
        self.running = True

    def is_complex_task(self, text: str) -> bool:
        """Matn murakkab ko'p bosqichli vazifa ekanligini aniqlaydi."""
        complex_keywords = [
            "fleshka", "usb", "rasm", "ko'chir", "olib o't", "ob-havo",
            "arxiv", "zip", "telegram", "brauzer", "saqla", "sarala",
            "yangi papka", "yuklab", "topib ber", "och va yoz",
        ]
        text_lower = text.lower()
        # Agar buyruq bir nechta kalit so'zlarni o'z ichiga olsa yoki uzun bo'lsa
        matches = sum(1 for kw in complex_keywords if kw in text_lower)
        return matches >= 2 or len(text.split()) >= 6

    def process_command(self, user_text: str, force_react: bool = False) -> bool:
        """Topshiriqni qayta ishlaydi.

        Murakkab vazifalar avtomatik ravishda ReAct tsikliga uzatiladi.
        """
        if not user_text:
            return True

        # Chiqish buyrug'i tekshiruvi
        exit_phrases = ["chiqish", "exit", "quit", "tamom", "to'xta", "to'xtat", "dasturni to'xtat", "dasturdan chiq"]
        if any(ep in user_text.lower().strip() for ep in exit_phrases):
            farewell = "Xizmatingizda bo'lganimdan mamnunman, hayr, janob Muzaffar!"
            self.streaming_voice.speak(farewell)
            self.running = False
            return False

        # Agar vazifa murakkab bo'lsa yoki majburiy ReAct belgilangan bo'lsa
        if force_react or self.is_complex_task(user_text):
            print(f"\n[ReAct Agent] Murakkab topshiriq aniqlandi. Rejalashtirish tsikli boshlanmoqda...")
            self.streaming_voice.speak("Topshiriq qabul qilindi, rejalashtirish va ijro tsiklini boshlayapman, janob.")

            def step_cb(step: int, thought: str, tool: str) -> None:
                print(f"  -> [Qadam {step}] {thought} (Asbob: {tool})")

            task_result: TaskResult = self.agent_loop.run_task(
                goal=user_text,
                on_step_callback=step_cb,
            )

            status_icon = "Muvaffaqiyatli" if task_result.success else "Qisman bajarildi"
            print(f"\n[ReAct Natija: {status_icon} | Qadamlar: {len(task_result.steps)} | Vaqt: {task_result.total_time}s | Manba: {task_result.source.upper()}]")
            print(f"Xulosa: {task_result.summary}\n")

            self.streaming_voice.speak(task_result.summary)
            self.voice.play_cue("done")
            return True

        # Oddiy buyruqlar uchun tezkor Brain ishlov berishi
        result: BrainResult = self.brain.process_input(user_text)
        reply = result.reply_text

        # 0. Chiqish va hayot sikli
        if result.intent == IntentCategory.EXIT:
            self.streaming_voice.speak(reply)
            self.running = False
            return False

        # 1. Window Management
        if result.intent == IntentCategory.WINDOW_MANAGE:
            act = result.action_type
            if act == "minimize":
                self.hybrid_vision.minimize_window("")
            elif act == "maximize":
                self.hybrid_vision.maximize_window("")
            elif act == "focus":
                win_title = result.parameters.get("title", "")
                ok = self.hybrid_vision.activate_window(win_title)
                if not ok:
                    reply = f"'{win_title}' oynasi topilmadi, janob."

        # 2. Vision (Screen Awareness)
        elif result.intent == IntentCategory.VISION_DESCRIBE:
            reply = self.vision.describe_current_screen()

        elif result.intent == IntentCategory.VISION_LOCATE:
            target = result.parameters.get("target", "")
            loc_result = self.vision.locate_target_full(target)
            reply = loc_result["message"]

        # 3. GUI Automation (Level 1 / Level 3)
        elif result.intent == IntentCategory.GUI_CLICK:
            target = result.parameters.get("target", "")
            # Avval 1-daraja: UI Automation orqali urinib ko'rish
            uia_res = self.omni.click_ui_element(name=target)
            if uia_res.success:
                reply = f"'{target}' UI elementi topildi va bosildi, janob!"
            else:
                pixel = self.vision.find_target_pixel(target)
                if pixel:
                    px, py = pixel
                    self.omni.click_coordinate(px, py)
                    reply = f"'{target}' vizual aniqlanib ({px}, {py}) bosildi, janob!"
                else:
                    reply = f"Kechirasiz janob, '{target}' elementi topilmadi."

        elif result.intent == IntentCategory.GUI_TYPE:
            text = result.parameters.get("text", "")
            res = self.omni.type_unicode_safe(text)
            reply = f"Matn xavfsiz kiritildi: '{text}', janob." if res.success else "Matn kiritishda xatolik yuz berdi."

        elif result.intent == IntentCategory.GUI_HOTKEY:
            keys = result.parameters.get("keys", [])
            if keys:
                self.omni.send_hotkey(*keys)
                reply = f"{'+'.join(keys).upper()} tugmalari bosildi, janob."

        elif result.intent == IntentCategory.GUI_SCROLL:
            clicks = result.parameters.get("clicks", -300)
            self.omni.scroll(clicks)
            reply = "Sahifa siljitildi, janob."

        # 4. OS Launchers & Hardware (Level 2)
        elif result.intent == IntentCategory.APP_LAUNCH:
            app = result.action_type
            if app == "notepad":
                self.omni.launch_target("notepad.exe")
            elif app == "explorer":
                self.omni.launch_target("explorer.exe")
            elif app == "terminal":
                self.omni.launch_target("cmd.exe")
            elif app == "taskmgr":
                self.omni.launch_target("taskmgr.exe")
            elif app == "chrome":
                self.omni.launch_target("chrome.exe")
            elif app == "telegram":
                self.omni.launch_target("telegram.exe")
            elif app == "calc":
                self.omni.launch_target("calc.exe")
            elif app == "youtube":
                self.actions.open_chrome("https://www.youtube.com")
            elif app == "google":
                self.actions.open_chrome("https://www.google.com")
            else:
                self.omni.launch_target(app)

        elif result.intent == IntentCategory.VOLUME:
            act = result.action_type
            if act == "volume_up":
                self.actions.volume_up()
            elif act == "volume_down":
                self.actions.volume_down()
            elif act == "volume_mute":
                self.actions.volume_mute()

        elif result.intent == IntentCategory.VOICE_MANAGE:
            act = result.action_type
            if act == "male":
                reply = self.streaming_voice.switch_to_male()
                self.voice.switch_to_male()
            elif act == "female":
                reply = self.streaming_voice.switch_to_female()
                self.voice.switch_to_female()
            elif act == "toggle":
                if "Sardor" in self.streaming_voice.current_voice_name:
                    reply = self.streaming_voice.switch_to_female()
                    self.voice.switch_to_female()
                else:
                    reply = self.streaming_voice.switch_to_male()
                    self.voice.switch_to_male()

        elif result.intent == IntentCategory.MEDIA:
            act = result.action_type
            if act == "play_pause":
                self.actions.media_play_pause()
            elif act == "next_track":
                self.actions.media_next()

        elif result.intent == IntentCategory.SCREENSHOT:
            path = self.vision.capture_screenshot() or self.actions.take_screenshot()
            reply = f"Skrinshot saqlandi: {Path(path).name}, janob!" if path else "Skrinshot olishda xatolik yuz berdi."

        elif result.intent == IntentCategory.TELEMETRY:
            reply = self.actions.get_telemetry()

        elif result.intent == IntentCategory.CLIPBOARD:
            reply = self.actions.read_clipboard()

        elif result.intent == IntentCategory.WEB_SEARCH:
            query = result.parameters.get("query", "")
            if result.action_type == "youtube":
                self.actions.search_youtube(query)
            else:
                self.actions.search_google(query)

        source_label = "Lokal Mantiq" if result.source == "lokal" else ("Gemini 2.5 Flash" if result.source == "gemini" else "Offline Zaxira")
        print(f"[Ijro: Bajarildi | Manba: {source_label}]")

        self.streaming_voice.speak(reply)
        self.voice.play_cue("done")
        return True

    def run_voice_loop(self) -> None:
        """Continuous noise-filtered voice recognition and command loop."""
        self.startup(interactive=False)
        print("\n[INFO] Ovozli rejim faol. 'To'xta' yoki 'Chiqish' deb tizimni yopishingiz mumkin.")

        while self.running:
            try:
                # 15 soniya gacha to'liq gapirish imkoni
                text = self.voice.listen(timeout=10, phrase_time_limit=15)
                if not text:
                    continue

                keep_running = self.process_command(text)
                self.voice.reset_listen_announcement()
                if not keep_running:
                    break

            except KeyboardInterrupt:
                print("\n[JARVIS] Foydalanuvchi tomonidan to'xtatildi.")
                self.streaming_voice.speak("Tizim to'xtatildi, xayr, janob!")
                break
            except Exception as e:
                logger.error("Kutilmagan xatolik yuz berdi: %s", e)
                self.voice.play_cue("error")

    def run_text_loop(self) -> None:
        """Interactive console text prompt loop with live HUD monitoring."""
        print(self.BANNER)
        self.brain.ensure_api_key(interactive=True)
        print("[INFO] Matnli buyruqlar rejimi faol. Buyruq kiriting yoki 'chiqish' deb yozing.\n")

        self.running = True
        while self.running:
            try:
                hud = self.get_hud_status()
                print(hud)
                user_input = input("Janob Muzaffar > ").strip()
                if not user_input:
                    continue

                keep_running = self.process_command(user_input)
                if not keep_running:
                    break

            except (KeyboardInterrupt, EOFError):
                print("\n[JARVIS] Dastur yakunlandi. Xayr, janob!")
                break


def main() -> None:
    parser = argparse.ArgumentParser(description="JARVIS Peak-Level Autonomous Multimodal AI Assistant")
    parser.add_argument("--text", "-t", action="store_true", help="Konsol matnli rejimida ishga tushirish")
    parser.add_argument("--voice", "-v", action="store_true", help="Mikrofon orqali ovozli rejimda ishga tushirish")
    parser.add_argument("--once", type=str, help="Bitta buyruqni bajarish va chiqish")
    parser.add_argument("--react", action="store_true", help="Majburiy ReAct avtonom tsiklini yoqish")
    args = parser.parse_args()

    app = JarvisCore()

    if args.once:
        app.process_command(args.once, force_react=args.react)
    elif args.voice:
        app.run_voice_loop()
    else:
        app.run_text_loop()


if __name__ == "__main__":
    main()
