import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from typing import Optional

from galaxy_bridge.core.detector import DeviceDetector, AndroidDevice
from galaxy_bridge.core.video_scanner import VideoScanner, VideoFile
from galaxy_bridge.core.transfer_engine import TransferEngine
from galaxy_bridge.core.auto_sync import AutoSyncManager

class GalaxyBridgeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Galaxy Video Bridge — S22 Ultra & Tab A")
        self.geometry("900x680")
        self.minsize(800, 600)
        self.configure(bg="#121417")

        self.detector = DeviceDetector()
        self.sender: Optional[AndroidDevice] = None
        self.receiver: Optional[AndroidDevice] = None
        self.scanner: Optional[VideoScanner] = None
        self.engine: Optional[TransferEngine] = None
        self.auto_sync: Optional[AutoSyncManager] = None
        self.videos = []

        self._apply_styles()
        self._create_widgets()
        self.after(500, self.refresh_devices)

    def _apply_styles(self):
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        
        # Dark Theme Palette
        self.style.configure(".", background="#121417", foreground="#E1E4EA")
        self.style.configure("TFrame", background="#121417")
        self.style.configure("Card.TFrame", background="#1A1D24", relief="flat")
        self.style.configure("TLabel", background="#121417", foreground="#E1E4EA", font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#00D26A")
        self.style.configure("SubHeader.TLabel", font=("Segoe UI", 11), foreground="#8A92A6")
        self.style.configure("DeviceTitle.TLabel", font=("Segoe UI", 11, "bold"), foreground="#FFFFFF", background="#1A1D24")
        self.style.configure("DeviceSubtitle.TLabel", font=("Segoe UI", 9), foreground="#8A92A6", background="#1A1D24")
        
        self.style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), background="#00D26A", foreground="#000000", borderwidth=0)
        self.style.map("Accent.TButton", background=[("active", "#00B85C"), ("disabled", "#334138")])

        self.style.configure("Secondary.TButton", font=("Segoe UI", 10), background="#2A2F3D", foreground="#FFFFFF", borderwidth=0)
        self.style.map("Secondary.TButton", background=[("active", "#3A4154")])

        self.style.configure("Treeview", background="#1A1D24", foreground="#E1E4EA", fieldbackground="#1A1D24", font=("Segoe UI", 9), rowheight=28)
        self.style.configure("Treeview.Heading", background="#242833", foreground="#FFFFFF", font=("Segoe UI", 10, "bold"))
        self.style.map("Treeview", background=[("selected", "#0078D7")])

    def _create_widgets(self):
        # Header
        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", padx=20, pady=(15, 10))
        
        title_lbl = ttk.Label(header_frame, text="⚡ Galaxy Video Bridge", style="Header.TLabel")
        title_lbl.pack(side="left")

        sub_lbl = ttk.Label(header_frame, text="S22 Ultra kamerasidagi videolarni Planshetga yuqori tezlikda o'tkazish", style="SubHeader.TLabel")
        sub_lbl.pack(side="left", padx=15, pady=(4, 0))

        guide_btn = ttk.Button(header_frame, text="📖 Yo'riqnoma", style="Accent.TButton", command=self.open_guide_dialog)
        guide_btn.pack(side="right", padx=(0, 8))

        refresh_btn = ttk.Button(header_frame, text="🔄 Yangilash", style="Secondary.TButton", command=self.refresh_devices)
        refresh_btn.pack(side="right")

        # Device Cards
        devices_container = ttk.Frame(self)
        devices_container.pack(fill="x", padx=20, pady=5)
        devices_container.columnconfigure(0, weight=1)
        devices_container.columnconfigure(1, weight=1)

        # Phone Card
        self.phone_card = ttk.Frame(devices_container, style="Card.TFrame", padding=12)
        self.phone_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.phone_lbl_title = ttk.Label(self.phone_card, text="📱 S22 Ultra: Qidirilmoqda...", style="DeviceTitle.TLabel")
        self.phone_lbl_title.pack(anchor="w")
        self.phone_lbl_info = ttk.Label(self.phone_card, text="Holat: Tekshirilmoqda...", style="DeviceSubtitle.TLabel")
        self.phone_lbl_info.pack(anchor="w", pady=(4, 0))

        # Tablet Card
        self.tablet_card = ttk.Frame(devices_container, style="Card.TFrame", padding=12)
        self.tablet_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        self.tablet_lbl_title = ttk.Label(self.tablet_card, text="📟 Planshet: Qidirilmoqda...", style="DeviceTitle.TLabel")
        self.tablet_lbl_title.pack(anchor="w")
        self.tablet_lbl_info = ttk.Label(self.tablet_card, text="Holat: Tekshirilmoqda...", style="DeviceSubtitle.TLabel")
        self.tablet_lbl_info.pack(anchor="w", pady=(4, 0))

        # Control Bar
        control_frame = ttk.Frame(self)
        control_frame.pack(fill="x", padx=20, pady=10)

        self.btn_sync_all = ttk.Button(
            control_frame,
            text="🚀 Barcha Yangi Videolarni O'tkazish",
            style="Accent.TButton",
            command=self.transfer_all_new
        )
        self.btn_sync_all.pack(side="left", padx=(0, 10))

        self.btn_sync_selected = ttk.Button(
            control_frame,
            text="📥 Tanlanganlarni O'tkazish",
            style="Secondary.TButton",
            command=self.transfer_selected
        )
        self.btn_sync_selected.pack(side="left", padx=(0, 10))

        self.btn_auto_sync = ttk.Button(
            control_frame,
            text="🔴 Avto-Sinxronizatsiya (O'chiq)",
            style="Secondary.TButton",
            command=self.toggle_auto_sync
        )
        self.btn_auto_sync.pack(side="left")

        # Video List (Treeview)
        list_frame = ttk.Frame(self)
        list_frame.pack(fill="both", expand=True, padx=20, pady=5)

        columns = ("name", "size", "date", "status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode="extended")
        self.tree.heading("name", text="Video Nomi")
        self.tree.heading("size", text="Hajmi")
        self.tree.heading("date", text="Olingan Sanasi")
        self.tree.heading("status", text="Holati")

        self.tree.column("name", width=340)
        self.tree.column("size", width=100, anchor="center")
        self.tree.column("date", width=140, anchor="center")
        self.tree.column("status", width=120, anchor="center")

        tree_scroll = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")

        # Progress & Status Bar
        status_frame = ttk.Frame(self)
        status_frame.pack(fill="x", padx=20, pady=(5, 15))

        self.progress_bar = ttk.Progressbar(status_frame, orient="horizontal", mode="determinate")
        self.progress_bar.pack(fill="x", pady=(0, 5))

        self.status_lbl = ttk.Label(status_frame, text="Tayyor.", font=("Segoe UI", 9), foreground="#8A92A6")
        self.status_lbl.pack(side="left")

        self.speed_lbl = ttk.Label(status_frame, text="", font=("Segoe UI", 9, "bold"), foreground="#00D26A")
        self.speed_lbl.pack(side="right")

    def log(self, message: str, speed_text: str = ""):
        self.status_lbl.config(text=message)
        if speed_text:
            self.speed_lbl.config(text=speed_text)

    def refresh_devices(self):
        self.log("Qurilmalar tekshirilmoqda...")
        threading.Thread(target=self._worker_refresh, daemon=True).start()

    def _worker_refresh(self):
        pair = self.detector.detect_pair()
        self.sender = pair["sender"]
        self.receiver = pair["receiver"]

        def update_ui():
            if self.sender:
                self.phone_lbl_title.config(text=f"📱 {self.sender.device_name}")
                self.phone_lbl_info.config(
                    text=f"Model: {self.sender.model} | Batareya: {self.sender.battery_level}% | Bo'sh joy: {self.sender.free_storage}"
                )
            else:
                self.phone_lbl_title.config(text="📱 S22 Ultra topilmadi")
                self.phone_lbl_info.config(text="Iltimos, telefonni USB orqali ulang")

            if self.receiver:
                self.tablet_lbl_title.config(text=f"📟 {self.receiver.device_name}")
                self.tablet_lbl_info.config(
                    text=f"Model: {self.receiver.model} | Batareya: {self.receiver.battery_level}% | Bo'sh joy: {self.receiver.free_storage}"
                )
            else:
                self.tablet_lbl_title.config(text="📟 Planshet topilmadi")
                self.tablet_lbl_info.config(text="Iltimos, planshetni USB orqali ulang")

            if self.sender and self.receiver:
                self.scanner = VideoScanner(self.detector.adb, self.sender.serial, self.receiver.serial)
                self.engine = TransferEngine(self.detector.adb, self.sender.serial, self.receiver.serial)
                self.load_videos()
            else:
                self.log("Ikkala qurilma ham USB orqali ulangan bo'lishi lozim.")

        self.after(0, update_ui)

    def load_videos(self):
        if not self.scanner:
            return
        threading.Thread(target=self._worker_load_videos, daemon=True).start()

    def _worker_load_videos(self):
        self.videos = self.scanner.scan_camera_videos()
        def update_tree():
            for item in self.tree.get_children():
                self.tree.delete(item)
            for v in self.videos:
                status_text = "✅ Planshetda bor" if v.is_transferred else "⏳ Yangi video"
                self.tree.insert("", "end", iid=v.filename, values=(v.filename, v.size_human, v.modified_date, status_text))
            
            new_count = sum(1 for v in self.videos if not v.is_transferred)
            self.log(f"Jami: {len(self.videos)} ta video topildi. Yangi o'tkazilmagan: {new_count} ta.")
        self.after(0, update_tree)

    def transfer_all_new(self):
        new_videos = [v for v in self.videos if not v.is_transferred]
        if not new_videos:
            messagebox.showinfo("Barchasi O'tgan", "Barcha videolar allaqachon planshetga o'tkazilgan!")
            return
        threading.Thread(target=self._worker_transfer, args=(new_videos,), daemon=True).start()

    def transfer_selected(self):
        selected_ids = self.tree.selection()
        if not selected_ids:
            messagebox.showwarning("Tanlov yo'q", "Iltimos, ro'yxatdan o'tkazmoqchi bo'lgan videolarni tanlang!")
            return
        selected_videos = [v for v in self.videos if v.filename in selected_ids]
        threading.Thread(target=self._worker_transfer, args=(selected_videos,), daemon=True).start()

    def _worker_transfer(self, videos_to_transfer):
        self.btn_sync_all.config(state="disabled")
        self.btn_sync_selected.config(state="disabled")
        total = len(videos_to_transfer)

        for idx, v in enumerate(videos_to_transfer, start=1):
            self.log(f"[{idx}/{total}] O'tkazilmoqda: {v.filename} ({v.size_human})...")
            
            def p_callback(fn, pct):
                self.progress_bar["value"] = pct
            
            res = self.engine.transfer_video(v.path, progress_callback=p_callback)
            if res.success:
                speed_str = f"Tezlik: {res.speed_mb_s:.1f} MB/s ⚡"
                self.log(f"[{idx}/{total}] Muvaffaqiyatli: {v.filename} ({res.duration_sec:.1f} soniya)", speed_str)
                v.is_transferred = True
                self.after(0, lambda fn=v.filename: self.tree.set(fn, "status", "✅ Planshetda bor"))
            else:
                self.log(f"Xatolik ({v.filename}): {res.error_message}")

        self.progress_bar["value"] = 100
        self.btn_sync_all.config(state="normal")
        self.btn_sync_selected.config(state="normal")
        self.log("Barcha tanlangan videolar planshet Galereyasiga joylandi! 🎉")

    def toggle_auto_sync(self):
        if not self.auto_sync or not self.auto_sync.is_running:
            if not self.scanner or not self.engine:
                messagebox.showerror("Xatolik", "Avval qurilmalarni ulang!")
                return
            self.auto_sync = AutoSyncManager(
                self.scanner,
                self.engine,
                on_video_synced=self._on_auto_synced,
                on_status_change=self.log
            )
            self.auto_sync.start()
            self.btn_auto_sync.config(text="🟢 Avto-Sinxronizatsiya (FAOL)")
        else:
            self.auto_sync.stop()
            self.btn_auto_sync.config(text="🔴 Avto-Sinxronizatsiya (O'chiq)")

    def open_guide_dialog(self):
        guide_win = tk.Toplevel(self)
        guide_win.title("📖 Galaxy Video Bridge — Rasmli Yo'riqnoma")
        guide_win.geometry("750x580")
        guide_win.configure(bg="#121417")

        frame = ttk.Frame(guide_win, padding=20)
        frame.pack(fill="both", expand=True)

        title = ttk.Label(frame, text="🚀 Qanday Foydalaniladi? (Oddiy va Tez)", font=("Segoe UI", 14, "bold"), foreground="#00D26A")
        title.pack(anchor="w", pady=(0, 10))

        text_content = (
            "📱 1-USUL: SIMSIZ (Wi-Fi yoki Hotspot orqali — Ko'chada va Uyda)\n"
            "------------------------------------------------------------------------------------\n"
            "1. Planshetda 1 marta: 'LocalSend' ilovasini ochib, Sozlamalar (⚙️) bo'limidan 'Быстрое сохранение' (Quick Save) ni yoqing.\n"
            "   (Endi planshet videolarni o'zi jim qabul qiladi, ekran o'chiq bo'lsa ham!)\n\n"
            "2. S22 Ultra telefoningizda: Galereyaga kiring, videoni tanlang va 'Ulashish' (Share / Поделиться) ni bosing.\n"
            "3. 'LocalSend' ni tanlang va ekranda chiqqan 'Galaxy Tab A' ni bosing.\n"
            "4. Video 40 MB/s tezlikda planshetga o'tadi va Galereyada paydo bo'ladi!\n\n"
            "💡 Ko'chada bo'lsangiz: S22 Ultra da 'Mobil Hotspot'ni yoqib, planshetni unga ulab oling (Internet sarflanmaydi).\n\n"
            "💻 2-USUL: ISH STOLIDA (Kompyuterga USB simi orqali ulangan paytda)\n"
            "------------------------------------------------------------------------------------\n"
            "1. S22 Ultra va Planshetni kompyuterga USB orqali ulang.\n"
            "2. Ushbu dasturda 'Barcha Yangi Videolarni O'tkazish' tugmasini bosing.\n"
            "3. Barcha 4K videolar 35 MB/s sim tezligida planshet Galereyasiga o'tadi.\n"
            "4. 'Avto-Sinxron' tugmasini yoqsangiz, har safar video olganingizda u 3 soniyada o'zi planshetga ko'chadi!"
        )

        txt = tk.Text(frame, bg="#1A1D24", fg="#E1E4EA", font=("Segoe UI", 10), wrap="word", relief="flat", padx=14, pady=14)
        txt.insert("1.0", text_content)
        txt.config(state="disabled")
        txt.pack(fill="both", expand=True, pady=(0, 15))

        btn_close = ttk.Button(frame, text="Tushundim, Rahmat!", style="Accent.TButton", command=guide_win.destroy)
        btn_close.pack(anchor="e")

    def _on_auto_synced(self, result: TransferEngine):
        self.after(0, self.load_videos)
