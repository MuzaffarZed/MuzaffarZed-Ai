"""
Unit tests for Brain Subsystem (GeminiBrain)
"""

import os
import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

os.environ["JARVIS_TEST_MODE"] = "1"

from brain.gemini_brain import GeminiBrain, IntentCategory, get_gemini_brain


def test_brain_health_check_and_sources():
    brain = GeminiBrain()
    health = brain.check_api_health()
    assert "ONLINE" in health or "OFFLINE" in health

    # Local commands must report source='lokal'
    res = brain.process_input("Vaqt necha bo'ldi?")
    assert res.source == "lokal"

    res_app = brain.process_input("Bloknotni och")
    assert res_app.source == "lokal"


def test_brain_intent_classification():
    brain = GeminiBrain()

    # Time & Date
    res_time = brain.process_input("Vaqt necha bo'ldi?")
    assert res_time.intent == IntentCategory.TIME_DATE
    assert "Hozirgi vaqt" in res_time.reply_text

    # Apps
    assert brain.process_input("Bloknotni och").intent == IntentCategory.APP_LAUNCH
    assert brain.process_input("Fayl menejerini och").intent == IntentCategory.APP_LAUNCH
    assert brain.process_input("Terminalni och").intent == IntentCategory.APP_LAUNCH
    assert brain.process_input("Vazifalar dispetcherini och").intent == IntentCategory.APP_LAUNCH
    assert brain.process_input("Sozlamalarni och").intent == IntentCategory.APP_LAUNCH
    assert brain.process_input("VS Code dasturini och").intent == IntentCategory.APP_LAUNCH
    assert brain.process_input("Google Chrome brauzerini och").intent == IntentCategory.APP_LAUNCH
    assert brain.process_input("Kalkulyatorni och").intent == IntentCategory.APP_LAUNCH

    # Volume & Media
    assert brain.process_input("Ovozni balandroq qil").intent == IntentCategory.VOLUME
    assert brain.process_input("Ovozni pasaytir").intent == IntentCategory.VOLUME
    assert brain.process_input("Ovozni o'chir").intent == IntentCategory.VOLUME
    assert brain.process_input("Musiqani to'xtat").intent == IntentCategory.MEDIA
    assert brain.process_input("Keyingi qo'shiqqa o'tkaz").intent == IntentCategory.MEDIA

    # Telemetry
    assert brain.process_input("Tizim holati qanday?").intent == IntentCategory.TELEMETRY

    # Screenshot
    assert brain.process_input("Ekranni rasmga ol, skrinshot qil").intent == IntentCategory.SCREENSHOT

    # Web search
    res_yt = brain.process_input("YouTubedan yangi xit qo'shiqlar qidir")
    assert res_yt.intent == IntentCategory.WEB_SEARCH
    assert "yangi xit" in res_yt.parameters.get("query", "")

    # Window Management
    res_min = brain.process_input("Oynani yashir")
    assert res_min.intent == IntentCategory.WINDOW_MANAGE
    assert res_min.action_type == "minimize"

    res_max = brain.process_input("Oynani kattalashtir")
    assert res_max.intent == IntentCategory.WINDOW_MANAGE
    assert res_max.action_type == "maximize"

    res_focus = brain.process_input("Chrome oynasiga o't")
    assert res_focus.intent == IntentCategory.WINDOW_MANAGE
    assert res_focus.action_type == "focus"
    assert "chrome" in res_focus.parameters.get("title", "")

    # Exit
    assert brain.process_input("Dasturdan chiqish").intent == IntentCategory.EXIT
    assert brain.process_input("Bo'ldi, to'xta").intent == IntentCategory.EXIT


def test_brain_vision_and_gui_intents():
    brain = GeminiBrain()

    # Vision Describe
    assert brain.process_input("Ekranga qara").intent == IntentCategory.VISION_DESCRIBE
    assert brain.process_input("Ekranda nima bor?").intent == IntentCategory.VISION_DESCRIBE
    assert brain.process_input("Qara").intent == IntentCategory.VISION_DESCRIBE
    assert brain.process_input("Ekranni tahlil qil").intent == IntentCategory.VISION_DESCRIBE

    # Vision Locate
    res_loc = brain.process_input("Ekrandan Start tugmasini top")
    assert res_loc.intent == IntentCategory.VISION_LOCATE
    assert "start tugmasi" in res_loc.parameters.get("target", "").lower()

    # GUI Click
    res_click = brain.process_input("Start tugmasini bos")
    assert res_click.intent == IntentCategory.GUI_CLICK
    assert "start" in res_click.parameters.get("target", "").lower()

    # GUI Double Click
    res_dbl = brain.process_input("Bloknot belgisini ikki marta bos")
    assert res_dbl.intent == IntentCategory.GUI_DOUBLE_CLICK

    # GUI Type
    res_type = brain.process_input("Matn kirit: Salom janob!")
    assert res_type.intent == IntentCategory.GUI_TYPE
    assert "salom janob!" in res_type.parameters.get("text", "").lower()

    # GUI Hotkey
    res_hotkey = brain.process_input("Alt F4 bos")
    assert res_hotkey.intent == IntentCategory.GUI_HOTKEY
    assert res_hotkey.parameters.get("keys") == ["alt", "f4"]

    # GUI Scroll
    res_scroll = brain.process_input("Sahifani pastga aylan")
    assert res_scroll.intent == IntentCategory.GUI_SCROLL
    assert res_scroll.parameters.get("clicks") == -300


def test_brain_local_knowledge():
    brain = GeminiBrain()

    res = brain.process_input("JARVIS nima?")
    assert "janob" in res.reply_text.lower() or "j.a.r.v.i.s" in res.reply_text.lower()

    res_py = brain.process_input("Python haqida gapirib ber")
    assert "python" in res_py.reply_text.lower()


def test_brain_singleton():
    b1 = get_gemini_brain()
    b2 = get_gemini_brain()
    assert b1 is b2
