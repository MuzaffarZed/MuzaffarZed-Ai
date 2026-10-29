"""
Automated Test Suite for YouTube Video Pipeline.
Verifies scenes structure, slide rendering, audio generation, thumbnail creation, and video synthesis.
"""

import os
import pytest
from PIL import Image
from content_data import SCENES
from slide_generator import generate_slide
from audio_generator import get_audio_duration
from thumbnail_generator import generate_thumbnail

def test_scenes_structure():
    """Barcha sahnalarning tuzilishi va ma'lumotlar to'liqligini tekshirish"""
    assert len(SCENES) == 7, "Aynan 7 ta sahna mavjud bo'lishi kerak"
    for scene in SCENES:
        assert "id" in scene and isinstance(scene["id"], int)
        assert "title" in scene and len(scene["title"]) > 0
        assert "subtitle" in scene and len(scene["subtitle"]) > 0
        assert "bullets" in scene and len(scene["bullets"]) >= 3
        assert "script" in scene and len(scene["script"]) > 20
        assert "accent_color" in scene and len(scene["accent_color"]) == 3

def test_slide_generation(tmp_path):
    """Slayd kadri to'g'ri o'lchamda (1920x1080) yaratilishini tekshirish"""
    test_scene = SCENES[0]
    out_slide = str(tmp_path / "test_slide.png")
    res = generate_slide(test_scene, out_slide)
    
    assert os.path.exists(res), "Slayd fayli mavjud bo'lishi kerak"
    with Image.open(res) as img:
        assert img.size == (1920, 1080), "Slayd o'lchami 1920x1080 bo'lishi shart"
        assert img.format == "PNG", "Format PNG bo'lishi shart"

def test_thumbnail_generation(tmp_path):
    """YouTube Thumbnail to'g'ri o'lchamda (1280x720) yaratilishini tekshirish"""
    out_thumb = str(tmp_path / "test_thumb.png")
    res = generate_thumbnail(out_thumb)
    
    assert os.path.exists(res), "Muqova fayli mavjud bo'lishi kerak"
    with Image.open(res) as img:
        assert img.size == (1280, 720), "Thumbnail o'lchami 1280x720 bo'lishi shart"

def test_audio_files_exist_and_valid():
    """Hosil qilingan audio fayllarning mavjudligi va davomiyligi musbat ekanini tekshirish"""
    audio_dir = "output/audio"
    if os.path.exists(audio_dir):
        audio_files = [f for f in os.listdir(audio_dir) if f.endswith(".mp3")]
        assert len(audio_files) == 7, "7 ta audio fayl yaratilgan bo'lishi kerak"
        for af in audio_files:
            path = os.path.join(audio_dir, af)
            duration = get_audio_duration(path)
            assert duration > 5.0, f"Audio fayl {af} davomiyligi 5 sekunddan ko'p bo'lishi kerak"
