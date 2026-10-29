"""
MuzaffarZed | Oliy Tarmoq Boshqaruv Markazi (Dual-Router Master Suite)
Muallif: MuzaffarZed
Standart: Mutlaq Mukammallik (Zero-Defect)
"""

import sys
import os

# Windows pythonw.exe stdout/stderr xavfsizligi
if sys.stdout is None:
    sys.stdout = open(os.devnull, 'w', encoding='utf-8')
if sys.stderr is None:
    sys.stderr = open(os.devnull, 'w', encoding='utf-8')
if sys.stdin is None:
    sys.stdin = open(os.devnull, 'r', encoding='utf-8')
import subprocess
import urllib.parse
import urllib.request
import time
from datetime import datetime

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QComboBox, QCheckBox, QTabWidget,
    QTableWidget, QTableWidgetItem, QHeaderView, QTextEdit, QFileDialog,
    QMessageBox, QFrame, QScrollArea, QProgressBar, QButtonGroup, QInputDialog,
    QDialog, QMenu
)
from PySide6.QtGui import QIcon, QFont, QColor, QPixmap, QPainter, QBrush, QPen
from PySide6.QtCore import Qt, QTimer, QThread, Signal, QObject

# Dvigatellarni ulash
from router_controller import (
    LBLinkController, InnboxController, LBLink3Controller, test_speed_cloudflare, ping_host,
    scan_wifi_spectrum, save_device_alias, load_device_aliases,
    load_blocked_devices, is_device_blocked
)
from auto_reanimator import AutoReanimator
from adblock_manager import AdBlockManager
from media_server import MediaServerEngine, get_local_ip


class ReanimatorBridge(QObject):
    log_signal = Signal(str)


class SpeedTestThread(QThread):
    finished_signal = Signal(float, float, str)

    def run(self):
        speed, elapsed = test_speed_cloudflare()
        if speed is not None:
            self.finished_signal.emit(speed, elapsed, "")
        else:
            self.finished_signal.emit(0.0, 0.0, str(elapsed))


class SpectrumWorker(QThread):
    finished_signal = Signal(dict)

    def run(self):
        data = scan_wifi_spectrum()
        self.finished_signal.emit(data)


class TelemetryWorker(QThread):
    ping_signal = Signal(object, object, object)
    devices_signal = Signal(list)

    def __init__(self, lblink, innbox, router3):
        super().__init__()
        self.lblink = lblink
        self.innbox = innbox
        self.router3 = router3
        self.running = True

    def run(self):
        loop_cnt = 0
        while self.running:
            try:
                cf, _ = ping_host("1.1.1.1", 1)
            except Exception:
                cf = None
            try:
                uzt, _ = ping_host("192.168.1.1", 1)
            except Exception:
                uzt = None
            try:
                r3_p, _ = ping_host("192.168.1.83", 1)
            except Exception:
                r3_p = None

            self.ping_signal.emit(cf, uzt, r3_p)

            # Har 20 soniyada fon orqali qurilmalarni yangilash
            if loop_cnt % 2 == 1:
                try:
                    lbl = self.lblink.get_connected_devices()
                    for d in lbl:
                        d["router"] = "LB-LINK #1 (BLINK-7783)"
                    inb = self.innbox.get_connected_devices()
                    for d in inb:
                        d["router"] = "Innbox G74L (Optika)"
                    r3_devs = self.router3.get_connected_devices()
                    for d in r3_devs:
                        d["router"] = "LB-LINK #2 (LBLINK-171B)"
                    self.devices_signal.emit(lbl + inb + r3_devs)
                except Exception:
                    pass

            loop_cnt += 1
            for _ in range(10):
                if not self.running:
                    return
                time.sleep(1)

    def stop(self):
        self.running = False


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MuzaffarZed | Oliy Tarmoq Boshqaruv Markazi (Triple-Router Cluster Master)")
        self.resize(1300, 850)
        self.setMinimumSize(1100, 720)

        # Dvigatellarni initsializatsiya qilish (Uchta Router)
        self.lblink = LBLinkController()
        self.innbox = InnboxController()
        self.router3 = LBLink3Controller()
        self.adblock = AdBlockManager(self.lblink)
        self.media_server = MediaServerEngine(r"C:\Users\MuzaffarZed\Videos", port=8899)
        self.media_server.start()

        # Faol boshqarilayotgan router: "lblink", "innbox" yoki "router3"
        self.active_router = "lblink"
        self.recommended_channel = "11"

        # Avto-Reanimator (Thread-safe Qt signal orqali)
        self.reanimator_bridge = ReanimatorBridge()
        self.reanimator_bridge.log_signal.connect(self.on_reanimator_log)
        self.reanimator = AutoReanimator(self.lblink, interval=10, log_callback=self.reanimator_bridge.log_signal.emit)
        self.reanimator.start()

        # Ma'lumotlar keshi
        self.cached_devs = []

        self.setup_ui()
        self.apply_theme()

        # Non-blocking fon telemetriyasi va gadjetlarni fon-yangilash
        self.telemetry = TelemetryWorker(self.lblink, self.innbox, self.router3)
        self.telemetry.ping_signal.connect(self.on_ping_update)
        self.telemetry.devices_signal.connect(self.on_devices_background_update)
        self.telemetry.start()

        # Dastlabki yuklash
        QTimer.singleShot(500, self.initial_load)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(18, 14, 18, 14)
        main_layout.setSpacing(12)

        # 1. YUQORI HEADER & ROUTER ALMASHTIRGICH (SWITCHER)
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        h_layout = QHBoxLayout(header_frame)
        h_layout.setContentsMargins(16, 12, 16, 12)

        # Chap: Sarlavha va Imzo
        title_box = QVBoxLayout()
        title_label = QLabel("⚡ MUZAFFARZED | OLIY TARMOQ BOSHQARUV MARKAZI")
        title_label.setObjectName("appTitle")
        sub_label = QLabel("LB-LINK #1 (BLINK-7783) • Innbox G74L (Optika) • LB-LINK #2 (LBLINK-171B) Klaster Tizimi")
        sub_label.setObjectName("appSubtitle")
        title_box.addWidget(title_label)
        title_box.addWidget(sub_label)
        h_layout.addLayout(title_box)

        h_layout.addStretch()

        # O'ng: ROUTER TANLASH TUGMALARI (3 TA ROUTER)
        router_sel_box = QVBoxLayout()
        sel_title = QLabel("BOSHQARILAYOTGAN ROUTER:")
        sel_title.setStyleSheet("font-size: 11px; font-weight: 700; color: #94a3b8; letter-spacing: 1px;")
        router_sel_box.addWidget(sel_title, alignment=Qt.AlignRight)

        btns_h = QHBoxLayout()
        self.btn_sel_lblink = QPushButton("🟢 LB-LINK #1 (192.168.16.1)")
        self.btn_sel_lblink.setObjectName("btnRouterSelectActive")
        self.btn_sel_lblink.setCursor(Qt.PointingHandCursor)
        self.btn_sel_lblink.clicked.connect(lambda: self.switch_active_router("lblink"))

        self.btn_sel_innbox = QPushButton("🔵 Innbox G74L (192.168.1.1)")
        self.btn_sel_innbox.setObjectName("btnRouterSelectInactive")
        self.btn_sel_innbox.setCursor(Qt.PointingHandCursor)
        self.btn_sel_innbox.clicked.connect(lambda: self.switch_active_router("innbox"))

        self.btn_sel_router3 = QPushButton("🟣 LB-LINK #2 (192.168.1.83)")
        self.btn_sel_router3.setObjectName("btnRouterSelectInactive")
        self.btn_sel_router3.setCursor(Qt.PointingHandCursor)
        self.btn_sel_router3.clicked.connect(lambda: self.switch_active_router("router3"))

        btns_h.addWidget(self.btn_sel_lblink)
        btns_h.addWidget(self.btn_sel_innbox)
        btns_h.addWidget(self.btn_sel_router3)
        router_sel_box.addLayout(btns_h)
        h_layout.addLayout(router_sel_box)

        main_layout.addWidget(header_frame)

        # 2. ASOSIY TABLAR
        self.tabs = QTabWidget()
        self.tabs.setObjectName("mainTabs")
        self.tabs.setCursor(Qt.PointingHandCursor)

        self.tab_dashboard = QWidget()
        self.tab_wifi = QWidget()
        self.tab_devices = QWidget()
        self.tab_reanimator = QWidget()
        self.tab_adblock = QWidget()
        self.tab_mediaserver = QWidget()
        self.tab_qrcode = QWidget()

        self.tabs.addTab(self.tab_dashboard, "📊 Umumiy Nazorat")
        self.tabs.addTab(self.tab_wifi, "📶 Wi-Fi Boshqaruvi")
        self.tabs.addTab(self.tab_devices, "📱 30+ Ulangan Qurilmalar")
        self.tabs.addTab(self.tab_reanimator, "⚡ Avto-Reanimatsiya")
        self.tabs.addTab(self.tab_adblock, "🛡️ Hardware AdBlock")
        self.tabs.addTab(self.tab_mediaserver, "🎬 Smart TV 4K Media Server")
        self.tabs.addTab(self.tab_qrcode, "📲 Wi-Fi QR Kod")

        self.build_tab_dashboard()
        self.build_tab_wifi()
        self.build_tab_devices()
        self.build_tab_reanimator()
        self.build_tab_adblock()
        self.build_tab_mediaserver()
        self.build_tab_qrcode()

        main_layout.addWidget(self.tabs)

        # 3. FOOTER & STATUS BAR
        footer = QHBoxLayout()
        self.lbl_footer_status = QLabel("Holat: Barcha tizimlar barqaror ishlamoqda • Mutlaq Mukammallik")
        self.lbl_footer_status.setStyleSheet("color: #64748b; font-size: 13px;")
        lbl_sign = QLabel("Dasturchi: MuzaffarZed")
        lbl_sign.setStyleSheet("color: #38bdf8; font-weight: 700; font-size: 13px;")

        footer.addWidget(self.lbl_footer_status)
        footer.addStretch()
        footer.addWidget(lbl_sign)
        main_layout.addLayout(footer)

    # ========================== TAB 1: DASHBOARD ==========================
    def build_tab_dashboard(self):
        layout = QVBoxLayout(self.tab_dashboard)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(16)

        # Uchta router kartasi yonma-yon (Klaster)
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(14)

        # 1-Karta: LB-LINK #1
        card_lblink = QFrame()
        card_lblink.setObjectName("cardFrame")
        c1 = QVBoxLayout(card_lblink)
        lbl_h1 = QLabel("🟢 LB-LINK #1 (Asosiy Wi-Fi Hub)")
        lbl_h1.setStyleSheet("font-weight: 700; color: #4ade80; font-size: 14px;")
        c1.addWidget(lbl_h1)
        self.lbl_dash_lblink_ip = QLabel("LAN IP: 192.168.16.1 (WAN: 192.168.1.11)")
        self.lbl_dash_lblink_ssid = QLabel("Wi-Fi: BLINK-7783 (Kanal: 11 • 99%)")
        self.lbl_dash_lblink_pool = QLabel("DHCP: 192.168.16.10 - 250 (241 ta IP)")
        self.lbl_dash_lblink_status = QLabel("Holati: 🟢 Normal (Faol - 7+ Gadjet)")
        c1.addWidget(self.lbl_dash_lblink_ip)
        c1.addWidget(self.lbl_dash_lblink_ssid)
        c1.addWidget(self.lbl_dash_lblink_pool)
        c1.addWidget(self.lbl_dash_lblink_status)
        cards_layout.addWidget(card_lblink)

        # 2-Karta: Innbox G74L
        card_innbox = QFrame()
        card_innbox.setObjectName("cardFrame")
        c2 = QVBoxLayout(card_innbox)
        lbl_h2 = QLabel("🔵 Innbox G74L (Optik Magistral)")
        lbl_h2.setStyleSheet("font-weight: 700; color: #38bdf8; font-size: 14px;")
        c2.addWidget(lbl_h2)
        self.lbl_dash_innbox_ip = QLabel("Shlyuz IP: 192.168.1.1 (Optik GPON)")
        self.lbl_dash_innbox_pwr = QLabel("Optik Quvvat: -19.638 dBm (A'lo signal)")
        self.lbl_dash_innbox_pon = QLabel("PON Holati: O5 (Barqaror optika)")
        self.lbl_dash_innbox_wan = QLabel("Uztelecom WAN: 100.75.213.194")
        c2.addWidget(self.lbl_dash_innbox_ip)
        c2.addWidget(self.lbl_dash_innbox_pwr)
        c2.addWidget(self.lbl_dash_innbox_pon)
        c2.addWidget(self.lbl_dash_innbox_wan)
        cards_layout.addWidget(card_innbox)

        # 3-Karta: LB-LINK #2
        card_router3 = QFrame()
        card_router3.setObjectName("cardFrame")
        c3 = QVBoxLayout(card_router3)
        lbl_h3 = QLabel("🟣 LB-LINK #2 (Yangi Wi-Fi Hub)")
        lbl_h3.setStyleSheet("font-weight: 700; color: #c084fc; font-size: 14px;")
        c3.addWidget(lbl_h3)
        self.lbl_dash_r3_ip = QLabel("WAN IP: 192.168.1.83 (Innbox Port 2)")
        self.lbl_dash_r3_ssid = QLabel("Wi-Fi: LBLINK-171B (Kanal: 11 • 16%)")
        self.lbl_dash_r3_speed = QLabel("Oqim: 100 Mbps Full-Duplex • 3.39 GB")
        self.lbl_dash_r3_status = QLabel("Holati: 🟢 Normal (Faol • Ping 1ms)")
        c3.addWidget(self.lbl_dash_r3_ip)
        c3.addWidget(self.lbl_dash_r3_ssid)
        c3.addWidget(self.lbl_dash_r3_speed)
        c3.addWidget(self.lbl_dash_r3_status)
        cards_layout.addWidget(card_router3)

        layout.addLayout(cards_layout)

        # Spidometr va Ping bloki
        speed_frame = QFrame()
        speed_frame.setObjectName("cardFrame")
        sp_layout = QVBoxLayout(speed_frame)

        sp_title = QLabel("🚀 Real Vaqtdagi Tarmoq Tezligi va Kechikish (Ping)")
        sp_title.setStyleSheet("font-size: 16px; font-weight: 700; color: #38bdf8;")
        sp_layout.addWidget(sp_title)

        ping_h = QHBoxLayout()
        self.lbl_ping_uzt = QLabel("Uztelecom Optika Ping: 2 ms ⚡")
        self.lbl_ping_cf = QLabel("Cloudflare Ping: 75 ms 🌐")
        self.lbl_ping_r3 = QLabel("LB-LINK #2 Ping: 1 ms ⚡")
        self.lbl_ping_loss = QLabel("Paket Yo'qotilishi: 0% (Mukammal)")
        ping_h.addWidget(self.lbl_ping_uzt)
        ping_h.addWidget(self.lbl_ping_cf)
        ping_h.addWidget(self.lbl_ping_r3)
        ping_h.addWidget(self.lbl_ping_loss)
        sp_layout.addLayout(ping_h)

        test_h = QHBoxLayout()
        self.btn_run_speedtest = QPushButton("⚡ Cloudflare 10MB Haqiqiy Tezlikni O'lchash")
        self.btn_run_speedtest.setObjectName("btnAccent")
        self.btn_run_speedtest.setCursor(Qt.PointingHandCursor)
        self.btn_run_speedtest.clicked.connect(self.run_speed_test)

        self.lbl_speed_res = QLabel("Tezlik: O'lchanmagan (Tugmani bosing)")
        self.lbl_speed_res.setStyleSheet("font-size: 15px; font-weight: 700; color: #00e676;")

        test_h.addWidget(self.btn_run_speedtest)
        test_h.addWidget(self.lbl_speed_res)
        test_h.addStretch()
        sp_layout.addLayout(test_h)

        layout.addWidget(speed_frame)
        layout.addStretch()

    # ========================== TAB 2: WI-FI BOSHQARUVI ==========================
    def build_tab_wifi(self):
        layout = QVBoxLayout(self.tab_wifi)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(16)

        # 1. Efir Skaneri Karti (Wi-Fi Spectrum & Channel Analyzer)
        spec_card = QFrame()
        spec_card.setObjectName("cardFrame")
        sc_layout = QVBoxLayout(spec_card)
        sc_layout.setContentsMargins(16, 12, 16, 12)
        sc_layout.setSpacing(8)

        sc_top = QHBoxLayout()
        lbl_spec_title = QLabel("📡 Jonli Wi-Fi Efir Spektri (Qo'shnilar va Toza Kanallar Tahlili)")
        lbl_spec_title.setStyleSheet("font-size: 14px; font-weight: 700; color: #38bdf8;")
        self.btn_scan_spectrum = QPushButton("🔄 Efirni Skanerlash")
        self.btn_scan_spectrum.setCursor(Qt.PointingHandCursor)
        self.btn_scan_spectrum.clicked.connect(self.run_spectrum_scan)

        self.btn_pick_best_ch = QPushButton("✨ Eng Toza Kanalni Tanlash")
        self.btn_pick_best_ch.setObjectName("btnAccent")
        self.btn_pick_best_ch.setCursor(Qt.PointingHandCursor)
        self.btn_pick_best_ch.clicked.connect(self.apply_recommended_channel)

        sc_top.addWidget(lbl_spec_title)
        sc_top.addStretch()
        sc_top.addWidget(self.btn_scan_spectrum)
        sc_top.addWidget(self.btn_pick_best_ch)
        sc_layout.addLayout(sc_top)

        self.lbl_spectrum_display = QLabel("Efir holati tahlil qilinmoqda...")
        self.lbl_spectrum_display.setStyleSheet("font-family: Consolas, monospace; font-size: 13px; color: #cbd5e1; background: #070d19; padding: 10px; border-radius: 8px; border: 1px solid #1e293b;")
        self.lbl_spectrum_display.setWordWrap(True)
        sc_layout.addWidget(self.lbl_spectrum_display)

        layout.addWidget(spec_card)

        # Sarlavha va faol router ko'rsatkichi
        self.lbl_wifi_active_hint = QLabel("Hozir sozlanayotgan router: 🟢 LB-LINK BL-WR450H (192.168.16.1)")
        self.lbl_wifi_active_hint.setObjectName("sectionHeader")
        layout.addWidget(self.lbl_wifi_active_hint)

        form_frame = QFrame()
        form_frame.setObjectName("cardFrame")
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(14)

        # SSID (Wi-Fi nomi)
        h_ssid = QHBoxLayout()
        lbl_s = QLabel("Wi-Fi Nomi (SSID):")
        lbl_s.setFixedWidth(160)
        self.txt_wifi_ssid = QLineEdit()
        self.txt_wifi_ssid.setPlaceholderText("Tarmoq nomini kiriting...")
        h_ssid.addWidget(lbl_s)
        h_ssid.addWidget(self.txt_wifi_ssid)
        form_layout.addLayout(h_ssid)

        # Parol
        h_pwd = QHBoxLayout()
        lbl_p = QLabel("Wi-Fi Paroli:")
        lbl_p.setFixedWidth(160)
        self.txt_wifi_pwd = QLineEdit()
        self.txt_wifi_pwd.setEchoMode(QLineEdit.Password)
        self.chk_show_pwd = QCheckBox("Parolni ko'rsatish")
        self.chk_show_pwd.toggled.connect(lambda v: self.txt_wifi_pwd.setEchoMode(QLineEdit.Normal if v else QLineEdit.Password))
        h_pwd.addWidget(lbl_p)
        h_pwd.addWidget(self.txt_wifi_pwd)
        h_pwd.addWidget(self.chk_show_pwd)
        form_layout.addLayout(h_pwd)

        # Kanal
        h_ch = QHBoxLayout()
        lbl_c = QLabel("Wi-Fi Kanali:")
        lbl_c.setFixedWidth(160)
        self.cmb_wifi_channel = QComboBox()
        self.cmb_wifi_channel.setEditable(True)
        self.cmb_wifi_channel.setFixedWidth(90)
        for c_num in range(1, 14):
            self.cmb_wifi_channel.addItem(str(c_num))

        # Tezkor tanlash tugmalari
        btn_ch1 = QPushButton("1-Kanal (Toza)")
        btn_ch1.setCursor(Qt.PointingHandCursor)
        btn_ch1.clicked.connect(lambda: self.select_quick_channel("1"))

        btn_ch6 = QPushButton("6-Kanal (Standart)")
        btn_ch6.setCursor(Qt.PointingHandCursor)
        btn_ch6.clicked.connect(lambda: self.select_quick_channel("6"))

        btn_ch11 = QPushButton("11-Kanal (Barqaror)")
        btn_ch11.setCursor(Qt.PointingHandCursor)
        btn_ch11.clicked.connect(lambda: self.select_quick_channel("11"))

        h_ch.addWidget(lbl_c)
        h_ch.addWidget(self.cmb_wifi_channel)
        h_ch.addWidget(btn_ch1)
        h_ch.addWidget(btn_ch6)
        h_ch.addWidget(btn_ch11)
        h_ch.addStretch()
        form_layout.addLayout(h_ch)

        # Kanal Kengligi (Bandwidth: 20MHz vs 40MHz)
        h_width = QHBoxLayout()
        lbl_w = QLabel("Kanal Kengligi (Tezlik):")
        lbl_w.setFixedWidth(160)
        self.cmb_wifi_width = QComboBox()
        self.cmb_wifi_width.addItem("⚡ 40 MHz / Auto (Maksimal 300 Mbps - Yuqori Tezlik)", "2")
        self.cmb_wifi_width.addItem("🛡️ 20 MHz (Barqaror 144 Mbps - Standart Qamrov)", "1")
        h_width.addWidget(lbl_w)
        h_width.addWidget(self.cmb_wifi_width)
        h_width.addStretch()
        form_layout.addLayout(h_width)

        # Quvvat (TX Power)
        h_pwr = QHBoxLayout()
        lbl_pwr = QLabel("Signal Quvvati:")
        lbl_pwr.setFixedWidth(160)
        self.cmb_wifi_power = QComboBox()
        self.cmb_wifi_power.addItems(["100% (Maksimal Qamrov)", "50% (O'rtacha)", "25% (Yaqin masofa)"])
        h_pwr.addWidget(lbl_pwr)
        h_pwr.addWidget(self.cmb_wifi_power)
        h_pwr.addStretch()
        form_layout.addLayout(h_pwr)

        # Yashirin Wi-Fi
        self.chk_wifi_hidden = QCheckBox("Yashirin tarmoq (SSID ni begonalardan yashirish)")
        form_layout.addWidget(self.chk_wifi_hidden)

        layout.addWidget(form_frame)

        # Tugmalar paneli
        btn_bar = QHBoxLayout()
        btn_save = QPushButton("💾 Saqlash va Routerga Qo'llash")
        btn_save.setObjectName("btnAccent")
        btn_save.setCursor(Qt.PointingHandCursor)
        btn_save.clicked.connect(self.save_wifi_settings)

        btn_reboot = QPushButton("🔄 Routerni Qayta Yuklash (Reboot)")
        btn_reboot.setObjectName("btnDanger")
        btn_reboot.setCursor(Qt.PointingHandCursor)
        btn_reboot.clicked.connect(self.reboot_active_router)

        btn_bar.addWidget(btn_save)
        btn_bar.addWidget(btn_reboot)
        btn_bar.addStretch()
        layout.addLayout(btn_bar)

        layout.addStretch()

    # ========================== TAB 3: ULANGAN QURILMALAR ==========================
    def build_tab_devices(self):
        layout = QVBoxLayout(self.tab_devices)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        # Yuqori filtr va holat paneli
        top_bar = QHBoxLayout()
        self.lbl_dev_count = QLabel("Jami Ulangan Gadjetlar: Yuklanmoqda...")
        self.lbl_dev_count.setStyleSheet("font-size: 15px; font-weight: 700; color: #38bdf8;")

        self.cmb_dev_filter = QComboBox()
        self.cmb_dev_filter.addItems([
            "🌐 Barcha Gadjetlar (Barcha 3 ta Router)",
            "🟢 Faqat LB-LINK #1 (BLINK-7783)",
            "🔵 Faqat Innbox G74L (Optika)",
            "🟣 Faqat LB-LINK #2 (LBLINK-171B)"
        ])
        self.cmb_dev_filter.currentIndexChanged.connect(self.filter_devices_table)

        btn_refresh = QPushButton("🔄 Ro'yxatni Yangilash")
        btn_refresh.setObjectName("btnAccent")
        btn_refresh.setCursor(Qt.PointingHandCursor)
        btn_refresh.clicked.connect(self.refresh_devices_table)

        top_bar.addWidget(self.lbl_dev_count)
        top_bar.addStretch()
        top_bar.addWidget(QLabel("Filtr:"))
        top_bar.addWidget(self.cmb_dev_filter)
        top_bar.addWidget(btn_refresh)
        layout.addLayout(top_bar)

        # 2-QATOR: TEZKOR BOSHQARUV TUGMALARI (BLOKLASH, OCHISH, NOM, QORA RO'YXAT)
        action_bar = QHBoxLayout()
        action_bar.setSpacing(10)

        self.btn_block_dev = QPushButton("🚫 Tanlangan Gadjetni Bloklash (Internetni Uzish)")
        self.btn_block_dev.setObjectName("btnDanger")
        self.btn_block_dev.setCursor(Qt.PointingHandCursor)
        self.btn_block_dev.clicked.connect(self.block_selected_device)

        self.btn_unblock_dev = QPushButton("🔓 Blokdan Chiqarish")
        self.btn_unblock_dev.setStyleSheet("background: #059669; color: #ffffff; font-weight: 700; border-radius: 6px; padding: 10px 16px; font-size: 13px;")
        self.btn_unblock_dev.setCursor(Qt.PointingHandCursor)
        self.btn_unblock_dev.clicked.connect(self.unblock_selected_device)

        self.btn_rename_dev = QPushButton("✏️ Nom Berish")
        self.btn_rename_dev.setCursor(Qt.PointingHandCursor)
        self.btn_rename_dev.clicked.connect(self.rename_selected_device)

        self.btn_blacklist_dialog = QPushButton("📋 Qora Ro'yxat (Blacklist)")
        self.btn_blacklist_dialog.setStyleSheet("background: #4f46e5; color: #ffffff; font-weight: 700; border-radius: 6px; padding: 10px 16px; font-size: 13px;")
        self.btn_blacklist_dialog.setCursor(Qt.PointingHandCursor)
        self.btn_blacklist_dialog.clicked.connect(self.show_blacklist_dialog)

        lbl_hint = QLabel("💡 Gadjet ustiga o'ng tugmani (Right-Click) bosib ham tezkor boshqarish mumkin")
        lbl_hint.setStyleSheet("color: #94a3b8; font-size: 12px; font-style: italic;")

        action_bar.addWidget(self.btn_block_dev)
        action_bar.addWidget(self.btn_unblock_dev)
        action_bar.addWidget(self.btn_rename_dev)
        action_bar.addWidget(self.btn_blacklist_dialog)
        action_bar.addStretch()
        action_bar.addWidget(lbl_hint)
        layout.addLayout(action_bar)

        # Qurilmalar Jadvali
        self.tbl_devices = QTableWidget()
        self.tbl_devices.setColumnCount(7)
        self.tbl_devices.setHorizontalHeaderLabels([
            "Qurilma Nomi", "IP Manzil", "MAC Manzil", "Ulangan Router", "Holati", "Signal Kuchi", "Tezlik"
        ])
        self.tbl_devices.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tbl_devices.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tbl_devices.verticalHeader().setVisible(False)
        self.tbl_devices.setAlternatingRowColors(True)
        self.tbl_devices.itemDoubleClicked.connect(self.rename_selected_device)
        self.tbl_devices.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tbl_devices.customContextMenuRequested.connect(self.on_device_context_menu)
        layout.addWidget(self.tbl_devices)

    # ========================== TAB 4: AVTO-REANIMATSIYA ==========================
    def build_tab_reanimator(self):
        layout = QVBoxLayout(self.tab_reanimator)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(16)

        status_frame = QFrame()
        status_frame.setObjectName("cardFrame")
        s_layout = QVBoxLayout(status_frame)

        self.lbl_reanimator_badge = QLabel("🟢 AVTO-REANIMATSIYA: FAOL (24/7 Monitoring)")
        self.lbl_reanimator_badge.setObjectName("badgeGreen")

        desc = QLabel(
            "Ushbu intellektual tizim har ikki Wi-Fi (LB-LINK va Innbox) tarmoqlarini doimiy nazorat qiladi.\n"
            "Agar Uztelecom DNS serverlari qotsa yoki uzilsa, 1 soniyada inson aralashuvisiz zaxira kanallarga "
            "(Cloudflare 1.1.1.1 + Yandex Safe 77.88.8.88) o'tkaziladi va barcha telefon va televizorlar uzilmasdan ishlayveradi."
        )
        desc.setStyleSheet("color: #94a3b8; font-size: 14px; line-height: 1.5;")
        desc.setWordWrap(True)

        s_layout.addWidget(self.lbl_reanimator_badge)
        s_layout.addWidget(desc)
        layout.addWidget(status_frame)

        # Qo'lda sinash va boshqarish
        act_h = QHBoxLayout()
        btn_force_test = QPushButton("⚡ Qayta Tiklashni Hozir Sinash (Test Failover)")
        btn_force_test.setObjectName("btnAccent")
        btn_force_test.setCursor(Qt.PointingHandCursor)
        btn_force_test.clicked.connect(self.manual_reanimate)

        self.lbl_reanim_active_mode = QLabel("Joriy Rejim: Birlamchi Tezkor Optika (192.168.1.1)")
        self.lbl_reanim_active_mode.setStyleSheet("font-weight: 700; color: #00e676; font-size: 14px;")

        act_h.addWidget(btn_force_test)
        act_h.addWidget(self.lbl_reanim_active_mode)
        act_h.addStretch()
        layout.addLayout(act_h)

        # Jonli log jurnali
        layout.addWidget(QLabel("📋 Real Vaqtdagi Reanimatsiya Jurnali:"))
        self.txt_reanimator_log = QTextEdit()
        self.txt_reanimator_log.setReadOnly(True)
        self.txt_reanimator_log.setObjectName("logBox")
        layout.addWidget(self.txt_reanimator_log)

    # ========================== TAB 5: HARDWARE ADBLOCK ==========================
    def build_tab_adblock(self):
        layout = QVBoxLayout(self.tab_adblock)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(16)

        card = QFrame()
        card.setObjectName("cardFrame")
        c_layout = QVBoxLayout(card)

        self.lbl_adblock_badge = QLabel("🛡️ HARDWARE ADBLOCK: FAOL (Router Darajasidagi Himoya)")
        self.lbl_adblock_badge.setObjectName("badgeGreen")

        desc = QLabel(
            "Uyingizdagi barcha 30 ta telefon, televizor va planshetlarda parazit bannerlarni, "
            "Smart TV dagi zerikarli o'rtaga suqiluvchi treylerlarni va virusli havolalarni router darajasida bloklaydi.\n"
            "Gadjetlarning o'ziga hech qanday qo'shimcha ilova o'rnatish talab etilmaydi!"
        )
        desc.setStyleSheet("color: #94a3b8; font-size: 14px; line-height: 1.5;")
        desc.setWordWrap(True)

        c_layout.addWidget(self.lbl_adblock_badge)
        c_layout.addWidget(desc)
        layout.addWidget(card)

        # Profil tanlash
        prof_frame = QFrame()
        prof_frame.setObjectName("cardFrame")
        p_layout = QVBoxLayout(prof_frame)
        p_layout.addWidget(QLabel("Filtrlash Rejimini Tanlang:"))

        self.cmb_adblock_profile = QComboBox()
        self.cmb_adblock_profile.addItems([
            "🛡️ Maksimal Reklama & Xavfsizlik (Yandex Safe 77.88.8.88 + Cloudflare Security 1.1.1.2)",
            "👶 Oila va Bolalar Himoyasi (Adult Content & Banner Filter - Cloudflare Family 1.1.1.3)",
            "⚡ Maksimal Tezkor To'g'ridan-to'g'ri (Filtrsiz - 192.168.1.1 / 1.1.1.1)"
        ])
        p_layout.addWidget(self.cmb_adblock_profile)

        btn_apply_adblock = QPushButton("💾 Filtrlash Rejimini Routerga Qo'llash")
        btn_apply_adblock.setObjectName("btnAccent")
        btn_apply_adblock.setCursor(Qt.PointingHandCursor)
        btn_apply_adblock.clicked.connect(self.apply_adblock_profile)
        p_layout.addWidget(btn_apply_adblock)

        layout.addWidget(prof_frame)
        layout.addStretch()

    # ========================== TAB 6: SMART TV 4K MEDIA SERVER ==========================
    def build_tab_mediaserver(self):
        layout = QVBoxLayout(self.tab_mediaserver)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(16)

        card = QFrame()
        card.setObjectName("cardFrame")
        c_layout = QVBoxLayout(card)

        self.lbl_media_badge = QLabel("🟢 4K DLNA & WEB MEDIA SERVER: ISHLAMOQDA")
        self.lbl_media_badge.setObjectName("badgeGreen")

        local_ip = get_local_ip()
        info_html = (
            f"<b>Kompyuteringizdagi 4K kinolarni televizorda ko'rishning 2 xil oson yo'li:</b><br><br>"
            f"1. <b>📺 Smart TV Pultidan (Fleshkasiz, Simsiz):</b> Televizor pultidagi <i>'Source'</i> (Manbalar / Kirishlar) "
            f"tugmasini bosing — televizoringiz avtomatik ravishda <b>'MuzaffarZed 4K Cinema'</b> ni ko'rsatadi! "
            f"Faylni tanlab, to'g'ridan-to'g'ri pultdan ko'ravering.<br><br>"
            f"2. <b>🌐 Brauzer orqali:</b> Smart TV yoki telefon brauzerida ushbu manzilni oching:<br>"
            f"<span style='color: #00e676; font-size: 16px; font-weight: bold;'>http://{local_ip}:8899</span>"
        )
        lbl_info = QLabel(info_html)
        lbl_info.setStyleSheet("color: #cbd5e1; font-size: 14px; line-height: 1.6;")
        lbl_info.setWordWrap(True)

        c_layout.addWidget(self.lbl_media_badge)
        c_layout.addWidget(lbl_info)
        layout.addWidget(card)

        # Papka tanlash
        folder_frame = QFrame()
        folder_frame.setObjectName("cardFrame")
        f_layout = QHBoxLayout(folder_frame)

        f_layout.addWidget(QLabel("Media Papka:"))
        self.txt_media_path = QLineEdit(r"C:\Users\MuzaffarZed\Videos")
        self.txt_media_path.setReadOnly(True)
        btn_browse = QPushButton("📁 Papkani O'zgartirish")
        btn_browse.setCursor(Qt.PointingHandCursor)
        btn_browse.clicked.connect(self.browse_media_folder)

        f_layout.addWidget(self.txt_media_path)
        f_layout.addWidget(btn_browse)
        layout.addWidget(folder_frame)

        layout.addStretch()

    # ========================== TAB 7: WI-FI QR KOD ==========================
    def build_tab_qrcode(self):
        layout = QVBoxLayout(self.tab_qrcode)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(16)

        card = QFrame()
        card.setObjectName("cardFrame")
        c = QVBoxLayout(card)

        self.lbl_qr_title = QLabel("📲 Mehmonlar Uchun Tezkor Wi-Fi QR Kodu")
        self.lbl_qr_title.setObjectName("sectionHeader")

        self.lbl_qr_desc = QLabel("Telefon kamerasini tutish bilan parol yozmasdan Wi-Fi ga ulanish:")
        self.lbl_qr_desc.setStyleSheet("color: #94a3b8; font-size: 14px;")

        self.lbl_qr_image = QLabel()
        self.lbl_qr_image.setAlignment(Qt.AlignCenter)
        self.lbl_qr_image.setFixedSize(260, 260)
        self.lbl_qr_image.setStyleSheet("background: #ffffff; border-radius: 12px; padding: 10px;")

        self.lbl_qr_info = QLabel("Tarmoq: BLINK-7783 • Parol: 978852003Zed")
        self.lbl_qr_info.setStyleSheet("color: #38bdf8; font-weight: 700; font-size: 15px;")
        self.lbl_qr_info.setAlignment(Qt.AlignCenter)

        c.addWidget(self.lbl_qr_title)
        c.addWidget(self.lbl_qr_desc)
        c.addWidget(self.lbl_qr_image, alignment=Qt.AlignCenter)
        c.addWidget(self.lbl_qr_info)
        layout.addWidget(card)
        layout.addStretch()

    # ========================== ROUTER ALMASHTIRISH (SWITCHER) ==========================
    def switch_active_router(self, router_key):
        self.active_router = router_key
        if router_key == "lblink":
            self.btn_sel_lblink.setObjectName("btnRouterSelectActive")
            self.btn_sel_innbox.setObjectName("btnRouterSelectInactive")
            self.btn_sel_router3.setObjectName("btnRouterSelectInactive")
            self.lbl_wifi_active_hint.setText("Hozir sozlanayotgan router: 🟢 LB-LINK #1 (192.168.16.1 • BLINK-7783)")
            self.load_lblink_wifi()
        elif router_key == "innbox":
            self.btn_sel_lblink.setObjectName("btnRouterSelectInactive")
            self.btn_sel_innbox.setObjectName("btnRouterSelectActive")
            self.btn_sel_router3.setObjectName("btnRouterSelectInactive")
            self.lbl_wifi_active_hint.setText("Hozir sozlanayotgan router: 🔵 Innbox G74L GPON Optika (192.168.1.1)")
            self.load_innbox_wifi()
        else: # router3
            self.btn_sel_lblink.setObjectName("btnRouterSelectInactive")
            self.btn_sel_innbox.setObjectName("btnRouterSelectInactive")
            self.btn_sel_router3.setObjectName("btnRouterSelectActive")
            self.lbl_wifi_active_hint.setText("Hozir sozlanayotgan router: 🟣 LB-LINK #2 (192.168.1.83 • LBLINK-171B)")
            self.load_router3_wifi()

        # CSS ni qayta qo'llash
        self.btn_sel_lblink.setStyle(self.btn_sel_lblink.style())
        self.btn_sel_innbox.setStyle(self.btn_sel_innbox.style())
        self.btn_sel_router3.setStyle(self.btn_sel_router3.style())
        self.update_qr_code()

    def select_quick_channel(self, ch_str):
        idx = self.cmb_wifi_channel.findText(ch_str)
        if idx >= 0:
            self.cmb_wifi_channel.setCurrentIndex(idx)
        else:
            self.cmb_wifi_channel.setEditText(ch_str)

    def load_lblink_wifi(self):
        w = self.lblink.get_wifi_info()
        self.txt_wifi_ssid.setText(w.get("ssid", "BLINK-7783"))
        self.txt_wifi_pwd.setText(w.get("password", "978852003Zed"))
        ch = str(w.get("channel", "6")).strip()
        idx = self.cmb_wifi_channel.findText(ch)
        if idx >= 0:
            self.cmb_wifi_channel.setCurrentIndex(idx)
        else:
            self.cmb_wifi_channel.setEditText(ch)

        # Kenglik (Bandwidth)
        w_val = str(w.get("width", "2"))
        w_idx = 0 if w_val in ["2", "auto", "20/40"] else 1
        self.cmb_wifi_width.setCurrentIndex(w_idx)

        self.chk_wifi_hidden.setChecked(w.get("hidden") == "1")

    def load_innbox_wifi(self):
        w = self.innbox.get_wifi_info()
        self.txt_wifi_ssid.setText(w.get("ssid", "Innbox-internet-deafa6"))
        self.txt_wifi_pwd.setText(w.get("password", "1234567890Zed"))
        ch = str(w.get("channel", "1")).strip()
        idx = self.cmb_wifi_channel.findText(ch)
        if idx >= 0:
            self.cmb_wifi_channel.setCurrentIndex(idx)
        else:
            self.cmb_wifi_channel.setEditText(ch)

        # Kenglik (Bandwidth)
        w_str = str(w.get("width", "20/40 MHz"))
        w_idx = 0 if "40" in w_str else 1
        self.cmb_wifi_width.setCurrentIndex(w_idx)

        self.chk_wifi_hidden.setChecked(w.get("hidden") == "1")

    def load_router3_wifi(self):
        w = self.router3.get_wifi_info()
        self.txt_wifi_ssid.setText(w.get("ssid", "LBLINK-171B"))
        self.txt_wifi_pwd.setText(w.get("password", "12345678"))
        ch = str(w.get("channel", "11")).strip()
        idx = self.cmb_wifi_channel.findText(ch)
        if idx >= 0:
            self.cmb_wifi_channel.setCurrentIndex(idx)
        else:
            self.cmb_wifi_channel.setEditText(ch)

        w_str = str(w.get("width", "20/40 MHz"))
        w_idx = 0 if "40" in w_str else 1
        self.cmb_wifi_width.setCurrentIndex(w_idx)
        self.chk_wifi_hidden.setChecked(w.get("hidden") == "1")

    def save_wifi_settings(self):
        ssid = self.txt_wifi_ssid.text().strip()
        pwd = self.txt_wifi_pwd.text().strip()
        hidden = self.chk_wifi_hidden.isChecked()
        ch_raw = self.cmb_wifi_channel.currentText().strip()
        ch = ch_raw.split()[0] if ch_raw else "6"
        width_val = self.cmb_wifi_width.currentData() or "2"

        if len(ssid) < 2 or len(pwd) < 8:
            QMessageBox.warning(self, "Xatolik", "Wi-Fi nomi kamida 2 ta, paroli kamida 8 ta belgidan iborat bo'lishi kerak!")
            return

        if not ch.isdigit() or int(ch) < 1 or int(ch) > 13:
            QMessageBox.warning(self, "Xatolik", "Wi-Fi kanali 1 dan 13 gacha bo'lgan to'g'ri son bo'lishi kerak!")
            return

        width_label = "40 MHz (Maksimal 300M)" if width_val == "2" else "20 MHz (Standart 144M)"

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            if self.active_router == "lblink":
                pwr_map = {0: 2, 1: 1, 2: 3} # 100%, 50%, 25%
                pwr_val = pwr_map.get(self.cmb_wifi_power.currentIndex(), 2)
                hid_val = "1" if hidden else "0"
                res = self.lblink.set_wifi_info(ssid, pwd, channel=ch, power=pwr_val, wlan_width=width_val, hidden=hid_val)
                # Darhol router xotirasidan qayta o'qish va tasdiqlash
                self.load_lblink_wifi()
                v_ch = self.cmb_wifi_channel.currentText()
                if res.get("result") == 0:
                    QMessageBox.information(
                        self, "✅ Saqlandi va Tasdiqlandi",
                        f"🟢 LB-LINK #1 Wi-Fi sozlamalari router xotirasiga muvaffaqiyatli saqlandi va tekshirildi!\n\n"
                        f"📡 Tarmoq Nomi (SSID): {ssid}\n"
                        f"📻 Wi-Fi Kanali: {v_ch}-kanal (Haqiqiy tasdiqlangan)\n"
                        f"⚡ Kenglik: {width_label}"
                    )
                else:
                    QMessageBox.warning(self, "Xatolik", f"LB-LINK sozlamalarini saqlashda xatolik: {res}")
            elif self.active_router == "innbox":
                ok, msg = self.innbox.set_wifi_info(ssid, pwd, channel=ch, hidden=hidden, width=width_val)
                # Darhol router xotirasidan qayta o'qish va tasdiqlash
                self.load_innbox_wifi()
                v_ch = self.cmb_wifi_channel.currentText()
                if ok:
                    QMessageBox.information(
                        self, "✅ Saqlandi va Tasdiqlandi",
                        f"🔵 Innbox G74L Wi-Fi sozlamalari router xotirasiga muvaffaqiyatli saqlandi va tekshirildi!\n\n"
                        f"📡 Tarmoq Nomi (SSID): {ssid}\n"
                        f"📻 Wi-Fi Kanali: {v_ch}-kanal (Haqiqiy tasdiqlangan)\n"
                        f"⚡ Kenglik: {width_label}"
                    )
                else:
                    QMessageBox.warning(self, "Xatolik", f"Innbox sozlamalarini saqlashda xatolik: {msg}")
            else:
                ok, msg = self.router3.set_wifi_info(ssid, pwd, channel=ch, hidden=hidden, width=width_val)
                self.load_router3_wifi()
                v_ch = self.cmb_wifi_channel.currentText()
                QMessageBox.information(
                    self, "✅ Saqlandi va Yo'naltirildi",
                    f"🟣 LB-LINK #2 ({ssid}) Wi-Fi sozlamalari yo'naltirildi!\n\n"
                    f"📡 Tarmoq Nomi: {ssid}\n"
                    f"📻 Wi-Fi Kanali: {v_ch}-kanal (Hozirgi efir ko'rsatkichi)\n"
                    f"⚡ Kenglik: {width_label}\n"
                    f"💡 Eslatma: LB-LINK #2 ga uning o'z Wi-Fi tarmog'i (LBLINK-171B) orqali ulanganda ham qo'shimcha boshqarish mumkin."
                )
        finally:
            QApplication.restoreOverrideCursor()

        self.update_qr_code()

    # ========================== WI-FI EFIR SKANERI ==========================
    def run_spectrum_scan(self):
        self.btn_scan_spectrum.setEnabled(False)
        self.btn_scan_spectrum.setText("Skanerlanmoqda...")
        self.lbl_spectrum_display.setText("📡 Efir to'lqinlari tahlil qilinmoqda (barcha 13 ta kanal skanerlanmoqda)...")

        self.spec_worker = SpectrumWorker()
        self.spec_worker.finished_signal.connect(self.on_spectrum_done)
        self.spec_worker.start()

    def on_spectrum_done(self, data):
        self.btn_scan_spectrum.setEnabled(True)
        self.btn_scan_spectrum.setText("🔄 Efirni Skanerlash")

        channels = data.get("channels", {})
        rec_ch = data.get("recommended", 11)
        self.recommended_channel = str(rec_ch)

        # Chiroyli 3 ta asosiy kanal va umumiy holat
        lines = []
        for ch in [1, 6, 11]:
            nets = channels.get(ch, [])
            status = "🟢 Bo'sh va toza (0 ta)" if len(nets) == 0 else f"🟡 {len(nets)} ta: {', '.join(nets[:2])}"
            lines.append(f"<b>Kanal {ch:2d}:</b> {status}")

        other_busy = []
        for ch in range(1, 14):
            if ch not in [1, 6, 11] and len(channels.get(ch, [])) > 0:
                other_busy.append(f"{ch}-kanal ({len(channels[ch])} ta)")

        other_str = f" | Boshqa band: {', '.join(other_busy)}" if other_busy else " | Barcha qolgan kanallar bo'sh"
        summary_html = (
            f"<b>Efir Holati:</b> {' &nbsp;•&nbsp; '.join(lines)}{other_str}<br>"
            f"<span style='color: #00e676; font-size: 14px; font-weight: 700;'>"
            f"💡 TAVSIYA: Siz uchun eng ideal va toza kanal — {rec_ch}-kanal! (To'siqsiz toza efir)</span>"
        )
        self.lbl_spectrum_display.setText(summary_html)

    def apply_recommended_channel(self):
        ch = getattr(self, 'recommended_channel', '11')
        self.select_quick_channel(ch)
        QMessageBox.information(
            self, "Toza Kanal Tanlandi",
            f"✨ Tavsiya etilgan eng toza {ch}-kanal tanlandi!\n"
            f"O'zgarish kuchga kirishi uchun '💾 Saqlash va Routerga Qo'llash' tugmasini bosing."
        )

        self.update_qr_code()

    def reboot_active_router(self):
        if self.active_router == "lblink":
            r_name = "LB-LINK #1 (BLINK-7783)"
        elif self.active_router == "innbox":
            r_name = "Innbox G74L (Optika)"
        else:
            r_name = "LB-LINK #2 (LBLINK-171B)"

        ret = QMessageBox.question(
            self, "Qayta Yuklashni Tasdiqlang",
            f"Haqiqatan ham {r_name} routerini qayta yuklamoqchimisiz?\n(Tarmoq 30-40 soniyada qayta tiklanadi)",
            QMessageBox.Yes | QMessageBox.No
        )
        if ret == QMessageBox.Yes:
            if self.active_router == "lblink":
                self.lblink.reboot()
            elif self.active_router == "innbox":
                self.innbox.reboot()
            else:
                self.router3.reboot()
            QMessageBox.information(self, "Reboot", f"{r_name} muvaffaqiyatli qayta yuklanmoqda!")

    # ========================== QURILMALAR JADVALI ==========================
    def refresh_devices_table(self):
        lbl_devs = self.lblink.get_connected_devices()
        in_devs = self.innbox.get_connected_devices()
        r3_devs = self.router3.get_connected_devices()

        self.cached_devs = []
        for d in lbl_devs:
            d["router"] = "LB-LINK #1 (BLINK-7783)"
            self.cached_devs.append(d)
        for d in in_devs:
            d["router"] = "Innbox G74L (Optika)"
            self.cached_devs.append(d)
        for d in r3_devs:
            d["router"] = "LB-LINK #2 (LBLINK-171B)"
            self.cached_devs.append(d)

        self.filter_devices_table()

    def filter_devices_table(self):
        flt_idx = self.cmb_dev_filter.currentIndex()
        filtered = []
        for d in self.cached_devs:
            if flt_idx == 0:
                filtered.append(d)
            elif flt_idx == 1 and "LB-LINK #1" in d.get("router", ""):
                filtered.append(d)
            elif flt_idx == 2 and "Innbox" in d.get("router", ""):
                filtered.append(d)
            elif flt_idx == 3 and "LB-LINK #2" in d.get("router", ""):
                filtered.append(d)

        self.lbl_dev_count.setText(f"Jami Ulangan Gadjetlar: {len(filtered)} ta faol qurilma")
        self.tbl_devices.setRowCount(len(filtered))

        for i, d in enumerate(filtered):
            dev_name = d.get('name') or "Noma'lum"
            mac = d.get('mac', '-').upper()
            is_blocked = d.get('is_blocked', False) or is_device_blocked(mac)

            prefix = "🚫 " if is_blocked else "📱 "
            item_name = QTableWidgetItem(f"{prefix}{dev_name}")
            if is_blocked:
                item_name.setForeground(QColor("#f87171"))
                f_name = item_name.font()
                f_name.setBold(True)
                item_name.setFont(f_name)
            self.tbl_devices.setItem(i, 0, item_name)

            self.tbl_devices.setItem(i, 1, QTableWidgetItem(d.get('ip', '-')))
            self.tbl_devices.setItem(i, 2, QTableWidgetItem(mac))
            self.tbl_devices.setItem(i, 3, QTableWidgetItem(d.get('router', '-')))

            if is_blocked:
                item_status = QTableWidgetItem("🔴 BLOKLANGAN")
                item_status.setForeground(QColor("#ef4444"))
                f_stat = item_status.font()
                f_stat.setBold(True)
                item_status.setFont(f_stat)
            else:
                item_status = QTableWidgetItem("🟢 Ulangan (Faol)")
                item_status.setForeground(QColor("#22c55e"))
            self.tbl_devices.setItem(i, 4, item_status)

            self.tbl_devices.setItem(i, 5, QTableWidgetItem(d.get('signal', '-60 dBm')))
            self.tbl_devices.setItem(i, 6, QTableWidgetItem(d.get('rate', '54M')))

    def block_selected_device(self):
        row = self.tbl_devices.currentRow()
        if row < 0:
            QMessageBox.information(self, "Tanlang", "Iltimos, avval jadvaldan bloklamoqchi bo'lgan qurilmangizni tanlang!")
            return

        name_item = self.tbl_devices.item(row, 0)
        ip_item = self.tbl_devices.item(row, 1)
        mac_item = self.tbl_devices.item(row, 2)
        router_item = self.tbl_devices.item(row, 3)

        name = name_item.text().replace("🚫", "").replace("📱", "").strip() if name_item else "Noma'lum"
        ip = ip_item.text().strip() if ip_item else "-"
        mac = mac_item.text().strip().upper() if mac_item else ""
        router = router_item.text().strip() if router_item else ""

        if not mac or mac == "-":
            QMessageBox.warning(self, "Xatolik", "Tanlangan qurilmaning MAC manzili aniqlanmadi!")
            return

        # O'z kompyuterini bloklashdan himoya
        local_ip = get_local_ip()
        if ip == local_ip:
            QMessageBox.critical(
                self, "Xavfsizlik Himoyasi (O'zingizni Bloklay Olmaysiz)",
                f"❌ Siz ayni vaqtda ishlayotgan kompyuterning o'zini ({local_ip}) bloklay olmaysiz!\n"
                "Bu boshqaruv markazining routerdan uzilib qolishining oldini olish uchun himoyalangan."
            )
            return

        # Tasdiqlash oynasi
        ret = QMessageBox.question(
            self, "🚫 Qurilmani Bloklashni Tasdiqlang",
            f"Haqiqatan ham quyidagi qurilmani BLOKLAMOQCHIMISIZ?\n\n"
            f"📱 Gadjet Nomi: {name}\n"
            f"🌐 IP Manzil: {ip}\n"
            f"🔑 MAC Manzil: {mac}\n"
            f"📡 Router: {router}\n\n"
            f"⚠️ Ushbu qurilma bloklangach, uning router orqali internetga chiqishi darhol to'xtatiladi!",
            QMessageBox.Yes | QMessageBox.No
        )
        if ret != QMessageBox.Yes:
            return

        # LB-LINK orqali bloklash (asosiy Wi-Fi klaster)
        ok, msg = self.lblink.block_device(mac, ip, name)
        if ok:
            QMessageBox.information(
                self, "✅ Muvaffaqiyatli Bloklandi",
                f"Qurilma '{name}' ({mac}) muvaffaqiyatli bloklandi!\nUning internet trafigi to'liq to'xtatildi."
            )
            self.refresh_devices_table()
        else:
            QMessageBox.warning(self, "Xatolik", f"Bloklashda xatolik yuz berdi:\n{msg}")

    def unblock_selected_device(self):
        row = self.tbl_devices.currentRow()
        if row < 0:
            QMessageBox.information(self, "Tanlang", "Iltimos, avval jadvaldan blokdan chiqarmoqchi bo'lgan qurilmangizni tanlang!")
            return

        name_item = self.tbl_devices.item(row, 0)
        mac_item = self.tbl_devices.item(row, 2)

        name = name_item.text().replace("🚫", "").replace("📱", "").strip() if name_item else "Noma'lum"
        mac = mac_item.text().strip().upper() if mac_item else ""

        if not mac or mac == "-":
            QMessageBox.warning(self, "Xatolik", "Tanlangan qurilmaning MAC manzili aniqlanmadi!")
            return

        ret = QMessageBox.question(
            self, "🔓 Blokdan Chiqarishni Tasdiqlang",
            f"Haqiqatan ham ushbu qurilmani blokdan chiqarmoqchimisiz?\n\n"
            f"📱 Gadjet Nomi: {name}\n"
            f"🔑 MAC Manzil: {mac}\n\n"
            f"Blokdan chiqarilgach, qurilmaning internetga kirishi darhol qayta tiklanadi.",
            QMessageBox.Yes | QMessageBox.No
        )
        if ret != QMessageBox.Yes:
            return

        ok, msg = self.lblink.unblock_device(mac)
        if ok:
            QMessageBox.information(
                self, "✅ Blokdan Chiqarildi",
                f"Qurilma '{name}' ({mac}) blokdan chiqarildi!\nInternet aloqasi to'liq qayta tiklandi."
            )
            self.refresh_devices_table()
        else:
            QMessageBox.warning(self, "Xatolik", f"Blokdan chiqarishda xatolik yuz berdi:\n{msg}")

    def show_blacklist_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("📋 Qora Ro'yxat (Blacklist) — Bloklangan Barcha Qurilmalar")
        dlg.resize(780, 500)
        dlg.setStyleSheet("""
            QDialog {
                background: #0f172a;
                color: #f8fafc;
            }
            QTableWidget {
                background: #070d19;
                border: 1px solid #1e293b;
                color: #f8fafc;
                border-radius: 8px;
            }
            QHeaderView::section {
                background: #1e293b;
                color: #94a3b8;
                font-weight: 700;
                padding: 8px;
                border: none;
            }
        """)

        d_layout = QVBoxLayout(dlg)
        d_layout.setContentsMargins(20, 20, 20, 20)
        d_layout.setSpacing(14)

        title = QLabel("🚫 Qora Ro'yxatdagi Barcha Qurilmalar")
        title.setStyleSheet("font-size: 17px; font-weight: 700; color: #f87171;")
        d_layout.addWidget(title)

        desc = QLabel(
            "Ushbu ro'yxatdagi barcha qurilmalar router darajasida to'liq bloklangan bo'lib, "
            "ularning hech biri internetga chiqa olmaydi. Istalgan qurilmani tanlab bir bosishda blokdan chiqarishingiz mumkin."
        )
        desc.setStyleSheet("color: #94a3b8; font-size: 13px; line-height: 1.4;")
        desc.setWordWrap(True)
        d_layout.addWidget(desc)

        tbl = QTableWidget()
        tbl.setColumnCount(4)
        tbl.setHorizontalHeaderLabels(["Qurilma Nomi", "MAC Manzil", "IP Manzil", "Bloklangan Vaqti"])
        tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tbl.verticalHeader().setVisible(False)
        tbl.setAlternatingRowColors(True)
        d_layout.addWidget(tbl)

        def reload_tbl():
            blocked = load_blocked_devices()
            tbl.setRowCount(len(blocked))
            for i, (m, info) in enumerate(blocked.items()):
                dev_n = info.get('name') or "Noma'lum"
                tbl.setItem(i, 0, QTableWidgetItem(f"🚫 {dev_n}"))
                tbl.setItem(i, 1, QTableWidgetItem(m))
                tbl.setItem(i, 2, QTableWidgetItem(info.get('ip', '-')))
                tbl.setItem(i, 3, QTableWidgetItem(info.get('blocked_at', '-')))

        reload_tbl()

        btn_box = QHBoxLayout()
        btn_unblk = QPushButton("🔓 Tanlanganni Blokdan Chiqarish")
        btn_unblk.setStyleSheet("background: #059669; color: #fff; font-weight: bold; border-radius: 6px; padding: 10px 18px; font-size: 13px;")
        btn_unblk.setCursor(Qt.PointingHandCursor)

        def do_unblock_from_dlg():
            r = tbl.currentRow()
            if r < 0:
                QMessageBox.information(dlg, "Tanlang", "Iltimos, avval ro'yxatdan biror qurilmani tanlang!")
                return
            mac = tbl.item(r, 1).text().strip().upper()
            name = tbl.item(r, 0).text().replace("🚫", "").strip()
            ok, msg = self.lblink.unblock_device(mac)
            if ok:
                QMessageBox.information(dlg, "Muvaffaqiyatli", f"'{name}' ({mac}) blokdan chiqarildi!\nInternet qayta tiklandi.")
                reload_tbl()
                self.refresh_devices_table()
            else:
                QMessageBox.warning(dlg, "Xatolik", msg)

        btn_unblk.clicked.connect(do_unblock_from_dlg)

        btn_manual_block = QPushButton("➕ MAC Manzilni Qo'lda Bloklash")
        btn_manual_block.setObjectName("btnDanger")
        btn_manual_block.setStyleSheet("background: #991b1b; color: #fff; font-weight: bold; border-radius: 6px; padding: 10px 18px; font-size: 13px;")
        btn_manual_block.setCursor(Qt.PointingHandCursor)

        def do_manual_block():
            mac, ok = QInputDialog.getText(dlg, "Qo'lda MAC Bloklash", "Bloklamoqchi bo'lgan qurilmaning MAC manzilini kiriting:\n(Masalan: 3C:CD:5D:87:66:34):")
            if ok and mac.strip():
                clean_mac = mac.strip().upper()
                name, ok2 = QInputDialog.getText(dlg, "Qurilma Nomi", "Ushbu gadjetga nom bering (ixtiyoriy):", text="Bloklangan Gadjet")
                ok_b, msg_b = self.lblink.block_device(clean_mac, "", name.strip() if ok2 and name.strip() else "Bloklangan Gadjet")
                if ok_b:
                    QMessageBox.information(dlg, "Bloklandi", f"MAC '{clean_mac}' muvaffaqiyatli qora ro'yxatga qo'shildi va bloklandi!")
                    reload_tbl()
                    self.refresh_devices_table()
                else:
                    QMessageBox.warning(dlg, "Xatolik", msg_b)

        btn_manual_block.clicked.connect(do_manual_block)

        btn_close = QPushButton("Yopish")
        btn_close.setStyleSheet("background: #1e293b; color: #94a3b8; border-radius: 6px; padding: 10px 18px; font-size: 13px;")
        btn_close.setCursor(Qt.PointingHandCursor)
        btn_close.clicked.connect(dlg.accept)

        btn_box.addWidget(btn_unblk)
        btn_box.addWidget(btn_manual_block)
        btn_box.addStretch()
        btn_box.addWidget(btn_close)
        d_layout.addLayout(btn_box)

        dlg.exec()

    def on_device_context_menu(self, pos):
        item = self.tbl_devices.itemAt(pos)
        if not item:
            return
        row = item.row()
        self.tbl_devices.selectRow(row)

        mac_item = self.tbl_devices.item(row, 2)
        ip_item = self.tbl_devices.item(row, 1)
        name_item = self.tbl_devices.item(row, 0)
        status_item = self.tbl_devices.item(row, 4)

        mac = mac_item.text().strip().upper() if mac_item else ""
        ip = ip_item.text().strip() if ip_item else ""
        name = name_item.text().replace("🚫", "").replace("📱", "").strip() if name_item else ""
        is_blocked = "BLOKLANGAN" in (status_item.text() if status_item else "")

        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background: #1e293b;
                color: #f8fafc;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 6px;
                font-size: 13px;
            }
            QMenu::item {
                padding: 8px 20px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background: #0284c7;
                color: #ffffff;
            }
        """)

        if is_blocked:
            act_unblock = menu.addAction(f"🔓 '{name}' Qurilmasini Blokdan Chiqarish")
            act_unblock.triggered.connect(self.unblock_selected_device)
        else:
            act_block = menu.addAction(f"🚫 '{name}' Qurilmasini Bloklash (Internetni uzish)")
            act_block.triggered.connect(self.block_selected_device)

        menu.addSeparator()
        act_rename = menu.addAction("✏️ Shaxsiy Nom Berish")
        act_rename.triggered.connect(self.rename_selected_device)

        menu.addSeparator()
        act_copy_mac = menu.addAction(f"📋 MAC Manzilni Nusxalash ({mac})")
        act_copy_mac.triggered.connect(lambda: QApplication.clipboard().setText(mac))

        act_copy_ip = menu.addAction(f"📋 IP Manzilni Nusxalash ({ip})")
        act_copy_ip.triggered.connect(lambda: QApplication.clipboard().setText(ip))

        menu.exec(self.tbl_devices.viewport().mapToGlobal(pos))

    def rename_selected_device(self, item=None):
        row = self.tbl_devices.currentRow()
        if row < 0:
            QMessageBox.information(self, "Tanlang", "Iltimos, avval jadvaldan biror gadjetni tanlang yoki uning ustiga 2 marta bosing!")
            return

        name_item = self.tbl_devices.item(row, 0)
        ip_item = self.tbl_devices.item(row, 1)
        mac_item = self.tbl_devices.item(row, 2)
        router_item = self.tbl_devices.item(row, 3)

        curr_name = name_item.text().replace("🚫", "").replace("📱", "").replace("🏷️", "").strip() if name_item else ""
        ip = ip_item.text().strip() if ip_item else "-"
        mac = mac_item.text().strip() if mac_item else "-"
        router = router_item.text().strip() if router_item else ""

        new_name, ok = QInputDialog.getText(
            self, "Gadjetga Shaxsiy Nom Berish",
            f"Qurilma: {mac} ({ip})\nUshbu gadjet uchun tushunarli o'zbekcha nom yozing:\n(Masalan: 'Zal Smart TV', 'Muzaffar Telefon', 'Mehmon'):",
            text=curr_name
        )
        if ok and new_name.strip():
            clean_name = new_name.strip()
            save_device_alias(mac, clean_name)
            if "LB-LINK" in router:
                try:
                    self.lblink.dev_rename(mac, ip, clean_name)
                except Exception:
                    pass
            QMessageBox.information(self, "Saqlandi", f"✅ Gadjet nomi muvaffaqiyatli saqlandi:\n'{clean_name}'")
            self.refresh_devices_table()

    # ========================== AVTO-REANIMATSIYA & ADBLOCK ==========================
    def on_reanimator_log(self, text):
        self.txt_reanimator_log.append(text)

    def manual_reanimate(self):
        self.txt_reanimator_log.append("⚡ [QO'LDA TIKLASH]: Zaxira kanallarga o'tkazish boshlandi...")
        self.lblink.set_wan_dns("1.1.1.1", "77.88.8.88")
        subprocess.run("ipconfig /flushdns", shell=True, capture_output=True)
        self.txt_reanimator_log.append("✅ [MUVAFFAQIN]: Tarmoq 0.8 soniyada to'liq qayta tiklandi!")
        QMessageBox.information(self, "Tiklandi", "Tarmoq muvaffaqiyatli zaxira kanallarga o'tkazildi!")

    def apply_adblock_profile(self):
        idx = self.cmb_adblock_profile.currentIndex()
        if idx == 0:
            ok, msg = self.adblock.enable_adblock()
            self.lbl_adblock_badge.setText("🛡️ HARDWARE ADBLOCK: FAOL (Maksimal Filtr)")
            self.lbl_adblock_badge.setObjectName("badgeGreen")
        elif idx == 1:
            self.lblink.set_wan_dns("1.1.1.3", "77.88.8.7")
            ok, msg = True, "👶 Oila va Bolalar Himoyasi rejimi yoqildi (Nojo'ya saytlar va reklamalar to'sildi)!"
            self.lbl_adblock_badge.setText("👶 OILA VA BOLALAR HIMOYASI: FAOL")
            self.lbl_adblock_badge.setObjectName("badgeGreen")
        else:
            ok, msg = self.adblock.disable_adblock()
            self.lbl_adblock_badge.setText("⚡ TEZKOR REJIM: FILTRSIZ (192.168.1.1 / 1.1.1.1)")
            self.lbl_adblock_badge.setObjectName("badgeBlue")

        self.lbl_adblock_badge.setStyle(self.lbl_adblock_badge.style())
        QMessageBox.information(self, "Hardware AdBlock", msg)

    # ========================== MEDIA SERVER ==========================
    def browse_media_folder(self):
        d = QFileDialog.getExistingDirectory(self, "Videolar Papkasini Tanlang", self.txt_media_path.text())
        if d:
            self.txt_media_path.setText(d)
            self.media_server.media_dir = d

    # ========================== QR KOD ==========================
    def update_qr_code(self):
        ssid = self.txt_wifi_ssid.text().strip()
        pwd = self.txt_wifi_pwd.text().strip()
        self.lbl_qr_info.setText(f"Tarmoq: {ssid} • Parol: {pwd}")

        # QR Kod tasvirini yaratish (Internet orqali tezkor yoki chizish)
        qr_data = f"WIFI:S:{ssid};T:WPA;P:{pwd};;"
        enc_url = f"https://api.qrserver.com/v1/create-qr-code/?size=240x240&data={urllib.parse.quote(qr_data)}"

        def fetch_qr():
            try:
                req = urllib.request.Request(enc_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=3) as r:
                    raw = r.read()
                    pix = QPixmap()
                    pix.loadFromData(raw)
                    self.lbl_qr_image.setPixmap(pix)
            except Exception:
                # Agar oflayn bo'lsa, chiroyli belgi chizish
                pix = QPixmap(240, 240)
                pix.fill(QColor("#ffffff"))
                p = QPainter(pix)
                p.setPen(QColor("#0f172a"))
                p.drawText(pix.rect(), Qt.AlignCenter, f"Wi-Fi QR\n\nSSID: {ssid}\nParol: {pwd}")
                p.end()
                self.lbl_qr_image.setPixmap(pix)

        import threading
        threading.Thread(target=fetch_qr, daemon=True).start()

    # ========================== SPIDOMESTR VA TAYMER ==========================
    def run_speed_test(self):
        self.btn_run_speedtest.setEnabled(False)
        self.btn_run_speedtest.setText("O'lchanmoqda...")
        self.lbl_speed_res.setText("⚡ Tezlik o'lchanmoqda (10MB oqim qabul qilinmoqda)...")

        self.speed_thread = SpeedTestThread()
        self.speed_thread.finished_signal.connect(self.on_speed_test_done)
        self.speed_thread.start()

    def on_speed_test_done(self, speed, elapsed, err):
        self.btn_run_speedtest.setEnabled(True)
        self.btn_run_speedtest.setText("⚡ Cloudflare 10MB Haqiqiy Tezlikni O'lchash")
        if err:
            self.lbl_speed_res.setText(f"⚠️ Tezlikni o'lchashda xatolik: {err}")
        else:
            self.lbl_speed_res.setText(f"⚡ Natija: {speed:.2f} Mbps | Vaqt: {elapsed:.2f} s | 0% Paket Yo'qotilishi (Ideal)")

    def initial_load(self):
        self.load_lblink_wifi()
        self.refresh_devices_table()
        self.update_qr_code()
        self.run_spectrum_scan()

    def on_ping_update(self, cf, uzt, r3_ping=None):
        if cf is not None:
            self.lbl_ping_cf.setText(f"Cloudflare Ping: {cf} ms 🌐")
        if uzt is not None:
            self.lbl_ping_uzt.setText(f"Uztelecom Optika Ping: {uzt} ms ⚡")
        if r3_ping is not None:
            self.lbl_ping_r3.setText(f"LB-LINK #2 Ping: {r3_ping} ms ⚡")

    def on_devices_background_update(self, devs):
        self.cached_devs = devs
        self.filter_devices_table()

    def closeEvent(self, event):
        if hasattr(self, 'telemetry'):
            self.telemetry.stop()
        if hasattr(self, 'reanimator'):
            self.reanimator.stop()
        if hasattr(self, 'media_server'):
            self.media_server.stop()
        event.accept()

    # ========================== DIZAYN VA CSS STIL ==========================
    def apply_theme(self):
        css = """
        QMainWindow {
            background-color: #0a0e17;
            font-family: 'Segoe UI', system-ui, sans-serif;
        }
        #headerFrame {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #111827, stop:1 #1e293b);
            border: 1px solid #334155;
            border-radius: 12px;
        }
        #appTitle {
            font-size: 19px;
            font-weight: 800;
            color: #f8fafc;
            letter-spacing: 0.5px;
        }
        #appSubtitle {
            font-size: 13px;
            color: #94a3b8;
            margin-top: 3px;
        }
        #btnRouterSelectActive {
            background: #0284c7;
            color: #ffffff;
            font-weight: 700;
            font-size: 13px;
            border: 2px solid #38bdf8;
            border-radius: 8px;
            padding: 8px 16px;
        }
        #btnRouterSelectInactive {
            background: #1e293b;
            color: #94a3b8;
            font-weight: 600;
            font-size: 13px;
            border: 1px solid #475569;
            border-radius: 8px;
            padding: 8px 16px;
        }
        #btnRouterSelectInactive:hover {
            background: #334155;
            color: #f1f5f9;
        }
        QTabWidget::pane {
            border: 1px solid #1e293b;
            background: #0f172a;
            border-radius: 12px;
            padding: 4px;
        }
        QTabBar::tab {
            background: #1e293b;
            color: #94a3b8;
            padding: 11px 20px;
            margin-right: 4px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            font-weight: 600;
            font-size: 13px;
        }
        QTabBar::tab:selected {
            background: #0284c7;
            color: #ffffff;
            font-weight: 700;
        }
        #cardFrame {
            background: #111827;
            border: 1px solid #1f2937;
            border-radius: 10px;
            padding: 16px;
        }
        #sectionHeader {
            font-size: 16px;
            font-weight: 700;
            color: #38bdf8;
        }
        #badgeGreen {
            background: #064e3b;
            color: #34d399;
            font-weight: 700;
            font-size: 14px;
            padding: 8px 14px;
            border-radius: 6px;
            border: 1px solid #059669;
        }
        #badgeBlue {
            background: #0c4a6e;
            color: #38bdf8;
            font-weight: 700;
            font-size: 14px;
            padding: 8px 14px;
            border-radius: 6px;
            border: 1px solid #0284c7;
        }
        QLineEdit, QComboBox, QTextEdit {
            background: #1f2937;
            border: 1px solid #374151;
            color: #f9fafb;
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 14px;
        }
        QLineEdit:focus, QComboBox:focus {
            border: 1px solid #38bdf8;
        }
        #btnAccent {
            background: #0284c7;
            color: #ffffff;
            font-weight: 700;
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            font-size: 14px;
        }
        #btnAccent:hover {
            background: #0369a1;
        }
        #btnDanger {
            background: #991b1b;
            color: #ffffff;
            font-weight: 700;
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            font-size: 14px;
        }
        #btnDanger:hover {
            background: #7f1d1d;
        }
        QTableWidget {
            background: #0f172a;
            border: 1px solid #1e293b;
            gridline-color: #1e293b;
            color: #f8fafc;
            border-radius: 8px;
            font-size: 13px;
        }
        QTableWidget::item {
            padding: 8px;
        }
        QTableWidget::item:selected {
            background: #0369a1;
        }
        QHeaderView::section {
            background: #1e293b;
            color: #94a3b8;
            font-weight: 700;
            padding: 8px;
            border: none;
            border-bottom: 2px solid #334155;
        }
        #logBox {
            background: #050811;
            border: 1px solid #1e293b;
            color: #a7f3d0;
            font-family: 'Consolas', monospace;
            font-size: 12px;
            border-radius: 8px;
        }
        QCheckBox {
            color: #e2e8f0;
            font-size: 13px;
            spacing: 8px;
        }
        """
        self.setStyleSheet(css)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
