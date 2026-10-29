"""
System Tray Interface using pystray.
Windows vazifalar panelida qulay grafik boshqaruv menyusi.
"""

import os
import subprocess
from typing import Optional
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem as item, Menu

from core.controller import BrightnessController
from core.sync_daemon import BrightnessSyncDaemon
from core.config import ConfigManager


def create_tray_icon_image() -> Image.Image:
    """Tizim patnisi uchun chiroyli quyoshcha/yorug'lik piktogrammasi yaratadi."""
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    center = size / 2.0
    r_core = size * 0.22

    # Asosiy doira
    draw.ellipse(
        (center - r_core, center - r_core, center + r_core, center + r_core),
        fill=(255, 205, 30, 255),
        outline=(255, 140, 0, 255),
        width=3,
    )

    # Nurlar
    import math

    r_in = size * 0.30
    r_out = size * 0.45
    for i in range(8):
        ang = i * (math.pi / 4.0)
        x1 = center + r_in * math.cos(ang)
        y1 = center + r_in * math.sin(ang)
        x2 = center + r_out * math.cos(ang)
        y2 = center + r_out * math.sin(ang)
        draw.line((x1, y1, x2, y2), fill=(255, 185, 0, 255), width=3)

    return img


class BrightnessTrayApp:
    """Tizim patnisida (Tray) ishlovchi yengil grafik interfeys."""

    def __init__(
        self,
        controller: BrightnessController,
        daemon: BrightnessSyncDaemon,
        config: ConfigManager,
        icon_path: Optional[str] = None,
    ):
        self.controller = controller
        self.daemon = daemon
        self.config = config

        # Piktogramma
        if icon_path and os.path.exists(icon_path):
            try:
                self.icon_image = Image.open(icon_path)
            except Exception:
                self.icon_image = create_tray_icon_image()
        else:
            self.icon_image = create_tray_icon_image()

        self.tray_icon: Optional[pystray.Icon] = None

    def _get_status_text(self) -> str:
        status = self.controller.get_status()
        lap = status.get("laptop_brightness", "?")
        ext_list = status.get("external_monitors", [])
        ext_str = f"{ext_list[0]['current']}%" if ext_list else "Aniqlanmadi"
        return f"Noutbuk: {lap}% | Tashqi: {ext_str}"

    def _on_sync_now(self, icon, item):
        self.daemon.sync_once()
        self._update_title()

    def _on_toggle_sync(self, icon, item):
        cur = bool(self.config.get("sync_enabled", True))
        self.config.set("sync_enabled", not cur)
        self.daemon.enabled = not cur
        self._update_title()

    def _is_sync_enabled(self, item) -> bool:
        return bool(self.config.get("sync_enabled", True))

    def _on_day_mode(self, icon, item):
        self.controller.set_all_brightness(80)
        self._update_title()

    def _on_night_mode(self, icon, item):
        self.controller.set_all_brightness(25)
        self._update_title()

    def _on_open_config(self, icon, item):
        try:
            subprocess.Popen(["notepad.exe", self.config.config_path])
        except Exception:
            pass

    def _on_exit(self, icon, item):
        self.stop()

    def _update_title(self):
        if self.tray_icon:
            self.tray_icon.title = f"Yorug'lik: {self._get_status_text()}"

    def _build_menu(self) -> Menu:
        return Menu(
            item(lambda text: self._get_status_text(), None, enabled=False),
            Menu.SEPARATOR,
            item(
                "Avtomatik sinxronlash",
                self._on_toggle_sync,
                checked=self._is_sync_enabled,
            ),
            item("Hozir sinxronlash", self._on_sync_now, default=True),
            Menu.SEPARATOR,
            item("Kunduzgi rejim (80%)", self._on_day_mode),
            item("Tungi rejim (25%)", self._on_night_mode),
            Menu.SEPARATOR,
            item("Sozlamalarni ochish (config.json)", self._on_open_config),
            item("Chiqish", self._on_exit),
        )

    def run(self):
        """Tray interfeysini ishga tushiradi."""
        self.tray_icon = pystray.Icon(
            "brightness_sync",
            self.icon_image,
            f"Yorug'lik: {self._get_status_text()}",
            menu=self._build_menu(),
        )

        # Daemonni alohida fonda ishga tushirish
        self.daemon.start(non_blocking=True)

        # Tray ikonasini ishga tushirish (bloklovchi tsikl)
        self.tray_icon.run()

    def stop(self):
        """Xizmatni to'xtatish."""
        self.daemon.stop()
        if self.tray_icon:
            self.tray_icon.stop()
