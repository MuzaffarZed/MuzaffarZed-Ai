import os
import sys
import subprocess
import threading
import tkinter as tk
import customtkinter as ctk
import pygame
import psutil

# Ensure current dir is in sys.path
sys.path.insert(0, os.path.dirname(__file__))

import sentinel
import vault
import system_guardian
import media_forge
import cognitive_cortex

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MuzaffarZedHUD(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("⚡ J.A.R.V.I.S  SENTINEL — MUZAFFARZED SUPREME HUB")
        self.geometry("1100x760")
        self.configure(fg_color="#0a0b10")

        self.vault_data = vault.load_vault()
        self.cortex = cognitive_cortex.CognitiveCortex()
        pygame.mixer.init()

        self.create_header()
        self.create_tabs()
        self.create_footer()

        self.update_telemetry_loop()

    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="#12141c", corner_radius=12)
        header.pack(fill="x", padx=16, pady=(14, 6))

        title = ctk.CTkLabel(
            header,
            text="⚡ J.A.R.V.I.S  SENTINEL  v17.0 — MUZAFFARZED APEX",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color="#00f0ff"
        )
        title.pack(side="left", padx=20, pady=12)

        voice_btn = ctk.CTkButton(
            header,
            text="🎙️ Ovozli Salom",
            command=self.play_jarvis_voice,
            fg_color="#1f2438",
            hover_color="#2b3252",
            text_color="#00ff9d",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            width=130,
            height=34
        )
        voice_btn.pack(side="right", padx=12, pady=10)

        boost_btn = ctk.CTkButton(
            header,
            text="⚡ Turbo Boost (RAM)",
            command=self.run_turbo_boost,
            fg_color="#0080ff",
            hover_color="#0055b3",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            width=150,
            height=34
        )
        boost_btn.pack(side="right", padx=4, pady=10)

    def create_tabs(self):
        self.tabview = ctk.CTkTabview(self, fg_color="#0e1017", corner_radius=12)
        self.tabview.pack(fill="both", expand=True, padx=16, pady=6)

        self.tab_cortex = self.tabview.add("🧠 Insoniy Intellekt va G'oyalar")
        self.tab_games = self.tabview.add("🎮 13 Ta Sara O'yinlar")
        self.tab_media = self.tabview.add("🎵 Musiqa & Media Zavodi")
        self.tab_system = self.tabview.add("🛡️ Tizim Shifokori")

        self.build_cortex_tab()
        self.build_games_tab()
        self.build_media_tab()
        self.build_system_tab()

    # =========================================================================
    # TAB 1: COGNITIVE CORTEX & INSONIY G'OYALAR
    # =========================================================================
    def build_cortex_tab(self):
        container = self.tab_cortex

        # Top Control & Perception Banner
        banner = ctk.CTkFrame(container, fg_color="#131622", corner_radius=10)
        banner.pack(fill="x", padx=8, pady=(6, 8))

        self.cortex_env_lbl = ctk.CTkLabel(
            banner,
            text="🔍 Atrof-muhit: Tahlil qilinmoqda...",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#00ff9d"
        )
        self.cortex_env_lbl.pack(side="left", padx=16, pady=10)

        refresh_btn = ctk.CTkButton(
            banner,
            text="🔄 G'oyalarni Yangilash",
            command=self.refresh_cortex_ideas,
            fg_color="#1f2438",
            hover_color="#2c3350",
            text_color="#00f0ff",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=30,
            width=160
        )
        refresh_btn.pack(side="right", padx=10, pady=8)

        # Scrollable Ideas Area
        self.cortex_scroll = ctk.CTkScrollableFrame(container, fg_color="#0a0b10", corner_radius=10)
        self.cortex_scroll.pack(fill="both", expand=True, padx=4, pady=4)

        self.populate_idea_cards()

    def refresh_cortex_ideas(self):
        self.cortex.generate_proactive_ideas()
        self.populate_idea_cards()

    def populate_idea_cards(self):
        for widget in self.cortex_scroll.winfo_children():
            widget.destroy()

        env = self.cortex.sense_environment()
        self.cortex_env_lbl.configure(
            text=f"🧠 Insoniy Sezgi: RAM {env['ram_percent']}% | CPU {env['cpu_percent']}% | Kesh: {env['temp_size_mb']} MB | Treklar: {env['music_count']} ta | O'yinlar: {env['games_count']} ta"
        )

        ideas = self.cortex.load_ideas()
        if not ideas:
            ideas = self.cortex.generate_proactive_ideas()

        for idea in ideas:
            card = ctk.CTkFrame(self.cortex_scroll, fg_color="#131622", corner_radius=10)
            card.pack(fill="x", padx=10, pady=8)

            # Card Header (Category + Impact Score)
            header_row = ctk.CTkFrame(card, fg_color="transparent")
            header_row.pack(fill="x", padx=14, pady=(10, 4))

            cat_lbl = ctk.CTkLabel(
                header_row,
                text=idea.get("category", "G'oya"),
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#00f0ff"
            )
            cat_lbl.pack(side="left")

            score = idea.get("impact_score", 90)
            score_badge = ctk.CTkLabel(
                header_row,
                text=f"⚡ Samaradorlik: {score}/100",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#00ff9d" if score >= 90 else "#ffcc00"
            )
            score_badge.pack(side="right")

            # Title & Summary
            title_lbl = ctk.CTkLabel(
                card,
                text=idea.get("title", ""),
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color="#ffffff",
                anchor="w"
            )
            title_lbl.pack(fill="x", padx=14, pady=(2, 4))

            summary_lbl = ctk.CTkLabel(
                card,
                text=idea.get("summary", ""),
                font=ctk.CTkFont(size=13),
                text_color="#a0a5b8",
                wraplength=980,
                justify="left"
            )
            summary_lbl.pack(fill="x", padx=14, pady=(0, 6))

            # Details
            details = idea.get("details", [])
            if details:
                detail_box = ctk.CTkFrame(card, fg_color="#0c0e14", corner_radius=6)
                detail_box.pack(fill="x", padx=14, pady=(2, 8))
                for d in details:
                    d_lbl = ctk.CTkLabel(
                        detail_box,
                        text=f"  • {d}",
                        font=ctk.CTkFont(size=12),
                        text_color="#7b8196",
                        anchor="w",
                        justify="left"
                    )
                    d_lbl.pack(fill="x", padx=8, pady=2)

            # Bottom Action Row
            action_row = ctk.CTkFrame(card, fg_color="transparent")
            action_row.pack(fill="x", padx=14, pady=(4, 10))

            is_done = (idea.get("status") == "COMPLETED")
            status_text = f"✅ Bajarildi: {idea.get('result_summary', '')}" if is_done else f"Holat: {idea.get('status', 'TAYYOR')} | Xavf: {idea.get('risk_level', '0%')}"
            status_color = "#00ff9d" if is_done else "#8890a6"

            status_lbl = ctk.CTkLabel(
                action_row,
                text=status_text,
                font=ctk.CTkFont(size=12),
                text_color=status_color
            )
            status_lbl.pack(side="left")

            exec_btn = ctk.CTkButton(
                action_row,
                text="✅ Amalga Oshirish" if not is_done else "🔄 Qayta Bajarish",
                command=lambda iid=idea["id"]: self.execute_idea_action(iid),
                fg_color="#00f0ff" if not is_done else "#1f2438",
                hover_color="#00b8cc" if not is_done else "#2a3048",
                text_color="#0a0b10" if not is_done else "#00ff9d",
                font=ctk.CTkFont(size=12, weight="bold"),
                height=30,
                width=160
            )
            exec_btn.pack(side="right")

    def execute_idea_action(self, idea_id: str):
        res = self.cortex.execute_idea(idea_id)
        self.populate_idea_cards()
        self.status_label.configure(
            text=f"🧠 {res.get('message', 'Bajarildi!')}",
            text_color="#00ff9d"
        )

    # =========================================================================
    # TAB 2: GAMES
    # =========================================================================
    def build_games_tab(self):
        telem_frame = ctk.CTkFrame(self.tab_games, fg_color="#141724", corner_radius=10)
        telem_frame.pack(fill="x", padx=10, pady=(6, 10))

        self.cpu_label = ctk.CTkLabel(telem_frame, text="CPU: 0%", font=ctk.CTkFont(size=13, weight="bold"), text_color="#ffffff")
        self.cpu_label.pack(side="left", padx=16, pady=8)

        self.ram_label = ctk.CTkLabel(telem_frame, text="RAM: 0%", font=ctk.CTkFont(size=13, weight="bold"), text_color="#00ff9d")
        self.ram_label.pack(side="left", padx=16, pady=8)

        self.disk_label = ctk.CTkLabel(telem_frame, text="D: Disk: 0 GB", font=ctk.CTkFont(size=13, weight="bold"), text_color="#00f0ff")
        self.disk_label.pack(side="left", padx=16, pady=8)

        self.status_label = ctk.CTkLabel(telem_frame, text="Holat: Barcha tizimlar soz", font=ctk.CTkFont(size=13), text_color="#a0a5b8")
        self.status_label.pack(side="right", padx=16, pady=8)

        scroll = ctk.CTkScrollableFrame(self.tab_games, fg_color="#0a0b10", corner_radius=10)
        scroll.pack(fill="both", expand=True, padx=4, pady=4)

        games = self.vault_data.get("games", [])
        cols = 3

        for idx, g in enumerate(games):
            r = idx // cols
            c = idx % cols

            card = ctk.CTkFrame(scroll, fg_color="#131622", corner_radius=10)
            card.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")
            scroll.grid_columnconfigure(c, weight=1)

            name_lbl = ctk.CTkLabel(card, text=g["name"], font=ctk.CTkFont(size=14, weight="bold"), text_color="#ffffff")
            name_lbl.pack(padx=12, pady=(10, 2), anchor="w")

            status_txt = "✅ Tayyor" if os.path.exists(g["exe"]) else "❌ Topilmadi"
            status_color = "#00ff9d" if os.path.exists(g["exe"]) else "#ff4d4d"
            card_status = ctk.CTkLabel(card, text=status_txt, text_color=status_color, font=ctk.CTkFont(size=12))
            card_status.pack(padx=12, pady=(0, 6), anchor="w")

            play_btn = ctk.CTkButton(
                card,
                text="▶ O'ynash",
                command=lambda exe=g["exe"], name=g["name"]: self.launch_game(exe, name),
                fg_color="#00f0ff",
                hover_color="#00b8cc",
                text_color="#0a0b10",
                font=ctk.CTkFont(size=13, weight="bold"),
                height=30
            )
            play_btn.pack(fill="x", padx=12, pady=(2, 10))

    # =========================================================================
    # TAB 3: MEDIA FORGE
    # =========================================================================
    def build_media_tab(self):
        container = ctk.CTkFrame(self.tab_media, fg_color="#121520", corner_radius=12)
        container.pack(fill="both", expand=True, padx=12, pady=12)

        lbl = ctk.CTkLabel(
            container,
            text="🎵 YOUTUBE / INTERNETDAN 320 KBPS MUSIQA VA FULL HD VIDEO YUKLASH",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#00ff9d"
        )
        lbl.pack(padx=20, pady=(20, 10), anchor="w")

        info_lbl = ctk.CTkLabel(
            container,
            text="Havolani kiriting, dastur avtomatik tarzda eng yuqori sifatda 'Desktop\\Musiqa_Fleshka_2026' papkasiga joylaydi:",
            font=ctk.CTkFont(size=13),
            text_color="#a0a5b8"
        )
        info_lbl.pack(padx=20, pady=(0, 16), anchor="w")

        self.url_entry = ctk.CTkEntry(
            container,
            placeholder_text="https://www.youtube.com/watch?v=... havolasini shu yerga qo'ying",
            width=700,
            height=42,
            font=ctk.CTkFont(size=14)
        )
        self.url_entry.pack(padx=20, pady=8, fill="x")

        btn_row = ctk.CTkFrame(container, fg_color="transparent")
        btn_row.pack(padx=20, pady=16, fill="x")

        mp3_btn = ctk.CTkButton(
            btn_row,
            text="🎵 MP3 320kbps Musiqa Yuklash (Fleshkaga)",
            command=self.download_mp3_action,
            fg_color="#00f0ff",
            hover_color="#00b8cc",
            text_color="#0a0b10",
            font=ctk.CTkFont(size=13, weight="bold"),
            height=38,
            width=280
        )
        mp3_btn.pack(side="left", padx=(0, 12))

        mp4_btn = ctk.CTkButton(
            btn_row,
            text="🎬 Full HD MP4 Video Yuklash",
            command=self.download_mp4_action,
            fg_color="#8a2be2",
            hover_color="#7322bf",
            text_color="#ffffff",
            font=ctk.CTkFont(size=13, weight="bold"),
            height=38,
            width=240
        )
        mp4_btn.pack(side="left", padx=4)

        self.media_status = ctk.CTkLabel(
            container,
            text="Kutilmoqda...",
            font=ctk.CTkFont(size=13),
            text_color="#8890a6"
        )
        self.media_status.pack(padx=20, pady=16, anchor="w")

    # =========================================================================
    # TAB 4: SYSTEM GUARDIAN
    # =========================================================================
    def build_system_tab(self):
        container = ctk.CTkFrame(self.tab_system, fg_color="#121520", corner_radius=12)
        container.pack(fill="both", expand=True, padx=12, pady=12)

        lbl = ctk.CTkLabel(
            container,
            text="🛡️ AVTONOM TIZIM SHIFOKORI VA DIAGNOSTIKA",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#00f0ff"
        )
        lbl.pack(padx=20, pady=(20, 14), anchor="w")

        health = system_guardian.get_system_health()
        info_text = (
            f"• CPU Yadrolari: {health['cpu_cores']} ta oqim\n"
            f"• Xotira Holati: {health['ram_health']}\n"
            f"• C: Diski Bo'sh Joy: {health['c_free_gb']} GB\n"
            f"• D: Diski Bo'sh Joy: {health['d_free_gb']} GB\n"
            f"• Batareya: {health['battery']}% (Quvvatlovchi: {'Ulangan' if health['power_plugged'] else 'Batareyada'})\n"
            f"• Tizim Holati: Barcha o'yin drayverlari va registrlari soz."
        )

        self.health_lbl = ctk.CTkLabel(
            container,
            text=info_text,
            font=ctk.CTkFont(size=14),
            text_color="#ffffff",
            justify="left"
        )
        self.health_lbl.pack(padx=20, pady=10, anchor="w")

        repair_btn = ctk.CTkButton(
            container,
            text="🔍 Siniq Yorliqlarni Qidirish va Avto-Tozalash",
            command=self.run_repair_action,
            fg_color="#00ff9d",
            hover_color="#00cc7d",
            text_color="#0a0b10",
            font=ctk.CTkFont(size=13, weight="bold"),
            height=38,
            width=300
        )
        repair_btn.pack(padx=20, pady=16, anchor="w")

        self.repair_status = ctk.CTkLabel(container, text="", font=ctk.CTkFont(size=13), text_color="#00ff9d")
        self.repair_status.pack(padx=20, pady=4, anchor="w")

    def create_footer(self):
        footer = ctk.CTkFrame(self, fg_color="#07080c", height=32, corner_radius=0)
        footer.pack(fill="x", side="bottom")

        left_lbl = ctk.CTkLabel(
            footer,
            text="MuzaffarZed Autonomous Core v17.0 (Zero-Defect Apex Standard)",
            font=ctk.CTkFont(size=11),
            text_color="#555a6d"
        )
        left_lbl.pack(side="left", padx=20, pady=4)

        sig_lbl = ctk.CTkLabel(
            footer,
            text="Dasturchi: MuzaffarZed",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#00f0ff"
        )
        sig_lbl.pack(side="right", padx=20, pady=4)

    def run_turbo_boost(self):
        res = sentinel.boost_ram()
        self.status_label.configure(
            text=f"⚡ {res['freed_ram_mb']} MB RAM tozalandi!",
            text_color="#00ff9d"
        )

    def play_jarvis_voice(self):
        voice_dir = r"C:\Users\MuzaffarZed\Desktop\MuzaffarZed_Boshqaruv_Paneli\Jarvis_Diktor_Ovozi"
        if os.path.exists(voice_dir):
            files = [os.path.join(voice_dir, f) for f in os.listdir(voice_dir) if f.endswith('.mp3')]
            if files:
                pygame.mixer.music.load(files[0])
                pygame.mixer.music.play()
                self.status_label.configure(text="🎙️ Salom, janob Muzaffar!", text_color="#00f0ff")

    def launch_game(self, exe_path, game_name):
        if os.path.exists(exe_path):
            workdir = os.path.dirname(exe_path)
            subprocess.Popen([exe_path], cwd=workdir)
            sentinel.boost_ram()
            self.status_label.configure(
                text=f"🎮 {game_name} ishga tushirildi!",
                text_color="#00ff9d"
            )
            vault.log_event(f"Game launched: {game_name}")
        else:
            self.status_label.configure(text=f"❌ {game_name} topilmadi!", text_color="#ff4d4d")

    def download_mp3_action(self):
        url = self.url_entry.get().strip()
        if not url:
            self.media_status.configure(text="❌ Iltimos, havola kiriting!", text_color="#ff4d4d")
            return
        self.media_status.configure(text="⏳ Musiqa yuklanmoqda va 320kbps formatga o'tkazilmoqda...", text_color="#00f0ff")
        def _dl():
            res = media_forge.download_audio_mp3(url)
            color = "#00ff9d" if res["status"] == "success" else "#ff4d4d"
            self.media_status.configure(text=res["message"], text_color=color)
        threading.Thread(target=_dl, daemon=True).start()

    def download_mp4_action(self):
        url = self.url_entry.get().strip()
        if not url:
            self.media_status.configure(text="❌ Iltimos, havola kiriting!", text_color="#ff4d4d")
            return
        self.media_status.configure(text="⏳ Video Full HD formatda yuklanmoqda...", text_color="#00f0ff")
        def _dl():
            res = media_forge.download_video_hd(url)
            color = "#00ff9d" if res["status"] == "success" else "#ff4d4d"
            self.media_status.configure(text=res["message"], text_color=color)
        threading.Thread(target=_dl, daemon=True).start()

    def run_repair_action(self):
        repaired = system_guardian.audit_and_repair_desktop_shortcuts()
        if repaired:
            self.repair_status.configure(text=f"✅ {len(repaired)} ta siniq yorliq tozalandi!", text_color="#00ff9d")
        else:
            self.repair_status.configure(text="✅ Tizim 100% toza! Birorta ham nosoz yorliq topilmadi.", text_color="#00ff9d")

    def update_telemetry_loop(self):
        def _loop():
            try:
                tel = sentinel.get_system_telemetry()
                self.cpu_label.configure(text=f"CPU: {tel['cpu_percent']}%")
                self.ram_label.configure(text=f"RAM: {tel['ram_percent']}% ({tel['ram_used_gb']} GB / {tel['ram_total_gb']} GB)")
                self.disk_label.configure(text=f"D: Disk: {tel['disk_free_gb']} GB Bo'sh")
            except Exception:
                pass
            self.after(2000, self.update_telemetry_loop)

        t = threading.Thread(target=_loop, daemon=True)
        t.start()

if __name__ == "__main__":
    app = MuzaffarZedHUD()
    app.mainloop()
