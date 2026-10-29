"""
tests/test_local_voice_ai.py — Tests for Hardware-Adapted Local LLM & Accent-Free Voice Subsystems.
"""

import os
import pytest
from brain.local_llm import LocalLLMEngine, get_local_llm
from brain.gemini_brain import GeminiBrain, IntentCategory
from senses.streaming_voice import StreamingVoiceEngine, VOICE_MADINA, VOICE_SARDOR
from senses.voice import VoiceEngine
from main import JarvisCore


@pytest.fixture
def local_llm():
    return LocalLLMEngine()


@pytest.fixture
def streaming_voice():
    return StreamingVoiceEngine(test_mode=True)


@pytest.fixture
def voice_engine():
    os.environ["JARVIS_TEST_MODE"] = "1"
    return VoiceEngine()


# =============================================================================
# 1. Local LLM Tests
# =============================================================================

def test_local_llm_initialization(local_llm):
    assert local_llm is not None
    status = local_llm.get_status_summary()
    assert "Lokal Dvigatel:" in status


def test_local_llm_empty_prompt(local_llm):
    reply = local_llm.query("")
    assert "tinglamoqdaman" in reply.lower()


def test_local_llm_math_calculation(local_llm):
    reply = local_llm.query("25 * 4")
    assert "100" in reply
    assert "janob" in reply.lower()

    reply_div = local_llm.query("100 / 5")
    assert "20" in reply_div


def test_local_llm_cognitive_muzaffar(local_llm):
    reply = local_llm.query("mening ismim Muzaffar, meni taniysanmi?")
    assert "muzaffar" in reply.lower()
    assert "muhandis" in reply.lower() or "do'st" in reply.lower() or "sohib" in reply.lower()


def test_local_llm_hardware_awareness(local_llm):
    reply = local_llm.query("kompyuterim xarakteristikasi qanday?")
    assert "i5" in reply or "intel" in reply.lower()
    assert "8 gb" in reply.lower() or "ram" in reply.lower()


def test_local_llm_jokes_and_quotes(local_llm):
    reply_joke = local_llm.query("menga bitta qiziqarli hazil aytib ber")
    assert len(reply_joke) > 20
    assert "janob" in reply_joke.lower() or "dasturchi" in reply_joke.lower()

    reply_quote = local_llm.query("biror hikmat yoki maslahat ber")
    assert len(reply_quote) > 20


# =============================================================================
# 2. Voice Switching & Accent-Free TTS Tests
# =============================================================================

def test_streaming_voice_switching(streaming_voice):
    # Default is Madina
    assert streaming_voice.voice == VOICE_MADINA
    assert "Madina" in streaming_voice.current_voice_name

    # Switch to Sardor
    msg = streaming_voice.switch_to_male()
    assert streaming_voice.voice == VOICE_SARDOR
    assert "Sardor" in streaming_voice.current_voice_name
    assert "Sardor" in msg

    # Switch back to Madina
    msg_female = streaming_voice.switch_to_female()
    assert streaming_voice.voice == VOICE_MADINA
    assert "Madina" in streaming_voice.current_voice_name
    assert "Madina" in msg_female


def test_voice_engine_switching(voice_engine):
    assert voice_engine.set_voice("sardor") is True
    assert voice_engine.voice_name == "uz-UZ-SardorNeural"

    assert voice_engine.set_voice("madina") is True
    assert voice_engine.voice_name == "uz-UZ-MadinaNeural"


# =============================================================================
# 3. Brain Intent Recognition for Voice
# =============================================================================

def test_brain_voice_intent():
    brain = GeminiBrain()

    res_male = brain.process_input("ovozingni erkak qil")
    assert res_male.intent == IntentCategory.VOICE_MANAGE
    assert res_male.action_type == "male"

    res_female = brain.process_input("madina ovoziga o't")
    assert res_female.intent == IntentCategory.VOICE_MANAGE
    assert res_female.action_type == "female"

    res_toggle = brain.process_input("ovozingni almashtir")
    assert res_toggle.intent == IntentCategory.VOICE_MANAGE
    assert res_toggle.action_type == "toggle"


def test_brain_offline_ai_reply():
    brain = GeminiBrain()
    brain.api_status = "[○ OFFLINE]"
    res = brain.process_input("koinot va yulduzlar haqida qisqacha ayt")
    assert res.intent == IntentCategory.CONVERSATION
    assert len(res.reply_text) > 10
    assert "lokal" in res.source


# =============================================================================
# 4. End-to-End Core Integration Test
# =============================================================================

def test_jarvis_core_voice_switch_execution():
    core = JarvisCore()
    core.streaming_voice.test_mode = True
    core.voice.test_mode = True

    # Process voice switch command
    ok = core.process_command("ovozingni erkak qil")
    assert ok is True
    assert core.streaming_voice.voice == VOICE_SARDOR

    ok2 = core.process_command("ovozingni ayol qil")
    assert ok2 is True
    assert core.streaming_voice.voice == VOICE_MADINA


def test_brain_colloquial_speech_recovery():
    brain = GeminiBrain()

    # Chala aytilgan "youtubeda o" darhol YouTube ochilishiga ulanishi kerak
    res_yt = brain.process_input("youtubeda o")
    assert res_yt.intent == IntentCategory.APP_LAUNCH
    assert res_yt.action_type == "youtube"

    # Chala aytilgan "kompy" yoki "kompyuterim" telemetriyani berishi kerak
    res_comp = brain.process_input("kompy")
    assert res_comp.intent == IntentCategory.TELEMETRY

    res_comp2 = brain.process_input("kompyuterim xarakteristikasi")
    assert res_comp2.intent == IntentCategory.TELEMETRY


def test_voice_engine_announcement_flag(voice_engine):
    assert voice_engine._listening_announced is False
    voice_engine._listening_announced = True
    voice_engine.reset_listen_announcement()
    assert voice_engine._listening_announced is False
