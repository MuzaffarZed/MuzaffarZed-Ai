"""
JARVIS-Core — Coordinate Mapper (Vision Subsystem)
Translates normalized coordinates ([0, 1000] or [0.0, 1.0]) from Multimodal Vision models
into precise physical screen pixel coordinates, accounting for resolution and boundaries.
"""

from __future__ import annotations
import os
import sys
import logging
from typing import Tuple, List, Optional, Union

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False

logger = logging.getLogger("JARVIS.Vision.CoordinateMapper")


class CoordinateMapper:
    """
    Precision coordinate translator and boundary safety guard.
    Converts model bounding boxes and normalized points into executable screen pixels.
    """

    def __init__(self, screen_width: Optional[int] = None, screen_height: Optional[int] = None) -> None:
        if screen_width is not None and screen_height is not None:
            self._width = screen_width
            self._height = screen_height
        else:
            self._width, self._height = self._detect_screen_size()

    def _detect_screen_size(self) -> Tuple[int, int]:
        """Detects current screen resolution with multi-source fallback."""
        if PYAUTOGUI_AVAILABLE and os.getenv("JARVIS_TEST_MODE", "0") != "1":
            try:
                sz = pyautogui.size()
                return int(sz[0]), int(sz[1])
            except Exception as e:
                logger.debug("pyautogui.size() failed: %s", e)

        if sys.platform == "win32" and os.getenv("JARVIS_TEST_MODE", "0") != "1":
            try:
                import ctypes
                user32 = ctypes.windll.user32
                # Enable DPI awareness to get physical pixels
                try:
                    user32.SetProcessDPIAware()
                except Exception:
                    pass
                w = user32.GetSystemMetrics(0)
                h = user32.GetSystemMetrics(1)
                if w > 0 and h > 0:
                    return w, h
            except Exception as e:
                logger.debug("Win32 GetSystemMetrics failed: %s", e)

        # Standard Full HD baseline fallback
        return 1920, 1080

    @property
    def screen_size(self) -> Tuple[int, int]:
        return self._width, self._height

    def normalize_to_pixel(
        self,
        norm_x: Union[int, float],
        norm_y: Union[int, float],
        scale_max: float = 1000.0,
    ) -> Tuple[int, int]:
        """
        Converts normalized coordinates (e.g. 0..1000 or 0.0..1.0) to screen pixel coordinates.
        Clamps results within safe screen boundaries.
        """
        # Automatically detect 0.0 - 1.0 vs 0 - 1000 scale
        if scale_max == 1000.0 and norm_x <= 1.0 and norm_y <= 1.0 and (norm_x > 0 or norm_y > 0):
            scale_max = 1.0

        px = int((norm_x / scale_max) * self._width)
        py = int((norm_y / scale_max) * self._height)

        # Clamp to screen boundary with a 2-pixel margin to avoid triggering corner fail-safes (0,0)
        px_clamped = max(2, min(self._width - 2, px))
        py_clamped = max(2, min(self._height - 2, py))

        return px_clamped, py_clamped

    def box_to_center_pixel(
        self,
        box_2d: List[Union[int, float]],
        scale_max: float = 1000.0,
    ) -> Tuple[int, int]:
        """
        Calculates center point from a bounding box [ymin, xmin, ymax, xmax].
        Returns (pixel_x, pixel_y).
        """
        if len(box_2d) < 4:
            raise ValueError(f"box_2d must contain 4 elements [ymin, xmin, ymax, xmax], got: {box_2d}")

        ymin, xmin, ymax, xmax = box_2d[:4]
        center_x = (xmin + xmax) / 2.0
        center_y = (ymin + ymax) / 2.0

        return self.normalize_to_pixel(center_x, center_y, scale_max=scale_max)

    def is_within_bounds(self, x: int, y: int) -> bool:
        """Verifies if (x, y) coordinates reside within the physical screen borders."""
        return 0 <= x < self._width and 0 <= y < self._height
