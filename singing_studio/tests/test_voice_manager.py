"""
Unit tests for VoiceManager in JARVIS AI Singing Studio.
"""

import tempfile
from pathlib import Path
import pytest

from singing_studio.core.audio_engine import AudioEngine
from singing_studio.core.voice_manager import VoiceManager


@pytest.fixture
def test_setup():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        engine = AudioEngine()
        vm = VoiceManager(data_root=root)
        yield engine, vm, root


def test_add_and_list_voice_sample(test_setup):
    engine, vm, root = test_setup

    # Test audio yaratamiz
    raw_audio = root / "temp_rec.wav"
    engine.generate_test_audio(raw_audio, duration=3.0)

    res = vm.add_voice_sample(raw_audio, custom_name="muzaffar_sample_1.wav")
    assert res["filename"].startswith("clean_")
    assert res["duration"] > 2.5

    samples = vm.list_voice_samples()
    assert len(samples) == 1
    assert samples[0]["filename"] == res["filename"]


def test_dataset_statistics_and_packaging(test_setup):
    engine, vm, root = test_setup

    # 2 ta audio qo'shamiz
    for i in range(2):
        s = root / f"sample_{i}.wav"
        engine.generate_test_audio(s, duration=4.0)
        vm.add_voice_sample(s)

    stats = vm.get_dataset_statistics()
    assert stats["sample_count"] == 2
    assert stats["total_seconds"] > 7.0
    assert stats["readiness_percent"] > 0

    zip_path = vm.package_dataset_zip()
    assert zip_path.exists()
    assert zip_path.stat().st_size > 0


def test_add_model_and_listing(test_setup):
    engine, vm, root = test_setup

    dummy_model = root / "muzaffar_vocal.pth"
    dummy_model.write_bytes(b"MODEL_WEIGHTS_MOCK_TEST_BINARY_123")

    res = vm.add_model(dummy_model, model_name="Muzaffar_Pro")
    assert res["name"] == "Muzaffar_Pro"

    models = vm.list_models()
    assert any(m["name"] == "Muzaffar_Pro" for m in models)
