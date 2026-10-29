import os
import sys
import threading
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import pygame

# Paths
MINUS_PATH = r"C:\Users\MuzaffarZed\Desktop\vakal minus\minus\Mani izlab ovvora boʻlmang karaoke.mp3"
VOCAL_PATH = r"C:\Users\MuzaffarZed\Desktop\vakal minus\vocall\untitled_2026-10-16 16-35-06_Insert 10.wav"
OUT_DIR = r"C:\Users\MuzaffarZed\Desktop\vakal minus"

class VocalSyncStudio:
    def __init__(self, root):
        self.root = root
        self.root.title("MuzaffarZed Studio - Vocal Sync & Master Pro")
        self.root.geometry("680x580")
        self.root.configure(bg="#0f172a")
        self.root.resizable(False, False)

        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)

        # Variables
        self.is_playing = False
        self.current_pos = 20.0 # start near the entrance
        self.offset_var = tk.DoubleVar(value=12.08)
        self.minus_vol_var = tk.DoubleVar(value=0.85)
        self.vocal_vol_var = tk.DoubleVar(value=1.0)
        self.status_var = tk.StringVar(value="Tayyor. Tinglash uchun 'Play (20s dan)' tugmasini bosing.")

        # Sounds
        self.chan_minus = pygame.mixer.Channel(0)
        self.chan_vocal = pygame.mixer.Channel(1)

        self.setup_ui()
        self.load_audio_cache()

    def setup_ui(self):
        # Header
        hdr = tk.Frame(self.root, bg="#1e293b", padx=20, pady=15)
        hdr.pack(fill="x")

        tk.Label(hdr, text="MUZAFFARZED STUDIO", font=("Segoe UI", 16, "bold"), fg="#38bdf8", bg="#1e293b").pack(anchor="w")
        tk.Label(hdr, text="Vokal va Minusni Millisekundigacha Jonli Moslash Pulti", font=("Segoe UI", 10), fg="#94a3b8", bg="#1e293b").pack(anchor="w")

        # Main Body
        body = tk.Frame(self.root, bg="#0f172a", padx=25, pady=20)
        body.pack(fill="both", expand=True)

        # Offset Display Card
        card = tk.Frame(body, bg="#1e293b", padx=20, pady=15, relief="ridge", bd=1)
        card.pack(fill="x", pady=10)

        tk.Label(card, text="VOKAL KIKIRISH VAQTI (DELAY OFFSET):", font=("Segoe UI", 10, "bold"), fg="#e2e8f0", bg="#1e293b").pack()
        self.lbl_offset = tk.Label(card, text="12.080 s  (12080 ms)", font=("Consolas", 26, "bold"), fg="#10b981", bg="#1e293b")
        self.lbl_offset.pack(pady=5)
        tk.Label(card, text="4-Takt Kuchli Zarbasi (Tavsiya etilgan me'yor: 12.08s)", font=("Segoe UI", 9, "italic"), fg="#64748b", bg="#1e293b").pack()

        # Slider
        slider_frame = tk.Frame(body, bg="#0f172a")
        slider_frame.pack(fill="x", pady=10)

        self.slider = ttk.Scale(slider_frame, from_=10.0, to_=14.0, orient="horizontal", variable=self.offset_var, command=self.on_slider_change)
        self.slider.pack(fill="x", pady=5)

        # Micro-Nudge Buttons
        btn_box = tk.Frame(body, bg="#0f172a")
        btn_box.pack(fill="x", pady=5)

        tk.Button(btn_box, text="-250ms (Oldinga)", command=lambda: self.nudge(-0.25), bg="#334155", fg="#f8fafc", font=("Segoe UI", 9, "bold"), padx=8, pady=4).pack(side="left", padx=4)
        tk.Button(btn_box, text="-50ms", command=lambda: self.nudge(-0.05), bg="#334155", fg="#f8fafc", font=("Segoe UI", 9, "bold"), padx=8, pady=4).pack(side="left", padx=4)
        tk.Button(btn_box, text="🎯 12.08s (Asosiy)", command=lambda: self.set_exact(12.08), bg="#059669", fg="#ffffff", font=("Segoe UI", 9, "bold"), padx=10, pady=4).pack(side="left", padx=8)
        tk.Button(btn_box, text="+50ms", command=lambda: self.nudge(0.05), bg="#334155", fg="#f8fafc", font=("Segoe UI", 9, "bold"), padx=8, pady=4).pack(side="left", padx=4)
        tk.Button(btn_box, text="+250ms (Orqaga)", command=lambda: self.nudge(0.25), bg="#334155", fg="#f8fafc", font=("Segoe UI", 9, "bold"), padx=8, pady=4).pack(side="left", padx=4)

        # Playback Controls
        ctrl = tk.Frame(body, bg="#0f172a")
        ctrl.pack(fill="x", pady=15)

        self.btn_play = tk.Button(ctrl, text="▶ 20-soniyadan Tinglash (Intro Kirishi)", command=self.toggle_play, bg="#2563eb", fg="#ffffff", font=("Segoe UI", 12, "bold"), pady=8)
        self.btn_play.pack(fill="x")

        # Export Button
        exp_frame = tk.Frame(body, bg="#0f172a")
        exp_frame.pack(fill="x", pady=10)

        self.btn_export = tk.Button(exp_frame, text="✨ SHU VAQT BILAN MUKAMMAL MASTER EKSPORT QILISH", command=self.export_master, bg="#d97706", fg="#ffffff", font=("Segoe UI", 11, "bold"), pady=10)
        self.btn_export.pack(fill="x")

        # Status Label
        lbl_status = tk.Label(self.root, textvariable=self.status_var, bg="#020617", fg="#38bdf8", font=("Segoe UI", 9), pady=6)
        lbl_status.pack(side="bottom", fill="x")

        # Signature
        sig = tk.Label(self.root, text="Dasturchi: MuzaffarZed | Studio Engine 2026", bg="#020617", fg="#475569", font=("Segoe UI", 8))
        sig.pack(side="bottom", fill="x")

    def load_audio_cache(self):
        # Pre-load sounds for quick preview
        threading.Thread(target=self._load_cache_thread, daemon=True).start()

    def _load_cache_thread(self):
        self.status_var.set("Audio keshga olinmoqda...")
        # create temporary 30-sec wav chunks starting from 18s for instant pygame playback
        tmp_minus = os.path.join(OUT_DIR, ".preview_minus.wav")
        tmp_vocal = os.path.join(OUT_DIR, ".preview_vocal.wav")
        if not os.path.exists(tmp_minus):
            subprocess.run(["ffmpeg", "-y", "-ss", "18", "-t", "30", "-i", MINUS_PATH, "-ar", "44100", "-ac", "2", tmp_minus], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if not os.path.exists(tmp_vocal):
            subprocess.run(["ffmpeg", "-y", "-ss", "0", "-t", "40", "-i", VOCAL_PATH, "-ar", "44100", "-ac", "2", tmp_vocal], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        self.snd_minus = pygame.mixer.Sound(tmp_minus)
        self.snd_vocal = pygame.mixer.Sound(tmp_vocal)
        self.status_var.set("Tayyor. '20-soniyadan Tinglash' tugmasini bosing.")

    def on_slider_change(self, val):
        v = float(val)
        self.lbl_offset.config(text=f"{v:.3f} s  ({int(v*1000)} ms)")

    def nudge(self, delta):
        cur = self.offset_var.get()
        new_val = round(cur + delta, 3)
        if 10.0 <= new_val <= 14.0:
            self.offset_var.set(new_val)
            self.on_slider_change(new_val)

    def set_exact(self, val):
        self.offset_var.set(val)
        self.on_slider_change(val)

    def toggle_play(self):
        if self.is_playing:
            self.stop_play()
        else:
            self.start_play()

    def start_play(self):
        if not hasattr(self, 'snd_minus') or not hasattr(self, 'snd_vocal'):
            messagebox.showinfo("Kuting", "Audio yuklanmoqda, 2 soniya kuting...")
            return

        self.is_playing = True
        self.btn_play.config(text="⏹ To'xtatish", bg="#dc2626")
        
        offset = self.offset_var.get()
        self.status_var.set(f"Ijro etilmoqda (Offset: {offset:.3f}s)...")

        # In preview, minus starts at 18.0s (so 0 in preview is 18s).
        # Vocal should start at offset seconds in absolute timeline.
        # In preview timeline, vocal enters at (offset - 18.0) seconds!
        vocal_delay_preview_sec = max(0, offset - 18.0)

        self.chan_minus.play(self.snd_minus)
        self.chan_minus.set_volume(0.85)

        # Schedule vocal with delay
        def play_vocal():
            import time
            time.sleep(vocal_delay_preview_sec)
            if self.is_playing:
                self.chan_vocal.play(self.snd_vocal)
                self.chan_vocal.set_volume(1.0)

        threading.Thread(target=play_vocal, daemon=True).start()

    def stop_play(self):
        self.is_playing = False
        self.chan_minus.stop()
        self.chan_vocal.stop()
        self.btn_play.config(text="▶ 20-soniyadan Tinglash (Intro Kirishi)", bg="#2563eb")
        self.status_var.set("To'xtatildi.")

    def export_master(self):
        offset = self.offset_var.get()
        delay_ms = int(offset * 1000)
        self.stop_play()
        self.btn_export.config(state="disabled", text="⏳ MASTER EKSPORT QILINMOQDA...")
        self.status_var.set(f"Studiya miksing & mastering renderi boshlandi ({delay_ms}ms)...")

        def run_export():
            filter_complex = (
                "[0:a]equalizer=f=3300:t=q:w=1.4:g=-3.5,equalizer=f=1200:t=q:w=1.2:g=-1.8,volume=0.90[minus_pocket];"
                f"[1:a]adelay={delay_ms}|{delay_ms},"
                "highpass=f=95,lowpass=f=16800,afftdn=nf=-42,deesser=i=0.55:m=0.5:f=0.55:s=o,"
                "equalizer=f=350:t=q:w=1.3:g=-3.5,equalizer=f=1300:t=q:w=1.1:g=+2.2,"
                "equalizer=f=3400:t=q:w=1.0:g=+4.2,equalizer=f=11500:t=h:g=+3.8,"
                "acompressor=threshold=-22dB:ratio=4.0:attack=6:release=90:makeup=3.5dB:knee=2dB,"
                "acompressor=threshold=-16dB:ratio=2.5:attack=25:release=220:makeup=2.5dB:knee=4dB,"
                "chorus=0.7:0.9:45:0.35:0.25:2[voc_sculpted];"
                "[voc_sculpted]asplit=2[voc_dry][voc_send];"
                "[voc_send]highpass=f=450,lowpass=f=5500,aecho=0.8:0.7:160|320:0.22|0.14,volume=0.22[voc_reverb];"
                "[voc_dry][voc_reverb]amix=inputs=2:weights=1.25 0.5:dropout_transition=0[voc_final];"
                "[minus_pocket][voc_final]amix=inputs=2:duration=first:weights=0.90 1.65:dropout_transition=0,"
                "loudnorm=I=-14:TP=-1.0:LRA=7[master_out]"
            )
            out_file = os.path.join(OUT_DIR, "Mani_izlab_ovvora_bolmang_(Mening_Masterim).mp3")
            cmd = [
                "ffmpeg", "-y",
                "-i", MINUS_PATH,
                "-i", VOCAL_PATH,
                "-filter_complex", filter_complex + ";[master_out]afade=t=out:st=138:d=6[final_radio]",
                "-map", "[final_radio]",
                "-t", "144",
                "-b:a", "320k",
                "-metadata", f"title=Mani izlab ovvora bo'lmang (Tanlangan Master {offset:.2f}s)",
                "-metadata", "artist=MuzaffarZed Studio",
                "-metadata", "comment=Mix & Master by MuzaffarZed",
                out_file
            ]
            res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
            if res.returncode == 0:
                self.root.after(0, lambda: self.on_export_success(out_file))
            else:
                self.root.after(0, lambda: messagebox.showerror("Xatolik", f"Eksport xatosi: {res.stderr[-200:]}"))
            self.root.after(0, lambda: self.btn_export.config(state="normal", text="✨ SHU VAQT BILAN MUKAMMAL MASTER EKSPORT QILISH"))

        threading.Thread(target=run_export, daemon=True).start()

    def on_export_success(self, path):
        self.status_var.set("Muvaffaqiyatli saqlandi!")
        messagebox.showinfo("Tabriklaymiz!", f"Qo'shiq mukammal tayyor bo'ldi!\n\nFayl:\n{os.path.basename(path)}\n\nPapka:\n{OUT_DIR}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VocalSyncStudio(root)
    root.mainloop()
