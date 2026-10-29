"""
JARVIS-Core — Screen Capture Engine (Vision Subsystem)
High-precision, mandatory DPI-aware screen capture utility for Windows 10 & 11.
Supports full desktop, active screen, custom regions, and direct byte serialization for LLMs.
"""

from __future__ import annotations
import io
import os
import sys
import base64
import logging
import datetime
from pathlib import Path
from typing import Optional, Tuple, Union

try:
    from PIL import Image, ImageGrab
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False
    Image = None

logger = logging.getLogger("JARVIS.Vision.ScreenCapture")


class ScreenCapture:
    """
    High-fidelity screen perception hardware interface.
    Mandatory DPI awareness ensures pixel coordinates match physical display on Windows 10/11.
    """

    def __init__(self, output_dir: Optional[Union[str, Path]] = None) -> None:
        workspace_root = Path(__file__).resolve().parent.parent
        self.output_dir = Path(output_dir or (workspace_root / "screenshots"))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.test_mode = os.getenv("JARVIS_TEST_MODE", "0") == "1"
        self._ensure_mandatory_dpi_awareness()

    def _ensure_mandatory_dpi_awareness(self) -> None:
        """
        Enforces process DPI awareness on Windows 10/11.
        Prevents OS scaling offsets (125%, 150%) from displacing mouse click targets.
        """
        if sys.platform == "win32" and not self.test_mode:
            try:
                import ctypes
                # PROCESS_PER_MONITOR_DPI_AWARE = 2
                try:
                    ctypes.windll.shcore.SetProcessDpiAwareness(2)
                except Exception:
                    ctypes.windll.user32.SetProcessDPIAware()
            except Exception as e:
                logger.debug("Mandatory DPI awareness adjustment: %s", e)

    def capture_image(
        self,
        bbox: Optional[Tuple[int, int, int, int]] = None,
        all_screens: bool = True,
    ) -> Optional["Image.Image"]:
        """
        Captures the screen as a PIL Image object.
        bbox: (left, top, right, bottom) pixel coordinates.
        all_screens: If True, captures virtual desktop across all monitors.
        """
        if self.test_mode:
            if PILLOW_AVAILABLE:
                return Image.new("RGB", (1920, 1080), color=(30, 30, 30))
            return None

        if not PILLOW_AVAILABLE:
            logger.error("Pillow kutubxonasi mavjud emas, skrinshot olib bo'lmaydi.")
            return None

        try:
            img = ImageGrab.grab(bbox=bbox, all_screens=all_screens)
            return img
        except Exception as e:
            logger.error("Skrinshot olishda xatolik: %s", e)
            return None

    def save_screenshot(
        self,
        filename: Optional[str] = None,
        bbox: Optional[Tuple[int, int, int, int]] = None,
    ) -> Optional[str]:
        """
        Captures screen and writes it to a file.
        Returns the absolute filepath of the saved image.
        """
        img = self.capture_image(bbox=bbox)
        if img is None:
            return None

        if not filename:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"jarvis_vision_{timestamp}.png"

        filepath = self.output_dir / filename
        try:
            img.save(str(filepath), format="PNG")
            logger.info("Skrinshot muvaffaqiyatli saqlandi: %s", filepath)
            return str(filepath.resolve())
        except Exception as e:
            logger.error("Skrinshotni saqlashda xatolik: %s", e)
            return None

    def capture_bytes(
        self,
        bbox: Optional[Tuple[int, int, int, int]] = None,
        format: str = "PNG",
        max_dimension: Optional[int] = 1920,
    ) -> Optional[bytes]:
        """
        Captures screen and returns in-memory bytes.
        Resizes proportionally if larger than max_dimension to preserve token limits and speed.
        """
        img = self.capture_image(bbox=bbox)
        if img is None:
            return None

        try:
            if max_dimension and (img.width > max_dimension or img.height > max_dimension):
                img.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)

            buffer = io.BytesIO()
            img.save(buffer, format=format)
            return buffer.getvalue()
        except Exception as e:
            logger.error("Rasmni baytlarga o'tkazishda xatolik: %s", e)
            return None

    def capture_base64(
        self,
        bbox: Optional[Tuple[int, int, int, int]] = None,
        format: str = "JPEG",
    ) -> Optional[str]:
        """Captures screen and encodes it as base64 string."""
        raw_bytes = self.capture_bytes(bbox=bbox, format=format)
        if raw_bytes is None:
            return None
        return base64.b64encode(raw_bytes).decode("utf-8")
