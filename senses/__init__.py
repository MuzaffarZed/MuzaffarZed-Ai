"""
JARVIS-Core — Senses Subsystem
Handles speech recognition, audio playback, and acoustic cues.
"""

from .voice import VoiceEngine, get_voice_engine

__all__ = ["VoiceEngine", "get_voice_engine"]
