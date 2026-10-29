"""
JARVIS-Core — Vision Engine (Vision Subsystem)
Unified facade uniting Screen Capture, Coordinate Mapping, and Multimodal Screen Analysis.
"""

from __future__ import annotations
import os
import logging
from typing import Optional, Tuple, Dict, Any

from vision.screen_capture import ScreenCapture
from vision.coordinate_mapper import CoordinateMapper
from vision.screen_analyzer import ScreenAnalyzer, UIElementLocation

logger = logging.getLogger("JARVIS.Vision.VisionEngine")


class VisionEngine:
    """
    Unified Vision System of JARVIS.
    Enables autonomous desktop perception:
    - High-speed screen capture
    - Real-time multimodal analysis
    - Precision screen pixel localization
    """

    def __init__(
        self,
        capture: Optional[ScreenCapture] = None,
        analyzer: Optional[ScreenAnalyzer] = None,
        mapper: Optional[CoordinateMapper] = None,
    ) -> None:
        self.capture = capture or ScreenCapture()
        self.analyzer = analyzer or ScreenAnalyzer()
        self.mapper = mapper or CoordinateMapper()

    def capture_screenshot(self, filename: Optional[str] = None) -> Optional[str]:
        """Captures full screen and saves to screenshots directory."""
        return self.capture.save_screenshot(filename=filename)

    def describe_current_screen(self, query: Optional[str] = None) -> str:
        """Captures current screen and explains active applications and state."""
        img = self.capture.capture_image()
        if img is None:
            return "Ekrandan tasvir olib bo'lmadi, janob."
        return self.analyzer.describe_screen(img, custom_query=query)

    def find_target_pixel(self, target_description: str) -> Optional[Tuple[int, int]]:
        """
        Takes a screenshot, identifies target GUI element via multimodal AI,
        and translates its coordinates to physical screen pixels (x, y).
        """
        img = self.capture.capture_image()
        if img is None:
            return None

        loc: UIElementLocation = self.analyzer.locate_element(img, target_description)
        if not loc.found:
            logger.info("Element topilmadi: %s", target_description)
            return None

        # If point [y, x] is provided, use it, else use box_2d
        if loc.point and (loc.point[0] > 0 or loc.point[1] > 0):
            norm_y, norm_x = loc.point[0], loc.point[1]
            return self.mapper.normalize_to_pixel(norm_x, norm_y)
        elif loc.box_2d and any(loc.box_2d):
            return self.mapper.box_to_center_pixel(loc.box_2d)

        return None

    def locate_target_full(self, target_description: str) -> Dict[str, Any]:
        """
        Performs full lookup returning detection status, pixel coordinates, and description.
        """
        img = self.capture.capture_image()
        if img is None:
            return {
                "found": False,
                "target": target_description,
                "message": "Ekran tasviri olinmadi.",
            }

        loc: UIElementLocation = self.analyzer.locate_element(img, target_description)
        if not loc.found:
            return {
                "found": False,
                "target": target_description,
                "message": f"'{target_description}' ekranda topilmadi, janob.",
            }

        # Translate to pixel
        if loc.point and (loc.point[0] > 0 or loc.point[1] > 0):
            norm_y, norm_x = loc.point[0], loc.point[1]
            px, py = self.mapper.normalize_to_pixel(norm_x, norm_y)
        elif loc.box_2d and any(loc.box_2d):
            px, py = self.mapper.box_to_center_pixel(loc.box_2d)
        else:
            px, py = self.mapper.screen_size[0] // 2, self.mapper.screen_size[1] // 2

        return {
            "found": True,
            "target": target_description,
            "pixel_x": px,
            "pixel_y": py,
            "confidence": loc.confidence,
            "description": loc.description,
            "message": f"'{target_description}' topildi: koordinata ({px}, {py}), janob.",
        }


_vision_engine: Optional[VisionEngine] = None


def get_vision_engine() -> VisionEngine:
    """Singleton getter for VisionEngine."""
    global _vision_engine
    if _vision_engine is None:
        _vision_engine = VisionEngine()
    return _vision_engine
