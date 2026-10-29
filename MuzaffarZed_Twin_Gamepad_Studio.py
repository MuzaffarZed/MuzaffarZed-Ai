import sys
import os
import time
import threading
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

# Set up environment
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

try:
    import pygame
    pygame.init()
    pygame.joystick.init()
    PYGAME_JOY = True
except Exception as e:
    PYGAME_JOY = False

APP_TITLE = "🎮 2x JOSTIK BOSHQARUV MARKAZI (PRO TWIN GAMEPAD STUDIO)"
APP_VERSION = "2026.1 Ultra"
AUTHOR = "MuzaffarZed"

BG_COLOR = "#0c1017"
PANEL_BG = "#131b26"
CARD_BG = "#1a2434"
TEXT_WHITE = "#f0f6fc"
TEXT_MUTED = "#8b949e"
ACCENT_CYAN = "#00e5ff"
ACCENT_GREEN = "#00e676"
ACCENT_GOLD = "#ffd700"
ACCENT_RED = "#ff5252"
BORDER_COLOR = "#2a3749"

class TwinGamepadStudio(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_TITLE} - by {AUTHOR}")
        self.geometry("1100x780")
        self.minsize(980, 700)
        self.configure(bg=BG_COLOR)

        self.joysticks = []
        self.running = True
        self.init_joysticks()

        self.build_ui()
        self.create_desktop_shortcut()

        # Start 60 FPS polling loop
        self.after(16, self.poll_gamepads)

    def init_joysticks(self):
        if not PYGAME_JOY:
            return
        pygame.joystick.quit()
        pygame.joystick.init()
        count = pygame.joystick.get_count()
        self.joysticks = []
        for i in range(count):
            try:
                j = pygame.joystick.Joystick(i)
                j.init()
                self.joysticks.append(j)
            except Exception:
                pass

    def build_ui(self):
        # 1. HEADER
        header_frame = tk.Frame(self, bg=PANEL_BG, highlightbackground=BORDER_COLOR, highlightthickness=1)
        header_frame.pack(fill=tk.X, padx=15, pady=(15, 10))

        title_lbl = tk.Label(
            header_frame,
            text="🎮 2x JOSTIK BOSHQARUV MARKAZI",
            font=("Segoe UI", 16, "bold"),
            fg=ACCENT_CYAN,
            bg=PANEL_BG
        )
        title_lbl.pack(anchor="w", padx=15, pady=(10, 2))

        sub_lbl = tk.Label(
            header_frame,
            text="1 ta USB Orqali 2 ta Jostikni Boshqarish, XInput (Xbox 360) Rejimiga Aylantirish va O'yinlarga Moslash",
            font=("Segoe UI", 10),
            fg=TEXT_MUTED,
            bg=PANEL_BG
        )
        sub_lbl.pack(anchor="w", padx=15, pady=(0, 10))

        # Status Bar inside Header
        status_frame = tk.Frame(header_frame, bg=PANEL_BG)
        status_frame.pack(fill=tk.X, padx=15, pady=(0, 12))

        self.usb_status_lbl = tk.Label(
            status_frame,
            text="● USB Ulanishi: Aniqlanmoqda...",
            font=("Segoe UI", 9, "bold"),
            fg=ACCENT_GREEN,
            bg=CARD_BG,
            padx=10, pady=4,
            relief=tk.FLAT
        )
        self.usb_status_lbl.pack(side=tk.LEFT, padx=(0, 10))

        self.vigem_status_lbl = tk.Label(
            status_frame,
            text="● ViGEmBus Dvigateli: Faol (Virtual Xbox)",
            font=("Segoe UI", 9, "bold"),
            fg=ACCENT_CYAN,
            bg=CARD_BG,
            padx=10, pady=4
        )
        self.vigem_status_lbl.pack(side=tk.LEFT, padx=(0, 10))

        author_lbl = tk.Label(
            status_frame,
            text=f"Dasturchi: {AUTHOR}",
            font=("Segoe UI", 9, "italic"),
            fg=TEXT_MUTED,
            bg=PANEL_BG
        )
        author_lbl.pack(side=tk.RIGHT, padx=5)

        # 2. MAIN SPLIT: JOYSTICK 1 vs JOYSTICK 2
        cards_container = tk.Frame(self, bg=BG_COLOR)
        cards_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        # Left Card: Player 1
        self.card_p1 = self.build_joystick_card(cards_container, 0, "1-O'YINCHI (JOYSTICK 1)", ACCENT_CYAN)
        self.card_p1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))

        # Right Card: Player 2
        self.card_p2 = self.build_joystick_card(cards_container, 1, "2-O'YINCHI (JOYSTICK 2)", ACCENT_GREEN)
        self.card_p2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(8, 0))

        # 3. ACTION BAR & GAME LAUNCHERS
        action_panel = tk.Frame(self, bg=PANEL_BG, highlightbackground=BORDER_COLOR, highlightthickness=1)
        action_panel.pack(fill=tk.X, padx=15, pady=10)

        action_title = tk.Label(
            action_panel,
            text="⚡ O'YINLAR VA EMULYATSIYA BOSHQARUVI (1-BOSISHDA ISHGA TUSHIRISH)",
            font=("Segoe UI", 10, "bold"),
            fg=ACCENT_GOLD,
            bg=PANEL_BG
        )
        action_title.pack(anchor="w", padx=15, pady=(8, 6))

        btn_row = tk.Frame(action_panel, bg=PANEL_BG)
        btn_row.pack(fill=tk.X, padx=15, pady=(0, 10))

        self.make_btn(btn_row, "🎮 XOutput (Xbox 360 ga Aylantirish)", self.launch_xoutput, ACCENT_CYAN).pack(side=tk.LEFT, padx=(0, 8))
        self.make_btn(btn_row, "⚙️ x360ce Sozlamalari", self.launch_x360ce, "#a371f7").pack(side=tk.LEFT, padx=(0, 8))
        self.make_btn(btn_row, "🏎️ Blur (2-O'yinchi Poyga)", self.launch_blur, ACCENT_GREEN).pack(side=tk.LEFT, padx=(0, 8))
        self.make_btn(btn_row, "🥊 Mortal Kombat", self.launch_mk, "#ff7b72").pack(side=tk.LEFT, padx=(0, 8))
        self.make_btn(btn_row, "🔧 Windows Joy.cpl", self.launch_joycpl, TEXT_MUTED).pack(side=tk.RIGHT)

        # 4. TIPS / HELP FOOTER
        tips_frame = tk.Frame(self, bg=BG_COLOR)
        tips_frame.pack(fill=tk.X, padx=15, pady=(0, 10))

        tip_txt = "💡 ESLATMA: Agar jostik tugmalari ishlamasa, uning o'rtasidagi MODE / ANALOG tugmasini 3 soniya bosib turing (chirog'i yonadi) hamda AAA batareyalarini tekshiring."
        tip_lbl = tk.Label(tips_frame, text=tip_txt, font=("Segoe UI", 9), fg=TEXT_MUTED, bg=BG_COLOR)
        tip_lbl.pack(anchor="w")

    def make_btn(self, parent, text, cmd, accent_col):
        btn = tk.Button(
            parent,
            text=text,
            command=cmd,
            font=("Segoe UI", 9, "bold"),
            fg=BG_COLOR,
            bg=accent_col,
            activebackground="#ffffff",
            activeforeground=BG_COLOR,
            relief=tk.FLAT,
            padx=12, pady=6,
            cursor="hand2"
        )
        return btn

    def build_joystick_card(self, parent, joy_idx, label_text, color):
        card = tk.Frame(parent, bg=PANEL_BG, highlightbackground=color, highlightthickness=1)

        # Card Title
        hdr = tk.Frame(card, bg=PANEL_BG)
        hdr.pack(fill=tk.X, padx=12, pady=8)

        t_lbl = tk.Label(hdr, text=label_text, font=("Segoe UI", 12, "bold"), fg=color, bg=PANEL_BG)
        t_lbl.pack(side=tk.LEFT)

        status_tag = tk.Label(hdr, text="KUTILMOQDA", font=("Segoe UI", 8, "bold"), fg=TEXT_WHITE, bg=CARD_BG, padx=6, pady=2)
        status_tag.pack(side=tk.RIGHT)

        # Canvas for interactive gamepad illustration
        canv = tk.Canvas(card, bg=CARD_BG, highlightthickness=0, height=360)
        canv.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 8))

        # Buttons state table
        btn_grid = tk.Frame(card, bg=PANEL_BG)
        btn_grid.pack(fill=tk.X, padx=10, pady=(0, 8))

        button_indicators = {}
        btn_names = [
            ("1 (△/Y)", 0), ("2 (○/B)", 1), ("3 (✕/A)", 2), ("4 (□/X)", 3),
            ("L1", 4), ("R1", 5), ("L2", 6), ("R2", 7),
            ("Select", 8), ("Start", 9), ("L3", 10), ("R3", 11)
        ]

        for i, (bname, bidx) in enumerate(btn_names):
            r = i // 4
            c = i % 4
            b_lbl = tk.Label(
                btn_grid,
                text=bname,
                font=("Consolas", 8, "bold"),
                fg=TEXT_MUTED,
                bg=CARD_BG,
                width=8,
                pady=2,
                relief=tk.FLAT
            )
            b_lbl.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")
            btn_grid.grid_columnconfigure(c, weight=1)
            button_indicators[bidx] = b_lbl

        # Store widgets in dictionary for polling
        card.data = {
            "idx": joy_idx,
            "status_tag": status_tag,
            "canvas": canv,
            "buttons": button_indicators,
            "color": color
        }
        return card

    def poll_gamepads(self):
        if not self.running:
            return

        if PYGAME_JOY:
            pygame.event.pump()
            num_connected = pygame.joystick.get_count()
            if num_connected >= 2:
                self.usb_status_lbl.config(
                    text="● USB Ulanishi: A'LO (1 ta USB orqali 2 ta Jostik Ulandi!)",
                    fg=ACCENT_GREEN
                )
            elif num_connected == 1:
                self.usb_status_lbl.config(
                    text="● USB Ulanishi: 1 ta Jostik faol (2-jostik batareyasini tekshiring)",
                    fg=ACCENT_GOLD
                )
            else:
                self.usb_status_lbl.config(
                    text="● USB Ulanishi: Jostik topilmadi (USB resiverni tekshiring)",
                    fg=ACCENT_RED
                )

            # Update Card 1 & Card 2
            self.update_card(self.card_p1)
            self.update_card(self.card_p2)

        self.after(16, self.poll_gamepads)

    def update_card(self, card):
        idx = card.data["idx"]
        status_tag = card.data["status_tag"]
        canv = card.data["canvas"]
        btn_dict = card.data["buttons"]
        color = card.data["color"]

        if idx >= len(self.joysticks):
            status_tag.config(text="ULANMAGAN", bg="#3a1d1d", fg=ACCENT_RED)
            canv.delete("all")
            canv.create_text(240, 160, text="Jostik topilmadi\n(Mode tugmasini 3s bosing)", fill=TEXT_MUTED, font=("Segoe UI", 11), justify=tk.CENTER)
            return

        j = self.joysticks[idx]
        status_tag.config(text="FAOL / ISHLAYAPTI", bg="#1b3d2f", fg=ACCENT_GREEN)

        # Read axes
        num_axes = j.get_numaxes()
        lx = j.get_axis(0) if num_axes > 0 else 0.0
        ly = j.get_axis(1) if num_axes > 1 else 0.0
        rx = j.get_axis(2) if num_axes > 2 else 0.0
        ry = j.get_axis(3) if num_axes > 3 else 0.0

        # Read hat
        num_hats = j.get_numhats()
        hat_x, hat_y = j.get_hat(0) if num_hats > 0 else (0, 0)

        # Read buttons
        num_btns = j.get_numbuttons()
        pressed_btns = [j.get_button(b) for b in range(num_btns)]

        # Update button indicators
        for bidx, lbl in btn_dict.items():
            if bidx < len(pressed_btns) and pressed_btns[bidx]:
                lbl.config(bg=color, fg=BG_COLOR)
            else:
                lbl.config(bg=CARD_BG, fg=TEXT_MUTED)

        # Draw Gamepad on Canvas
        canv.delete("all")
        cw = canv.winfo_width() or 480
        ch = canv.winfo_height() or 340
        cx = cw // 2
        cy = ch // 2 - 10

        # Gamepad Body Silhouette
        canv.create_oval(cx - 180, cy - 70, cx + 180, cy + 90, fill="#232f42", outline=BORDER_COLOR, width=2)
        canv.create_oval(cx - 200, cy - 30, cx - 100, cy + 120, fill="#1c2737", outline=BORDER_COLOR, width=2)
        canv.create_oval(cx + 100, cy - 30, cx + 200, cy + 120, fill="#1c2737", outline=BORDER_COLOR, width=2)

        # D-Pad Cross (Left side)
        dpx = cx - 110
        dpy = cy - 10
        dpad_up = hat_y == 1
        dpad_down = hat_y == -1
        dpad_left = hat_x == -1
        dpad_right = hat_x == 1

        canv.create_rectangle(dpx - 8, dpy - 28, dpx + 8, dpy - 8, fill=color if dpad_up else "#33445c", outline="")
        canv.create_rectangle(dpx - 8, dpy + 8, dpx + 8, dpy + 28, fill=color if dpad_down else "#33445c", outline="")
        canv.create_rectangle(dpx - 28, dpy - 8, dpx - 8, dpy + 8, fill=color if dpad_left else "#33445c", outline="")
        canv.create_rectangle(dpx + 8, dpy - 8, dpx + 28, dpy + 8, fill=color if dpad_right else "#33445c", outline="")
        canv.create_text(dpx, dpy, text="D-PAD", font=("Segoe UI", 7, "bold"), fill=TEXT_MUTED)

        # Action Buttons (Right side: Triangle, Circle, Cross, Square)
        abx = cx + 110
        aby = cy - 10
        b_tri = pressed_btns[0] if len(pressed_btns) > 0 else 0
        b_cir = pressed_btns[1] if len(pressed_btns) > 1 else 0
        b_cro = pressed_btns[2] if len(pressed_btns) > 2 else 0
        b_squ = pressed_btns[3] if len(pressed_btns) > 3 else 0

        canv.create_oval(abx - 10, aby - 30, abx + 10, aby - 10, fill=color if b_tri else "#33445c", outline="")
        canv.create_text(abx, aby - 20, text="△", font=("Segoe UI", 8, "bold"), fill=BG_COLOR if b_tri else TEXT_WHITE)

        canv.create_oval(abx + 10, aby - 10, abx + 30, aby + 10, fill=color if b_cir else "#33445c", outline="")
        canv.create_text(abx + 20, aby, text="○", font=("Segoe UI", 8, "bold"), fill=BG_COLOR if b_cir else TEXT_WHITE)

        canv.create_oval(abx - 10, aby + 10, abx + 10, aby + 30, fill=color if b_cro else "#33445c", outline="")
        canv.create_text(abx, aby + 20, text="✕", font=("Segoe UI", 8, "bold"), fill=BG_COLOR if b_cro else TEXT_WHITE)

        canv.create_oval(abx - 30, aby - 10, abx - 10, aby + 10, fill=color if b_squ else "#33445c", outline="")
        canv.create_text(abx - 20, aby, text="□", font=("Segoe UI", 8, "bold"), fill=BG_COLOR if b_squ else TEXT_WHITE)

        # Left Analog Stick (lx, ly)
        lsx = cx - 55
        lsy = cy + 50
        canv.create_oval(lsx - 28, lsy - 28, lsx + 28, lsy + 28, fill="#121824", outline=BORDER_COLOR, width=2)
        # moving thumbstick
        tx = lsx + int(lx * 16)
        ty = lsy + int(ly * 16)
        b_l3 = pressed_btns[10] if len(pressed_btns) > 10 else 0
        canv.create_oval(tx - 16, ty - 16, tx + 16, ty + 16, fill=color if b_l3 else "#3a4a63", outline="")
        canv.create_text(lsx, lsy + 36, text=f"L-Stick ({lx:.2f}, {ly:.2f})", font=("Segoe UI", 7), fill=TEXT_MUTED)

        # Right Analog Stick (rx, ry)
        rsx = cx + 55
        rsy = cy + 50
        canv.create_oval(rsx - 28, rsy - 28, rsx + 28, rsy + 28, fill="#121824", outline=BORDER_COLOR, width=2)
        # moving thumbstick
        rx_pos = rsx + int(rx * 16)
        ry_pos = rsy + int(ry * 16)
        b_r3 = pressed_btns[11] if len(pressed_btns) > 11 else 0
        canv.create_oval(rx_pos - 16, ry_pos - 16, rx_pos + 16, ry_pos + 16, fill=color if b_r3 else "#3a4a63", outline="")
        canv.create_text(rsx, rsy + 36, text=f"R-Stick ({rx:.2f}, {ry:.2f})", font=("Segoe UI", 7), fill=TEXT_MUTED)

        # Center Buttons: Select & Start & Mode
        b_sel = pressed_btns[8] if len(pressed_btns) > 8 else 0
        b_sta = pressed_btns[9] if len(pressed_btns) > 9 else 0
        canv.create_rectangle(cx - 38, cy - 20, cx - 12, cy - 10, fill=color if b_sel else "#33445c", outline="")
        canv.create_text(cx - 25, cy - 15, text="SELECT", font=("Segoe UI", 6, "bold"), fill=BG_COLOR if b_sel else TEXT_WHITE)

        canv.create_rectangle(cx + 12, cy - 20, cx + 38, cy - 10, fill=color if b_sta else "#33445c", outline="")
        canv.create_text(cx + 25, cy - 15, text="START", font=("Segoe UI", 6, "bold"), fill=BG_COLOR if b_sta else TEXT_WHITE)

        # Shoulders (L1, R1, L2, R2)
        b_l1 = pressed_btns[4] if len(pressed_btns) > 4 else 0
        b_r1 = pressed_btns[5] if len(pressed_btns) > 5 else 0
        b_l2 = pressed_btns[6] if len(pressed_btns) > 6 else 0
        b_r2 = pressed_btns[7] if len(pressed_btns) > 7 else 0

        canv.create_rectangle(cx - 160, cy - 80, cx - 100, cy - 65, fill=color if b_l1 else "#23334d", outline=BORDER_COLOR)
        canv.create_text(cx - 130, cy - 73, text="L1 BUMPER", font=("Segoe UI", 7, "bold"), fill=BG_COLOR if b_l1 else TEXT_MUTED)

        canv.create_rectangle(cx + 100, cy - 80, cx + 160, cy - 65, fill=color if b_r1 else "#23334d", outline=BORDER_COLOR)
        canv.create_text(cx + 130, cy - 73, text="R1 BUMPER", font=("Segoe UI", 7, "bold"), fill=BG_COLOR if b_r1 else TEXT_MUTED)

        canv.create_rectangle(cx - 150, cy - 95, cx - 110, cy - 82, fill=color if b_l2 else "#192437", outline=BORDER_COLOR)
        canv.create_text(cx - 130, cy - 89, text="L2", font=("Segoe UI", 6, "bold"), fill=BG_COLOR if b_l2 else TEXT_MUTED)

        canv.create_rectangle(cx + 110, cy - 95, cx + 150, cy - 82, fill=color if b_r2 else "#192437", outline=BORDER_COLOR)
        canv.create_text(cx + 130, cy - 89, text="R2", font=("Segoe UI", 6, "bold"), fill=BG_COLOR if b_r2 else TEXT_MUTED)

    # Launchers
    def launch_xoutput(self):
        xoutput_path = r"C:\Users\MuzaffarZed\ai_workspace\XOutput\XOutput.exe"
        if os.path.exists(xoutput_path):
            subprocess.Popen([xoutput_path])
        else:
            messagebox.showerror("Xato", f"XOutput topilmadi: {xoutput_path}")

    def launch_x360ce(self):
        x360ce_path = r"C:\Users\MuzaffarZed\ai_workspace\x360ce\x360ce.exe"
        if os.path.exists(x360ce_path):
            subprocess.Popen([x360ce_path])
        else:
            messagebox.showerror("Xato", f"x360ce topilmadi: {x360ce_path}")

    def launch_blur(self):
        blur_path = r"D:\KANPIYUTER O'YINLARI\Blur\Blur.exe"
        if os.path.exists(blur_path):
            cwd = os.path.dirname(blur_path)
            subprocess.Popen([blur_path], cwd=cwd)
        else:
            messagebox.showinfo("Blur", f"O'yin manzili topilmadi:\n{blur_path}")

    def launch_mk(self):
        mk_folder = r"D:\KANPIYUTER O'YINLARI\Mortol  kombat"
        if os.path.exists(mk_folder):
            for f in os.listdir(mk_folder):
                if f.lower().endswith(".exe"):
                    subprocess.Popen([os.path.join(mk_folder, f)], cwd=mk_folder)
                    return
            subprocess.Popen(["explorer.exe", mk_folder])
        else:
            messagebox.showinfo("Mortal Kombat", "Mortal Kombat papkasi ochildi.")

    def launch_joycpl(self):
        subprocess.Popen(["control", "joy.cpl"])

    def create_desktop_shortcut(self):
        desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
        shortcut_path = os.path.join(desktop, "2x Jostik Boshqaruv Markazi.lnk")
        if not os.path.exists(shortcut_path):
            try:
                import win32com.client
                shell = win32com.client.Dispatch("WScript.Shell")
                sc = shell.CreateShortCut(shortcut_path)
                sc.TargetPath = sys.executable
                sc.Arguments = f'"{os.path.abspath(__file__)}"'
                sc.WorkingDirectory = os.path.abspath(os.path.dirname(__file__))
                sc.Description = "Twin USB Gamepad 2x Jostik Boshqaruv Markazi by MuzaffarZed"
                sc.IconLocation = r"C:\Windows\System32\shell32.dll,24"
                sc.save()
            except Exception as e:
                print(f"Shortcut creation error: {e}")

if __name__ == '__main__':
    app = TwinGamepadStudio()
    app.mainloop()
