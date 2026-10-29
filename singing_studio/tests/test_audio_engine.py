"""
Unit tests for AudioEngine in JARVIS AI Singing Studio.
Master Architect standard: 100% executable zero-defect verification.
"""

import os
import tempfile
from pathlib import Path
import pytest

from singing_studio.core.audio_engine import AudioEngine, AudioEngineError


@pytest.fixture
def engine():
    return AudioEngine()


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as td:
        yield Path(td)


def test_engine_initialization(engine):
    """FFmpeg va FFprobe muvaffaqiyatli aniqlanishini tekshirish."""
    assert engine.ffmpeg is not None
    assert engine.ffprobe is not None


def test_generate_and_probe_audio(engine, temp_dir):
    """Sinov audio yaratish va uning davomiyligini tahlil qilish."""
    test_wav = temp_dir / "test_sine.wav"
    engine.generate_test_audio(test_wav, duration=2.0, frequency=440)
    assert test_wav.exists()

    info = engine.get_audio_info(test_wav)
    assert info["duration"] > 1.8 and info["duration"] < 2.2
    assert info["sample_rate"] == 44100
    assert info["channels"] >= 1


def test_format_conversion_mp3(engine, temp_dir):
    """WAV dan 320kbps MP3 formatga o'girish."""
    src_wav = temp_dir / "src.wav"
    out_mp3 = temp_dir / "out.mp3"
    engine.generate_test_audio(src_wav, duration=1.5)

    engine.convert_format(src_wav, out_mp3, bitrate="320k")
    assert out_mp3.exists()
    assert out_mp3.stat().st_size > 0

    info = engine.get_audio_info(out_mp3)
    assert info["duration"] > 1.3


def test_pitch_shifting(engine, temp_dir):
    """Audioning pitch (ohang) balandligini sur'atni o'zgartirmasdan siljitish."""
    src_wav = temp_dir / "base.wav"
    pitch_up = temp_dir / "up_2.wav"
    pitch_down = temp_dir / "down_2.wav"

    engine.generate_test_audio(src_wav, duration=2.0, frequency=440)

    # +2 semiton
    engine.shift_pitch(src_wav, pitch_up, semitones=2.0)
    assert pitch_up.exists()
    info_up = engine.get_audio_info(pitch_up)
    # Davomiylik saqlanishi kerak
    assert abs(info_up["duration"] - 2.0) < 0.3

    # -2 semiton
    engine.shift_pitch(src_wav, pitch_down, semitones=-2.0)
    assert pitch_down.exists()
    info_down = engine.get_audio_info(pitch_down)
    assert abs(info_down["duration"] - 2.0) < 0.3


def test_vocal_chain_reverb(engine, temp_dir):
    """Vokalga studiya reverbi va filtrlarini qo'llash."""
    src_wav = temp_dir / "vocal_raw.wav"
    out_fx = temp_dir / "vocal_fx.wav"

    engine.generate_test_audio(src_wav, duration=2.0)
    engine.apply_vocal_chain(src_wav, out_fx, reverb_level=0.3, echo_level=0.1)

    assert out_fx.exists()
    assert out_fx.stat().st_size > 0


def test_clean_voice_sample(engine, temp_dir):
    """Ovoz namunasini tozalash va tayyorlash."""
    src_wav = temp_dir / "dirty_voice.wav"
    out_clean = temp_dir / "clean_voice.wav"

    engine.generate_test_audio(src_wav, duration=2.0)
    engine.clean_voice_sample(src_wav, out_clean, noise_reduction=True, trim_silence=True)

    assert out_clean.exists()
    assert out_clean.stat().st_size > 0


def test_mix_song_mastering(engine, temp_dir):
    """Vokal va minusovkani EBU R128 mastering bilan birlashtirish."""
    voc_wav = temp_dir / "voc.wav"
    min_wav = temp_dir / "min.wav"
    final_song = temp_dir / "song_mastered.mp3"

    engine.generate_test_audio(voc_wav, duration=2.5, frequency=520)
    engine.generate_test_audio(min_wav, duration=2.5, frequency=220)

    engine.mix_song(voc_wav, min_wav, final_song, vocal_vol=1.1, minus_vol=0.85, apply_mastering=True)

    assert final_song.exists()
    assert final_song.stat().st_size > 0
    info = engine.get_audio_info(final_song)
    assert info["duration"] > 2.0
