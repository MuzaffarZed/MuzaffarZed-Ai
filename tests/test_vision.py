"""
Unit tests for Vision Subsystem (ScreenCapture, CoordinateMapper, ScreenAnalyzer, VisionEngine)
"""

import os
import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

os.environ["JARVIS_TEST_MODE"] = "1"

from vision.coordinate_mapper import CoordinateMapper
from vision.screen_capture import ScreenCapture
from vision.screen_analyzer import ScreenAnalyzer, UIElementLocation
from vision.vision_engine import VisionEngine, get_vision_engine


def test_coordinate_mapper_normalization():
    mapper = CoordinateMapper(screen_width=1920, screen_height=1080)
    assert mapper.screen_size == (1920, 1080)

    # Center of screen in 0..1000 scale
    px, py = mapper.normalize_to_pixel(500, 500, scale_max=1000.0)
    assert px == 960
    assert py == 540

    # Test 0.0..1.0 scale
    px_float, py_float = mapper.normalize_to_pixel(0.5, 0.5)
    assert px_float == 960
    assert py_float == 540

    # Test boundary clamping (margin of 2 pixels from edge)
    px_min, py_min = mapper.normalize_to_pixel(-100, -100)
    assert px_min == 2
    assert py_min == 2

    px_max, py_max = mapper.normalize_to_pixel(2000, 2000)
    assert px_max == 1918
    assert py_max == 1078


def test_coordinate_mapper_box_center():
    mapper = CoordinateMapper(screen_width=1920, screen_height=1080)
    # Box [ymin, xmin, ymax, xmax] -> center is at y=500, x=500
    box = [400, 400, 600, 600]
    cx, cy = mapper.box_to_center_pixel(box, scale_max=1000.0)
    assert cx == 960
    assert cy == 540

    assert mapper.is_within_bounds(960, 540) is True
    assert mapper.is_within_bounds(2500, 540) is False


def test_screen_capture_image_and_bytes():
    capture = ScreenCapture()
    img = capture.capture_image()
    assert img is not None
    assert img.width == 1920
    assert img.height == 1080

    raw_bytes = capture.capture_bytes(format="PNG")
    assert raw_bytes is not None
    assert len(raw_bytes) > 0

    b64_str = capture.capture_base64()
    assert b64_str is not None
    assert len(b64_str) > 0

    saved_path = capture.save_screenshot(filename="test_screenshot.png")
    assert saved_path is not None
    assert os.path.exists(saved_path)
    # Cleanup test screenshot
    try:
        os.remove(saved_path)
    except Exception:
        pass


def test_screen_analyzer_locate_and_describe():
    analyzer = ScreenAnalyzer()
    img = ScreenCapture().capture_image()

    desc = analyzer.describe_screen(img)
    assert "janob" in desc or "faol" in desc

    loc: UIElementLocation = analyzer.locate_element(img, "Start tugmasi")
    assert loc.found is True
    assert loc.target == "Start tugmasi"
    assert loc.confidence > 0.0


def test_vision_engine_facade():
    engine = VisionEngine()
    desc = engine.describe_current_screen()
    assert len(desc) > 0

    coords = engine.find_target_pixel("Start tugmasi")
    assert coords is not None
    px, py = coords
    assert 0 <= px <= 1920
    assert 0 <= py <= 1080

    full_info = engine.locate_target_full("Start tugmasi")
    assert full_info["found"] is True
    assert "pixel_x" in full_info
    assert "pixel_y" in full_info


def test_vision_engine_singleton():
    v1 = get_vision_engine()
    v2 = get_vision_engine()
    assert v1 is v2
