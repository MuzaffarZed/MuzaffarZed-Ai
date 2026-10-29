"""
O'zbek Musiqa Markazi Pro - Zamonaviy Grafik Interfeys (CustomTkinter GUI)
Muallif: Premier Software Architect (janob Muzaffar uchun maxsus ishlab chiqilgan)
Versiya: 9.0 Omni-Studio Masterpiece Edition
(Windows AIMP 5 & IDM • Android Poweramp & CapCut • Apple Music • Linux FFmpeg Sintezi)

Asosiy Arxitektura va Imkoniyatlar (v9.0 Omni-Studio):
1. 🎨 5-Skin Dinamik Tema Tizimi: AIMP Onyx, Cyber Emerald, Midnight Gold, Crimson Sport va Kunduzgi Kristal.
2. 🔍 Global Qidiruv + 📋 Smart Clipboard Link Monitor + Interaktiv Tanlab Yuklash Jadvali.
3. 👤 50+ San'atkorlar (6 Kategoriya + Qidiruv + Yangi Qo'shish) va 🎼 16+ Musiqa Uslublari & Janrlar.
4. 🔢 Erkin Yuklash Soni (1..200) va 🎚️ Bitrate Sifat Tanlagich (320k / 256k / 192k / 128k).
5. 🎧 AIMP Kutubxona & Omni-Studio:
   - 🌐 Barcha Papkalar | ❤️ Sevimlilar | 🕒 Tarix | 📁 Joriy Papka filtrlari
   - 🔀 Saralash (Nomi, Yangiligi, Davomiyligi, Hajmi) + 📲 1-Bosishda Sevimlilarni Fleshkaga Yozish
   - 🎚️ 10-Polosali Ekvayzer + 🎛️ Studio Audio FX (Slowed+Reverb, 8D Audio, Nightcore, Speed, Vocal Cut)
   - 🏷️ ID3v2 Pasport + 🖼️ MP3 Muqova Rasmini Almashtirish
6. 🎛️ AIMP Master Deck:
   - 80-Bar Waveform Seekbar + 🔁 Real-Time A-B Loop ([A .. B]) + ✂️ Audio Kesish (Trimmer)
   - ❤️ 1-Click Favorite + 💤 Uyqu Taymeri (Sleep Timer) + ⌨️ Klaviatura Qaynoq Tugmalari (Space, Left/Right, Up/Down, M, F, Ctrl+F).
"""

import io
import os
import re
import sys
import time
import math
import random
import queue
import shutil
import threading
import concurrent.futures
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk

try:
    from PIL import Image
    _PIL_AVAILABLE = True
except ImportError:
    _PIL_AVAILABLE = False

try:
    import speech_recognition as sr
    _SR_AVAILABLE = True
except ImportError:
    _SR_AVAILABLE = False

import music_engine

# CustomTkinter boshlang'ich sozlamalari
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def format_mm_ss(seconds: float) -> str:
    """Soniyani MM:SS formatiga o'tkazish."""
    s = max(0, int(seconds))
    return f"{s // 60:02d}:{s % 60:02d}"


# =========================================================================
# 5-SKIN DINAMIK TEMA VA RANG PALITRASI TIZIMI
# =========================================================================

THEME_SKINS = {
    "🌑 AIMP Onyx": {
        "mode": "dark",
        "bg_main": "#0b0f19",
        "bg_header": "#090d16",
        "bg_panel": "#131b2e",
        "bg_card": "#1e293b",
        "bg_deck": "#0a0e17",
        "bg_canvas": "#070a12",
        "accent": "#38bdf8",
        "accent_btn": "#0284c7",
        "accent_hover": "#0369a1",
        "secondary": "#10b981",
        "text_main": "#f8fafc",
        "text_sub": "#94a3b8",
        "border": "#334155",
    },
    "💚 Cyber Emerald": {
        "mode": "dark",
        "bg_main": "#06130e",
        "bg_header": "#040d0a",
        "bg_panel": "#0c2219",
        "bg_card": "#133326",
        "bg_deck": "#05100c",
        "bg_canvas": "#040b08",
        "accent": "#10b981",
        "accent_btn": "#059669",
        "accent_hover": "#047857",
        "secondary": "#fbbf24",
        "text_main": "#ecfdf5",
        "text_sub": "#6ee7b7",
        "border": "#065f46",
    },
    "🏆 Midnight Gold": {
        "mode": "dark",
        "bg_main": "#120f08",
        "bg_header": "#0d0a05",
        "bg_panel": "#1f190d",
        "bg_card": "#2e2514",
        "bg_deck": "#0f0c06",
        "bg_canvas": "#0a0804",
        "accent": "#fbbf24",
        "accent_btn": "#d97706",
        "accent_hover": "#b45309",
        "secondary": "#38bdf8",
        "text_main": "#fef3c7",
        "text_sub": "#fcd34d",
        "border": "#78350f",
    },
    "🍷 Crimson Sport": {
        "mode": "dark",
        "bg_main": "#14080c",
        "bg_header": "#0f0508",
        "bg_panel": "#240e15",
        "bg_card": "#361520",
        "bg_deck": "#110609",
        "bg_canvas": "#0c0406",
        "accent": "#fb7185",
        "accent_btn": "#e11d48",
        "accent_hover": "#be123c",
        "secondary": "#fbbf24",
        "text_main": "#ffe4e6",
        "text_sub": "#fda4af",
        "border": "#881337",
    },
    "☀️ Kunduzgi Kristal": {
        "mode": "light",
        "bg_main": "#e2e8f0",
        "bg_header": "#cbd5e1",
        "bg_panel": "#f8fafc",
        "bg_card": "#ffffff",
        "bg_deck": "#cbd5e1",
        "bg_canvas": "#0f172a",
        "accent": "#0284c7",
        "accent_btn": "#0284c7",
        "accent_hover": "#0369a1",
        "secondary": "#059669",
        "text_main": "#0f172a",
        "text_sub": "#475569",
        "border": "#94a3b8",
    },
}

TXT_PRIMARY = ("#0f172a", "#f8fafc")
TXT_SECONDARY = ("#475569", "#94a3b8")
TXT_MUTED = ("#64748b", "#64748b")
TXT_ACCENT_BLUE = ("#0369a1", "#38bdf8")
TXT_ACCENT_GREEN = ("#047857", "#10b981")
TXT_ACCENT_GOLD = ("#b45309", "#f59e0b")

BG_PANEL_TUPLE = ("#f8fafc", "#131b2e")
BG_CARD_TUPLE = ("#ffffff", "#1e293b")
BG_ROW_TUPLE = ("#e2e8f0", "#162032")
BG_ACTIVE_ROW_TUPLE = ("#d1fae5", "#064e3b")


# =========================================================================
# 1. AIMP 3-REJIMLI VIZUALIZATOR: DUAL L/R VU-METER • PEAK SPEKTR • OSSILLOSKOP
# =========================================================================

class VisualizerWidget(ctk.CTkFrame):
    """
    AIMP klassik 3-in-1 vizualizatori:
    - Rejim 1 ('VU'): AIMP Dual L/R Stereo Analog VU-Meter (Ikki kanalli ignali strelka)
    - Rejim 2 ('EQ'): AIMP 20-Band Peak-Hold Spektr Ekvayzer (Cho'qqi ushlagichli LED ustunlar)
    - Rejim 3 ('OSC'): AIMP Stereo Waveform Ossilloskop (Jonli sinusoida to'lqini)
    """

    def __init__(self, master, width=235, height=84, **kwargs):
        super().__init__(master, width=width, height=height, corner_radius=8, fg_color=("#1e293b", "#070a12"), **kwargs)
        self.width = width
        self.height = height
        self.mode = "VU"  # 'VU' -> 'EQ' -> 'OSC'
        self.bg_hex = "#070a12"

        self.canvas = tk.Canvas(
            self,
            width=self.width,
            height=self.height,
            bg=self.bg_hex,
            highlightthickness=0,
            cursor="hand2"
        )
        self.canvas.pack(fill="both", expand=True, padx=2, pady=2)
        self.canvas.bind("<Button-1>", lambda e: self.toggle_mode())

        self.val_l = 0.12
        self.val_r = 0.12
        self.eq_bars = [0.08] * 20
        self.peak_caps = [0.10] * 20
        self.osc_phase = 0.0
        self.is_active = False

        self._render_canvas()

    def set_canvas_bg(self, bg_hex: str):
        self.bg_hex = bg_hex
        self.canvas.configure(bg=bg_hex)
        self._render_canvas()

    def toggle_mode(self):
        modes = ["VU", "EQ", "OSC"]
        idx = (modes.index(self.mode) + 1) % len(modes) if self.mode in modes else 0
        self.mode = modes[idx]
        self._render_canvas()

    def update_activity(self, is_playing: bool):
        self.is_active = is_playing
        if is_playing:
            target_l = random.uniform(0.32, 0.94)
            target_r = max(0.25, min(0.96, target_l + random.uniform(-0.14, 0.14)))
            self.val_l += (target_l - self.val_l) * 0.42
            self.val_r += (target_r - self.val_r) * 0.42

            for i in range(len(self.eq_bars)):
                weight = 1.0 - (abs(i - 6) / 24.0)
                new_v = random.uniform(0.18, 0.96) * max(0.55, weight)
                self.eq_bars[i] = new_v
                if new_v >= self.peak_caps[i]:
                    self.peak_caps[i] = min(0.98, new_v + 0.03)
                else:
                    self.peak_caps[i] = max(0.08, self.peak_caps[i] - 0.045)

            self.osc_phase = (self.osc_phase + 0.45) % (2 * math.pi)
        else:
            self.val_l = max(0.05, self.val_l * 0.75)
            self.val_r = max(0.05, self.val_r * 0.75)
            self.eq_bars = [max(0.05, b * 0.75) for b in self.eq_bars]
            self.peak_caps = [max(0.06, p * 0.85) for p in self.peak_caps]

        self._render_canvas()

    def _render_canvas(self):
        self.canvas.delete("all")
        if self.mode == "VU":
            self._draw_dual_vu_meter()
        elif self.mode == "EQ":
            self._draw_peak_spectrum()
        else:
            self._draw_oscilloscope()

    def _draw_dual_vu_meter(self):
        w = self.width
        h = self.height

        self.canvas.create_rectangle(3, 3, w - 3, h - 3, fill="#0d1322", outline="#1e293b", width=1)
        self.canvas.create_text(w // 2, 11, text="AIMP STEREO VU-METER (L / R)", fill="#f59e0b", font=("Consolas", 8, "bold"))

        dial_w = (w - 16) // 2
        for ch_idx, (ch_name, val) in enumerate([("L", self.val_l), ("R", self.val_r)]):
            x0 = 6 + ch_idx * (dial_w + 4)
            cx = x0 + dial_w // 2
            cy = h - 10
            r = min(dial_w * 0.48, h * 0.62)

            self.canvas.create_rectangle(x0, 20, x0 + dial_w, h - 13, fill="#131c31", outline="#1e293b")
            self.canvas.create_arc(cx - r, cy - r, cx + r, cy + r, start=50, extent=80, style="arc", outline="#38bdf8", width=2)
            self.canvas.create_arc(cx - r, cy - r, cx + r, cy + r, start=30, extent=20, style="arc", outline="#ef4444", width=2)

            led_col = "#ef4444" if val > 0.82 else "#1e293b"
            self.canvas.create_oval(x0 + dial_w - 11, 23, x0 + dial_w - 5, 29, fill=led_col, outline="")
            self.canvas.create_text(x0 + 10, 26, text=ch_name, fill="#94a3b8", font=("Consolas", 7, "bold"))

            angle_deg = 130.0 - (val * 80.0)
            rad = math.radians(angle_deg)
            nx = cx + (r * 0.92) * math.cos(rad)
            ny = cy - (r * 0.92) * math.sin(rad)

            needle_col = "#ef4444" if val > 0.82 else "#fbbf24"
            self.canvas.create_line(cx, cy, nx, ny, fill=needle_col, width=2)
            self.canvas.create_oval(cx - 4, cy - 4, cx + 4, cy + 4, fill="#475569", outline="#94a3b8")

        self.canvas.create_text(w // 2, h - 6, text="[Bosilsa: VU ➔ Spektr ➔ Ossilloskop]", fill="#64748b", font=("Segoe UI", 7))

    def _draw_peak_spectrum(self):
        w = self.width
        h = self.height

        self.canvas.create_rectangle(3, 3, w - 3, h - 3, fill="#080c16", outline="#1e293b", width=1)
        self.canvas.create_text(w // 2, 11, text="AIMP PEAK SPECTRUM (20-BAND)", fill="#38bdf8", font=("Consolas", 8, "bold"))

        num_bars = len(self.eq_bars)
        pad = 2
        bar_w = (w - 18 - (num_bars * pad)) / num_bars
        max_h = h - 30
        base_y = h - 13

        for i, val in enumerate(self.eq_bars):
            bx = 9 + i * (bar_w + pad)
            bh = val * max_h
            by1 = base_y - bh

            color = "#ef4444" if val > 0.82 else ("#f59e0b" if val > 0.55 else "#10b981")
            self.canvas.create_rectangle(bx, by1, bx + bar_w, base_y, fill=color, outline="")

            cap_y = base_y - (self.peak_caps[i] * max_h)
            self.canvas.create_line(bx, cap_y, bx + bar_w, cap_y, fill="#f8fafc", width=2)

        self.canvas.create_text(w // 2, h - 6, text="[Bosilsa: VU ➔ Spektr ➔ Ossilloskop]", fill="#64748b", font=("Segoe UI", 7))

    def _draw_oscilloscope(self):
        w = self.width
        h = self.height

        self.canvas.create_rectangle(3, 3, w - 3, h - 3, fill="#070b14", outline="#1e293b", width=1)
        self.canvas.create_text(w // 2, 11, text="AIMP STEREO OSCILLOSCOPE", fill="#10b981", font=("Consolas", 8, "bold"))

        mid_y = h // 2 + 2
        self.canvas.create_line(8, mid_y, w - 8, mid_y, fill="#1e293b", dash=(2, 2))

        pts = []
        amp = (self.val_l + self.val_r) * 14.0 if self.is_active else 2.0
        for x in range(8, w - 8, 3):
            t = (x / 18.0) + self.osc_phase
            y = mid_y + math.sin(t) * amp * math.cos(t * 0.35)
            pts.extend([x, y])

        if len(pts) >= 4:
            self.canvas.create_line(*pts, fill="#10b981", width=2, smooth=True)

        self.canvas.create_text(w // 2, h - 6, text="[Bosilsa: VU ➔ Spektr ➔ Ossilloskop]", fill="#64748b", font=("Segoe UI", 7))


# =========================================================================
# 2. AIMP WAVEFORM SEEKBAR (A-B LOOP VA KESISH CHEGARALARI BILAN)
# =========================================================================

class AIMPWaveformSeekbar(ctk.CTkFrame):
    """
    AIMP uslubidagi 80-ustunli interaktiv audio to'lqin shkalasi (Waveform Scrubbing) +
    Visual [A .. B] Loop va Kesish (Trim) hududi ko'rsatkichi.
    """

    def __init__(self, master, on_seek_cb=None, height=30, **kwargs):
        super().__init__(master, height=height, corner_radius=6, fg_color=("#0f172a", "#070a12"), **kwargs)
        self.on_seek_cb = on_seek_cb
        self.waveform = [0.35 + 0.25 * math.sin(i * 0.3) for i in range(80)]
        self.progress = 0.0
        self.duration_sec = 210.0
        self.loop_a_sec = None
        self.loop_b_sec = None
        self.mode = "STUDIO"
        self.hover_ratio = None

        self.canvas = tk.Canvas(
            self,
            height=height,
            bg="#070a12",
            highlightthickness=0,
            cursor="hand2"
        )
        self.canvas.pack(fill="both", expand=True, padx=4, pady=2)

        self.canvas.bind("<Configure>", lambda e: self._render_waveform())
        self.canvas.bind("<Button-1>", self._on_click_or_drag)
        self.canvas.bind("<B1-Motion>", self._on_click_or_drag)
        self.canvas.bind("<Motion>", self._on_hover)
        self.canvas.bind("<Leave>", self._on_leave)

    def set_waveform(self, waveform_list, duration_sec: float):
        if waveform_list:
            self.waveform = list(waveform_list)
        self.duration_sec = max(1.0, float(duration_sec or 210.0))
        self._render_waveform()

    def set_loop_markers(self, loop_a_sec, loop_b_sec):
        self.loop_a_sec = loop_a_sec
        self.loop_b_sec = loop_b_sec
        self._render_waveform()

    def set_progress(self, pos_sec: float, duration_sec: float, mode: str = "STUDIO", loop_a_sec=None, loop_b_sec=None):
        self.duration_sec = max(1.0, float(duration_sec or 210.0))
        self.progress = max(0.0, min(1.0, float(pos_sec) / self.duration_sec))
        self.mode = mode
        self.loop_a_sec = loop_a_sec
        self.loop_b_sec = loop_b_sec
        self._render_waveform()

    def _on_click_or_drag(self, event):
        w = max(1, self.canvas.winfo_width())
        ratio = max(0.0, min(1.0, event.x / w))
        self.progress = ratio
        self._render_waveform()
        if self.on_seek_cb:
            self.on_seek_cb(ratio * self.duration_sec)

    def _on_hover(self, event):
        w = max(1, self.canvas.winfo_width())
        self.hover_ratio = max(0.0, min(1.0, event.x / w))
        self._render_waveform()

    def _on_leave(self, _event):
        self.hover_ratio = None
        self._render_waveform()

    def _render_waveform(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 20 or h < 10:
            return

        n = len(self.waveform)
        pad = 2
        bar_w = max(2.0, (w - (n * pad)) / n)
        mid_y = h / 2.0

        active_color = "#10b981" if self.mode == "STUDIO" else "#ef4444"
        played_idx = int(self.progress * n)

        a_idx = int((self.loop_a_sec / self.duration_sec) * n) if self.loop_a_sec is not None else None
        b_idx = int((self.loop_b_sec / self.duration_sec) * n) if self.loop_b_sec is not None else None

        for i, amp in enumerate(self.waveform):
            bx = i * (bar_w + pad)
            half_h = max(2.0, amp * (h * 0.44))
            if a_idx is not None and b_idx is not None and a_idx <= i <= b_idx:
                col = "#38bdf8"  # A-B Loop hududi firuza rangda ajralib turadi!
            else:
                col = active_color if i <= played_idx else "#26334d"
            self.canvas.create_rectangle(bx, mid_y - half_h, bx + bar_w, mid_y + half_h, fill=col, outline="")

        # [A va B] chiziqlari
        if self.loop_a_sec is not None:
            ax = (self.loop_a_sec / self.duration_sec) * w
            self.canvas.create_line(ax, 0, ax, h, fill="#38bdf8", width=2)
            self.canvas.create_text(min(w - 10, ax + 8), 7, text="A", fill="#38bdf8", font=("Consolas", 8, "bold"))

        if self.loop_b_sec is not None:
            bx_pos = (self.loop_b_sec / self.duration_sec) * w
            self.canvas.create_line(bx_pos, 0, bx_pos, h, fill="#38bdf8", width=2)
            self.canvas.create_text(max(10, bx_pos - 8), 7, text="B", fill="#38bdf8", font=("Consolas", 8, "bold"))

        px = self.progress * w
        self.canvas.create_line(px, 0, px, h, fill="#f59e0b", width=2)

        if self.hover_ratio is not None:
            hx = self.hover_ratio * w
            target_time = format_mm_ss(self.hover_ratio * self.duration_sec)
            self.canvas.create_line(hx, 0, hx, h, fill="#f8fafc", width=1, dash=(2, 2))
            tx = min(w - 28, max(28, hx))
            self.canvas.create_rectangle(tx - 20, 1, tx + 20, 13, fill="#0284c7", outline="")
            self.canvas.create_text(tx, 7, text=target_time, fill="#ffffff", font=("Consolas", 8, "bold"))


# =========================================================================
# ASOSIY ILOVA (MusicCenterApp - Versiya 9.0 Omni-Studio Masterpiece)
# =========================================================================

class MusicCenterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Oyna xususiyatlari
        self.title("O'zbek Musiqa Markazi Pro • AIMP Omni-Studio & IDM 32x (Versiya 9.0)")
        self.normal_geometry = "1200x860"
        self.geometry(self.normal_geometry)
        self.minsize(1050, 760)

        # Holat o'zgaruvchilari
        self.player = music_engine.AudiophilePlayer()
        self.current_skin_name = "🌑 AIMP Onyx"
        self.is_downloading = False
        self.cancel_requested = False
        self.is_searching_preview = False
        self.log_queue = queue.Queue()
        self.current_usb_drives = []
        self.custom_base_dir = ""
        self.queue_items_widgets = {}
        self.aimp_playlist_rows = {}
        self.search_preview_items = []
        self.selected_artist_category = "Barchasi"
        self.is_mini_dock = False
        self.toast_dismissed = False
        self.selected_tag_file = None
        self.selected_cover_image_path = None
        self.eq_sliders = []
        self.themed_cards = []
        self.last_clipboard_text = ""
        self.sleep_timer_end_ts = None
        self.sleep_timer_mode = "O'chiq"

        # UI elementlarini qurish
        self._build_header()
        self._build_toast_banner()
        self._build_usb_cockpit_panel()
        self._build_main_tabs()
        self._build_audiophile_player_panel()
        self._bind_global_hotkeys()

        # Dastlabki tekshiruvlar va skanerlash
        self.apply_skin(self.current_skin_name)
        self._refresh_drives()
        self._refresh_aimp_playlist()

        # Davriy taymerlar
        self.after(100, self._process_log_queue)
        self.after(80, self._visualizer_loop)
        self.after(200, self._player_sync_loop)
        self.after(1500, self._clipboard_monitor_loop)

    # =========================================================================
    # KLAVIATURA QAYNOQ TUGMALARI (HOTKEYS: SPACE, LEFT/RIGHT, UP/DOWN, M, F, CTRL+F)
    # =========================================================================

    def _bind_global_hotkeys(self):
        self.bind("<space>", self._on_hotkey_space)
        self.bind("<Left>", lambda e: self._on_hotkey_seek(e, -5.0))
        self.bind("<Right>", lambda e: self._on_hotkey_seek(e, 5.0))
        self.bind("<Up>", lambda e: self._on_hotkey_volume(e, 0.05))
        self.bind("<Down>", lambda e: self._on_hotkey_volume(e, -0.05))
        self.bind("<KeyPress-m>", self._on_hotkey_mute)
        self.bind("<KeyPress-M>", self._on_hotkey_mute)
        self.bind("<KeyPress-f>", self._on_hotkey_favorite)
        self.bind("<KeyPress-F>", self._on_hotkey_favorite)
        self.bind("<Control-f>", self._on_hotkey_focus_search)
        self.bind("<Control-F>", self._on_hotkey_focus_search)

    def _is_typing_in_input(self, event) -> bool:
        w = event.widget
        if not w:
            return False
        cls_name = str(w.winfo_class()).lower()
        return "entry" in cls_name or "text" in cls_name

    def _on_hotkey_space(self, event):
        if not self._is_typing_in_input(event):
            self._toggle_playback()

    def _on_hotkey_seek(self, event, delta: float):
        if not self._is_typing_in_input(event):
            self._step_seek_action(delta)

    def _on_hotkey_volume(self, event, delta: float):
        if not self._is_typing_in_input(event):
            new_v = max(0.0, min(1.0, self.player.volume + delta))
            self.vol_slider.set(new_v)
            self._on_volume_change(new_v)

    def _on_hotkey_mute(self, event):
        if not self._is_typing_in_input(event):
            self._toggle_mute_action()

    def _on_hotkey_favorite(self, event):
        if not self._is_typing_in_input(event):
            self._toggle_current_playing_favorite()

    def _on_hotkey_focus_search(self, _event):
        self.entry_global_search.focus_set()

    # =========================================================================
    # 1. YUQORI HEADER (GLOBAL QIDIRUV + AVTO-LINK + 5-SKIN TEMA + MINI-DOCK)
    # =========================================================================

    def _build_header(self):
        self.header_frame = ctk.CTkFrame(self, corner_radius=0, height=64, fg_color=("#cbd5e1", "#090d16"))
        self.header_frame.pack(side="top", fill="x", padx=0, pady=0)

        # Chap qism: Brend va Versiya
        title_box = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        title_box.pack(side="left", padx=(14, 8), pady=6)

        title_row = ctk.CTkFrame(title_box, fg_color="transparent")
        title_row.pack(anchor="w")

        self.lbl_app_title = ctk.CTkLabel(
            title_row,
            text="🎵 O'ZBEK MUSIQA MARKAZI PRO",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color=TXT_ACCENT_BLUE
        )
        self.lbl_app_title.pack(side="left")

        self.lbl_app_badge = ctk.CTkLabel(
            title_row,
            text=" v9.0 OMNI-STUDIO ",
            font=ctk.CTkFont(size=10, weight="bold"),
            fg_color="#059669",
            text_color="#ffffff",
            corner_radius=6
        )
        self.lbl_app_badge.pack(side="left", padx=6)

        self.lbl_app_subtitle = ctk.CTkLabel(
            title_box,
            text="AIMP Deck • Slowed+Reverb & 8D FX • A-B Trimmer • IDM 32-Oqim • Qaynoq Tugmalar (Space, ⬅️/➡️, F)",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color=TXT_SECONDARY
        )
        self.lbl_app_subtitle.pack(anchor="w")

        # O'rta qism: GLOBAL TEZKOR QIDIRUV SATRI
        quick_search_box = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        quick_search_box.pack(side="left", fill="x", expand=True, padx=8, pady=10)

        self.entry_global_search = ctk.CTkEntry(
            quick_search_box,
            placeholder_text="🔍 Istalgan qo'shiq, san'atkor yoki YouTube linkni yozing (Enter / Ctrl+F)...",
            height=34,
            font=ctk.CTkFont(size=12),
            text_color=TXT_PRIMARY
        )
        self.entry_global_search.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.entry_global_search.bind("<Return>", lambda _e: self._on_global_quick_search())

        self.btn_global_search = ctk.CTkButton(
            quick_search_box,
            text="🔍 Topish",
            width=82,
            height=34,
            fg_color="#0284c7",
            hover_color="#0369a1",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._on_global_quick_search
        )
        self.btn_global_search.pack(side="left", padx=(0, 6))

        self.chk_clipboard_monitor = ctk.CTkCheckBox(
            quick_search_box,
            text="📋 Link-Avto",
            width=85,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=TXT_PRIMARY,
            onvalue=True,
            offvalue=False
        )
        self.chk_clipboard_monitor.select()
        self.chk_clipboard_monitor.pack(side="left")

        # O'ng tarafdagi boshqaruv (5-Skin Tema Tanlagich + Mini-Dock)
        right_box = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        right_box.pack(side="right", padx=(4, 14), pady=8)

        ctk.CTkLabel(
            right_box,
            text="🎨 Tema:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=TXT_PRIMARY
        ).pack(side="left", padx=(0, 4))

        skin_names = list(THEME_SKINS.keys())
        self.combo_skin = ctk.CTkComboBox(
            right_box,
            values=skin_names,
            width=150,
            height=28,
            state="readonly",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self.apply_skin
        )
        self.combo_skin.set(self.current_skin_name)
        self.combo_skin.pack(side="left", padx=(0, 8))

        self.btn_mini_dock = ctk.CTkButton(
            right_box,
            text="🪟 Mini-Dock",
            width=100,
            height=28,
            fg_color="#334155",
            hover_color="#475569",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self._toggle_mini_dock
        )
        self.btn_mini_dock.pack(side="left")

    def _clipboard_monitor_loop(self):
        """IDM / 1DM+ uslubidagi Smart Clipboard YouTube Link Sezgich."""
        try:
            if hasattr(self, "chk_clipboard_monitor") and self.chk_clipboard_monitor.get():
                clip = self.clipboard_get().strip()
                if clip and clip != self.last_clipboard_text:
                    self.last_clipboard_text = clip
                    if re.match(r"^https?://(www\.)?(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)", clip, re.I):
                        self.entry_global_search.delete(0, "end")
                        self.entry_global_search.insert(0, clip)
                        self.entry_search.delete(0, "end")
                        self.entry_search.insert(0, clip)
                        self.log(f"📋 YouTube link nusxalandi va qidiruvga olindi: {clip[:45]}...")
        except Exception:
            pass
        self.after(1500, self._clipboard_monitor_loop)

    def _on_global_quick_search(self):
        query = self.entry_global_search.get().strip()
        if not query:
            self.tabview.set("🔍 Qidiruv & Tanlab Yuklash")
            self.entry_search.focus_set()
            return
        self.entry_search.delete(0, "end")
        self.entry_search.insert(0, query)
        self.tabview.set("🔍 Qidiruv & Tanlab Yuklash")
        self._start_interactive_search_preview()

    def apply_skin(self, skin_name: str):
        """5 xil professional temadan birini butun dasturga jonli qo'llash."""
        if skin_name not in THEME_SKINS:
            skin_name = "🌑 AIMP Onyx"
        self.current_skin_name = skin_name
        skin = THEME_SKINS[skin_name]

        ctk.set_appearance_mode(skin["mode"])
        self.configure(fg_color=skin["bg_main"])

        if hasattr(self, "header_frame"):
            self.header_frame.configure(fg_color=skin["bg_header"])
        if hasattr(self, "lbl_app_title"):
            self.lbl_app_title.configure(text_color=skin["accent"])
        if hasattr(self, "lbl_app_badge"):
            self.lbl_app_badge.configure(fg_color=skin["accent_btn"])
        if hasattr(self, "cockpit_frame"):
            self.cockpit_frame.configure(fg_color=skin["bg_panel"], border_width=1, border_color=skin["border"])
        if hasattr(self, "player_frame"):
            self.player_frame.configure(fg_color=skin["bg_deck"], border_width=1, border_color=skin["border"])
        if hasattr(self, "tabview"):
            self.tabview.configure(
                fg_color=skin["bg_panel"],
                segmented_button_selected_color=skin["accent_btn"],
                segmented_button_selected_hover_color=skin["accent_hover"],
                text_color=skin["text_main"]
            )
        if hasattr(self, "visualizer"):
            self.visualizer.set_canvas_bg(skin["bg_canvas"])

        for frame_attr in ("aimp_left_pane", "aimp_eq_card", "aimp_fx_card", "aimp_tag_card", "search_top_card", "search_results_card"):
            w = getattr(self, frame_attr, None)
            if w and w.winfo_exists():
                w.configure(fg_color=skin["bg_card"], border_width=1, border_color=skin["border"])

        for card in list(self.themed_cards):
            if card and card.winfo_exists():
                card.configure(fg_color=skin["bg_card"], border_width=1, border_color=skin["border"])

    def _on_theme_change(self, val):
        if val in THEME_SKINS:
            self.apply_skin(val)
        elif str(val).lower() in ("yorug'", "light"):
            self.apply_skin("☀️ Kunduzgi Kristal")
        else:
            self.apply_skin("🌑 AIMP Onyx")

    # =========================================================================
    # 2. SMART TOAST BANNER
    # =========================================================================

    def _build_toast_banner(self):
        self.toast_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=("#047857", "#064e3b"), height=38)

        self.lbl_toast_text = ctk.CTkLabel(
            self.toast_frame,
            text="⚡ USB Fleshka aniqlandi! Bitta bosishda 2026-yilning TOP-25 ta xitlarini yozamizmi?",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#ecfdf5"
        )
        self.lbl_toast_text.pack(side="left", padx=(15, 10), pady=5)

        self.btn_toast_burn = ctk.CTkButton(
            self.toast_frame,
            text="🚀 1-Bosishda Fleshkaga Yozish",
            width=185,
            height=26,
            fg_color="#10b981",
            hover_color="#059669",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._quick_burn_action
        )
        self.btn_toast_burn.pack(side="left", padx=6, pady=5)

        btn_close_toast = ctk.CTkButton(
            self.toast_frame,
            text="✕",
            width=26,
            height=24,
            fg_color="transparent",
            hover_color="#047857",
            command=self._dismiss_toast
        )
        btn_close_toast.pack(side="right", padx=8)

    def _show_toast(self, drive_display: str):
        if not self.toast_dismissed and not self.is_mini_dock:
            self.lbl_toast_text.configure(
                text=f"⚡ Fleshka tayyor ({drive_display})! 1-Bosishda 2026 TOP-25 Xitlarini yozamizmi?"
            )
            self.toast_frame.pack(side="top", fill="x", padx=15, pady=(6, 0), before=self.cockpit_frame)

    def _dismiss_toast(self):
        self.toast_dismissed = True
        self.toast_frame.pack_forget()

    def _quick_burn_action(self):
        self.dest_mode_var.set("usb")
        col = music_engine.COLLECTIONS_2026[0]
        self._start_collection_turbo(col)

    # =========================================================================
    # 3. SAQLASH MANZILI, BITRATE SIFAT VA PAPKA ARXITEKTURASI PANELI
    # =========================================================================

    def _build_usb_cockpit_panel(self):
        self.cockpit_frame = ctk.CTkFrame(self, corner_radius=12, fg_color=BG_PANEL_TUPLE)
        self.cockpit_frame.pack(side="top", fill="x", padx=15, pady=(6, 4))

        # 1-QATOR: Xotira manbai (USB / Desktop / Maxsus) + Bitrate Sifat + Smart Sync
        top_row = ctk.CTkFrame(self.cockpit_frame, fg_color="transparent")
        top_row.pack(fill="x", padx=14, pady=(6, 2))

        cockpit_title = ctk.CTkLabel(
            top_row,
            text="💾 SAQLASH & SIFAT:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TXT_ACCENT_BLUE
        )
        cockpit_title.pack(side="left", padx=(0, 10))

        self.dest_mode_var = ctk.StringVar(value="desktop")

        self.rb_use_usb = ctk.CTkRadioButton(
            top_row,
            text="USB Fleshka",
            variable=self.dest_mode_var,
            value="usb",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TXT_PRIMARY,
            command=self._on_dest_mode_toggle
        )
        self.rb_use_usb.pack(side="left", padx=(0, 8))

        self.rb_use_desktop = ctk.CTkRadioButton(
            top_row,
            text="Ish stoli (Desktop)",
            variable=self.dest_mode_var,
            value="desktop",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TXT_PRIMARY,
            command=self._on_dest_mode_toggle
        )
        self.rb_use_desktop.pack(side="left", padx=(0, 8))

        self.rb_use_custom = ctk.CTkRadioButton(
            top_row,
            text="Maxsus Joy",
            variable=self.dest_mode_var,
            value="custom",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TXT_PRIMARY,
            command=self._on_dest_mode_toggle
        )
        self.rb_use_custom.pack(side="left", padx=(0, 6))

        self.btn_browse_base = ctk.CTkButton(
            top_row,
            text="📂 Tanlash",
            width=82,
            height=25,
            fg_color="#334155",
            hover_color="#475569",
            font=ctk.CTkFont(size=11),
            command=self._choose_custom_base_dir
        )
        self.btn_browse_base.pack(side="left", padx=(0, 8))

        self.usb_combo = ctk.CTkComboBox(
            top_row,
            values=["Fleshka aniqlanmadi"],
            width=195,
            height=25,
            state="readonly",
            font=ctk.CTkFont(size=11),
            command=self._on_usb_selected
        )
        self.usb_combo.pack(side="left", padx=(0, 4))

        self.btn_refresh_usb = ctk.CTkButton(
            top_row,
            text="🔄",
            width=32,
            height=25,
            fg_color="#334155",
            hover_color="#475569",
            command=self._refresh_drives
        )
        self.btn_refresh_usb.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            top_row,
            text="🎚️ Sifat:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=TXT_ACCENT_GOLD
        ).pack(side="left", padx=(0, 4))

        self.combo_bitrate = ctk.CTkComboBox(
            top_row,
            values=["320k", "256k", "192k", "128k"],
            width=76,
            height=25,
            state="normal",
            font=ctk.CTkFont(size=11, weight="bold")
        )
        self.combo_bitrate.set("256k")
        self.combo_bitrate.pack(side="left")

        self.chk_smart_sync = ctk.CTkCheckBox(
            top_row,
            text="⚡ Smart Sync (Takrorlamaslik)",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=TXT_PRIMARY,
            onvalue=True,
            offvalue=False
        )
        self.chk_smart_sync.select()
        self.chk_smart_sync.pack(side="right")

        # 2-QATOR: Papka tanlash (yozish mumkin!), Yangi papka, Ichki avto-papka, Tartiblash va Ochish
        bottom_row = ctk.CTkFrame(self.cockpit_frame, fg_color="transparent")
        bottom_row.pack(fill="x", padx=14, pady=(2, 6))

        self.lbl_storage_info = ctk.CTkLabel(
            bottom_row,
            text="Manzil: Ish stoli (Desktop)",
            font=ctk.CTkFont(size=11),
            text_color=TXT_SECONDARY
        )
        self.lbl_storage_info.pack(side="left", padx=(0, 8))

        self.storage_progress = ctk.CTkProgressBar(bottom_row, width=105, height=7)
        self.storage_progress.set(0.25)
        self.storage_progress.pack(side="left", padx=(0, 12))

        folder_lbl = ctk.CTkLabel(
            bottom_row,
            text="📁 Asosiy Papka:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TXT_PRIMARY
        )
        folder_lbl.pack(side="left", padx=(0, 5))

        folder_names = [f["folder"] for f in music_engine.EXTENDED_CAR_FOLDERS]
        self.combo_target_folder = ctk.CTkComboBox(
            bottom_row,
            values=folder_names,
            width=210,
            height=26,
            state="normal",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=lambda _v: self._refresh_aimp_playlist()
        )
        self.combo_target_folder.set(folder_names[0])
        self.combo_target_folder.pack(side="left", padx=(0, 6))

        self.btn_new_folder = ctk.CTkButton(
            bottom_row,
            text="➕ Yangi Papka",
            width=96,
            height=26,
            fg_color="#059669",
            hover_color="#047857",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self._create_custom_folder_dialog
        )
        self.btn_new_folder.pack(side="left", padx=(0, 8))

        self.chk_auto_subfolder = ctk.CTkCheckBox(
            bottom_row,
            text="🗂️ San'atkor uchun alohida ichki papka",
            font=ctk.CTkFont(size=11),
            text_color=TXT_PRIMARY,
            onvalue=True,
            offvalue=False
        )
        self.chk_auto_subfolder.pack(side="left", padx=(4, 8))

        self.btn_open_target = ctk.CTkButton(
            bottom_row,
            text="📂 Papkani Ochish",
            width=118,
            height=26,
            fg_color="#0284c7",
            hover_color="#0369a1",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self._open_target_folder
        )
        self.btn_open_target.pack(side="right", padx=(4, 0))

        self.btn_organize_folder = ctk.CTkButton(
            bottom_row,
            text="🧹 Tartiblash (01..99)",
            width=128,
            height=26,
            fg_color="#d97706",
            hover_color="#b45309",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self._organize_current_folder_action
        )
        self.btn_organize_folder.pack(side="right", padx=(4, 4))

    def _choose_custom_base_dir(self):
        chosen = filedialog.askdirectory(title="Qo'shiqlar saqlanadigan asosiy disk yoki jildni tanlang")
        if chosen:
            self.custom_base_dir = chosen
            self.dest_mode_var.set("custom")
            self.lbl_storage_info.configure(text=f"Manzil: {chosen[:30]}...")
            self._refresh_aimp_playlist()

    def _create_custom_folder_dialog(self):
        dialog = ctk.CTkInputDialog(
            text="Yangi papka nomini kiriting (Masalan: 08_MENING_XITLARIM yoki To'y Bazmi):",
            title="➕ Yangi Papka Yaratish"
        )
        new_name = dialog.get_input()
        if new_name and new_name.strip():
            clean_folder = music_engine.sanitize_title(new_name.strip()).replace(" ", "_")
            if not clean_folder:
                clean_folder = "YANGI_PAPKA"
            cur_vals = list(self.combo_target_folder.cget("values"))
            if clean_folder not in cur_vals:
                cur_vals.append(clean_folder)
                self.combo_target_folder.configure(values=cur_vals)
            self.combo_target_folder.set(clean_folder)
            target_path = self._get_target_directory()
            self._refresh_aimp_playlist()
            messagebox.showinfo("Papka Yaratildi", f"Yangi papka tayyor:\n{target_path}")

    def _organize_current_folder_action(self):
        target_dir = self._get_target_directory()
        res = music_engine.organize_folder_mp3s(target_dir)
        self._refresh_aimp_playlist()
        messagebox.showinfo(
            "Papka Tartiblandi",
            f"📁 Papka: {os.path.basename(target_dir)}\n"
            f"✅ Tartiblangan va raqamlangan qo'shiqlar: {res['renamed']} / {res['total']} ta\n"
            f"🎵 Avto-magnitola pleylisti (00_Barcha_Qoshiqlar.m3u) yangilandi!"
        )

    # =========================================================================
    # 4. ASOSIY BO'LIMLAR (TABVIEW)
    # =========================================================================

    def _build_main_tabs(self):
        self.tabview = ctk.CTkTabview(self, corner_radius=12, height=495)
        self.tabview.pack(side="top", fill="both", expand=True, padx=15, pady=(2, 4))

        self.tab_aimp = self.tabview.add("🎧 AIMP Kutubxona & Studio")
        self.tab_search = self.tabview.add("🔍 Qidiruv & Tanlab Yuklash")
        self.tab_artists = self.tabview.add("👤 50+ San'atkorlar")
        self.tab_collections = self.tabview.add("🎼 16+ Uslublar & Janrlar")
        self.tab_queue = self.tabview.add("⚡ Turbo Yuklash Paneli (Live)")
        self.tab_simulator = self.tabview.add("🚗 Magnitola Simulyatori")

        self._build_aimp_studio_tab()
        self._build_search_tab()
        self._build_artists_tab()
        self._build_collections_tab()
        self._build_queue_tab()
        self._build_simulator_tab()

        self.tabview.set("👤 50+ San'atkorlar")

    # =========================================================================
    # BO'LIM A: 👤 50+ SAN'ATKORLAR KATALOGI (6 KATEGORIYA + QIDIRUV + ERKIN SON)
    # =========================================================================

    def _build_artists_tab(self):
        top_bar = ctk.CTkFrame(self.tab_artists, fg_color="transparent")
        top_bar.pack(fill="x", padx=8, pady=(4, 4))

        lbl = ctk.CTkLabel(
            top_bar,
            text="🎤 San'atkorlar Katalogi (50+ Xonanda):",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TXT_PRIMARY
        )
        lbl.pack(side="left", padx=(0, 8))

        self.entry_artist_filter = ctk.CTkEntry(
            top_bar,
            placeholder_text="🔎 San'atkorni tez izlash (Masalan: Yulduz, Sherali, Konsta, Miyagi)...",
            width=310,
            height=28,
            font=ctk.CTkFont(size=12),
            text_color=TXT_PRIMARY
        )
        self.entry_artist_filter.pack(side="left", padx=(0, 8))
        self.entry_artist_filter.bind("<KeyRelease>", lambda _e: self._render_artist_cards())

        btn_add_artist = ctk.CTkButton(
            top_bar,
            text="➕ San'atkor Qo'shish",
            width=135,
            height=28,
            fg_color="#059669",
            hover_color="#047857",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self._add_custom_artist_dialog
        )
        btn_add_artist.pack(side="left")

        self.combo_artist_count = ctk.CTkComboBox(
            top_bar,
            values=["1", "3", "5", "10", "15", "20", "25", "35", "50", "100"],
            width=82,
            height=28,
            state="normal",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.combo_artist_count.set("15")
        self.combo_artist_count.pack(side="right", padx=(4, 0))

        count_lbl = ctk.CTkLabel(
            top_bar,
            text="🔢 Yuklash soni (yozish mumkin):",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TXT_ACCENT_GOLD
        )
        count_lbl.pack(side="right", padx=(8, 4))

        cat_bar = ctk.CTkFrame(self.tab_artists, fg_color="transparent")
        cat_bar.pack(fill="x", padx=8, pady=(0, 4))

        self.seg_artist_cats = ctk.CTkSegmentedButton(
            cat_bar,
            values=music_engine.ARTIST_CATEGORIES,
            height=28,
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self._on_artist_category_change
        )
        self.seg_artist_cats.set("Barchasi")
        self.seg_artist_cats.pack(fill="x")

        self.artists_scroll = ctk.CTkScrollableFrame(self.tab_artists, fg_color="transparent")
        self.artists_scroll.pack(fill="both", expand=True, padx=4, pady=2)
        self.artists_scroll.grid_columnconfigure(0, weight=1)
        self.artists_scroll.grid_columnconfigure(1, weight=1)

        self._render_artist_cards()

    def _on_artist_category_change(self, cat_val: str):
        self.selected_artist_category = cat_val
        self._render_artist_cards()

    def _render_artist_cards(self):
        for child in self.artists_scroll.winfo_children():
            child.destroy()

        all_artists = music_engine.get_all_artists()
        q = self.entry_artist_filter.get().strip().lower() if hasattr(self, "entry_artist_filter") else ""
        cat = self.selected_artist_category

        filtered = []
        for art in all_artists:
            if cat != "Barchasi" and art.get("category", "") != cat:
                continue
            if q and (q not in art["name"].lower() and q not in art.get("desc", "").lower()):
                continue
            filtered.append(art)

        skin = THEME_SKINS.get(self.current_skin_name, THEME_SKINS["🌑 AIMP Onyx"])

        if not filtered:
            ctk.CTkLabel(
                self.artists_scroll,
                text="Siz qidirgan san'atkor ro'yxatda topilmadi. '➕ San'atkor Qo'shish' tugmasini bosing yoki Qidiruv bo'limidan izlang!",
                font=ctk.CTkFont(size=12),
                text_color=TXT_SECONDARY
            ).grid(row=0, column=0, columnspan=2, pady=30)
            return

        for idx, item in enumerate(filtered):
            row = idx // 2
            col = idx % 2

            card = ctk.CTkFrame(
                self.artists_scroll,
                corner_radius=8,
                fg_color=skin["bg_card"],
                border_width=1,
                border_color=skin["border"]
            )
            card.grid(row=row, column=col, sticky="nsew", padx=5, pady=4)
            self.themed_cards.append(card)

            info_box = ctk.CTkFrame(card, fg_color="transparent")
            info_box.pack(side="left", fill="both", expand=True, padx=10, pady=6)

            name_lbl = ctk.CTkLabel(
                info_box,
                text=f"{item['name']}  •  {item.get('category', '')}",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=TXT_PRIMARY,
                anchor="w"
            )
            name_lbl.pack(fill="x")

            desc_lbl = ctk.CTkLabel(
                info_box,
                text=item.get("desc", "Eng sara xitlar"),
                font=ctk.CTkFont(size=11),
                text_color=TXT_SECONDARY,
                anchor="w"
            )
            desc_lbl.pack(fill="x")

            btn_box = ctk.CTkFrame(card, fg_color="transparent")
            btn_box.pack(side="right", padx=8, pady=6)

            btn_preview = ctk.CTkButton(
                btn_box,
                text="🔍 Tanlash",
                width=78,
                height=28,
                fg_color="#334155",
                hover_color="#475569",
                font=ctk.CTkFont(size=11, weight="bold"),
                command=lambda art=item: self._preview_artist_tracks(art)
            )
            btn_preview.pack(side="left", padx=(0, 5))

            btn_dl = ctk.CTkButton(
                btn_box,
                text="⚡ Yuklash",
                width=85,
                height=28,
                fg_color=skin["accent_btn"],
                hover_color=skin["accent_hover"],
                font=ctk.CTkFont(size=11, weight="bold"),
                command=lambda art=item: self._start_artist_turbo(art)
            )
            btn_dl.pack(side="left")

    def _add_custom_artist_dialog(self):
        dialog = ctk.CTkInputDialog(
            text="Qo'shmoqchi bo'lgan san'atkor ismini kiriting (Masalan: Tahir Sodiqov yoki Eminem):",
            title="➕ Yangi San'atkor Qo'shish"
        )
        name = dialog.get_input()
        if name and name.strip():
            music_engine.add_custom_artist(name.strip(), category="🔥 Zamonaviy Xit", desc="Maxsus qo'shilgan san'atkor")
            self.seg_artist_cats.set("Barchasi")
            self.selected_artist_category = "Barchasi"
            self._render_artist_cards()
            messagebox.showinfo("Qo'shildi", f"'{name.strip()}' katalogga muvaffaqiyatli qo'shildi!")

    def _preview_artist_tracks(self, artist_info: dict):
        count = music_engine.parse_track_count(self.combo_artist_count.get(), default=15)
        self.combo_search_count.set(str(count))
        self.entry_search.delete(0, "end")
        self.entry_search.insert(0, artist_info["query"])
        self.tabview.set("🔍 Qidiruv & Tanlab Yuklash")
        self._start_interactive_search_preview()

    # =========================================================================
    # BO'LIM B: 🎼 16+ USLUBLAR & JANRLAR (ERKIN SON + KO'RIB TANLASH)
    # =========================================================================

    def _build_collections_tab(self):
        top_bar = ctk.CTkFrame(self.tab_collections, fg_color="transparent")
        top_bar.pack(fill="x", padx=10, pady=(4, 6))

        lbl = ctk.CTkLabel(
            top_bar,
            text="🎼 16+ Musiqa Uslublari, Janrlar va Hududiy To'plamlar:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TXT_PRIMARY
        )
        lbl.pack(side="left")

        self.combo_style_count = ctk.CTkComboBox(
            top_bar,
            values=["5", "10", "15", "20", "25", "30", "40", "50", "100"],
            width=85,
            height=28,
            state="normal",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.combo_style_count.set("20")
        self.combo_style_count.pack(side="right", padx=(4, 0))

        ctk.CTkLabel(
            top_bar,
            text="🔢 Yuklash soni (yozish mumkin):",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TXT_ACCENT_GOLD
        ).pack(side="right", padx=(10, 4))

        scroll = ctk.CTkScrollableFrame(self.tab_collections, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=5, pady=0)
        scroll.grid_columnconfigure(0, weight=1)
        scroll.grid_columnconfigure(1, weight=1)

        skin = THEME_SKINS.get(self.current_skin_name, THEME_SKINS["🌑 AIMP Onyx"])

        for idx, col_item in enumerate(music_engine.COLLECTIONS_2026):
            r = idx // 2
            c = idx % 2
            card = ctk.CTkFrame(
                scroll,
                corner_radius=10,
                fg_color=skin["bg_card"],
                border_width=1,
                border_color=skin["border"]
            )
            card.grid(row=r, column=c, sticky="nsew", padx=6, pady=5)
            self.themed_cards.append(card)

            info = ctk.CTkFrame(card, fg_color="transparent")
            info.pack(side="left", fill="both", expand=True, padx=12, pady=8)

            title_l = ctk.CTkLabel(
                info,
                text=col_item["title"],
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=TXT_ACCENT_BLUE,
                anchor="w"
            )
            title_l.pack(fill="x")

            sub_l = ctk.CTkLabel(
                info,
                text=f"📁 Tavsiya papka: {col_item['target_folder']}",
                font=ctk.CTkFont(size=11),
                text_color=TXT_SECONDARY,
                anchor="w"
            )
            sub_l.pack(fill="x")

            btn_box = ctk.CTkFrame(card, fg_color="transparent")
            btn_box.pack(side="right", padx=10, pady=8)

            btn_prev = ctk.CTkButton(
                btn_box,
                text="🔍 Tanlash",
                width=78,
                height=28,
                fg_color="#334155",
                hover_color="#475569",
                font=ctk.CTkFont(size=11, weight="bold"),
                command=lambda ci=col_item: self._preview_collection_tracks(ci)
            )
            btn_prev.pack(side="left", padx=(0, 5))

            btn = ctk.CTkButton(
                btn_box,
                text="⚡ Yuklash",
                width=88,
                height=28,
                fg_color="#2563eb",
                hover_color="#1d4ed8",
                font=ctk.CTkFont(size=11, weight="bold"),
                command=lambda ci=col_item: self._start_collection_turbo(ci)
            )
            btn.pack(side="left")

    def _preview_collection_tracks(self, col_item: dict):
        count = music_engine.parse_track_count(self.combo_style_count.get(), default=col_item.get("count", 20))
        self.combo_search_count.set(str(count))
        self.entry_search.delete(0, "end")
        self.entry_search.insert(0, col_item["query"])
        self.tabview.set("🔍 Qidiruv & Tanlab Yuklash")
        self._start_interactive_search_preview()

    # =========================================================================
    # BO'LIM C: 🔍 INTERAKTIV QIDIRUV VA TANLAB YUKLASH STUDIYASI
    # =========================================================================

    def _build_search_tab(self):
        self.search_top_card = ctk.CTkFrame(self.tab_search, corner_radius=10, fg_color=BG_CARD_TUPLE)
        self.search_top_card.pack(fill="x", padx=8, pady=(4, 6))

        search_row = ctk.CTkFrame(self.search_top_card, fg_color="transparent")
        search_row.pack(fill="x", padx=12, pady=(8, 6))

        self.entry_search = ctk.CTkEntry(
            search_row,
            placeholder_text="🔍 Qo'shiq nomi, san'atkor yoki YouTube linkini kiriting (Masalan: Jaloliddin Ahmadaliyev Qora ko'z)...",
            height=36,
            font=ctk.CTkFont(size=13),
            text_color=TXT_PRIMARY
        )
        self.entry_search.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.entry_search.bind("<Return>", lambda _e: self._start_interactive_search_preview())

        self.btn_voice_search = ctk.CTkButton(
            search_row,
            text="🎙️ Ovozli Qidiruv",
            width=125,
            height=36,
            fg_color="#dc2626",
            hover_color="#b91c1c",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._start_voice_search
        )
        self.btn_voice_search.pack(side="right")

        opt_frame = ctk.CTkFrame(self.search_top_card, fg_color="transparent")
        opt_frame.pack(fill="x", padx=12, pady=(0, 8))

        ctk.CTkLabel(
            opt_frame,
            text="🔢 Qidiruv/Yuklash soni (yozish mumkin):",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TXT_ACCENT_GOLD
        ).pack(side="left", padx=(0, 6))

        self.combo_search_count = ctk.CTkComboBox(
            opt_frame,
            values=["1", "3", "5", "10", "15", "25", "50", "100"],
            width=85,
            height=30,
            state="normal",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.combo_search_count.set("15")
        self.combo_search_count.pack(side="left", padx=(0, 12))

        self.btn_search_preview = ctk.CTkButton(
            opt_frame,
            text="🔍 Qidirib Ro'yxatni Ko'rish (Tanlab Yuklash)",
            width=265,
            height=32,
            fg_color="#0284c7",
            hover_color="#0369a1",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._start_interactive_search_preview
        )
        self.btn_search_preview.pack(side="left", padx=(0, 8))

        self.btn_search_auto_dl = ctk.CTkButton(
            opt_frame,
            text="🚀 Darhol Avto-Yuklash",
            width=175,
            height=32,
            fg_color="#059669",
            hover_color="#047857",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._start_custom_search_turbo
        )
        self.btn_search_auto_dl.pack(side="left")

        self.btn_dl_checked = ctk.CTkButton(
            opt_frame,
            text="📥 Belgilanganlarni Yuklash",
            width=195,
            height=32,
            fg_color="#d97706",
            hover_color="#b45309",
            font=ctk.CTkFont(size=12, weight="bold"),
            state="disabled",
            command=self._download_selected_preview_tracks
        )
        self.btn_dl_checked.pack(side="right")

        self.search_results_card = ctk.CTkFrame(self.tab_search, corner_radius=10, fg_color=BG_CARD_TUPLE)
        self.search_results_card.pack(fill="both", expand=True, padx=8, pady=(0, 4))

        res_header = ctk.CTkFrame(self.search_results_card, fg_color="transparent")
        res_header.pack(fill="x", padx=12, pady=(6, 2))

        self.lbl_search_status = ctk.CTkLabel(
            res_header,
            text="💡 Qo'shiq nomini yozib '🔍 Qidirib Ro'yxatni Ko'rish' tugmasini bosing — topilgan qo'shiqlarni ko'rib, xohlaganingizni yuklaysiz!",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TXT_ACCENT_BLUE
        )
        self.lbl_search_status.pack(side="left")

        self.btn_toggle_all_preview = ctk.CTkButton(
            res_header,
            text="☑️ Barchasini belgilash/bo'shatish",
            width=195,
            height=24,
            fg_color="#334155",
            hover_color="#475569",
            font=ctk.CTkFont(size=11),
            command=self._toggle_all_search_checkboxes
        )
        self.btn_toggle_all_preview.pack(side="right")

        self.search_results_scroll = ctk.CTkScrollableFrame(self.search_results_card, fg_color="transparent")
        self.search_results_scroll.pack(fill="both", expand=True, padx=6, pady=4)

    def _start_interactive_search_preview(self):
        query = self.entry_search.get().strip()
        if not query:
            messagebox.showwarning("Qidiruv bo'sh", "Iltimos, qidirish uchun qo'shiq yoki san'atkor nomini yozing!")
            return
        if self.is_searching_preview:
            return

        limit = music_engine.parse_track_count(self.combo_search_count.get(), default=15)
        self.is_searching_preview = True
        self.btn_search_preview.configure(text="⏳ Qidirilmoqda...", state="disabled")
        self.lbl_search_status.configure(text=f"🔎 YouTube'dan '{query}' bo'yicha {limit} ta qo'shiq qidirilmoqda...")

        for child in self.search_results_scroll.winfo_children():
            child.destroy()

        def preview_worker():
            tracks = music_engine.search_youtube(
                query=query,
                limit=limit,
                log_cb=self.log,
                cancel_check=lambda: False
            )
            self.after(0, lambda: self._render_search_preview_results(query, tracks))

        threading.Thread(target=preview_worker, daemon=True).start()

    def _render_search_preview_results(self, query: str, tracks: list):
        self.is_searching_preview = False
        self.btn_search_preview.configure(text="🔍 Qidirib Ro'yxatni Ko'rish (Tanlab Yuklash)", state="normal")

        for child in self.search_results_scroll.winfo_children():
            child.destroy()
        self.search_preview_items.clear()

        if not tracks:
            self.lbl_search_status.configure(text=f"⚠️ '{query}' bo'yicha qo'shiq topilmadi. Boshqa so'z bilan urinib ko'ring.")
            self.btn_dl_checked.configure(state="disabled")
            return

        self.lbl_search_status.configure(
            text=f"✅ '{query}' bo'yicha {len(tracks)} ta qo'shiq topildi! Bittalab yoki belgilab yuklab oling:"
        )
        self.btn_dl_checked.configure(state="normal", text=f"📥 Belgilanganlarni Yuklash ({len(tracks)})")

        for idx, tr in enumerate(tracks, 1):
            row = ctk.CTkFrame(self.search_results_scroll, corner_radius=8, fg_color=BG_ROW_TUPLE, height=40)
            row.pack(fill="x", padx=4, pady=3)

            chk_var = ctk.BooleanVar(value=True)
            chk = ctk.CTkCheckBox(
                row,
                text="",
                variable=chk_var,
                width=24,
                onvalue=True,
                offvalue=False,
                command=self._update_checked_button_count
            )
            chk.pack(side="left", padx=(8, 4), pady=6)

            dur_str = format_mm_ss(tr.get("duration") or 210)
            ch_name = tr.get("channel") or "YouTube Audio"

            lbl_t = ctk.CTkLabel(
                row,
                text=f"{idx:02d}. {tr['title']}",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=TXT_PRIMARY,
                anchor="w"
            )
            lbl_t.pack(side="left", fill="x", expand=True, padx=4, pady=6)

            lbl_info = ctk.CTkLabel(
                row,
                text=f"⏱ {dur_str}  •  📺 {ch_name[:22]}",
                font=ctk.CTkFont(family="Consolas", size=10),
                text_color=TXT_SECONDARY
            )
            lbl_info.pack(side="right", padx=8)

            btn_one = ctk.CTkButton(
                row,
                text="⬇️ Shu Trekni Yuklash",
                width=145,
                height=26,
                fg_color="#059669",
                hover_color="#047857",
                font=ctk.CTkFont(size=11, weight="bold"),
                command=lambda single_tr=tr: self._start_direct_tracks_turbo([single_tr], single_tr["title"])
            )
            btn_one.pack(side="right", padx=(6, 8), pady=5)

            self.search_preview_items.append({"var": chk_var, "track": tr})

    def _update_checked_button_count(self):
        selected = [it["track"] for it in self.search_preview_items if it["var"].get()]
        self.btn_dl_checked.configure(
            text=f"📥 Belgilanganlarni Yuklash ({len(selected)})",
            state="normal" if selected else "disabled"
        )

    def _toggle_all_search_checkboxes(self):
        if not self.search_preview_items:
            return
        any_unchecked = any(not it["var"].get() for it in self.search_preview_items)
        for it in self.search_preview_items:
            it["var"].set(any_unchecked)
        self._update_checked_button_count()

    def _download_selected_preview_tracks(self):
        selected = [it["track"] for it in self.search_preview_items if it["var"].get()]
        if not selected:
            messagebox.showwarning("Tanlanmagan", "Yuklash uchun kamida 1 ta qo'shiqni belgilang!")
            return
        self._start_direct_tracks_turbo(selected, f"Tanlangan {len(selected)} ta qo'shiq")

    # =========================================================================
    # BO'LIM D: 🎧 AIMP KUTUBXONA & OMNI-STUDIO (SEVIMLILAR + TARIX + SARALASH + FX + EQ + TEG)
    # =========================================================================

    def _build_aimp_studio_tab(self):
        main_split = ctk.CTkFrame(self.tab_aimp, fg_color="transparent")
        main_split.pack(fill="both", expand=True, padx=6, pady=4)

        # CHAP PANEL: AIMP YAGONA KUTUBXONA VA PLEYLISH MENEJERI
        self.aimp_left_pane = ctk.CTkFrame(main_split, corner_radius=10, fg_color=BG_CARD_TUPLE)
        self.aimp_left_pane.pack(side="left", fill="both", expand=True, padx=(0, 6))

        pl_header = ctk.CTkFrame(self.aimp_left_pane, fg_color="transparent")
        pl_header.pack(fill="x", padx=10, pady=(6, 2))

        lbl_pl = ctk.CTkLabel(
            pl_header,
            text="🎵 AIMP Yagona Kutubxona (Qo'shiq ustiga bosing — yangraydi, ❤️ bosing — Sevimlilarga tushadi!)",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TXT_ACCENT_GOLD
        )
        lbl_pl.pack(side="left")

        self.lbl_aimp_count = ctk.CTkLabel(
            pl_header,
            text="0 ta trek",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=TXT_ACCENT_GREEN
        )
        self.lbl_aimp_count.pack(side="right")

        # 4-Rejimli Ko'rish Filtri: Barcha Papkalar | Sevimlilar | Tarix | Joriy Papka
        scope_bar = ctk.CTkFrame(self.aimp_left_pane, fg_color="transparent")
        scope_bar.pack(fill="x", padx=10, pady=(2, 4))

        self.seg_library_scope = ctk.CTkSegmentedButton(
            scope_bar,
            values=[
                "🌐 Barcha Papkalar (Hammasi)",
                "❤️ Sevimlilar",
                "🕒 Oxirgi Eshitilganlar",
                "📁 Faqat Joriy Papka"
            ],
            height=26,
            font=ctk.CTkFont(size=11, weight="bold"),
            command=lambda _v: self._refresh_aimp_playlist()
        )
        self.seg_library_scope.set("🌐 Barcha Papkalar (Hammasi)")
        self.seg_library_scope.pack(fill="x")

        # Qidiruv, Saralash va Amallar satri
        pl_tools = ctk.CTkFrame(self.aimp_left_pane, fg_color="transparent")
        pl_tools.pack(fill="x", padx=10, pady=(0, 4))

        self.entry_aimp_filter = ctk.CTkEntry(
            pl_tools,
            placeholder_text="🔍 Kutubxonadan tez izlash...",
            height=26,
            font=ctk.CTkFont(size=11),
            text_color=TXT_PRIMARY
        )
        self.entry_aimp_filter.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.entry_aimp_filter.bind("<KeyRelease>", lambda _e: self._refresh_aimp_playlist())

        self.combo_library_sort = ctk.CTkComboBox(
            pl_tools,
            values=["Nomi (A-Z)", "Yangilari oldinda", "Hajmi (MB)"],
            width=125,
            height=26,
            state="readonly",
            font=ctk.CTkFont(size=11),
            command=lambda _v: self._refresh_aimp_playlist()
        )
        self.combo_library_sort.set("Nomi (A-Z)")
        self.combo_library_sort.pack(side="left", padx=(0, 6))

        self.btn_send_favs_usb = ctk.CTkButton(
            pl_tools,
            text="📲 Sevimlilarni Fleshkaga",
            width=145,
            height=26,
            fg_color="#059669",
            hover_color="#047857",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self._copy_favorites_to_usb_or_folder
        )
        self.btn_send_favs_usb.pack(side="left", padx=(0, 4))

        btn_pl_add = ctk.CTkButton(
            pl_tools,
            text="➕ MP3 Qo'shish",
            width=105,
            height=26,
            fg_color="#0284c7",
            hover_color="#0369a1",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self._import_external_mp3s
        )
        btn_pl_add.pack(side="left")

        self.aimp_playlist_scroll = ctk.CTkScrollableFrame(self.aimp_left_pane, fg_color="transparent")
        self.aimp_playlist_scroll.pack(fill="both", expand=True, padx=6, pady=4)

        # O'NG PANEL: 10-BAND EQ + STUDIO FX LAB + ID3v2 PASPORT & MUQOVA
        right_pane = ctk.CTkFrame(main_split, width=415, corner_radius=10, fg_color="transparent")
        right_pane.pack(side="right", fill="y", padx=(4, 0))
        right_pane.pack_propagate(False)

        # 1. AIMP 10-Band Equalizer
        self.aimp_eq_card = ctk.CTkFrame(right_pane, corner_radius=10, fg_color=BG_CARD_TUPLE)
        self.aimp_eq_card.pack(fill="x", pady=(0, 5))

        eq_top = ctk.CTkFrame(self.aimp_eq_card, fg_color="transparent")
        eq_top.pack(fill="x", padx=10, pady=(4, 2))

        ctk.CTkLabel(
            eq_top,
            text="🎚️ AIMP 10-Band EQ",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TXT_ACCENT_BLUE
        ).pack(side="left")

        preset_names = list(music_engine.AIMP_EQ_PRESETS.keys())
        self.combo_aimp_eq_preset = ctk.CTkComboBox(
            eq_top,
            values=preset_names,
            width=215,
            height=22,
            state="readonly",
            font=ctk.CTkFont(size=10),
            command=self._on_aimp_preset_selected
        )
        self.combo_aimp_eq_preset.set(preset_names[0])
        self.combo_aimp_eq_preset.pack(side="right")

        sliders_row = ctk.CTkFrame(self.aimp_eq_card, fg_color="transparent")
        sliders_row.pack(fill="x", padx=8, pady=2)

        self.eq_sliders.clear()
        default_gains = music_engine.AIMP_EQ_PRESETS[preset_names[0]]
        for lbl_txt, init_g in zip(music_engine.AIMP_EQ_LABELS, default_gains):
            col_f = ctk.CTkFrame(sliders_row, fg_color="transparent")
            col_f.pack(side="left", expand=True, fill="y", padx=1)

            val_lbl = ctk.CTkLabel(col_f, text=f"{init_g:+.1f}", font=ctk.CTkFont(family="Consolas", size=8), text_color=TXT_SECONDARY)
            val_lbl.pack()

            sl = ctk.CTkSlider(
                col_f,
                orientation="vertical",
                from_=-6.0,
                to=6.0,
                height=56,
                width=13,
                button_color="#f59e0b",
                progress_color="#0284c7"
            )
            sl.set(init_g)
            sl.configure(command=lambda v, l=val_lbl: l.configure(text=f"{float(v):+.1f}"))
            sl.pack(pady=1)

            freq_lbl = ctk.CTkLabel(col_f, text=lbl_txt.replace("Hz", ""), font=ctk.CTkFont(size=8), text_color=TXT_MUTED)
            freq_lbl.pack()

            self.eq_sliders.append((sl, val_lbl))

        self.btn_apply_eq = ctk.CTkButton(
            self.aimp_eq_card,
            text="⚡ Joriy Qo'shiqqa 10-Band EQ Muhrlash",
            height=25,
            fg_color="#059669",
            hover_color="#047857",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self._apply_eq_to_current_track
        )
        self.btn_apply_eq.pack(fill="x", padx=10, pady=(2, 5))

        # 2. Poweramp & CapCut Studio Audio FX Lab (Slowed+Reverb, 8D, Nightcore, Speed)
        self.aimp_fx_card = ctk.CTkFrame(right_pane, corner_radius=10, fg_color=BG_CARD_TUPLE)
        self.aimp_fx_card.pack(fill="x", pady=(0, 5))

        fx_top = ctk.CTkFrame(self.aimp_fx_card, fg_color="transparent")
        fx_top.pack(fill="x", padx=10, pady=(4, 2))

        ctk.CTkLabel(
            fx_top,
            text="🎛️ Studio FX & Tezlik (Slowed+Reverb / 8D / Speed)",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=TXT_ACCENT_GOLD
        ).pack(side="left")

        fx_row = ctk.CTkFrame(self.aimp_fx_card, fg_color="transparent")
        fx_row.pack(fill="x", padx=10, pady=(2, 5))

        fx_names = list(music_engine.STUDIO_FX_PRESETS.keys())
        self.combo_studio_fx = ctk.CTkComboBox(
            fx_row,
            values=fx_names,
            width=245,
            height=25,
            state="readonly",
            font=ctk.CTkFont(size=11)
        )
        self.combo_studio_fx.set(fx_names[0])
        self.combo_studio_fx.pack(side="left", padx=(0, 6))

        self.btn_apply_fx = ctk.CTkButton(
            fx_row,
            text="✨ Qo'llash",
            width=120,
            height=25,
            fg_color="#d97706",
            hover_color="#b45309",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self._apply_studio_fx_action
        )
        self.btn_apply_fx.pack(side="right")

        # 3. AIMP ID3v2 Pasport va Muqova Tahrirlagich
        self.aimp_tag_card = ctk.CTkFrame(right_pane, corner_radius=10, fg_color=BG_CARD_TUPLE)
        self.aimp_tag_card.pack(fill="both", expand=True)

        tag_top = ctk.CTkFrame(self.aimp_tag_card, fg_color="transparent")
        tag_top.pack(fill="x", padx=10, pady=(4, 2))

        ctk.CTkLabel(
            tag_top,
            text="🏷️ ID3v2 Pasport & Muqova",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=TXT_ACCENT_GREEN
        ).pack(side="left")

        self.lbl_aimp_tech_specs = ctk.CTkLabel(
            tag_top,
            text="256 kbps • 44.1 kHz",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color=TXT_SECONDARY
        )
        self.lbl_aimp_tech_specs.pack(side="right")

        form_box = ctk.CTkFrame(self.aimp_tag_card, fg_color="transparent")
        form_box.pack(fill="x", padx=10, pady=1)

        self.entry_tag_title = ctk.CTkEntry(form_box, placeholder_text="Qo'shiq nomi (Title)", height=24, font=ctk.CTkFont(size=11), text_color=TXT_PRIMARY)
        self.entry_tag_title.pack(fill="x", pady=1)

        self.entry_tag_artist = ctk.CTkEntry(form_box, placeholder_text="San'atkor (Artist)", height=24, font=ctk.CTkFont(size=11), text_color=TXT_PRIMARY)
        self.entry_tag_artist.pack(fill="x", pady=1)

        self.entry_tag_album = ctk.CTkEntry(form_box, placeholder_text="Albom (Album)", height=24, font=ctk.CTkFont(size=11), text_color=TXT_PRIMARY)
        self.entry_tag_album.pack(fill="x", pady=1)

        tag_btn_row = ctk.CTkFrame(self.aimp_tag_card, fg_color="transparent")
        tag_btn_row.pack(fill="x", padx=10, pady=(3, 4))

        self.btn_choose_cover = ctk.CTkButton(
            tag_btn_row,
            text="🖼️ Rasm Tanlash",
            width=125,
            height=25,
            fg_color="#334155",
            hover_color="#475569",
            font=ctk.CTkFont(size=11),
            command=self._choose_custom_cover_image
        )
        self.btn_choose_cover.pack(side="left", padx=(0, 6))

        self.btn_save_tags = ctk.CTkButton(
            tag_btn_row,
            text="💾 Teg & Muqovani Saqlash",
            height=25,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self._save_current_tags
        )
        self.btn_save_tags.pack(side="left", fill="x", expand=True)

    # =========================================================================
    # BO'LIM E: ⚡ TURBO YUKLASH PANELI (LIVE LOG + STATISTIKA + CLICK-TO-PLAY)
    # =========================================================================

    def _build_queue_tab(self):
        top_row = ctk.CTkFrame(self.tab_queue, fg_color="transparent")
        top_row.pack(fill="x", padx=10, pady=(4, 2))

        self.lbl_queue_header = ctk.CTkLabel(
            top_row,
            text="⚡ IDM 32-Oqim Yuklovchi (Yuklangan qo'shiq ustiga bosing — darhol eshitasiz!)",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TXT_ACCENT_BLUE
        )
        self.lbl_queue_header.pack(side="left")

        self.btn_cancel_turbo = ctk.CTkButton(
            top_row,
            text="⏹️ To'xtatish",
            width=95,
            height=26,
            fg_color="#dc2626",
            hover_color="#b91c1c",
            state="disabled",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self._cancel_download
        )
        self.btn_cancel_turbo.pack(side="right", padx=(8, 0))

        self.combo_idm_streams = ctk.CTkComboBox(
            top_row,
            values=["32 Oqim (IDM Maksimal)", "16 Oqim (Tezkor)", "8 Oqim (Standart)"],
            width=175,
            height=26,
            state="readonly",
            font=ctk.CTkFont(size=11)
        )
        self.combo_idm_streams.set("32 Oqim (IDM Maksimal)")
        self.combo_idm_streams.pack(side="right", padx=(8, 0))

        self.lbl_idm_speed = ctk.CTkLabel(
            top_row,
            text="⚡ Tezlik: 0.0 MB/s",
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color=TXT_ACCENT_GREEN
        )
        self.lbl_idm_speed.pack(side="right", padx=(10, 10))

        status_banner = ctk.CTkFrame(self.tab_queue, corner_radius=8, fg_color=BG_ROW_TUPLE, height=30)
        status_banner.pack(fill="x", padx=10, pady=(2, 4))

        self.lbl_live_log = ctk.CTkLabel(
            status_banner,
            text="🟢 Tizim tayyor. Katalogdan, Uslublardan yoki Qidiruvdan qo'shiq tanlab yuklang.",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=TXT_PRIMARY,
            anchor="w"
        )
        self.lbl_live_log.pack(side="left", fill="x", expand=True, padx=10, pady=4)

        self.lbl_queue_stats = ctk.CTkLabel(
            status_banner,
            text="Jami: 0 | Tayyor: 0",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=TXT_ACCENT_GOLD
        )
        self.lbl_queue_stats.pack(side="right", padx=10, pady=4)

        self.queue_scroll = ctk.CTkScrollableFrame(self.tab_queue, fg_color="transparent")
        self.queue_scroll.pack(fill="both", expand=True, padx=5, pady=2)

        self.lbl_empty_queue = ctk.CTkLabel(
            self.queue_scroll,
            text="Hozircha navbatda treklar yo'q.\n'⚡ Yuklash' tugmasini bosing — yuklangan har bir trek ustiga bosib AIMP pleyerda tinglashingiz yoki papkasini ochishingiz mumkin!",
            font=ctk.CTkFont(size=12),
            text_color=TXT_SECONDARY
        )
        self.lbl_empty_queue.pack(pady=40)

    # =========================================================================
    # BO'LIM F: 🚗 VIRTUAL MAGNITOLA SIMULYATORI
    # =========================================================================

    def _build_simulator_tab(self):
        container = ctk.CTkFrame(self.tab_simulator, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=10)

        car_frame = ctk.CTkFrame(container, corner_radius=16, fg_color=("#1e293b", "#0b0f19"), border_width=3, border_color="#334155")
        car_frame.pack(fill="both", expand=True, padx=10, pady=5)

        status_bar = ctk.CTkFrame(car_frame, corner_radius=0, height=26, fg_color=("#0f172a", "#070a12"))
        status_bar.pack(side="top", fill="x")

        car_brand_l = ctk.CTkLabel(status_bar, text="🚗 CHEVROLET MYLINK / ANDROID AUTO • AIMP BRIDGE", font=ctk.CTkFont(size=10, weight="bold"), text_color="#38bdf8")
        car_brand_l.pack(side="left", padx=15)

        car_stat_r = ctk.CTkLabel(status_bar, text="12:45 • 24°C • 4G LTE • USB HI-FI", font=ctk.CTkFont(size=10), text_color="#94a3b8")
        car_stat_r.pack(side="right", padx=15)

        display_body = ctk.CTkFrame(car_frame, fg_color="transparent")
        display_body.pack(fill="both", expand=True, padx=25, pady=15)

        left_art = ctk.CTkFrame(display_body, width=165, height=165, corner_radius=12, fg_color=("#0f172a", "#131b2e"), border_width=2, border_color="#38bdf8")
        left_art.pack(side="left", padx=(0, 25))
        left_art.pack_propagate(False)

        self.sim_art_label = ctk.CTkLabel(left_art, text="🎵\nALBUM\nCOVER", font=ctk.CTkFont(size=16, weight="bold"), text_color="#38bdf8")
        self.sim_art_label.pack(expand=True, fill="both")

        right_info = ctk.CTkFrame(display_body, fg_color="transparent")
        right_info.pack(side="left", fill="both", expand=True)

        self.sim_song_title = ctk.CTkLabel(
            right_info,
            text="Jaloliddin Ahmadaliyev - Qora ko'z",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#f8fafc",
            anchor="w"
        )
        self.sim_song_title.pack(fill="x", pady=(5, 2))

        self.sim_artist = ctk.CTkLabel(
            right_info,
            text="San'atkor: O'zbek Xitlari 2026",
            font=ctk.CTkFont(size=13),
            text_color="#38bdf8",
            anchor="w"
        )
        self.sim_artist.pack(fill="x", pady=(0, 8))

        specs_box = ctk.CTkFrame(right_info, fg_color=("#0f172a", "#111827"), corner_radius=6)
        specs_box.pack(fill="x", pady=(0, 10))

        self.sim_specs_text = ctk.CTkLabel(
            specs_box,
            text="  Format: LAME MP3 256k CBR  |  Filtr: EBU R128 (-14 LUFS)  |  FAT32 Standart  ",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color="#22c55e"
        )
        self.sim_specs_text.pack(pady=4)

        self.sim_time_progress = ctk.CTkProgressBar(right_info, height=8)
        self.sim_time_progress.set(0.0)
        self.sim_time_progress.pack(fill="x", pady=(0, 4))

        time_row = ctk.CTkFrame(right_info, fg_color="transparent")
        time_row.pack(fill="x", pady=(0, 12))
        self.sim_lbl_time = ctk.CTkLabel(time_row, text="00:00 / 03:30", font=ctk.CTkFont(family="Consolas", size=11), text_color="#94a3b8")
        self.sim_lbl_time.pack(side="left")

        touch_btns = ctk.CTkFrame(right_info, fg_color="transparent")
        touch_btns.pack(anchor="w")

        btn_prev = ctk.CTkButton(touch_btns, text="⏮", width=45, height=32, fg_color="#334155", command=self._prev_track_action)
        btn_prev.pack(side="left", padx=(0, 6))

        self.btn_sim_play = ctk.CTkButton(
            touch_btns,
            text="▶",
            width=55,
            height=32,
            fg_color="#0284c7",
            command=self._toggle_playback
        )
        self.btn_sim_play.pack(side="left", padx=(0, 6))

        btn_next = ctk.CTkButton(touch_btns, text="⏭", width=45, height=32, fg_color="#334155", command=self._next_track_action)
        btn_next.pack(side="left", padx=(0, 12))

        lbl_car_preset = ctk.CTkLabel(touch_btns, text="Akustika: Gentra / Cobalt / Malibu / Tracker", font=ctk.CTkFont(size=11), text_color="#fbbf24")
        lbl_car_preset.pack(side="left")

    # =========================================================================
    # 5. DOIMIY PASTKI AIMP MASTER DECK (WAVEFORM + A-B LOOP & TRIM + FAVORITE + SLEEP TIMER + VU)
    # =========================================================================

    def _build_audiophile_player_panel(self):
        self.player_frame = ctk.CTkFrame(self, corner_radius=12, fg_color=("#cbd5e1", "#0a0e17"), height=125)
        self.player_frame.pack(side="bottom", fill="x", padx=15, pady=(0, 8))

        main_row = ctk.CTkFrame(self.player_frame, fg_color="transparent")
        main_row.pack(fill="x", padx=12, pady=(6, 2))

        # 1. Chapda: Mini Album Cover Art (58x58)
        self.deck_art_frame = ctk.CTkFrame(main_row, width=62, height=62, corner_radius=8, fg_color=("#1e293b", "#131b2e"), border_width=1, border_color="#38bdf8")
        self.deck_art_frame.pack(side="left", padx=(0, 10))
        self.deck_art_frame.pack_propagate(False)

        self.lbl_deck_art = ctk.CTkLabel(self.deck_art_frame, text="🎵\nAIMP", font=ctk.CTkFont(size=11, weight="bold"), text_color="#38bdf8")
        self.lbl_deck_art.pack(expand=True, fill="both")

        # 2. O'rtada: Transport + A-B Loop & Trim + Waveform Seekbar
        center_deck = ctk.CTkFrame(main_row, fg_color="transparent")
        center_deck.pack(side="left", fill="both", expand=True)

        ctrl_sub = ctk.CTkFrame(center_deck, fg_color="transparent")
        ctrl_sub.pack(anchor="w", fill="x")

        self.btn_prev = ctk.CTkButton(ctrl_sub, text="⏮", width=28, height=25, fg_color="#1e293b", hover_color="#334155", command=self._prev_track_action)
        self.btn_prev.pack(side="left", padx=(0, 2))

        self.btn_step_back = ctk.CTkButton(ctrl_sub, text="⏪5s", width=38, height=25, fg_color="#1e293b", hover_color="#334155", font=ctk.CTkFont(size=10), command=lambda: self._step_seek_action(-5.0))
        self.btn_step_back.pack(side="left", padx=(0, 2))

        self.btn_play_pause = ctk.CTkButton(
            ctrl_sub,
            text="▶ Tinglash",
            width=78,
            height=25,
            fg_color="#0284c7",
            hover_color="#0369a1",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self._toggle_playback
        )
        self.btn_play_pause.pack(side="left", padx=(0, 2))

        self.btn_stop = ctk.CTkButton(
            ctrl_sub,
            text="⏹",
            width=28,
            height=25,
            fg_color="#1e293b",
            hover_color="#334155",
            command=self._stop_playback
        )
        self.btn_stop.pack(side="left", padx=(0, 2))

        self.btn_step_fwd = ctk.CTkButton(ctrl_sub, text="5s⏩", width=38, height=25, fg_color="#1e293b", hover_color="#334155", font=ctk.CTkFont(size=10), command=lambda: self._step_seek_action(5.0))
        self.btn_step_fwd.pack(side="left", padx=(0, 2))

        self.btn_next = ctk.CTkButton(ctrl_sub, text="⏭", width=28, height=25, fg_color="#1e293b", hover_color="#334155", command=self._next_track_action)
        self.btn_next.pack(side="left", padx=(0, 4))

        self.btn_shuffle = ctk.CTkButton(ctrl_sub, text="🔀", width=28, height=25, fg_color="#1e293b", hover_color="#334155", command=self._toggle_shuffle_action)
        self.btn_shuffle.pack(side="left", padx=(0, 2))

        self.btn_repeat = ctk.CTkButton(ctrl_sub, text="🔁 All", width=46, height=25, fg_color="#0284c7", hover_color="#0369a1", font=ctk.CTkFont(size=10, weight="bold"), command=self._toggle_repeat_action)
        self.btn_repeat.pack(side="left", padx=(0, 4))

        self.btn_deck_fav = ctk.CTkButton(
            ctrl_sub,
            text="🤍",
            width=28,
            height=25,
            fg_color="#1e293b",
            hover_color="#334155",
            font=ctk.CTkFont(size=11),
            command=self._toggle_current_playing_favorite
        )
        self.btn_deck_fav.pack(side="left", padx=(0, 6))

        # A-B Loop & Audio Cutter (Trimmer) tugmalari
        self.btn_loop_a = ctk.CTkButton(
            ctrl_sub,
            text="[A",
            width=30,
            height=25,
            fg_color="#1e293b",
            hover_color="#0284c7",
            font=ctk.CTkFont(size=10, weight="bold"),
            command=self._set_loop_a_action
        )
        self.btn_loop_a.pack(side="left", padx=(0, 2))

        self.btn_loop_b = ctk.CTkButton(
            ctrl_sub,
            text="B]",
            width=30,
            height=25,
            fg_color="#1e293b",
            hover_color="#0284c7",
            font=ctk.CTkFont(size=10, weight="bold"),
            command=self._set_loop_b_action
        )
        self.btn_loop_b.pack(side="left", padx=(0, 2))

        self.btn_loop_clear = ctk.CTkButton(
            ctrl_sub,
            text="✕",
            width=24,
            height=25,
            fg_color="#1e293b",
            hover_color="#dc2626",
            font=ctk.CTkFont(size=10),
            command=self._clear_ab_loop_action
        )
        self.btn_loop_clear.pack(side="left", padx=(0, 3))

        self.btn_trim_ab = ctk.CTkButton(
            ctrl_sub,
            text="✂️ Kesish",
            width=68,
            height=25,
            fg_color="#d97706",
            hover_color="#b45309",
            font=ctk.CTkFont(size=10, weight="bold"),
            command=self._trim_current_ab_segment_action
        )
        self.btn_trim_ab.pack(side="left", padx=(0, 8))

        self.lbl_player_title = ctk.CTkLabel(
            ctrl_sub,
            text="🎵 Ijro: Qo'shiq ustiga bosing yoki ▶ Tinglash tugmasini bosing",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TXT_PRIMARY,
            anchor="w"
        )
        self.lbl_player_title.pack(side="left", fill="x", expand=True)

        # O'rta qator: AIMP 80-Bar Waveform Seekbar
        self.waveform_seekbar = AIMPWaveformSeekbar(center_deck, on_seek_cb=self._on_waveform_seek, height=28)
        self.waveform_seekbar.pack(fill="x", pady=(4, 3))

        # Pastki qator: A/B Test + Ovoz + Vaqt + Uyqu Taymeri + Faylni ko'rsatish
        sub_row = ctk.CTkFrame(center_deck, fg_color="transparent")
        sub_row.pack(anchor="w", fill="x")

        self.btn_ab_toggle = ctk.CTkButton(
            sub_row,
            text="🎧 A/B Test: 🟢 STUDIYA DSP 256k",
            width=195,
            height=24,
            fg_color="#059669",
            hover_color="#047857",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self._toggle_ab_test
        )
        self.btn_ab_toggle.pack(side="left", padx=(0, 6))

        self.btn_mute = ctk.CTkButton(
            sub_row,
            text="🔊",
            width=26,
            height=24,
            fg_color="transparent",
            hover_color="#334155",
            text_color=TXT_PRIMARY,
            command=self._toggle_mute_action
        )
        self.btn_mute.pack(side="left", padx=(0, 2))

        self.vol_slider = ctk.CTkSlider(sub_row, width=80, height=14, from_=0.0, to=1.0, command=self._on_volume_change)
        self.vol_slider.set(0.85)
        self.vol_slider.pack(side="left", padx=(0, 8))

        self.lbl_player_time = ctk.CTkLabel(
            sub_row,
            text="00:00 / 00:00",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=TXT_ACCENT_GOLD
        )
        self.lbl_player_time.pack(side="left", padx=(0, 8))

        self.lbl_player_specs = ctk.CTkLabel(
            sub_row,
            text="256 kbps • 44.1 kHz",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color=TXT_SECONDARY
        )
        self.lbl_player_specs.pack(side="left", padx=(0, 8))

        ctk.CTkLabel(
            sub_row,
            text="💤 Taymer:",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=TXT_SECONDARY
        ).pack(side="left", padx=(2, 3))

        self.combo_sleep_timer = ctk.CTkComboBox(
            sub_row,
            values=["O'chiq", "15 daqiqa", "30 daqiqa", "60 daqiqa"],
            width=92,
            height=22,
            state="readonly",
            font=ctk.CTkFont(size=10),
            command=self._on_sleep_timer_change
        )
        self.combo_sleep_timer.set("O'chiq")
        self.combo_sleep_timer.pack(side="left")

        self.btn_reveal_playing = ctk.CTkButton(
            sub_row,
            text="📂 Faylni Ko'rsatish",
            width=120,
            height=22,
            fg_color="#334155",
            hover_color="#475569",
            font=ctk.CTkFont(size=10, weight="bold"),
            command=self._reveal_current_playing_file
        )
        self.btn_reveal_playing.pack(side="right")

        # 3. O'ng taraf: AIMP 3-IN-1 VIZUALIZATOR
        self.visualizer = VisualizerWidget(main_row, width=235, height=84)
        self.visualizer.pack(side="right", padx=(10, 0))

        self.overall_progress = ctk.CTkProgressBar(self.player_frame, height=4)
        self.overall_progress.set(0)
        self.overall_progress.pack(fill="x", padx=12, pady=(2, 4))

    def _on_sleep_timer_change(self, val: str):
        self.sleep_timer_mode = val
        if val == "O'chiq":
            self.sleep_timer_end_ts = None
            return
        mins = music_engine.parse_track_count(val, default=15)
        self.sleep_timer_end_ts = time.time() + (mins * 60)
        self.log(f"💤 Uyqu taymeri yoqildi: {mins} daqiqadan so'ng musiqa avtomatik to'xtaydi.")

    def _set_loop_a_action(self):
        if not self.player.current_studio_file:
            return
        a_s = self.player.set_loop_a()
        self.btn_loop_a.configure(text=f"[A:{format_mm_ss(a_s)}", fg_color="#0284c7")
        self.waveform_seekbar.set_loop_markers(self.player.loop_a_sec, self.player.loop_b_sec)

    def _set_loop_b_action(self):
        if not self.player.current_studio_file:
            return
        b_s = self.player.set_loop_b()
        if b_s is not None:
            self.btn_loop_b.configure(text=f"B:{format_mm_ss(b_s)}]", fg_color="#059669")
            self.waveform_seekbar.set_loop_markers(self.player.loop_a_sec, self.player.loop_b_sec)
        else:
            messagebox.showinfo("A-B Loop", "B nuqtasi A nuqtasidan kamida 1 soniya keyin bo'lishi kerak!")

    def _clear_ab_loop_action(self):
        self.player.clear_ab_loop()
        self.btn_loop_a.configure(text="[A", fg_color="#1e293b")
        self.btn_loop_b.configure(text="B]", fg_color="#1e293b")
        self.waveform_seekbar.set_loop_markers(None, None)

    def _trim_current_ab_segment_action(self):
        cur_f = self.player.current_studio_file or self.selected_tag_file
        if not cur_f or not os.path.exists(cur_f):
            messagebox.showinfo("Qo'shiq tanlanmagan", "Kesib olish uchun avval qo'shiqni ijro eting va [A hamda B] nuqtalarni belgilang!")
            return
        a_s = self.player.loop_a_sec if self.player.loop_a_sec is not None else 0.0
        b_s = self.player.loop_b_sec if self.player.loop_b_sec is not None else min(30.0, self.player.duration_sec)
        if b_s - a_s < 1.0:
            messagebox.showwarning("Qism juda qisqa", "Avval qo'shiq tinglayotganda [A (boshlanish) va B] (tugash) tugmalarini bosing!")
            return

        self.btn_trim_ab.configure(text="⏳...", state="disabled")

        def trim_worker():
            out_p = music_engine.trim_mp3_segment(cur_f, a_s, b_s, save_as_copy=True)
            self.after(0, lambda: self._on_trim_done(out_p, a_s, b_s))

        threading.Thread(target=trim_worker, daemon=True).start()

    def _on_trim_done(self, out_p: str, a_s: float, b_s: float):
        self.btn_trim_ab.configure(text="✂️ Kesish", state="normal")
        if out_p and os.path.exists(out_p):
            self._clear_ab_loop_action()
            self._refresh_aimp_playlist()
            self._play_specific_track(out_p)
            messagebox.showinfo(
                "✂️ Qo'shiq Kesildi!",
                f"Belgilangan [{format_mm_ss(a_s)} - {format_mm_ss(b_s)}] qismi alohida MP3 sifatida saqlandi va ijro etilmoqda:\n\n{os.path.basename(out_p)}"
            )
        else:
            messagebox.showerror("Xatolik", "Audio qismini kesishda xatolik yuz berdi.")

    def _toggle_current_playing_favorite(self):
        cur_f = self.player.current_studio_file or self.selected_tag_file
        if not cur_f or not os.path.exists(cur_f):
            return
        is_fav = music_engine.toggle_favorite_track(cur_f)
        self.btn_deck_fav.configure(text="❤️" if is_fav else "🤍", fg_color="#be123c" if is_fav else "#1e293b")
        self._refresh_aimp_playlist()

    def _reveal_current_playing_file(self):
        cur = self.player.current_studio_file
        if cur and os.path.exists(cur):
            self._reveal_file_in_explorer(cur)
        else:
            self._open_target_folder()

    def _reveal_file_in_explorer(self, file_path: str):
        if file_path and os.path.exists(file_path):
            norm_p = os.path.normpath(os.path.abspath(file_path))
            subprocess.Popen(f'explorer /select,"{norm_p}"')

    # =========================================================================
    # FLOATING MINI-DOCK FUNKSIYASI
    # =========================================================================

    def _toggle_mini_dock(self):
        if not self.is_mini_dock:
            self.normal_geometry = self.geometry()
            self.geometry("580x195")
            self.minsize(540, 185)
            self.cockpit_frame.pack_forget()
            self.tabview.pack_forget()
            self.toast_frame.pack_forget()
            self.attributes("-topmost", True)
            self.btn_mini_dock.configure(text="🗖 Kengaytirish", fg_color="#059669")
            self.is_mini_dock = True
        else:
            self.attributes("-topmost", False)
            self.minsize(1050, 760)
            self.geometry(self.normal_geometry)
            self.cockpit_frame.pack(side="top", fill="x", padx=15, pady=(6, 4))
            self.tabview.pack(side="top", fill="both", expand=True, padx=15, pady=(2, 4))
            self.btn_mini_dock.configure(text="🪟 Mini-Dock", fg_color="#334155")
            self.is_mini_dock = False

    # =========================================================================
    # OVOZLI QIDIRUV (VOICE AI SEARCH)
    # =========================================================================

    def _start_voice_search(self):
        if not _SR_AVAILABLE:
            messagebox.showinfo(
                "Ovozli Qidiruv",
                "Ovozni aniqlash tizimi sozlanmoqda.\nIltimos, qo'shiq nomini qidiruv satriga yozing."
            )
            return

        self.btn_voice_search.configure(text="🔴 Eshitilmoqda...", fg_color="#eab308")

        def listen_worker():
            try:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=0.8)
                    audio = r.listen(source, timeout=4, phrase_time_limit=5)
                    text = r.recognize_google(audio, language="uz-UZ")
                    if text:
                        self.after(0, lambda: self._apply_voice_result(text))
            except Exception:
                self.after(0, lambda: self._apply_voice_fallback())

        threading.Thread(target=listen_worker, daemon=True).start()

    def _apply_voice_result(self, text):
        self.btn_voice_search.configure(text="🎙️ Ovozli Qidiruv", fg_color="#dc2626")
        self.entry_search.delete(0, "end")
        self.entry_search.insert(0, text)
        self._start_interactive_search_preview()

    def _apply_voice_fallback(self):
        self.btn_voice_search.configure(text="🎙️ Ovozli Qidiruv", fg_color="#dc2626")
        messagebox.showinfo("Ovoz aniqlanmadi", "Ovoz aniqlanmadi yoki mikrofon ulanmagan. Iltimos matnni qo'lda kiriting.")

    # =========================================================================
    # AIMP PLEYER, SEEKBAR, PLEYLISH VA VIZUALIZATOR SINXRONIZATSIYASI
    # =========================================================================

    def _visualizer_loop(self):
        is_playing = self.player.is_playing and not self.player.is_paused
        self.visualizer.update_activity(is_playing)
        self.after(80, self._visualizer_loop)

    def _player_sync_loop(self):
        # Uyqu taymerini tekshirish
        if self.sleep_timer_end_ts is not None:
            rem = self.sleep_timer_end_ts - time.time()
            if rem <= 0:
                self.sleep_timer_end_ts = None
                self.combo_sleep_timer.set("O'chiq")
                self._stop_playback()
                self.log("💤 Uyqu taymeri vaqti tugadi — ijro to'xtatildi.")

        next_file = self.player.check_auto_advance()
        if next_file and next_file != self.player.current_studio_file:
            self._update_now_playing_display(next_file)
            self._highlight_active_track_everywhere(next_file)

        status = self.player.get_status()
        if status["is_playing"]:
            pos_s = status["pos_sec"]
            dur_s = max(1.0, status["duration_sec"])
            time_str = f"{format_mm_ss(pos_s)} / {format_mm_ss(dur_s)}"
            self.lbl_player_time.configure(text=time_str)
            self.sim_lbl_time.configure(text=time_str)
            self.sim_time_progress.set(min(1.0, pos_s / dur_s))
            self.waveform_seekbar.set_progress(
                pos_s,
                dur_s,
                status["mode"],
                status.get("loop_a_sec"),
                status.get("loop_b_sec")
            )
        self.after(200, self._player_sync_loop)

    def _play_specific_track(self, st_file: str, raw_file: str = None):
        """Istalgan yuklangan qo'shiq ustiga bosilganda darhol AIMP pleyerda ijro etish!"""
        if not st_file or not os.path.exists(st_file):
            messagebox.showinfo("Fayl topilmadi", "Ushbu qo'shiq hali to'liq yuklanmagan yoki o'chirilgan.")
            return

        if not raw_file:
            raw_file = music_engine.find_matching_raw_preview(st_file)

        self.player.load_and_play(st_file, raw_file, os.path.basename(st_file))
        self._clear_ab_loop_action()
        self.btn_play_pause.configure(text="⏸ Pauza", fg_color="#eab308")
        self.btn_sim_play.configure(text="⏸")
        self.btn_ab_toggle.configure(text="🎧 A/B Test: 🟢 STUDIYA DSP 256k", fg_color="#059669")
        self._update_now_playing_display(st_file)
        self._highlight_active_track_everywhere(st_file)

    def _toggle_playback(self):
        if not self.player.is_playing:
            all_items = music_engine.scan_all_library_mp3s(self._get_base_directory(), self._get_target_directory(), scan_all=True)
            if all_items:
                self._play_specific_track(all_items[0]["path"])
            else:
                messagebox.showinfo("Musiqa yo'q", "Hali musiqa yuklanmagan. Avval musiqalarni yuklang yoki ➕ MP3 Qo'shish tugmasini bosing!")
        else:
            self.player.toggle_play_pause()
            if self.player.is_paused:
                self.btn_play_pause.configure(text="▶ Davom", fg_color="#0284c7")
                self.btn_sim_play.configure(text="▶")
            else:
                self.btn_play_pause.configure(text="⏸ Pauza", fg_color="#eab308")
                self.btn_sim_play.configure(text="⏸")

    def _stop_playback(self):
        self.player.stop()
        self.btn_play_pause.configure(text="▶ Tinglash", fg_color="#0284c7")
        self.btn_sim_play.configure(text="▶")
        self.waveform_seekbar.set_progress(0.0, self.player.duration_sec, self.player.current_mode)
        self.lbl_player_time.configure(text=f"00:00 / {format_mm_ss(self.player.duration_sec)}")

    def _on_waveform_seek(self, target_sec: float):
        if self.player.current_studio_file:
            self.player.seek(target_sec)
            self.lbl_player_time.configure(text=f"{format_mm_ss(target_sec)} / {format_mm_ss(self.player.duration_sec)}")

    def _step_seek_action(self, delta_sec: float):
        if self.player.current_studio_file:
            self.player.step_seek(delta_sec)

    def _prev_track_action(self):
        prev_f = self.player.prev_track()
        if prev_f:
            self.btn_play_pause.configure(text="⏸ Pauza", fg_color="#eab308")
            self.btn_sim_play.configure(text="⏸")
            self._update_now_playing_display(prev_f)
            self._highlight_active_track_everywhere(prev_f)

    def _next_track_action(self):
        next_f = self.player.next_track(auto=False)
        if next_f:
            self.btn_play_pause.configure(text="⏸ Pauza", fg_color="#eab308")
            self.btn_sim_play.configure(text="⏸")
            self._update_now_playing_display(next_f)
            self._highlight_active_track_everywhere(next_f)

    def _toggle_shuffle_action(self):
        shuf = self.player.toggle_shuffle()
        self.btn_shuffle.configure(fg_color="#f59e0b" if shuf else "#1e293b")

    def _toggle_repeat_action(self):
        rep = self.player.toggle_repeat()
        if rep == "ALL":
            self.btn_repeat.configure(text="🔁 All", fg_color="#0284c7")
        elif rep == "ONE":
            self.btn_repeat.configure(text="🔂 One", fg_color="#059669")
        else:
            self.btn_repeat.configure(text="➡️ Off", fg_color="#334155")

    def _toggle_mute_action(self):
        muted = self.player.toggle_mute()
        self.btn_mute.configure(text="🔇" if muted else "🔊", text_color="#ef4444" if muted else TXT_PRIMARY)

    def _toggle_ab_test(self):
        new_mode = self.player.toggle_ab()
        if new_mode == "RAW":
            self.btn_ab_toggle.configure(text="🎧 A/B Test: 🔴 ASL YOUTUBE 128k", fg_color="#dc2626")
        else:
            self.btn_ab_toggle.configure(text="🎧 A/B Test: 🟢 STUDIYA DSP 256k", fg_color="#059669")

    def _on_volume_change(self, val):
        self.player.set_volume(float(val))
        self.btn_mute.configure(text="🔊", text_color=TXT_PRIMARY)

    def _update_now_playing_display(self, file_or_name: str):
        full_path = file_or_name if os.path.isabs(file_or_name) else os.path.join(self._get_target_directory(), file_or_name)
        meta = self.player.current_metadata if (self.player.current_studio_file == full_path and self.player.current_metadata) else music_engine.read_mp3_metadata(full_path)

        clean_name = os.path.splitext(os.path.basename(full_path))[0]
        folder_badge = os.path.basename(os.path.dirname(full_path))
        self.lbl_player_title.configure(text=f"🎵 {clean_name}  [{folder_badge}]")
        self.sim_song_title.configure(text=meta.get("title") or clean_name)
        self.sim_artist.configure(text=f"San'atkor: {meta.get('artist', 'O\'zbek San\'atkori')}")

        is_fav = music_engine.is_favorite_track(full_path)
        self.btn_deck_fav.configure(text="❤️" if is_fav else "🤍", fg_color="#be123c" if is_fav else "#1e293b")

        dur_s = meta.get("duration_sec", 210.0)
        br = meta.get("bitrate_kbps", 256)
        sr_hz = meta.get("sample_rate", 44100)
        sz_mb = meta.get("size_mb", 0.0)

        specs_str = f"{br} kbps • {sr_hz // 1000:.1f} kHz • {sz_mb} MB"
        self.lbl_player_specs.configure(text=specs_str)
        self.lbl_aimp_tech_specs.configure(text=specs_str)
        self.waveform_seekbar.set_waveform(meta.get("waveform"), dur_s)

        self._load_track_into_tag_editor(full_path, meta)

        cover_bytes = meta.get("cover_bytes")
        if _PIL_AVAILABLE and cover_bytes:
            try:
                pil_img_deck = Image.open(io.BytesIO(cover_bytes)).resize((58, 58))
                ctk_img_deck = ctk.CTkImage(light_image=pil_img_deck, dark_image=pil_img_deck, size=(58, 58))
                self.lbl_deck_art.configure(image=ctk_img_deck, text="")
                self.lbl_deck_art._image_ref = ctk_img_deck

                pil_img_sim = Image.open(io.BytesIO(cover_bytes)).resize((160, 160))
                ctk_img_sim = ctk.CTkImage(light_image=pil_img_sim, dark_image=pil_img_sim, size=(160, 160))
                self.sim_art_label.configure(image=ctk_img_sim, text="")
                self.sim_art_label._image_ref = ctk_img_sim
            except Exception:
                pass

    def _highlight_active_track_everywhere(self, active_path: str):
        norm_active = os.path.normcase(os.path.abspath(active_path)) if active_path else ""

        for path_key, widgets in self.aimp_playlist_rows.items():
            is_curr = os.path.normcase(os.path.abspath(path_key)) == norm_active
            row_f = widgets.get("row")
            btn_p = widgets.get("btn_play")
            if row_f and row_f.winfo_exists():
                row_f.configure(
                    fg_color=BG_ACTIVE_ROW_TUPLE if is_curr else BG_ROW_TUPLE,
                    border_width=2 if is_curr else 0,
                    border_color="#10b981"
                )
            if btn_p and btn_p.winfo_exists():
                btn_p.configure(text="🔊" if is_curr else "▶", fg_color="#10b981" if is_curr else "#0284c7")

        for _idx, q_item in self.queue_items_widgets.items():
            q_path = q_item.get("file_path")
            card = q_item.get("card")
            btn_p = q_item.get("btn_play")
            if q_path and card and card.winfo_exists():
                is_curr = os.path.normcase(os.path.abspath(q_path)) == norm_active
                card.configure(
                    border_width=2 if is_curr else 0,
                    border_color="#10b981"
                )
                if btn_p and btn_p.winfo_exists():
                    btn_p.configure(text="🔊 Ijroda" if is_curr else "▶ Tinglash", fg_color="#10b981" if is_curr else "#059669")

    # =========================================================================
    # AIMP YAGONA KUTUBXONA, SEVIMLILAR, STUDIO FX, 10-BAND EQ VA ID3v2 FUNKSIYALARI
    # =========================================================================

    def _refresh_aimp_playlist(self):
        if not hasattr(self, "aimp_playlist_scroll"):
            return

        for child in self.aimp_playlist_scroll.winfo_children():
            child.destroy()
        self.aimp_playlist_rows.clear()

        base_dir = self._get_base_directory()
        target_dir = self._get_target_directory()
        scope_val = self.seg_library_scope.get() if hasattr(self, "seg_library_scope") else "🌐 Barcha Papkalar (Hammasi)"

        scan_all = "Faqat Joriy" not in scope_val
        all_items = music_engine.scan_all_library_mp3s(base_dir, target_dir, scan_all=scan_all)

        # Sevimlilar yoki Tarix filtri
        if "Sevimlilar" in scope_val:
            all_items = [it for it in all_items if music_engine.is_favorite_track(it["path"])]
        elif "Oxirgi Eshitilganlar" in scope_val:
            state = music_engine.load_user_library_state()
            hist_paths = [os.path.normcase(os.path.abspath(p)) for p in state.get("history", []) if os.path.exists(p)]
            item_map = {os.path.normcase(os.path.abspath(it["path"])): it for it in all_items}
            ordered_hist = []
            for hp in hist_paths:
                if hp in item_map:
                    ordered_hist.append(item_map[hp])
                elif os.path.exists(hp):
                    ordered_hist.append({
                        "path": hp,
                        "filename": os.path.basename(hp),
                        "folder": os.path.basename(os.path.dirname(hp)),
                        "mtime": os.path.getmtime(hp),
                        "size_mb": round(os.path.getsize(hp) / (1024 * 1024), 2)
                    })
            all_items = ordered_hist

        # Saralash
        sort_mode = self.combo_library_sort.get() if hasattr(self, "combo_library_sort") else "Nomi (A-Z)"
        if "Oxirgi Eshitilganlar" not in scope_val:
            if sort_mode == "Yangilari oldinda":
                all_items.sort(key=lambda x: x.get("mtime", 0), reverse=True)
            elif sort_mode == "Hajmi (MB)":
                all_items.sort(key=lambda x: x.get("size_mb", 0), reverse=True)
            else:
                all_items.sort(key=lambda x: x["filename"].lower())

        all_mp3_paths = [it["path"] for it in all_items]
        self.player.set_playlist(all_mp3_paths)

        filter_q = self.entry_aimp_filter.get().strip().lower() if hasattr(self, "entry_aimp_filter") else ""
        filtered = [
            it for it in all_items
            if not filter_q or filter_q in it["filename"].lower() or filter_q in it["folder"].lower()
        ]
        self.lbl_aimp_count.configure(text=f"Jami: {len(filtered)} ta MP3")

        if not filtered:
            empty_msg = (
                "❤️ Sevimlilar ro'yxati hozircha bo'sh.\nQo'shiqlar yonidagi '🤍' tugmasini bosib sevimlilarga qo'shing!"
                if "Sevimlilar" in scope_val else
                "Hozircha MP3 qo'shiqlar topilmadi.\nKatalogdan yuklang yoki '➕ MP3 Qo'shish' tugmasini bosing."
            )
            ctk.CTkLabel(
                self.aimp_playlist_scroll,
                text=empty_msg,
                font=ctk.CTkFont(size=12),
                text_color=TXT_SECONDARY
            ).pack(pady=35)
            return

        active_norm = os.path.normcase(os.path.abspath(self.player.current_studio_file)) if self.player.current_studio_file else ""

        for idx, item_info in enumerate(filtered, 1):
            mp3_path = item_info["path"]
            folder_label = item_info["folder"]
            is_curr = os.path.normcase(os.path.abspath(mp3_path)) == active_norm
            is_fav = music_engine.is_favorite_track(mp3_path)
            meta = music_engine.read_mp3_metadata(mp3_path)

            row = ctk.CTkFrame(
                self.aimp_playlist_scroll,
                corner_radius=8,
                fg_color=BG_ACTIVE_ROW_TUPLE if is_curr else BG_ROW_TUPLE,
                border_width=2 if is_curr else 0,
                border_color="#10b981",
                height=44,
                cursor="hand2"
            )
            row.pack(fill="x", padx=4, pady=3)

            btn_play = ctk.CTkButton(
                row,
                text="🔊" if is_curr else "▶",
                width=30,
                height=26,
                fg_color="#10b981" if is_curr else "#0284c7",
                hover_color="#059669",
                command=lambda p=mp3_path: self._play_specific_track(p)
            )
            btn_play.pack(side="left", padx=(6, 4), pady=6)

            btn_fav = ctk.CTkButton(
                row,
                text="❤️" if is_fav else "🤍",
                width=28,
                height=26,
                fg_color="#be123c" if is_fav else "#334155",
                hover_color="#e11d48",
                font=ctk.CTkFont(size=11),
                command=lambda p=mp3_path: self._toggle_row_favorite(p)
            )
            btn_fav.pack(side="left", padx=(0, 5), pady=6)

            badge_folder = ctk.CTkLabel(
                row,
                text=f" 📁 {folder_label[:18]} ",
                font=ctk.CTkFont(size=10, weight="bold"),
                fg_color=("#cbd5e1", "#1e293b"),
                text_color=TXT_ACCENT_BLUE,
                corner_radius=5
            )
            badge_folder.pack(side="left", padx=(0, 6), pady=6)

            lbl_title = ctk.CTkLabel(
                row,
                text=f"{idx:02d}. {meta['artist']} - {meta['title']}",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=TXT_PRIMARY,
                anchor="w",
                cursor="hand2"
            )
            lbl_title.pack(side="left", fill="x", expand=True, pady=6)

            btn_del = ctk.CTkButton(
                row,
                text="🗑️",
                width=26,
                height=26,
                fg_color="#7f1d1d",
                hover_color="#dc2626",
                command=lambda p=mp3_path: self._delete_library_mp3(p)
            )
            btn_del.pack(side="right", padx=(2, 6))

            btn_tag = ctk.CTkButton(
                row,
                text="🏷️",
                width=26,
                height=26,
                fg_color="#334155",
                hover_color="#475569",
                command=lambda p=mp3_path, m=meta: self._load_track_into_tag_editor(p, m)
            )
            btn_tag.pack(side="right", padx=2)

            btn_loc = ctk.CTkButton(
                row,
                text="📂",
                width=26,
                height=26,
                fg_color="#0284c7",
                hover_color="#0369a1",
                command=lambda p=mp3_path: self._reveal_file_in_explorer(p)
            )
            btn_loc.pack(side="right", padx=2)

            info_txt = f"{format_mm_ss(meta['duration_sec'])} • {meta['size_mb']}MB"
            lbl_meta = ctk.CTkLabel(
                row,
                text=info_txt,
                font=ctk.CTkFont(family="Consolas", size=10),
                text_color=TXT_SECONDARY,
                cursor="hand2"
            )
            lbl_meta.pack(side="right", padx=(4, 6))

            for clickable in (row, badge_folder, lbl_title, lbl_meta):
                clickable.bind("<Button-1>", lambda _e, p=mp3_path: self._play_specific_track(p))

            self.aimp_playlist_rows[mp3_path] = {
                "row": row,
                "btn_play": btn_play
            }

    def _toggle_row_favorite(self, mp3_path: str):
        is_fav = music_engine.toggle_favorite_track(mp3_path)
        if self.player.current_studio_file and os.path.normcase(os.path.abspath(self.player.current_studio_file)) == os.path.normcase(os.path.abspath(mp3_path)):
            self.btn_deck_fav.configure(text="❤️" if is_fav else "🤍", fg_color="#be123c" if is_fav else "#1e293b")
        self._refresh_aimp_playlist()

    def _copy_favorites_to_usb_or_folder(self):
        state = music_engine.load_user_library_state()
        favs = [f for f in state.get("favorites", []) if os.path.exists(f)]
        if not favs:
            messagebox.showinfo(
                "Sevimlilar bo'sh",
                "Avval yoqtirgan qo'shiqlaringiz yonidagi '🤍' tugmasini bosib ularni '❤️ Sevimlilar'ga qo'shing!"
            )
            return

        if self.current_usb_drives:
            cur_idx = self.usb_combo.cget("values").index(self.usb_combo.get()) if self.usb_combo.get() in self.usb_combo.cget("values") else 0
            dest_root = self.current_usb_drives[cur_idx]["root"]
            dest_dir = os.path.join(dest_root, "02_SEVIMLI_SANATKORLAR")
        else:
            dest_dir = os.path.join(self._get_base_directory(), "02_SEVIMLI_SANATKORLAR")

        copied = music_engine.copy_tracks_to_folder(favs, dest_dir)
        self._refresh_aimp_playlist()
        messagebox.showinfo(
            "📲 Sevimlilar Ko'chirildi!",
            f"❤️ {copied} ta Sevimli qo'shiq muvaffaqiyatli ko'chirildi va pleylist tuzildi:\n\n📁 {dest_dir}"
        )

    def _apply_studio_fx_action(self):
        target_mp3 = self.player.current_studio_file or self.selected_tag_file
        if not target_mp3 or not os.path.exists(target_mp3):
            messagebox.showinfo("Trek tanlanmagan", "Studio FX (Slowed+Reverb / 8D / Speed) qo'llash uchun avval biror qo'shiqni tanlang!")
            return

        fx_name = self.combo_studio_fx.get()
        self.btn_apply_fx.configure(text="⏳ Ishlanmoqda...", state="disabled")

        def fx_worker():
            out_path = music_engine.apply_studio_fx_to_track(target_mp3, fx_name, save_as_copy=True)
            self.after(0, lambda: self._on_studio_fx_done(out_path, fx_name))

        threading.Thread(target=fx_worker, daemon=True).start()

    def _on_studio_fx_done(self, out_path: str, fx_name: str):
        self.btn_apply_fx.configure(text="✨ Qo'llash", state="normal")
        if out_path and os.path.exists(out_path):
            self._refresh_aimp_playlist()
            self._play_specific_track(out_path)
            messagebox.showinfo(
                "🎛️ Studio FX Tayyor!",
                f"'{fx_name}' effekti muvaffaqiyatli qo'llandi va yangi MP3 sifatida ijro etilmoqda:\n\n{os.path.basename(out_path)}"
            )
        else:
            messagebox.showerror("Xatolik", "Studio FX qo'llashda xatolik yuz berdi.")

    def _choose_custom_cover_image(self):
        img_p = filedialog.askopenfilename(
            title="MP3 uchun muqova rasmini tanlang",
            filetypes=[("Rasmlar", "*.jpg *.jpeg *.png")]
        )
        if img_p and os.path.exists(img_p):
            self.selected_cover_image_path = img_p
            self.btn_choose_cover.configure(text="✅ Rasm Tanlandi", fg_color="#059669")

    def _delete_library_mp3(self, mp3_path: str):
        if not os.path.exists(mp3_path):
            return
        ans = messagebox.askyesno("Qo'shiqni o'chirish", f"Ushbu MP3 faylni o'chirib tashlaymizmi?\n\n{os.path.basename(mp3_path)}")
        if ans:
            if self.player.current_studio_file and os.path.normcase(os.path.abspath(self.player.current_studio_file)) == os.path.normcase(os.path.abspath(mp3_path)):
                self._stop_playback()
            try:
                os.remove(mp3_path)
                self._refresh_aimp_playlist()
            except Exception as e:
                messagebox.showerror("Xatolik", f"Faylni o'chirishda xatolik:\n{e}")

    def _import_external_mp3s(self):
        files = filedialog.askopenfilenames(
            title="Pleylistga MP3 qo'shiqlar qo'shish",
            filetypes=[("MP3 Audio Fayllar", "*.mp3")]
        )
        if not files:
            return

        target_dir = self._get_target_directory()
        copied = music_engine.copy_tracks_to_folder(list(files), target_dir)
        if copied > 0:
            self._refresh_aimp_playlist()
            first_added = os.path.join(target_dir, os.path.basename(files[0]))
            if os.path.exists(first_added):
                self._play_specific_track(first_added)

    def _on_aimp_preset_selected(self, preset_name: str):
        gains = music_engine.AIMP_EQ_PRESETS.get(preset_name)
        if not gains or not self.eq_sliders:
            return
        for (sl, val_lbl), g in zip(self.eq_sliders, gains):
            sl.set(g)
            val_lbl.configure(text=f"{g:+.1f}")

    def _apply_eq_to_current_track(self):
        target_mp3 = self.player.current_studio_file or self.selected_tag_file
        if not target_mp3 or not os.path.exists(target_mp3):
            messagebox.showinfo("Trek tanlanmagan", "Avval pleylistdan yoki yuklash navbatidan biror qo'shiqni tanlang!")
            return

        gains = [round(float(sl.get()), 1) for sl, _ in self.eq_sliders]
        saved_pos = self.player.get_position_sec() if self.player.is_playing else 0.0
        was_playing = self.player.is_playing
        if was_playing:
            self.player.stop()

        self.btn_apply_eq.configure(text="⏳ Studio EQ qo'llanmoqda...", state="disabled")

        def eq_worker():
            ok = music_engine.remaster_track_with_eq(target_mp3, gains, preamp_db=0.0)
            self.after(0, lambda: self._on_eq_remaster_done(ok, target_mp3, saved_pos, was_playing))

        threading.Thread(target=eq_worker, daemon=True).start()

    def _on_eq_remaster_done(self, ok: bool, target_mp3: str, saved_pos: float, was_playing: bool):
        self.btn_apply_eq.configure(text="⚡ Joriy Qo'shiqqa 10-Band EQ Muhrlash", state="normal")
        if ok:
            self._play_specific_track(target_mp3)
            if saved_pos > 0.5:
                self.player.seek(saved_pos)
            messagebox.showinfo("AIMP Studio EQ", "10-Polosali Ekvayzer sozlamalari qo'shiqqa muvaffaqiyatli muhrlandi va ijro yangilandi!")
        else:
            messagebox.showerror("Xatolik", "Ekvayzerni qo'llashda xatolik yuz berdi.")

    def _load_track_into_tag_editor(self, mp3_path: str, meta: dict = None):
        if not mp3_path or not os.path.exists(mp3_path):
            return
        self.selected_tag_file = mp3_path
        self.selected_cover_image_path = None
        if hasattr(self, "btn_choose_cover"):
            self.btn_choose_cover.configure(text="🖼️ Rasm Tanlash", fg_color="#334155")
        meta = meta or music_engine.read_mp3_metadata(mp3_path)

        for entry, key in [
            (self.entry_tag_title, "title"),
            (self.entry_tag_artist, "artist"),
            (self.entry_tag_album, "album"),
        ]:
            entry.delete(0, "end")
            entry.insert(0, str(meta.get(key, "")))

    def _save_current_tags(self):
        target_mp3 = self.selected_tag_file or self.player.current_studio_file
        if not target_mp3 or not os.path.exists(target_mp3):
            messagebox.showinfo("Trek tanlanmagan", "Teglarni saqlash uchun avval qo'shiqni tanlang!")
            return

        new_title = self.entry_tag_title.get().strip() or "Qo'shiq"
        new_artist = self.entry_tag_artist.get().strip() or "O'zbek San'atkori"
        new_album = self.entry_tag_album.get().strip() or "Avto Magnitola To'plami"

        ok = music_engine.update_mp3_tags(
            target_mp3,
            new_title,
            new_artist,
            new_album,
            "2026",
            cover_image_path=self.selected_cover_image_path
        )
        if ok:
            self.selected_cover_image_path = None
            self.btn_choose_cover.configure(text="🖼️ Rasm Tanlash", fg_color="#334155")
            self.player.current_metadata = music_engine.read_mp3_metadata(target_mp3)
            self._update_now_playing_display(target_mp3)
            self._refresh_aimp_playlist()
            messagebox.showinfo("ID3v2 Saqlandi", f"Teglar va muqova muvaffaqiyatli yangilandi:\n{new_artist} - {new_title}")
        else:
            messagebox.showerror("Xatolik", "ID3v2 teglarni saqlashda xatolik yuz berdi.")

    # =========================================================================
    # FLESHKA VA SAQLASH MANZILI FUNKSIYALARI
    # =========================================================================

    def _refresh_drives(self):
        drives = music_engine.detect_usb_drives()
        self.current_usb_drives = drives

        if drives:
            vals = [d["display"] for d in drives]
            self.usb_combo.configure(values=vals)
            self.usb_combo.set(vals[0])
            self._on_usb_selected(vals[0])
            self._show_toast(vals[0])
        else:
            self.usb_combo.configure(values=["Fleshka aniqlanmadi"])
            self.usb_combo.set("Fleshka aniqlanmadi")
            if self.dest_mode_var.get() == "usb":
                self.dest_mode_var.set("desktop")
            self.lbl_storage_info.configure(text="Manzil: Ish stoli (Desktop)")
            self.storage_progress.set(0.2)
            self._dismiss_toast()

    def _on_usb_selected(self, choice):
        if not self.current_usb_drives:
            return
        idx = self.usb_combo.cget("values").index(choice) if choice in self.usb_combo.cget("values") else 0
        d = self.current_usb_drives[idx]
        pct = d["used_percent"] / 100.0
        self.storage_progress.set(pct)
        self.lbl_storage_info.configure(text=f"Fleshka ({d['letter']}:): {d['free_gb']} GB bo'sh / {d['total_gb']} GB")
        self._refresh_aimp_playlist()

    def _on_dest_mode_toggle(self):
        mode = self.dest_mode_var.get()
        if mode == "usb" and not self.current_usb_drives:
            messagebox.showwarning("Fleshka yo'q", "Fleshka aniqlanmadi! Fleshkani ulab 🔄 tugmasini bosing.")
            self.dest_mode_var.set("desktop")
        elif mode == "custom" and not self.custom_base_dir:
            self._choose_custom_base_dir()
        self._refresh_aimp_playlist()

    def _get_base_directory(self) -> str:
        mode = self.dest_mode_var.get()
        if mode == "usb" and self.current_usb_drives:
            cur_idx = self.usb_combo.cget("values").index(self.usb_combo.get()) if self.usb_combo.get() in self.usb_combo.cget("values") else 0
            return self.current_usb_drives[cur_idx]["root"]
        elif mode == "custom" and self.custom_base_dir and os.path.exists(self.custom_base_dir):
            return self.custom_base_dir
        return os.path.join(os.environ.get("USERPROFILE", ""), "Desktop")

    def _get_target_directory(self, subfolder_name: str = "") -> str:
        raw_folder = self.combo_target_folder.get().strip() or "01_YANGI_XITLAR_2026"
        clean_folder = music_engine.sanitize_title(raw_folder).replace(" ", "_") or "01_YANGI_XITLAR_2026"
        base_dir = self._get_base_directory()
        target = os.path.join(base_dir, clean_folder)
        if subfolder_name and hasattr(self, "chk_auto_subfolder") and self.chk_auto_subfolder.get():
            clean_sub = music_engine.sanitize_title(subfolder_name)
            if clean_sub:
                target = os.path.join(target, clean_sub)
        os.makedirs(target, exist_ok=True)
        return target

    def _open_target_folder(self):
        t = self._get_target_directory()
        if os.path.exists(t):
            subprocess.Popen(f'explorer "{os.path.normpath(t)}"')
        else:
            messagebox.showinfo("Jild", f"Jild hali yaratilmagan: {t}")

    def _get_selected_bitrate(self) -> str:
        raw_b = self.combo_bitrate.get().strip().lower() if hasattr(self, "combo_bitrate") else "256k"
        m = re.search(r"\d+", raw_b)
        if m:
            val = max(96, min(320, int(m.group(0))))
            return f"{val}k"
        return "256k"

    # =========================================================================
    # TURBO PARALLEL ENGINE (3-BOSQICHLI KAFOLAT + JONLI MONITORING)
    # =========================================================================

    def _start_artist_turbo(self, artist_info):
        if self.is_downloading:
            messagebox.showwarning("Jarayon band", "Hozirda yuklash jarayoni ketmoqda.")
            return

        count = music_engine.parse_track_count(self.combo_artist_count.get(), default=15)
        self.combo_target_folder.set("02_SEVIMLI_SANATKORLAR")
        self._start_turbo_pipeline(artist_info["query"], count, artist_info["name"], subfolder=artist_info["name"])

    def _start_collection_turbo(self, col_info):
        if self.is_downloading:
            messagebox.showwarning("Jarayon band", "Hozirda yuklash jarayoni ketmoqda.")
            return

        count = music_engine.parse_track_count(
            self.combo_style_count.get() if hasattr(self, "combo_style_count") else col_info.get("count", 20),
            default=col_info.get("count", 20)
        )
        self.combo_target_folder.set(col_info["target_folder"])
        self._start_turbo_pipeline(col_info["query"], count, col_info["title"], subfolder="")

    def _start_custom_search_turbo(self):
        if self.is_downloading:
            messagebox.showwarning("Jarayon band", "Hozirda yuklash jarayoni ketmoqda.")
            return

        text = self.entry_search.get().strip()
        if not text:
            messagebox.showwarning("Matn yo'q", "Qo'shiq nomi yoki YouTube linkini kiriting!")
            return

        count = music_engine.parse_track_count(self.combo_search_count.get(), default=15)
        self._start_turbo_pipeline(text, count, f"'{text}'", subfolder="")

    def _start_direct_tracks_turbo(self, tracks_list: list, title_display: str):
        if self.is_downloading:
            messagebox.showwarning("Jarayon band", "Hozirda yuklash jarayoni ketmoqda.")
            return

        self.is_downloading = True
        self.cancel_requested = False
        self.btn_cancel_turbo.configure(state="normal")
        self.overall_progress.set(0)
        self.tabview.set("⚡ Turbo Yuklash Paneli (Live)")

        t = threading.Thread(
            target=self._worker_turbo_pipeline,
            args=("", len(tracks_list), title_display, "", tracks_list),
            daemon=True
        )
        t.start()

    def _start_turbo_pipeline(self, query: str, limit: int, title_display: str, subfolder: str = ""):
        self.is_downloading = True
        self.cancel_requested = False
        self.btn_cancel_turbo.configure(state="normal")
        self.overall_progress.set(0)
        self.tabview.set("⚡ Turbo Yuklash Paneli (Live)")
        self.log(f"🔎 '{title_display}' bo'yicha {limit} ta qo'shiq qidirilmoqda...")

        t = threading.Thread(
            target=self._worker_turbo_pipeline,
            args=(query, limit, title_display, subfolder, None),
            daemon=True
        )
        t.start()

    def _cancel_download(self):
        self.cancel_requested = True
        self.log("⏹️ [Diqqat] Jarayonni to'xtatish so'rovi yuborildi...")

    def _find_existing_file_by_title(self, target_dir: str, title: str) -> str:
        norm = music_engine.normalize_title_for_comparison(title)
        if not os.path.exists(target_dir):
            return None
        for f in os.listdir(target_dir):
            if f.lower().endswith(".mp3") and music_engine.normalize_title_for_comparison(f) == norm:
                return os.path.join(target_dir, f)
        return None

    def _worker_turbo_pipeline(self, query: str, limit: int, title_display: str, subfolder: str = "", pre_tracks: list = None):
        try:
            target_dir = self._get_target_directory(subfolder_name=subfolder)
            use_smart_sync = self.chk_smart_sync.get()
            num_streams = int(self.combo_idm_streams.get().split()[0]) if hasattr(self, "combo_idm_streams") else 32
            chosen_bitrate = self._get_selected_bitrate()

            if pre_tracks is not None:
                tracks = list(pre_tracks)
            else:
                tracks = music_engine.search_youtube(
                    query=query,
                    limit=limit,
                    log_cb=self.log,
                    cancel_check=lambda: self.cancel_requested
                )

            if not tracks:
                self.log("⚠️ Qidiruv bo'yicha qo'shiqlar topilmadi yoki bekor qilindi.")
                return

            existing_tracks = music_engine.scan_existing_tracks(target_dir) if use_smart_sync else set()
            total_tracks = len(tracks)

            self.after(0, lambda: self._setup_queue_widgets(tracks, existing_tracks, target_dir, num_streams))
            self.after(0, lambda: self.lbl_queue_stats.configure(text=f"Jami: {total_tracks} | Tayyor: 0"))

            max_workers = 4
            completed_count = 0
            success_count = 0
            lock = threading.Lock()

            def process_single(task_tuple):
                nonlocal success_count
                idx, tr = task_tuple
                if self.cancel_requested:
                    return None

                if use_smart_sync and music_engine.is_track_already_present(tr["title"], existing_tracks):
                    existing_mp3 = self._find_existing_file_by_title(target_dir, tr["title"])
                    with lock:
                        success_count += 1
                    self.after(0, lambda i=idx, fp=existing_mp3: self._update_queue_item_status(i, 1.0, "Sinxron (Mavjud) ⏩", "#0284c7", 0.0, [1.0] * num_streams, file_path=fp))
                    return existing_mp3

                def on_track_prog(i, p, s, spd=0.0, s_arr=None):
                    col = "#22c55e" if p >= 1.0 else ("#ef4444" if "Xato" in s else "#38bdf8")
                    self.after(0, lambda: self._update_queue_item_status(i, p, s, col, spd or 0.0, s_arr))

                st_file, raw_file = music_engine.download_and_process_track(
                    track=tr,
                    out_dir=target_dir,
                    index=idx,
                    bitrate=chosen_bitrate,
                    dsp_profile=music_engine.DEFAULT_DSP_PROFILE,
                    keep_preview_raw=True,
                    num_streams=num_streams,
                    log_cb=self.log,
                    task_progress_cb=on_track_prog,
                    cancel_check=lambda: self.cancel_requested
                )

                if st_file and os.path.exists(st_file):
                    with lock:
                        success_count += 1
                    self.after(0, lambda i=idx, fp=st_file, rf=raw_file: self._update_queue_item_status(i, 1.0, "Tayyor ✅ (Bosib eshiting)", "#22c55e", 0.0, [1.0] * num_streams, file_path=fp, raw_path=rf))
                    self.after(0, self._refresh_aimp_playlist)
                    if not self.player.is_playing:
                        self.after(0, lambda fp=st_file, rf=raw_file: self._play_specific_track(fp, rf))

                return st_file

            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {executor.submit(process_single, (idx, tr)): idx for idx, tr in enumerate(tracks, 1)}

                for future in concurrent.futures.as_completed(futures):
                    if self.cancel_requested:
                        break
                    _ = future.result()
                    with lock:
                        completed_count += 1
                        prog = completed_count / total_tracks
                        sc = success_count
                        cc = completed_count
                        self.after(0, lambda p=prog, c=cc, s=sc: (
                            self.overall_progress.set(p),
                            self.lbl_queue_stats.configure(text=f"Jami: {total_tracks} | Tayyor: {s} ({c}/{total_tracks})")
                        ))

            music_engine.generate_playlist(target_dir)
            self.after(0, self._refresh_aimp_playlist)
            self.log(f"✅ Yuklash yakunlandi! Muvaffaqiyatli: {success_count}/{total_tracks} ta qo'shiq ({target_dir})")

            self.after(0, lambda sc=success_count: messagebox.showinfo(
                "IDM Turbo Yuklash Yakunlandi",
                f"Qo'shiqlar muvaffaqiyatli yuklandi va studiyaviy {chosen_bitrate} MP3 formatga o'girildi!\n\n"
                f"✅ Tayyor treklar: {sc} / {total_tracks} ta\n"
                f"📁 Saqlangan papka:\n{target_dir}\n\n"
                f"🎧 Istalgan qo'shiq ustiga bosib AIMP pleyerda eshitishingiz yoki '🎧 AIMP Kutubxona & Studio' bo'limida barchasini ko'rishingiz mumkin!"
            ))

        except Exception as e:
            self.log(f"❌ Xatolik: {str(e)}")
            self.after(0, lambda: messagebox.showerror("Xatolik", f"Yuklashda xatolik yuz berdi:\n{str(e)}"))

        finally:
            self.is_downloading = False
            self.cancel_requested = False
            self.after(0, lambda: self.btn_cancel_turbo.configure(state="disabled"))
            self.after(0, lambda: self.lbl_idm_speed.configure(text="⚡ Tezlik: 0.0 MB/s"))

    def _setup_queue_widgets(self, tracks, existing_tracks, target_dir, num_streams=32):
        for child in self.queue_scroll.winfo_children():
            child.destroy()
        self.queue_items_widgets.clear()

        for idx, tr in enumerate(tracks, 1):
            is_present = music_engine.is_track_already_present(tr["title"], existing_tracks)
            existing_mp3 = self._find_existing_file_by_title(target_dir, tr["title"]) if is_present else None

            card = ctk.CTkFrame(self.queue_scroll, corner_radius=8, fg_color=BG_ROW_TUPLE, height=62)
            card.pack(fill="x", pady=4, padx=5)

            left_box = ctk.CTkFrame(card, fg_color="transparent")
            left_box.pack(side="left", fill="both", expand=True, padx=12, pady=6)

            title_l = ctk.CTkLabel(
                left_box,
                text=f"{idx:02d}. {tr['title']}",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=TXT_PRIMARY,
                anchor="w"
            )
            title_l.pack(fill="x")

            prog_bar = ctk.CTkProgressBar(left_box, height=5)
            prog_bar.set(1.0 if is_present else 0.0)
            prog_bar.pack(fill="x", pady=(2, 2))

            matrix_canvas = tk.Canvas(left_box, height=8, bg="#0b0f19", highlightthickness=0)
            matrix_canvas.pack(fill="x", pady=(1, 0))

            btn_open_loc = ctk.CTkButton(
                card,
                text="📂",
                width=30,
                height=28,
                fg_color="#0284c7" if existing_mp3 else "#334155",
                hover_color="#0369a1",
                state="normal" if existing_mp3 else "disabled",
                command=lambda fp=existing_mp3: self._reveal_file_in_explorer(fp) if fp else None
            )
            btn_open_loc.pack(side="right", padx=(4, 10), pady=6)

            btn_play_item = ctk.CTkButton(
                card,
                text="▶ Tinglash",
                width=92,
                height=28,
                fg_color="#059669" if existing_mp3 else "#334155",
                hover_color="#047857",
                state="normal" if existing_mp3 else "disabled",
                font=ctk.CTkFont(size=11, weight="bold"),
                command=lambda fp=existing_mp3: self._play_specific_track(fp) if fp else None
            )
            btn_play_item.pack(side="right", padx=(4, 4), pady=6)

            status_text = "Sinxron (Bosib eshiting) ⏩" if is_present else f"IDM {num_streams}x Kutilmoqda ⏳"
            status_color = "#0284c7" if is_present else TXT_SECONDARY

            status_lbl = ctk.CTkLabel(card, text=status_text, font=ctk.CTkFont(size=11, weight="bold"), text_color=status_color, width=175)
            status_lbl.pack(side="right", padx=6, pady=6)

            self.queue_items_widgets[idx] = {
                "card": card,
                "left_box": left_box,
                "title_lbl": title_l,
                "prog": prog_bar,
                "status_lbl": status_lbl,
                "btn_play": btn_play_item,
                "btn_loc": btn_open_loc,
                "canvas": matrix_canvas,
                "num_streams": num_streams,
                "file_path": existing_mp3,
                "raw_path": None
            }

            if existing_mp3:
                self._bind_card_click_to_play(idx, existing_mp3, None)

    def _bind_card_click_to_play(self, idx: int, file_path: str, raw_path: str = None):
        if idx not in self.queue_items_widgets or not file_path:
            return
        item = self.queue_items_widgets[idx]
        item["file_path"] = file_path
        item["raw_path"] = raw_path

        btn_p = item.get("btn_play")
        if btn_p and btn_p.winfo_exists():
            btn_p.configure(
                state="normal",
                fg_color="#059669",
                command=lambda fp=file_path, rf=raw_path: self._play_specific_track(fp, rf)
            )

        btn_loc = item.get("btn_loc")
        if btn_loc and btn_loc.winfo_exists():
            btn_loc.configure(
                state="normal",
                fg_color="#0284c7",
                command=lambda fp=file_path: self._reveal_file_in_explorer(fp)
            )

        for w in (item.get("card"), item.get("left_box"), item.get("title_lbl"), item.get("status_lbl")):
            if w and w.winfo_exists():
                w.configure(cursor="hand2")
                w.bind("<Button-1>", lambda _e, fp=file_path, rf=raw_path: self._play_specific_track(fp, rf))

    def _update_queue_item_status(self, idx, progress, status_text, color="#38bdf8", speed=0.0, stream_arr=None, file_path=None, raw_path=None):
        if idx in self.queue_items_widgets:
            item = self.queue_items_widgets[idx]
            item["prog"].set(progress)
            item["status_lbl"].configure(text=status_text, text_color=color)

            if file_path:
                self._bind_card_click_to_play(idx, file_path, raw_path)

            if speed > 0.0 and hasattr(self, "lbl_idm_speed"):
                self.lbl_idm_speed.configure(text=f"⚡ Tezlik: {speed:.1f} MB/s")

            canvas = item.get("canvas")
            if canvas and canvas.winfo_width() > 10:
                cw = canvas.winfo_width()
                canvas.delete("all")
                n_str = item.get("num_streams", 32)
                pad = 1
                bw = max(2, (cw - (n_str * pad)) / n_str)

                for si in range(n_str):
                    sp = stream_arr[si] if (stream_arr and si < len(stream_arr)) else (1.0 if progress >= 1.0 else 0.0)
                    bx = si * (bw + pad)
                    col = "#10b981" if sp >= 0.9 else ("#38bdf8" if sp > 0.05 else "#1e293b")
                    canvas.create_rectangle(bx, 0, bx + bw, 8, fill=col, outline="")

    def log(self, text: str):
        self.log_queue.put(text)

    def _process_log_queue(self):
        latest_msg = None
        while not self.log_queue.empty():
            latest_msg = self.log_queue.get_nowait()
        if latest_msg and hasattr(self, "lbl_live_log") and self.lbl_live_log.winfo_exists():
            self.lbl_live_log.configure(text=f"📡 {latest_msg}")
        self.after(100, self._process_log_queue)


def main():
    app = MusicCenterApp()
    app.mainloop()


if __name__ == "__main__":
    main()
