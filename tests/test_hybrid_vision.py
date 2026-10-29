"""tests/test_hybrid_vision.py - Unit tests for HybridVisionEngine."""

import pytest
from PIL import Image
from vision.hybrid_vision import HybridVisionEngine, get_hybrid_vision, VisualContext


def test_hybrid_vision_singleton():
    vis1 = get_hybrid_vision()
    vis2 = get_hybrid_vision()
    assert vis1 is vis2
    assert isinstance(vis1, HybridVisionEngine)


def test_hybrid_vision_screen_size_and_cursor():
    vis = HybridVisionEngine()
    w, h = vis.get_screen_size()
    assert w > 0 and h > 0
    cx, cy = vis.get_cursor_position()
    assert isinstance(cx, int) and isinstance(cy, int)


def test_hybrid_vision_capture_and_bytes():
    vis = HybridVisionEngine()
    img = vis.capture_screen()
    assert isinstance(img, Image.Image)
    assert img.width > 0 and img.height > 0
    raw_bytes = vis.capture_as_bytes()
    assert isinstance(raw_bytes, bytes)
    assert len(raw_bytes) > 0


def test_hybrid_vision_window_topology():
    vis = HybridVisionEngine()
    active_win, visible_wins = vis.get_window_topology()
    assert isinstance(visible_wins, list)
    # Kamida bir nechta oyna ochiq bo'lishi kutiladi
    for win in visible_wins[:5]:
        assert win.width > 0
        assert win.height > 0
        assert isinstance(win.rect, tuple)


def test_hybrid_vision_visual_context_prompt():
    vis = HybridVisionEngine()
    ctx = vis.get_full_visual_context()
    assert isinstance(ctx, VisualContext)
    prompt_text = ctx.get_prompt_context()
    assert "Ekran o'lchami" in prompt_text
    assert "Kursor hozirgi o'rni" in prompt_text
