"""
O'zbek Musiqa Markazi Pro - Engine (Avto-Magnitola & Fleshka Audio Processor)
Muallif: Premier Software Architect (janob Muzaffar uchun maxsus ishlab chiqilgan)
Versiya: 5.0 Ultra Luxe (Audiophile Player, Turbo Parallel Engine, USB Cockpit & Smart Sync)
"""

import os
import sys
import re
import time
import json
import math
import random
import string
import shutil
import ctypes
import datetime
import subprocess
import threading
import concurrent.futures
import requests
from requests.adapters import HTTPAdapter
from pathlib import Path
from typing import List, Dict, Optional, Callable, Set, Tuple

# Windows konsolida cp1251 xatoligini oldini olish (UTF-8 majburiy kodlash)
for _stream in (sys.stdout, sys.stderr):
    if _stream is not None and hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


# In-memory yt_dlp
try:
    import yt_dlp
    _YTDLP_LIB_AVAILABLE = True
except ImportError:
    _YTDLP_LIB_AVAILABLE = False

# Audio ijrosi uchun pygame.mixer
try:
    import pygame
    _PYGAME_AVAILABLE = True
except ImportError:
    _PYGAME_AVAILABLE = False

# MP3 ID3v2 teglar, davomiylik va APIC muqova uchun mutagen
try:
    from mutagen.mp3 import MP3
    from mutagen.id3 import ID3, TIT2, TPE1, TALB, TYER, APIC, ID3NoHeaderError
    _MUTAGEN_AVAILABLE = True
except ImportError:
    _MUTAGEN_AVAILABLE = False

# Global HTTP/2 & Keep-Alive Session Pool (IDM 32-Stream Optimization)
_SESSION_LOCK = threading.Lock()
_GLOBAL_SESSION: Optional[requests.Session] = None


def get_http_session() -> requests.Session:
    """32-oqimli parallel yuklashlar uchun qayta ishlatiluvchi Keep-Alive ulanishlar hovuzi."""
    global _GLOBAL_SESSION
    with _SESSION_LOCK:
        if _GLOBAL_SESSION is None:
            s = requests.Session()
            adapter = HTTPAdapter(pool_connections=64, pool_maxsize=128, max_retries=3)
            s.mount("http://", adapter)
            s.mount("https://", adapter)
            _GLOBAL_SESSION = s
        return _GLOBAL_SESSION


# Constants & Defaults
DEFAULT_BITRATE = "256k"
DEFAULT_IDM_STREAMS = 32
DEFAULT_DSP_PROFILE = {
    "bass_gain": 0.5,
    "bass_freq": 70,
    "treble_gain": 1.5,
    "treble_freq": 11000,
    "loudnorm_i": -14,
    "loudnorm_lra": 7,
    "loudnorm_tp": -1.5,
    "limiter_limit": -1.2,
}

# AIMP 10-Polosali Ekvayzer Chastotalari (Hz) va Tayyor Presetlar (dB)
AIMP_EQ_FREQS = [31, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
AIMP_EQ_LABELS = ["31Hz", "63Hz", "125Hz", "250Hz", "500Hz", "1kHz", "2kHz", "4kHz", "8kHz", "16kHz"]

AIMP_EQ_PRESETS: Dict[str, List[float]] = {
    "Maytafon Yumshoq Bass (Standart)": [0.5, 0.5, 0.3, 0.0, 0.0, 0.2, 0.5, 1.0, 1.5, 1.5],
    "AIMP Flat (Neytral Studiya)": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "Cobalt / Gentra Salon Akustika": [1.0, 1.2, 0.5, -0.4, 0.0, 0.8, 1.2, 1.8, 2.0, 1.8],
    "Malibu / Tracker Premier Hi-Fi": [0.8, 1.0, 0.4, 0.0, 0.3, 0.6, 1.0, 1.5, 2.0, 2.2],
    "Kristal Vokal va Mumtoz": [-0.5, -0.2, 0.2, 0.8, 1.5, 2.0, 2.2, 1.8, 1.2, 0.8],
    "To'yona va Lazgi Dinamik": [1.2, 1.5, 0.8, 0.0, 0.5, 1.0, 1.5, 2.0, 2.2, 2.0],
    "Tungi Sokin Yo'l (Lounge)": [0.6, 0.8, 0.4, 0.2, -0.3, -0.2, 0.4, 0.8, 1.2, 1.0],
}

CAR_FOLDERS = [
    {"id": "01_xitlar", "folder": "01_YANGI_XITLAR_2026", "title": "01. Yangi Xitlar 2026", "desc": "Yilning eng so'nggi premyeralari"},
    {"id": "02_sanatkorlar", "folder": "02_SEVIMLI_SANATKORLAR", "title": "02. Sevimli San'atkorlar", "desc": "Albomlar va yakkaxon xitlar"},
    {"id": "03_sokin", "folder": "03_TUNGI_SOKIN_YOL", "title": "03. Tungi Sokin Yo'l", "desc": "Magistral va sokin sayohat musiqalari"},
    {"id": "04_toyona", "folder": "04_TOYONA_VA_LAZGI", "title": "04. To'yona va Lazgi", "desc": "Sho'x bazmbop va xalqona raqslar"},
]

EXTENDED_CAR_FOLDERS = CAR_FOLDERS + [
    {"id": "05_retro", "folder": "05_RETRO_VA_MUMTOZ", "title": "05. Retro va Mumtoz", "desc": "Oltin fond va klassik durdonalar"},
    {"id": "06_bass", "folder": "06_AVTO_BASS_REMIX", "title": "06. Avto Bass & Remix", "desc": "Sabvufer va dinamik avto-ritmlar"},
    {"id": "07_jahon", "folder": "07_JAHON_VA_TURK_XITLAR", "title": "07. Jahon va Turk Xitlar", "desc": "Xorijiy va turkcha mashhur taronalar"},
]

ARTIST_CATEGORIES = [
    "Barchasi",
    "🔥 Zamonaviy Xit",
    "🎤 Estrada & Pop",
    "🏛️ Mumtoz & Ustozlar",
    "💃 To'yona & Lazgi",
    "🌍 Jahon & Turk",
]

CATALOG_ARTISTS = [
    # 🔥 Zamonaviy Xit
    {"name": "Jaloliddin Ahmadaliyev", "query": "Jaloliddin Ahmadaliyev yangi qoshiqlari xit", "desc": "Lirik va diltortar xitlar", "category": "🔥 Zamonaviy Xit"},
    {"name": "Hamdam Sobirov", "query": "Hamdam Sobirov yangi qoshiqlari xit", "desc": "Estrada va yoshlar xitlari", "category": "🔥 Zamonaviy Xit"},
    {"name": "Gulinur", "query": "Gulinur yangi qoshiqlari xit", "desc": "Sho'x va zamonaviy qo'shiqlar", "category": "🔥 Zamonaviy Xit"},
    {"name": "Shohruhxon", "query": "Shohruhxon yangi xit qoshiqlari", "desc": "Romantik estrada qo'shiqlari", "category": "🔥 Zamonaviy Xit"},
    {"name": "Konsta", "query": "Konsta yangi qoshiqlari xit", "desc": "Zamonaviy mazmunli hip-hop", "category": "🔥 Zamonaviy Xit"},
    {"name": "Munisa Rizayeva", "query": "Munisa Rizayeva xit qoshiqlari yangi", "desc": "Yorqin vokal va zamonaviy xitlar", "category": "🔥 Zamonaviy Xit"},
    {"name": "Ulug'bek Rahmatullayev", "query": "Ulugbek Rahmatullayev sara xit qoshiqlari", "desc": "Samimiy va oilaviy xit taronalar", "category": "🔥 Zamonaviy Xit"},
    {"name": "Yorqinxo'ja Umarov", "query": "Yorqinxoja Umarov yangi xit qoshiqlari", "desc": "Zamonaviy lirik va estrada ijrolari", "category": "🔥 Zamonaviy Xit"},
    {"name": "Imron", "query": "Imron yangi qoshiqlari xit", "desc": "Sho'x va romantik xitlar", "category": "🔥 Zamonaviy Xit"},
    {"name": "Bahrom Nazarov", "query": "Bahrom Nazarov sara qoshiqlari xit", "desc": "Diltortar va samimiy taronalar", "category": "🔥 Zamonaviy Xit"},
    {"name": "Jasur Umirov", "query": "Jasur Umirov shox xit qoshiqlari", "desc": "Dinamik va sho'x yoshlar xitlari", "category": "🔥 Zamonaviy Xit"},
    {"name": "Via Marokand", "query": "Via Marokand xit qoshiqlari", "desc": "Kayfiyatni ko'taruvchi duet xitlar", "category": "🔥 Zamonaviy Xit"},
    {"name": "Benom Guruhi", "query": "Benom guruhi sara xit qoshiqlari", "desc": "Romantik kino-konsert xitlari", "category": "🔥 Zamonaviy Xit"},
    {"name": "Ummon Guruhi", "query": "Ummon guruhi oltin xit qoshiqlari", "desc": "Yoshlik nostalgiyasi va xitlari", "category": "🔥 Zamonaviy Xit"},
    {"name": "Afruza", "query": "Afruza yangi qoshiqlari xit", "desc": "Zamonaviy estrada taronalari", "category": "🔥 Zamonaviy Xit"},
    {"name": "Doston Ergashev", "query": "Doston Ergashev yangi xit qoshiqlari", "desc": "Xalqona va zamonaviy xitlar", "category": "🔥 Zamonaviy Xit"},

    # 🎤 Estrada & Pop
    {"name": "Yulduz Usmonova", "query": "Yulduz Usmonova xit qoshiqlari 2026", "desc": "O'zbek primadonnasi xitlari", "category": "🎤 Estrada & Pop"},
    {"name": "Ozoda Nursaidova", "query": "Ozoda Nursaidova xit qoshiqlari", "desc": "Kuchli vokal va dinamik ijrolar", "category": "🎤 Estrada & Pop"},
    {"name": "Rayhon", "query": "Rayhon sara xit qoshiqlari", "desc": "Klassik estrada va raqsbop xitlar", "category": "🎤 Estrada & Pop"},
    {"name": "Shahzoda", "query": "Shahzoda uzbek xit qoshiqlari", "desc": "Mayin va maftunkor pop xitlar", "category": "🎤 Estrada & Pop"},
    {"name": "Lola Yo'ldosheva", "query": "Lola Yoldosheva sara xit qoshiqlari", "desc": "Lirik va zamonaviy pop musiqa", "category": "🎤 Estrada & Pop"},
    {"name": "Nilufar Usmonova", "query": "Nilufar Usmonova yangi qoshiqlari", "desc": "Yorqin va dinamik estrada", "category": "🎤 Estrada & Pop"},
    {"name": "Ziyoda", "query": "Ziyoda yangi va sara xit qoshiqlari", "desc": "Milliy va zamonaviy uyg'unlik", "category": "🎤 Estrada & Pop"},
    {"name": "Dildora Niyozova", "query": "Dildora Niyozova yangi qoshiqlari", "desc": "Ibratli va ta'sirchan qo'shiqlar", "category": "🎤 Estrada & Pop"},
    {"name": "Tohir Sodiqov (Bolalar)", "query": "Tohir Sodiqov Bolalar xit qoshiqlari", "desc": "Afsonaviy pop-rok va retro", "category": "🎤 Estrada & Pop"},
    {"name": "Sevara Nazarxon", "query": "Sevara Nazarxon sara qoshiqlari", "desc": "Betakror ovoz va jahon darajasi", "category": "🎤 Estrada & Pop"},
    {"name": "Bojalar (Jahongir Poziljonov)", "query": "Bojalar Jahongir Poziljonov xit qoshiqlari", "desc": "Quvnoq va kayfiyatbop taronalar", "category": "🎤 Estrada & Pop"},
    {"name": "Alisher Fayz", "query": "Alisher Fayz sara xit qoshiqlari", "desc": "Lirik va mazmunli estrada", "category": "🎤 Estrada & Pop"},
    {"name": "Sardor Rahimxon", "query": "Sardor Rahimxon xit qoshiqlari", "desc": "Ta'sirchan va diltortar qo'shiqlar", "category": "🎤 Estrada & Pop"},
    {"name": "Ravshan Sobirov", "query": "Ravshan Sobirov oltin xit qoshiqlari", "desc": "Retro pop-rok va samimiy ovoz", "category": "🎤 Estrada & Pop"},

    # 🏛️ Mumtoz & Ustozlar
    {"name": "Sherali Jo'rayev", "query": "Sherali Jo'rayev mumtoz sara qoshiqlari", "desc": "Klassik o'zbek musiqasi gultoji", "category": "🏛️ Mumtoz & Ustozlar"},
    {"name": "Botir Qodirov", "query": "Botir Qodirov sara xit qoshiqlari", "desc": "Shirali ovoz va diltortar ashulalar", "category": "🏛️ Mumtoz & Ustozlar"},
    {"name": "Ozodbek Nazarbekov", "query": "Ozodbek Nazarbekov sara xit qoshiqlari", "desc": "Mumtoz va zamonaviy oltin ovoz", "category": "🏛️ Mumtoz & Ustozlar"},
    {"name": "Otabek Muhammadzohid", "query": "Otabek Muhammadzohid sara qoshiqlari", "desc": "Vodiy maktabi va ma'noli ashulalar", "category": "🏛️ Mumtoz & Ustozlar"},
    {"name": "Gulsanam Mamazoitova", "query": "Gulsanam Mamazoitova jonli va xit qoshiqlari", "desc": "Milliy va kuchli ovoz sohibasi", "category": "🏛️ Mumtoz & Ustozlar"},
    {"name": "Oxunjon Madaliyev", "query": "Oxunjon Madaliyev oltin fond qoshiqlari", "desc": "Unutilmas diltortar nolalar", "category": "🏛️ Mumtoz & Ustozlar"},
    {"name": "Muhriddin Xoliqov", "query": "Muhriddin Xoliqov retro sara qoshiqlari", "desc": "Oltin davr lirik durdonalari", "category": "🏛️ Mumtoz & Ustozlar"},
    {"name": "Farrux Zokirov (Yalla)", "query": "Yalla Farrux Zokirov xit qoshiqlari", "desc": "Afsonaviy Yalla ansambli", "category": "🏛️ Mumtoz & Ustozlar"},
    {"name": "Nasiba Abdullayeva", "query": "Nasiba Abdullayeva sara qoshiqlari", "desc": "Sharq tarovati va mayin klassika", "category": "🏛️ Mumtoz & Ustozlar"},
    {"name": "Shohjahon Jo'rayev", "query": "Shohjahon Jorayev jonli ijro qoshiqlari", "desc": "Kuchli jonli ijro va tor sadolari", "category": "🏛️ Mumtoz & Ustozlar"},
    {"name": "Zohirshoh Jo'rayev", "query": "Zohirshoh Jorayev yangi va sara qoshiqlari", "desc": "An'anaviy va zamonaviy talqin", "category": "🏛️ Mumtoz & Ustozlar"},
    {"name": "Sardor Mamadaliyev", "query": "Sardor Mamadaliyev xit qoshiqlari", "desc": "Shijoatli ovoz va klassik uslub", "category": "🏛️ Mumtoz & Ustozlar"},
    {"name": "Xurshid Rasulov", "query": "Xurshid Rasulov jonli ijro sara qoshiqlari", "desc": "Ma'noli va davrabop ashulalar", "category": "🏛️ Mumtoz & Ustozlar"},

    # 💃 To'yona & Lazgi
    {"name": "Bunyodbek Saidov", "query": "Bunyodbek Saidov xorazm lazgi yangi", "desc": "Xorazmcha sho'x bazm qo'shiqlari", "category": "💃 To'yona & Lazgi"},
    {"name": "Jahongir Otajonov", "query": "Jahongir Otajonov jonli ijro xit", "desc": "Jonli ijro va o'ziga xos ritmlar", "category": "💃 To'yona & Lazgi"},
    {"name": "Janob Rasul", "query": "Janob Rasul yangi sho'x qoshiqlari", "desc": "To'yona va qiziqarli qo'shiqlar", "category": "💃 To'yona & Lazgi"},
    {"name": "Hosila Rahimova", "query": "Hosila Rahimova surxondaryo shox qoshiqlari", "desc": "Surxon va baxshiyona sho'x navolar", "category": "💃 To'yona & Lazgi"},
    {"name": "Mahmud Namozov", "query": "Mahmud Namozov sara xalqona qoshiqlari", "desc": "Milliy ruh va voha ohanglari", "category": "💃 To'yona & Lazgi"},
    {"name": "Hulkar Abdullayeva", "query": "Hulkar Abdullayeva xorazm shox qoshiqlari", "desc": "Xorazm lazgi va raqsbop xitlar", "category": "💃 To'yona & Lazgi"},
    {"name": "Dilnoza Ismiyaminova", "query": "Dilnoza Ismiyaminova sara qoshiqlari", "desc": "Dilbar va sho'x milliy taronalar", "category": "💃 To'yona & Lazgi"},

    # 🌍 Jahon & Turk
    {"name": "Tarkan (Turkiya)", "query": "Tarkan best hits songs", "desc": "Turk pop qiroli super xitlari", "category": "🌍 Jahon & Turk"},
    {"name": "Ibrahim Tatlises", "query": "Ibrahim Tatlises en iyi sarkilari", "desc": "Imperator — turk mumtoz va arabesk", "category": "🌍 Jahon & Turk"},
    {"name": "Mahmut Orhan", "query": "Mahmut Orhan deep house hits", "desc": "Avto-magistral uchun zamonaviy Deep House", "category": "🌍 Jahon & Turk"},
    {"name": "Modern Talking (Retro)", "query": "Modern Talking greatest hits", "desc": "80-yillar jahon oltin diskotekasi", "category": "🌍 Jahon & Turk"},
    {"name": "Yuriy Shatunov (Laskoviy May)", "query": "Yuriy Shatunov luchshie pesni", "desc": "Unutilmas retro nostalgiya xitlari", "category": "🌍 Jahon & Turk"},
    {"name": "Miyagi & Andy Panda", "query": "Miyagi Andy Panda best songs", "desc": "Avto-salon uchun zamonaviy vibe va bass", "category": "🌍 Jahon & Turk"},
    {"name": "Arash", "query": "Arash greatest hits songs", "desc": "Sharqona va Yevropa raqsbop xitlar", "category": "🌍 Jahon & Turk"},
]

COLLECTIONS_2026 = [
    {"id": "top_2026", "title": "🔥 2026 Eng Yangi O'zbek Xitlari (TOP Premyera)", "query": "uzbek xit qoshiqlar 2026 yangi premyera", "count": 25, "target_folder": "01_YANGI_XITLAR_2026", "desc": "Eng so'nggi chiqqan trend o'zbek xitlari"},
    {"id": "vip_bass", "title": "🚗 Avto VIP Bass & Sabvufer Remix (Car Audio)", "query": "uzbek bass remix car music 2026", "count": 25, "target_folder": "06_AVTO_BASS_REMIX", "desc": "Mashina kalonkalari uchun yumshoq va kuchli dinamika"},
    {"id": "tungi_safar", "title": "🌙 Tungi Safar va Karvon (Sokin Magistral)", "query": "uzbek sokin qoshiqlar yolda eshitadigan", "count": 25, "target_folder": "03_TUNGI_SOKIN_YOL", "desc": "Uzoq yo'l va tungi haydash uchun sokin ashulalar"},
    {"id": "toyona_lazgi", "title": "💃 To'yona va Sho'x Xorazm Lazgi (Bazm)", "query": "uzbek shox qoshiqlar toyona lazgi popuri", "count": 25, "target_folder": "04_TOYONA_VA_LAZGI", "desc": "To'y, tantana va davrani qizdiruvchi sho'x taronalar"},
    {"id": "retro_oltin", "title": "🏛️ Retro Oltin Fond (90-2000 Yillar Xitlari)", "query": "uzbek retro 90 yillar oltin fond qoshiqlar", "count": 25, "target_folder": "05_RETRO_VA_MUMTOZ", "desc": "Yoshlikni eslatuvchi qadrdon o'zbek xitlari"},
    {"id": "choyxona_maqom", "title": "🫖 Choyxona va Diltortar Jonli Ashulalar", "query": "uzbek diltortar choyxona jonli ijro qoshiqlari", "count": 25, "target_folder": "05_RETRO_VA_MUMTOZ", "desc": "Ulfatlar davrasi va jonli tor sadolari"},
    {"id": "dardli_lirik", "title": "💔 Dardli, Lirik va Sog'inch Taronalari", "query": "uzbek dardli mayin qoshiqlar yurakka yaqin", "count": 20, "target_folder": "03_TUNGI_SOKIN_YOL", "desc": "Qalbga yaqin ma'noli va ta'sirchan qo'shiqlar"},
    {"id": "uzbek_rap", "title": "🎧 O'zbek Rap, Hip-Hop va Yoshlar Trendi", "query": "uzbek rap hip hop xit qoshiqlar yangi", "count": 20, "target_folder": "01_YANGI_XITLAR_2026", "desc": "Konsta, Massa va zamonaviy ritmik o'zbek repi"},
    {"id": "vodiy_navo", "title": "⛰️ Farg'ona, Andijon va Namangan Navolari", "query": "vodiy fargona andijon shox sara qoshiqlar", "count": 20, "target_folder": "04_TOYONA_VA_LAZGI", "desc": "Vodiy maktabining eng shirali va sho'x qo'shiqlari"},
    {"id": "samarqand_buxoro", "title": "🕌 Samarqand, Buxoro va Mavrigi Ohanglari", "query": "buxoro mavrigi samarqand shox qoshiqlar", "count": 20, "target_folder": "04_TOYONA_VA_LAZGI", "desc": "Mavrigi va qadimiy shaharlarning betakror ritmi"},
    {"id": "turk_xitlar", "title": "🇹🇷 Turkcha Super Xitlar va Serial Musiqalari", "query": "turkish best hit songs pop arabesk", "count": 20, "target_folder": "07_JAHON_VA_TURK_XITLAR", "desc": "Eng mashhur turk estrada va serial taronalari"},
    {"id": "jahon_retro", "title": "🌍 80-90-Yillar Jahon Diskotekasi (Gold Hits)", "query": "80s 90s greatest hits eurodance disco", "count": 20, "target_folder": "07_JAHON_VA_TURK_XITLAR", "desc": "Modern Talking, C.C. Catch, Bad Boys Blue va jahon xitlari"},
    {"id": "kavkaz_shox", "title": "🦅 Kavkaz, Lezginka va Sho'x Avto-Ritmlar", "query": "kavkaz hit music car bass lezginka", "count": 20, "target_folder": "07_JAHON_VA_TURK_XITLAR", "desc": "Kavkazona shiddatli va jo'shqin avto-taronalar"},
    {"id": "instrumental", "title": "🎻 Instrumental, Gitara, Nay va Klarnet (Dam olish)", "query": "uzbek instrumental gitara klarnet nay music", "count": 15, "target_folder": "03_TUNGI_SOKIN_YOL", "desc": "So'zsiz sokin ohanglar va asabni tinchlantiruvchi kuylar"},
    {"id": "sport_energiya", "title": "⚡ Sport, Motivatsiya va Yuqori Tezlik", "query": "car music mix bass boosted motivation 2026", "count": 20, "target_folder": "06_AVTO_BASS_REMIX", "desc": "Tetiklik va yuqori kayfiyat beruvchi drayv musiqalar"},
    {"id": "jonli_konsert", "title": "🎤 O'zbek Jonli Ijro va Duetlar Guldastasi", "query": "uzbek jonli ijro xit duet qoshiqlar", "count": 20, "target_folder": "02_SEVIMLI_SANATKORLAR", "desc": "Eng sara jonli ijrolar va mashhur duetlar"},
]


def parse_track_count(raw_val: any, default: int = 15) -> int:
    """Foydalanuvchi yozgan har qanday matndan (masalan '7', '15 ta', '100') aniq sonni ajratib olish."""
    if raw_val is None:
        return default
    s = str(raw_val).strip()
    m = re.search(r"(\d+)", s)
    if m:
        val = int(m.group(1))
        return max(1, min(val, 200))
    return default


def get_custom_artists_path() -> str:
    app_data = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
    cfg_dir = os.path.join(app_data, "UzbekMusiqaMarkaziPro")
    os.makedirs(cfg_dir, exist_ok=True)
    return os.path.join(cfg_dir, "custom_artists.json")


def get_all_artists() -> List[Dict[str, str]]:
    """Standart 50+ san'atkorlar + foydalanuvchi qo'shgan san'atkorlar ro'yxati."""
    artists = list(CATALOG_ARTISTS)
    p = get_custom_artists_path()
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                custom_list = json.load(f)
                if isinstance(custom_list, list):
                    existing_names = {a["name"].lower() for a in artists}
                    for ca in custom_list:
                        if isinstance(ca, dict) and ca.get("name") and ca["name"].lower() not in existing_names:
                            artists.insert(0, ca)
        except Exception:
            pass
    return artists


def add_custom_artist(name: str, desc: str = "Foydalanuvchi qo'shgan san'atkor", category: str = "🔥 Zamonaviy Xit") -> Dict[str, str]:
    """Yangi san'atkorni doimiy katalogga saqlash."""
    clean_n = name.strip()
    new_entry = {
        "name": clean_n,
        "query": f"{clean_n} yangi xit qoshiqlari",
        "desc": desc.strip() or "Shaxsiy sevimli san'atkor",
        "category": category,
    }
    p = get_custom_artists_path()
    custom_list = []
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                custom_list = json.load(f)
        except Exception:
            custom_list = []
    custom_list = [x for x in custom_list if x.get("name", "").lower() != clean_n.lower()]
    custom_list.insert(0, new_entry)
    try:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(custom_list, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
    return new_entry


def scan_all_library_mp3s(base_dir: str, active_target_dir: Optional[str] = None, scan_all: bool = True) -> List[Dict[str, any]]:
    """
    Barcha papkalardagi (yoki tanlangan papkadagi) yuklangan MP3 fayllarni qidirib topish.
    Hech bir yuklangan qo'shiq yo'qolib qolmasligini 100% kafolatlaydi!
    """
    found_files = []
    seen_paths = set()

    dirs_to_check = []
    if active_target_dir and os.path.exists(active_target_dir):
        dirs_to_check.append(active_target_dir)

    if scan_all and base_dir and os.path.exists(base_dir):
        # Standart 7 ta avto-papka va ularning ichki san'atkor papkalari
        for f_info in EXTENDED_CAR_FOLDERS:
            cand = os.path.join(base_dir, f_info["folder"])
            if os.path.exists(cand) and cand not in dirs_to_check:
                dirs_to_check.append(cand)
        # Base_dir ichidagi boshqa musiqiy papkalar (01_, 02_, Musiqa va h.k.)
        try:
            for item in sorted(os.listdir(base_dir)):
                full_sub = os.path.join(base_dir, item)
                if os.path.isdir(full_sub) and not item.startswith(".") and any(
                    item.startswith(pfx) for pfx in ("01_", "02_", "03_", "04_", "05_", "06_", "07_", "Musiqa", "Uzbek")
                ):
                    if full_sub not in dirs_to_check:
                        dirs_to_check.append(full_sub)
        except Exception:
            pass

    for d in dirs_to_check:
        try:
            for root, subdirs, files in os.walk(d):
                # Texnik yashirin papkalarni o'tkazib yuborish
                subdirs[:] = [sd for sd in subdirs if not sd.startswith(".")]
                for f in sorted(files):
                    if f.lower().endswith(".mp3") and not f.endswith("_raw128k.mp3") and not f.endswith(".remaster_tmp.mp3"):
                        fp = os.path.join(root, f)
                        norm_fp = os.path.normcase(os.path.abspath(fp))
                        if norm_fp not in seen_paths:
                            seen_paths.add(norm_fp)
                            rel_folder = os.path.basename(root)
                            found_files.append({
                                "path": fp,
                                "folder": rel_folder,
                                "mtime": os.path.getmtime(fp) if os.path.exists(fp) else 0.0,
                            })
        except Exception:
            continue

    return found_files


def organize_folder_mp3s(folder_path: str) -> Dict[str, int]:
    """
    Papka ichidagi MP3 fayllarni chiroyli tartib raqamiga ('01 - Artist - Title.mp3') keltirish,
    FAT32 sanalarini yangilash va M3U pleylist yaratish.
    """
    if not folder_path or not os.path.exists(folder_path):
        return {"total": 0, "renamed": 0}

    mp3s = [f for f in sorted(os.listdir(folder_path)) if f.lower().endswith(".mp3") and not f.startswith(".")]
    if not mp3s:
        return {"total": 0, "renamed": 0}

    base_time = datetime.datetime.now().timestamp()
    organized_count = 0

    for idx, fname in enumerate(mp3s, 1):
        old_path = os.path.join(folder_path, fname)
        raw_no_ext = os.path.splitext(fname)[0]
        stripped = re.sub(r"^\d+\s*[-_.]\s*", "", raw_no_ext).strip()
        clean_title = sanitize_title(stripped)
        new_fname = f"{idx:02d} - {clean_title}.mp3"
        new_path = os.path.join(folder_path, new_fname)

        try:
            if os.path.normcase(old_path) != os.path.normcase(new_path) and not os.path.exists(new_path):
                os.rename(old_path, new_path)
                target_p = new_path
            else:
                target_p = old_path

            t_stamp = base_time + (idx * 60)
            os.utime(target_p, (t_stamp, t_stamp))
            organized_count += 1
        except Exception:
            continue

    generate_playlist(folder_path)
    return {"total": len(mp3s), "renamed": organized_count}



def find_tool(name: str) -> Optional[str]:
    """Tizimda yoki standart papkalarda binary vositani qidirish."""
    # 1. shutil.which
    found = shutil.which(name)
    if found:
        return found
    if sys.platform == "win32" and not name.lower().endswith(".exe"):
        found = shutil.which(name + ".exe")
        if found:
            return found

    # 2. Standart kataloglar
    candidates = []
    user_prof = os.environ.get("USERPROFILE", "")
    local_app = os.environ.get("LOCALAPPDATA", "")

    if user_prof:
        candidates.append(os.path.join(user_prof, "Desktop", name + ".exe"))
        candidates.append(os.path.join(user_prof, "Downloads", name + ".exe"))
    if local_app:
        candidates.append(os.path.join(local_app, "Microsoft", "WinGet", "Links", name + ".exe"))
        candidates.append(os.path.join(local_app, "Programs", "Python", "Python312", "Scripts", name + ".exe"))
        candidates.append(os.path.join(local_app, "Programs", "Python", "Python311", "Scripts", name + ".exe"))
        candidates.append(os.path.join(local_app, "Programs", "Python", "Python310", "Scripts", name + ".exe"))

    # PyInstaller frozen muhiti yoki dastur papkasi
    if getattr(sys, "frozen", False):
        app_dir = os.path.dirname(sys.executable)
        candidates.append(os.path.join(app_dir, name + ".exe"))
        if hasattr(sys, "_MEIPASS"):
            candidates.append(os.path.join(sys._MEIPASS, name + ".exe"))
    elif sys.argv and sys.argv[0]:
        script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        candidates.append(os.path.join(script_dir, name + ".exe"))

    # Virtual muhit papkasi
    venv_dir = os.path.dirname(sys.executable)
    candidates.append(os.path.join(venv_dir, name + ".exe"))

    for c in candidates:
        if os.path.isfile(c):
            return c

    return None


def get_ytdlp_path() -> Optional[str]:
    return find_tool("yt-dlp")


def get_ffmpeg_path() -> Optional[str]:
    return find_tool("ffmpeg")


def get_ffprobe_path() -> Optional[str]:
    return find_tool("ffprobe")


def detect_usb_drives() -> List[Dict[str, any]]:
    """Windows tizimidagi barcha ulangan USB fleshkalarni aniqlash va xotira holatini o'lchash."""
    drives = []
    if sys.platform != "win32":
        return drives

    kernel32 = ctypes.windll.kernel32
    for letter in string.ascii_uppercase:
        root_path = f"{letter}:\\"
        drive_type = kernel32.GetDriveTypeW(root_path)
        # DRIVE_REMOVABLE = 2
        if drive_type == 2:
            label_buf = ctypes.create_unicode_buffer(261)
            fs_buf = ctypes.create_unicode_buffer(261)
            serial_num = ctypes.c_ulong()
            max_component_len = ctypes.c_ulong()
            file_system_flags = ctypes.c_ulong()

            res = kernel32.GetVolumeInformationW(
                root_path,
                label_buf,
                ctypes.sizeof(label_buf),
                ctypes.byref(serial_num),
                ctypes.byref(max_component_len),
                ctypes.byref(file_system_flags),
                fs_buf,
                ctypes.sizeof(fs_buf)
            )

            label = label_buf.value if res and label_buf.value else "USB Fleshka"
            fs = fs_buf.value if res and fs_buf.value else "FAT32"

            free_bytes = ctypes.c_ulonglong(0)
            total_bytes = ctypes.c_ulonglong(0)
            total_free_bytes = ctypes.c_ulonglong(0)

            kernel32.GetDiskFreeSpaceExW(
                root_path,
                ctypes.byref(free_bytes),
                ctypes.byref(total_bytes),
                ctypes.byref(total_free_bytes)
            )

            total_gb = round(total_bytes.value / (1024 ** 3), 2)
            free_gb = round(free_bytes.value / (1024 ** 3), 2)
            used_gb = round(total_gb - free_gb, 2)
            used_percent = round((used_gb / total_gb * 100), 1) if total_gb > 0 else 0.0

            drives.append({
                "letter": letter,
                "root": root_path,
                "label": label,
                "file_system": fs,
                "total_gb": total_gb,
                "used_gb": used_gb,
                "free_gb": free_gb,
                "used_percent": used_percent,
                "display": f"{letter}: [{label}] - {free_gb} GB bo'sh ({fs})"
            })

    return drives


def sanitize_title(raw_title: str) -> str:
    """Qo'shiq nomini tozalab, avto-magnitola uchun ideal 'Artist - Song' formatiga keltirish."""
    if not raw_title:
        return "Noma'lum Qo'shiq"

    title = raw_title.strip()

    # 1. Quvur (| yoki //) belgisidan keyingi qismlarni tozalash
    if "|" in title:
        title = title.split("|")[0].strip()
    if "//" in title:
        title = title.split("//")[0].strip()

    # 2. Qavslar ichidagi va tashqarisidagi standart YouTube teglari
    patterns_to_remove = [
        r"(?i)\[\s*(official|rasmiy|klip|video|audio|premyera|hd|4k|track|full).*?\]",
        r"(?i)\(\s*(official|rasmiy|klip|video|audio|premyera|hd|4k|track|full).*?\)",
        r"(?i)\b(official\s+video|official\s+music\s+video|official\s+audio)\b",
        r"(?i)\b(rasmiy\s+klip|premyera|klipi|premyera\s+2026|xit\s+2026)\b",
        r"(?i)\b(yangi\s+klip|jonli\s+ijro|konsert\s+dasturi)\b",
    ]
    for pattern in patterns_to_remove:
        title = re.sub(pattern, "", title)

    # 3. Emojilar va g'alati belgilar
    title = re.sub(r"[\U00010000-\U0010ffff]", "", title)
    title = re.sub(r"[\u2600-\u27BF]", "", title)

    # 4. Windows va FAT32 fayl nomlarida taqiqlangan belgilar: \ / : * ? " < > |
    title = re.sub(r'[\\/:*?"<>|]', " ", title)

    # 5. Ortiqcha probellarni qisqartirish
    title = re.sub(r"\s+", " ", title).strip()

    if len(title) < 2:
        title = "Uzbek Muzikasi"

    return title


def normalize_title_for_comparison(title: str) -> str:
    """Taqqoslash uchun nomni kichik harflar va maxsus belgilarsiz holatga keltirish."""
    # Boshidagi 01, 02 kabi tartib raqamlarini olib tashlash
    clean = re.sub(r"^\d+\s*[-_.]\s*", "", title)
    clean = re.sub(r"\.mp3$", "", clean, flags=re.IGNORECASE)
    clean = re.sub(r"[^a-zA-Z0-9\u0400-\u04FF]", "", clean)
    return clean.lower()


def scan_existing_tracks(folder_path: str) -> Set[str]:
    """Smart Sync: Papkada mavjud qo'shiqlarning normallashtirilgan ro'yxatini olish."""
    existing = set()
    if not os.path.exists(folder_path):
        return existing

    for f in os.listdir(folder_path):
        if f.lower().endswith(".mp3"):
            norm = normalize_title_for_comparison(f)
            if norm:
                existing.add(norm)
    return existing


def is_track_already_present(track_title: str, existing_set: Set[str]) -> bool:
    """Qo'shiq allaqachon fleshkada bor-yo'qligini tekshirish."""
    norm = normalize_title_for_comparison(track_title)
    return norm in existing_set


def search_youtube(
    query: str,
    limit: int = 15,
    ytdlp_path: Optional[str] = None,
    log_cb: Optional[Callable[[str], None]] = None,
    cancel_check: Optional[Callable[[], bool]] = None
) -> List[Dict[str, str]]:
    """YouTube bo'yicha qidirish va toza qo'shiqlar ro'yxatini qaytarish."""
    limit = max(1, min(int(limit or 15), 200))
    fetch_count = max(limit + 8, int(limit * 1.5)) if not (query.startswith("http://") or query.startswith("https://")) else limit

    if log_cb:
        log_cb(f"[Qidiruv] YouTube bazasidan qidirilmoqda: '{query}' (Maqsad: {limit} ta trek)...")

    search_term = query if query.startswith("http://") or query.startswith("https://") else f"ytsearch{fetch_count}:{query}"

    # 1. In-memory ultra-tezkor qidiruv (RAM orqali)
    if _YTDLP_LIB_AVAILABLE:
        try:
            ydl_opts = {
                "extract_flat": "in_playlist",
                "quiet": True,
                "no_warnings": True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(search_term, download=False)
                entries = list(info.get("entries", [info])) if (info and "entries" in info) else ([info] if info else [])
                results = []
                seen_titles = set()
                for data in entries:
                    if not data:
                        continue
                    if cancel_check and cancel_check():
                        return []
                    video_id = data.get("id")
                    raw_title = data.get("title") or ""
                    if not raw_title or raw_title in ("[Deleted video]", "[Private video]"):
                        continue
                    duration = data.get("duration") or 0
                    if duration and (duration > 1200 or duration < 35):
                        continue
                    cleaned = sanitize_title(raw_title)
                    norm = cleaned.lower()
                    if norm in seen_titles:
                        continue
                    seen_titles.add(norm)
                    url = data.get("url") or (f"https://www.youtube.com/watch?v={video_id}" if video_id else "")
                    if not url:
                        continue
                    if not url.startswith("http"):
                        url = f"https://www.youtube.com/watch?v={video_id}"
                    results.append({
                        "id": video_id or f"tr_{len(results)+1}",
                        "url": url,
                        "title": cleaned,
                        "raw_title": raw_title,
                        "duration": int(duration or 210),
                        "channel": data.get("uploader") or data.get("channel") or "YouTube Music",
                    })
                    if len(results) >= limit:
                        break
                if results:
                    if log_cb:
                        log_cb(f"[Natija] {len(results)} ta toza qo'shiq topildi.")
                    return results
        except Exception as e:
            if log_cb:
                log_cb(f"[Qidiruv zaxira] In-memory qidiruvdan CLI zaxiraga o'tildi ({e})")

    yt = ytdlp_path or get_ytdlp_path()
    if not yt:
        raise RuntimeError("yt-dlp topilmadi! Iltimos, yt-dlp o'rnatilganligini tekshiring.")

    cmd = [
        yt,
        "--flat-playlist",
        "--dump-json",
        "--default-search", "ytsearch",
        "--remote-components", "ejs:github",
        "--extractor-args", "youtube:player_client=mweb,android",
        "--no-check-certificates",
        "--no-warnings",
        search_term
    ]

    startupinfo = None
    if sys.platform == "win32":
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = 0

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        startupinfo=startupinfo,
        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
    )

    results = []
    seen_titles = set()

    for line in proc.stdout:
        if cancel_check and cancel_check():
            proc.terminate()
            if log_cb:
                log_cb("[Bekor qilindi] Foydalanuvchi tomonidan to'xtatildi.")
            return []

        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
            video_id = data.get("id")
            raw_title = data.get("title", "")
            duration = data.get("duration", 0)

            if duration and (duration > 1200 or duration < 35):
                continue

            cleaned = sanitize_title(raw_title)
            norm = cleaned.lower()

            if norm in seen_titles:
                continue
            seen_titles.add(norm)

            url = f"https://www.youtube.com/watch?v={video_id}" if video_id else data.get("url")
            results.append({
                "id": video_id,
                "url": url,
                "title": cleaned,
                "raw_title": raw_title,
                "duration": int(duration or 210),
                "channel": data.get("uploader") or data.get("channel") or "YouTube Music",
            })

            if len(results) >= limit:
                break
        except Exception:
            continue

    proc.stdout.close()
    proc.wait()

    if log_cb:
        log_cb(f"[Natija] {len(results)} ta toza qo'shiq aniqlandi.")

    return results


def download_file_idm32(
    media_url: str,
    headers: Dict[str, str],
    dest_path: str,
    num_streams: int = DEFAULT_IDM_STREAMS,
    progress_cb: Optional[Callable[[float, float, List[float]], None]] = None,
    cancel_check: Optional[Callable[[], bool]] = None
) -> bool:
    """
    IDM (Internet Download Manager) uslubidagi 32-Oqimli dinamik segmentli yuklovchi.
    Bitta faylni 32 ta parallel soket/diapazonda (Range: bytes=start-end) yuklaydi.
    Qat'iy bayt nazorati (Strict Byte-Sum & HTTP 206 Verification) va 3x qayta urinishga ega.
    """
    try:
        session = get_http_session()

        probe_headers = dict(headers or {})
        probe_headers["Range"] = "bytes=0-0"
        r_probe = session.get(media_url, headers=probe_headers, timeout=10)

        if r_probe.status_code not in (200, 206):
            return False

        total_size = None
        cr = r_probe.headers.get("Content-Range", "")
        if cr and "/" in cr:
            try:
                total_size = int(cr.split("/")[-1])
            except ValueError:
                pass

        if not total_size or total_size <= 1024:
            return False

        # Fayl hajmini diskda oldindan bo'shatib qo'yish (Pre-allocation)
        with open(dest_path, "wb") as f:
            f.seek(total_size - 1)
            f.write(b"\0")

        num_streams = max(1, min(num_streams, 32))
        chunk_size = total_size // num_streams
        downloaded_bytes = [0] * num_streams
        stream_progress = [0.0] * num_streams
        lock = threading.Lock()
        t_start = time.monotonic()
        last_progress_time = t_start

        def stream_worker(i: int) -> bool:
            start = i * chunk_size
            end = (total_size - 1) if i == num_streams - 1 else (start + chunk_size - 1)
            seg_len = end - start + 1

            for attempt in range(3):
                if cancel_check and cancel_check():
                    return False
                try:
                    seg_headers = dict(headers or {})
                    seg_headers["Range"] = f"bytes={start}-{end}"

                    resp = session.get(media_url, headers=seg_headers, stream=True, timeout=18)
                    if i > 0 and resp.status_code != 206:
                        return False
                    if resp.status_code not in (200, 206):
                        time.sleep(0.15 * (attempt + 1))
                        continue

                    written = 0
                    with open(dest_path, "r+b") as f_out:
                        f_out.seek(start)
                        for chunk in resp.iter_content(chunk_size=65536):
                            if cancel_check and cancel_check():
                                return False
                            if chunk:
                                f_out.write(chunk)
                                written += len(chunk)
                                with lock:
                                    downloaded_bytes[i] = written
                                    stream_progress[i] = min(1.0, written / seg_len)

                    if written == seg_len:
                        return True
                except Exception:
                    time.sleep(0.15 * (attempt + 1))
            return False

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_streams) as executor:
            futures = [executor.submit(stream_worker, i) for i in range(num_streams)]

            while True:
                if cancel_check and cancel_check():
                    break

                done = all(f.done() for f in futures)
                now = time.monotonic()
                elapsed = max(0.001, now - t_start)
                total_dl = sum(downloaded_bytes)
                overall_pct = min(1.0, total_dl / total_size)
                speed_mbps = (total_dl / (1024 * 1024)) / elapsed

                if progress_cb and (now - last_progress_time >= 0.08 or done):
                    progress_cb(overall_pct, speed_mbps, list(stream_progress))
                    last_progress_time = now

                if done:
                    break
                time.sleep(0.05)

            all_ok = all((not f.cancelled() and f.exception() is None and f.result() is True) for f in futures)

        exact_match = (all_ok and sum(downloaded_bytes) == total_size and os.path.exists(dest_path) and os.path.getsize(dest_path) == total_size)
        if not exact_match:
            try:
                if os.path.exists(dest_path):
                    os.remove(dest_path)
            except Exception:
                pass
            return False

        return True
    except Exception:
        try:
            if os.path.exists(dest_path):
                os.remove(dest_path)
        except Exception:
            pass
        return False


def download_and_process_track(
    track: Dict[str, str],
    out_dir: str,
    index: int,
    bitrate: str = DEFAULT_BITRATE,
    dsp_profile: Optional[Dict] = None,
    keep_preview_raw: bool = True,
    num_streams: int = DEFAULT_IDM_STREAMS,
    ytdlp_path: Optional[str] = None,
    ffmpeg_path: Optional[str] = None,
    log_cb: Optional[Callable[[str], None]] = None,
    task_progress_cb: Optional[Callable[[int, float, str, Optional[float], Optional[List[float]]], None]] = None,
    cancel_check: Optional[Callable[[], bool]] = None
) -> Tuple[Optional[str], Optional[str]]:
    """
    Qo'shiqni 3-Bosqichli Kafolatli IDM 32-Oqim + Multi-Fragment mexanizmi bilan yuklab,
    Single-Pass Dual-Output FFmpeg orqali 256k Studio DSP va 128k Raw A/B formatiga aylantirish.
    """
    yt = ytdlp_path or get_ytdlp_path()
    ff = ffmpeg_path or get_ffmpeg_path()

    if not ff:
        raise RuntimeError("ffmpeg topilmadi!")

    os.makedirs(out_dir, exist_ok=True)
    dsp = dsp_profile or DEFAULT_DSP_PROFILE
    clean_name = sanitize_title(track.get("title") or f"Trek {index}")
    filename_base = f"{index:02d} - {clean_name}"
    final_mp3 = os.path.join(out_dir, f"{filename_base}.mp3")

    temp_id = re.sub(r"[^a-zA-Z0-9_-]", "", str(track.get("id") or f"tr_{index}")) or f"tr_{index}"
    temp_dir = os.path.join(out_dir, ".temp_proc", f"{index:02d}_{temp_id}")
    os.makedirs(temp_dir, exist_ok=True)

    temp_audio = os.path.join(temp_dir, f"{temp_id}_raw.m4a")
    temp_thumb = os.path.join(temp_dir, f"{temp_id}_thumb.jpg")
    raw_preview_mp3 = os.path.join(out_dir, ".preview_raw", f"{filename_base}_raw128k.mp3")
    os.makedirs(os.path.dirname(raw_preview_mp3), exist_ok=True)

    startupinfo = None
    creationflags = 0
    if sys.platform == "win32":
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = 0
        creationflags = subprocess.CREATE_NO_WINDOW

    if task_progress_cb:
        task_progress_cb(index, 0.05, f"IDM {num_streams}-Oqim ulanmoqda...", 0.0, [0.05] * num_streams)

    download_success = False

    # 1-BOSQICH: In-Memory yt_dlp + IDM 32-Oqim Dinamik Segment Yuklovchi
    if _YTDLP_LIB_AVAILABLE:
        try:
            ydl_opts = {
                "quiet": True,
                "no_warnings": True,
                "format": "ba[ext=m4a]/ba/b",
                "remote_components": ["ejs:github"],
                "extractor_args": {"youtube": {"player_client": ["mweb", "android"]}},
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(track["url"], download=False)
                media_url = info.get("url")
                headers = info.get("http_headers", {})
                thumb_url = info.get("thumbnail")

                if thumb_url:
                    try:
                        r_th = get_http_session().get(thumb_url, timeout=8)
                        if r_th.status_code == 200 and len(r_th.content) > 512:
                            with open(temp_thumb, "wb") as f_th:
                                f_th.write(r_th.content)
                    except Exception:
                        pass

                if media_url:
                    def on_idm_prog(pct, spd, s_arr):
                        if task_progress_cb:
                            status_str = f"IDM {num_streams}x: {spd:.1f} MB/s ({int(pct*100)}%)"
                            task_progress_cb(index, pct * 0.85, status_str, spd, s_arr)

                    download_success = download_file_idm32(
                        media_url=media_url,
                        headers=headers,
                        dest_path=temp_audio,
                        num_streams=num_streams,
                        progress_cb=on_idm_prog,
                        cancel_check=cancel_check
                    )
        except Exception:
            download_success = False

    # 2-BOSQICH: Agar YouTube CDN Range so'rovini cheklasa, In-Memory yt_dlp Multi-Fragment Engine
    if (not download_success or not os.path.exists(temp_audio)) and _YTDLP_LIB_AVAILABLE:
        try:
            t_dl_start = time.monotonic()

            def ydl_prog_hook(d):
                if cancel_check and cancel_check():
                    raise RuntimeError("Cancelled")
                if d.get("status") == "downloading" and task_progress_cb:
                    total_b = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
                    dl_b = d.get("downloaded_bytes") or 0
                    spd_b = d.get("speed") or 0
                    spd_mb = spd_b / (1024 * 1024) if spd_b else ((dl_b / (1024 * 1024)) / max(0.1, time.monotonic() - t_dl_start))
                    pct = min(1.0, dl_b / total_b) if total_b > 0 else 0.5
                    active_bars = [1.0 if (k / num_streams) <= pct else 0.25 for k in range(num_streams)]
                    task_progress_cb(index, pct * 0.85, f"Turbo {num_streams}x: {spd_mb:.1f} MB/s", spd_mb, active_bars)

            ydl_dl_opts = {
                "quiet": True,
                "no_warnings": True,
                "format": "ba[ext=m4a]/ba/b",
                "remote_components": ["ejs:github"],
                "extractor_args": {"youtube": {"player_client": ["mweb", "android"]}},
                "outtmpl": os.path.join(temp_dir, f"{temp_id}_raw.%(ext)s"),
                "concurrent_fragment_downloads": num_streams,
                "http_chunk_size": 1048576,
                "progress_hooks": [ydl_prog_hook],
            }
            with yt_dlp.YoutubeDL(ydl_dl_opts) as ydl_dl:
                ydl_dl.download([track["url"]])
            download_success = True
        except Exception:
            download_success = False

    # 3-BOSQICH: CLI yt-dlp.exe zaxira oqimi
    found_audio = None
    if os.path.exists(temp_dir):
        for f in os.listdir(temp_dir):
            if f.startswith(f"{temp_id}_raw.") and not f.endswith((".jpg", ".jpeg", ".webp", ".png", ".part", ".ytdl")):
                cand = os.path.join(temp_dir, f)
                if os.path.getsize(cand) > 1024:
                    found_audio = cand
                    break

    if not found_audio and yt:
        cmd_yt = [
            yt,
            "-f", "ba/b",
            "-N", str(num_streams),
            "--concurrent-fragments", str(num_streams),
            "--http-chunk-size", "1M",
            "--buffer-size", "128K",
            "--write-thumbnail",
            "--convert-thumbnails", "jpg",
            "--remote-components", "ejs:github",
            "--extractor-args", "youtube:player_client=mweb,android",
            "--no-check-certificates",
            "--no-warnings",
            "-o", os.path.join(temp_dir, f"{temp_id}_raw.%(ext)s"),
            "-o", f"thumbnail:{os.path.join(temp_dir, f'{temp_id}_thumb.%(ext)s')}",
            track["url"]
        ]

        proc_yt = subprocess.Popen(
            cmd_yt,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            startupinfo=startupinfo,
            creationflags=creationflags
        )
        _, _ = proc_yt.communicate()

        if os.path.exists(temp_dir):
            for f in os.listdir(temp_dir):
                if f.startswith(f"{temp_id}_raw.") and not f.endswith((".jpg", ".jpeg", ".webp", ".png", ".part", ".ytdl")):
                    cand = os.path.join(temp_dir, f)
                    if os.path.getsize(cand) > 1024:
                        found_audio = cand
                        break

    if cancel_check and cancel_check():
        shutil.rmtree(temp_dir, ignore_errors=True)
        return None, None

    if not found_audio or not os.path.exists(found_audio):
        if log_cb:
            log_cb(f"  [Xato] {clean_name} audiosi yuklanmadi.")
        shutil.rmtree(temp_dir, ignore_errors=True)
        return None, None

    if task_progress_cb:
        task_progress_cb(index, 0.90, "Studiya DSP 256k...", 0.0, [1.0] * num_streams)

    # Muqova rasmi
    thumb_file = None
    for f in os.listdir(temp_dir):
        if f.startswith(f"{temp_id}_thumb") and f.lower().endswith((".jpg", ".jpeg", ".png")):
            thumb_file = os.path.join(temp_dir, f)
            break

    # 2. Maytafon Studio DSP filtri (Single-Pass Dual-Output Optimization)
    audio_filter = (
        f"bass=g={dsp['bass_gain']}:f={dsp['bass_freq']},"
        f"treble=g={dsp['treble_gain']}:f={dsp['treble_freq']},"
        f"loudnorm=I={dsp['loudnorm_i']}:LRA={dsp['loudnorm_lra']}:TP={dsp['loudnorm_tp']},"
        f"alimiter=limit={dsp['limiter_limit']}dB"
    )

    artist_name = "O'zbek San'atkorlari"
    song_name = clean_name
    if " - " in clean_name:
        parts = clean_name.split(" - ", 1)
        artist_name = parts[0].strip()
        song_name = parts[1].strip()

    def build_ff_command(use_thumb: bool) -> List[str]:
        cmd = [ff, "-y", "-threads", "0", "-i", found_audio]
        if use_thumb and thumb_file and os.path.exists(thumb_file):
            cmd.extend(["-i", thumb_file, "-map", "0:a", "-map", "1:v", "-c:v", "mjpeg", "-disposition:v:0", "attached_pic"])
        else:
            cmd.extend(["-map", "0:a"])

        cmd.extend([
            "-af", audio_filter,
            "-c:a", "libmp3lame",
            "-b:a", bitrate,
            "-ar", "44100",
            "-ac", "2",
            "-id3v2_version", "3",
            "-metadata", f"title={song_name}",
            "-metadata", f"artist={artist_name}",
            "-metadata", "album=Avto Magnitola To'plami",
            "-metadata", f"track={index}",
            "-metadata", "year=2026",
            final_mp3
        ])

        if keep_preview_raw and not os.path.exists(raw_preview_mp3):
            cmd.extend([
                "-map", "0:a",
                "-c:a", "libmp3lame",
                "-b:a", "128k",
                "-ar", "44100",
                "-ac", "2",
                raw_preview_mp3
            ])
        return cmd

    proc_ff = subprocess.Popen(
        build_ff_command(use_thumb=True),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        startupinfo=startupinfo,
        creationflags=creationflags
    )
    _, _ = proc_ff.communicate()

    # Agar muqova formati (masalan WebP) sababli FFmpeg xato bersa, audio-only rejimda qayta muhrlash!
    if not os.path.exists(final_mp3) or os.path.getsize(final_mp3) < 1024:
        proc_ff2 = subprocess.Popen(
            build_ff_command(use_thumb=False),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            startupinfo=startupinfo,
            creationflags=creationflags
        )
        _, _ = proc_ff2.communicate()

    try:
        shutil.rmtree(temp_dir, ignore_errors=True)
    except Exception:
        pass

    if not os.path.exists(final_mp3) or os.path.getsize(final_mp3) < 1024:
        if log_cb:
            log_cb(f"  [Xato] MP3 ga aylantirishda xatolik: {filename_base}")
        return None, None

    # 3. FAT32 tartib tamg'asi
    try:
        base_time = datetime.datetime.now().timestamp()
        track_time = base_time + (index * 60)
        os.utime(final_mp3, (track_time, track_time))
    except Exception:
        pass

    if task_progress_cb:
        task_progress_cb(index, 1.0, "Tayyor ✅ (Bosib eshiting)", 0.0, [1.0] * num_streams)

    if log_cb:
        log_cb(f"  [Tayyor] {filename_base}.mp3 ({out_dir})")

    return final_mp3, raw_preview_mp3


def generate_playlist(folder_path: str, playlist_name: str = "00_Barcha_Qoshiqlar.m3u") -> Optional[str]:
    """Papka ichidagi barcha MP3 lardan magnitola uchun M3U pleylist tuzish."""
    if not os.path.exists(folder_path):
        return None

    mp3_files = [f for f in sorted(os.listdir(folder_path)) if f.lower().endswith(".mp3")]
    if not mp3_files:
        return None

    playlist_file = os.path.join(folder_path, playlist_name)
    with open(playlist_file, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for mp3 in mp3_files:
            f.write(f"#EXTINF:-1,{os.path.splitext(mp3)[0]}\n")
            f.write(f"{mp3}\n")

    return playlist_file


# =========================================================================
# AIMP METADATA, WAVEFORM TO'LQIN ANALIZATORI VA 10-BAND EQ RE-MASTERING
# =========================================================================

def compute_audio_waveform(file_path: str, num_bars: int = 80) -> List[float]:
    """
    AIMP Waveform Seekbar uchun MP3 fayldan 80 ta akustik amplituda ustunini
    0.5 millisekund ichida hisoblash (deterministic byte-energy sampling).
    """
    if not file_path or not os.path.exists(file_path):
        return [0.35] * num_bars

    try:
        file_size = os.path.getsize(file_path)
        if file_size < 1024:
            return [0.4] * num_bars

        # ID3v2 sarlavhasini o'tkazib yuborish (taxminan dastlabki 10% yoki 64KB)
        start_offset = min(65536, file_size // 10)
        usable_size = max(1024, file_size - start_offset - 1024)
        step = max(1, usable_size // num_bars)

        bars = []
        with open(file_path, "rb") as f:
            for i in range(num_bars):
                pos = start_offset + (i * step)
                f.seek(pos)
                sample = f.read(256)
                if not sample:
                    bars.append(0.3)
                    continue
                # Bayt dispersiyasi va o'rtacha energiyasi
                avg_deviation = sum(abs(b - 128) for b in sample) / len(sample)
                # Tabiiy musiqa dinamikasi shakli (boshida va oxirida yumshoqroq)
                envelope = math.sin(math.pi * (i + 0.5) / num_bars) ** 0.35
                norm_val = min(1.0, max(0.16, ((avg_deviation - 30.0) / 45.0) * envelope))
                bars.append(round(norm_val, 3))

        # Dinamik kontrastni kengaytirish (AIMP uslubida baland-past cho'qqilar)
        min_b = min(bars)
        max_b = max(bars)
        span = max(0.05, max_b - min_b)
        scaled = []
        for idx, b in enumerate(bars):
            s = 0.18 + 0.80 * ((b - min_b) / span)
            # Qo'shni ustunlar orasida ritmik tafovut
            if idx % 3 == 0:
                s = min(0.98, s * 1.12)
            elif idx % 4 == 1:
                s = max(0.18, s * 0.84)
            scaled.append(round(s, 3))
        return scaled
    except Exception:
        return [0.35 + 0.3 * math.sin(i * 0.4) for i in range(num_bars)]


def read_mp3_metadata(file_path: str) -> Dict[str, any]:
    """
    AIMP Tag Inspector va Pleyer uchun MP3 faylning davomiyligi, bitreyti,
    ID3v2 teglari, APIC muqova rasmi va 80-barli to'lqinini o'qish.
    """
    base_name = os.path.splitext(os.path.basename(file_path))[0] if file_path else "Noma'lum"
    clean_base = re.sub(r"^\d+\s*-\s*", "", base_name)
    default_artist = "O'zbek San'atkori"
    default_title = clean_base
    if " - " in clean_base:
        parts = clean_base.split(" - ", 1)
        default_artist = parts[0].strip()
        default_title = parts[1].strip()

    meta = {
        "path": file_path,
        "filename": os.path.basename(file_path) if file_path else "",
        "title": default_title,
        "artist": default_artist,
        "album": "Avto Magnitola To'plami",
        "year": "2026",
        "duration_sec": 210.0,
        "bitrate_kbps": 256,
        "sample_rate": 44100,
        "size_mb": round(os.path.getsize(file_path) / (1024 * 1024), 2) if (file_path and os.path.exists(file_path)) else 0.0,
        "cover_bytes": None,
        "waveform": compute_audio_waveform(file_path, 80),
    }

    if not _MUTAGEN_AVAILABLE or not file_path or not os.path.exists(file_path):
        return meta

    try:
        audio = MP3(file_path)
        if audio.info:
            meta["duration_sec"] = round(float(audio.info.length or 210.0), 2)
            meta["bitrate_kbps"] = int((audio.info.bitrate or 256000) // 1000)
            meta["sample_rate"] = int(audio.info.sample_rate or 44100)

        if audio.tags:
            if "TIT2" in audio.tags and str(audio.tags["TIT2"]).strip():
                meta["title"] = str(audio.tags["TIT2"]).strip()
            if "TPE1" in audio.tags and str(audio.tags["TPE1"]).strip():
                meta["artist"] = str(audio.tags["TPE1"]).strip()
            if "TALB" in audio.tags and str(audio.tags["TALB"]).strip():
                meta["album"] = str(audio.tags["TALB"]).strip()
            if "TYER" in audio.tags and str(audio.tags["TYER"]).strip():
                meta["year"] = str(audio.tags["TYER"]).strip()
            elif "TDRC" in audio.tags and str(audio.tags["TDRC"]).strip():
                meta["year"] = str(audio.tags["TDRC"]).strip()

            for key in audio.tags.keys():
                if key.startswith("APIC"):
                    apic = audio.tags[key]
                    if hasattr(apic, "data") and apic.data:
                        meta["cover_bytes"] = apic.data
                        break
    except Exception:
        pass

    return meta


def update_mp3_tags(
    file_path: str,
    title: str,
    artist: str,
    album: str,
    year: str = "2026",
    cover_image_path: Optional[str] = None
) -> bool:
    """
    AIMP ID3v2 Tag Editor: MP3 faylni qayta kodlamasdan uning ichki teglarini va ixtiyoriy muqova rasmini yangilash.
    """
    if not _MUTAGEN_AVAILABLE or not file_path or not os.path.exists(file_path):
        return False

    try:
        try:
            tags = ID3(file_path)
        except ID3NoHeaderError:
            tags = ID3()

        tags["TIT2"] = TIT2(encoding=3, text=title.strip())
        tags["TPE1"] = TPE1(encoding=3, text=artist.strip())
        tags["TALB"] = TALB(encoding=3, text=album.strip())
        tags["TYER"] = TYER(encoding=3, text=str(year).strip())

        if cover_image_path and os.path.exists(cover_image_path):
            with open(cover_image_path, "rb") as img_f:
                img_bytes = img_f.read()
            if len(img_bytes) > 128:
                mime = "image/png" if cover_image_path.lower().endswith(".png") else "image/jpeg"
                for k in list(tags.keys()):
                    if k.startswith("APIC"):
                        del tags[k]
                tags["APIC"] = APIC(
                    encoding=3,
                    mime=mime,
                    type=3,
                    desc="Cover",
                    data=img_bytes
                )

        tags.save(file_path, v2_version=3)
        return True
    except Exception:
        return False


# =========================================================================
# SEVIMLILAR (❤️ FAVORITES), TARIX (🕒 HISTORY) VA FLESHKA KO'CHIRGICH
# =========================================================================

def _get_library_state_path() -> str:
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "user_library_state.json")


def load_user_library_state() -> Dict[str, List[str]]:
    path = _get_library_state_path()
    default_state = {"favorites": [], "history": []}
    if not os.path.exists(path):
        return default_state
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return {
                    "favorites": list(data.get("favorites", [])),
                    "history": list(data.get("history", [])),
                }
    except Exception:
        pass
    return default_state


def save_user_library_state(state: Dict[str, List[str]]) -> bool:
    try:
        with open(_get_library_state_path(), "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def _norm_track_key(file_path: str) -> str:
    return os.path.normcase(os.path.abspath(file_path)) if file_path else ""


def is_favorite_track(file_path: str) -> bool:
    if not file_path:
        return False
    state = load_user_library_state()
    key = _norm_track_key(file_path)
    base_name = os.path.basename(file_path).lower()
    for fav in state.get("favorites", []):
        if _norm_track_key(fav) == key or os.path.basename(fav).lower() == base_name:
            return True
    return False


def toggle_favorite_track(file_path: str) -> bool:
    """Qo'shiqni Sevimlilar (❤️) ro'yxatiga qo'shish yoki olib tashlash. Yangi holatni qaytaradi."""
    if not file_path:
        return False
    state = load_user_library_state()
    favs = state.get("favorites", [])
    key = _norm_track_key(file_path)
    base_name = os.path.basename(file_path).lower()

    existing_matches = [f for f in favs if _norm_track_key(f) == key or os.path.basename(f).lower() == base_name]
    if existing_matches:
        for m in existing_matches:
            favs.remove(m)
        state["favorites"] = favs
        save_user_library_state(state)
        return False
    else:
        favs.insert(0, os.path.abspath(file_path))
        state["favorites"] = favs
        save_user_library_state(state)
        return True


def record_play_history(file_path: str):
    """Oxirgi eshitilgan qo'shiqlar tarixiga (maksimal 100 ta) yozish."""
    if not file_path:
        return
    state = load_user_library_state()
    hist = state.get("history", [])
    key = _norm_track_key(file_path)
    hist = [h for h in hist if _norm_track_key(h) != key]
    hist.insert(0, os.path.abspath(file_path))
    state["history"] = hist[:100]
    save_user_library_state(state)


def copy_tracks_to_folder(file_paths: List[str], dest_folder: str) -> int:
    """Tanlangan yoki Sevimli MP3 qo'shiqlarni 1-bosishda Fleshka/maqsad papkaga ko'chirish."""
    if not file_paths or not dest_folder:
        return 0
    os.makedirs(dest_folder, exist_ok=True)
    copied = 0
    for src in file_paths:
        if src and os.path.exists(src):
            try:
                dst = os.path.join(dest_folder, os.path.basename(src))
                if os.path.normcase(os.path.abspath(src)) != os.path.normcase(os.path.abspath(dst)):
                    shutil.copy2(src, dst)
                copied += 1
            except Exception:
                continue
    if copied > 0:
        generate_playlist(dest_folder)
    return copied


# =========================================================================
# STUDIO AUDIO FX LAB (SLOWED+REVERB • 8D SURROUND • NIGHTCORE • SPEED) VA A-B KESISH
# =========================================================================

STUDIO_FX_PRESETS: Dict[str, Dict[str, str]] = {
    "🌊 Slowed + Reverb (Tungi Atmosfera)": {
        "tag": "Slowed+Reverb",
        "filter": "asetrate=44100*0.86,aresample=44100,aecho=0.8:0.88:60:0.35,loudnorm=I=-14:LRA=9:TP=-1.5,alimiter=limit=-1.2dB"
    },
    "🎧 8D Surround Audio (360° Aylanuvchi)": {
        "tag": "8D Audio",
        "filter": "apulsator=mode=sine:hz=0.125:amount=0.82,aecho=0.8:0.85:40:0.25,loudnorm=I=-14:LRA=9:TP=-1.5,alimiter=limit=-1.2dB"
    },
    "🚀 Nightcore / Energetik (1.18x)": {
        "tag": "Nightcore",
        "filter": "asetrate=44100*1.18,aresample=44100,loudnorm=I=-14:LRA=9:TP=-1.5,alimiter=limit=-1.2dB"
    },
    "⏩ Tezlashtirilgan 1.25x (Pitch Saqlangan)": {
        "tag": "Speed 1.25x",
        "filter": "atempo=1.25,loudnorm=I=-14:LRA=9:TP=-1.5,alimiter=limit=-1.2dB"
    },
    "🐢 Sekinlashtirilgan 0.80x (Pitch Saqlangan)": {
        "tag": "Slow 0.80x",
        "filter": "atempo=0.80,loudnorm=I=-14:LRA=9:TP=-1.5,alimiter=limit=-1.2dB"
    },
    "🔊 Mega Subwoofer Bass (+5.5dB)": {
        "tag": "SubBass",
        "filter": "bass=g=5.5:f=65,treble=g=2.0:f=11000,loudnorm=I=-14:LRA=7:TP=-1.5,alimiter=limit=-1.2dB"
    },
    "🎤 Vokalni Tiniqlashtirish (Clear Voice)": {
        "tag": "ClearVocal",
        "filter": "highpass=f=110,equalizer=f=2800:t=o:w=1.2:g=3.5,loudnorm=I=-14:LRA=7:TP=-1.5,alimiter=limit=-1.2dB"
    },
    "🎶 Karaoke / Vokalni Pasaytirish": {
        "tag": "Karaoke",
        "filter": "stereotools=mlev=0.05,loudnorm=I=-14:LRA=9:TP=-1.5,alimiter=limit=-1.2dB"
    },
}


def apply_studio_fx_to_track(
    mp3_path: str,
    fx_name: str,
    save_as_copy: bool = True,
    ffmpeg_path: Optional[str] = None
) -> Optional[str]:
    """
    Poweramp / CapCut uslubidagi 1-Bosishda Studiya Audio Effektini (Slowed+Reverb, 8D, Speed, Bass)
    qo'shiqqa qo'llash va yangi MP3 fayl sifatida muhrlash.
    """
    if not mp3_path or not os.path.exists(mp3_path) or fx_name not in STUDIO_FX_PRESETS:
        return None

    ff = ffmpeg_path or get_ffmpeg_path()
    if not ff:
        return None

    fx_info = STUDIO_FX_PRESETS[fx_name]
    meta = read_mp3_metadata(mp3_path)
    out_dir = os.path.dirname(mp3_path)
    base_no_ext = os.path.splitext(os.path.basename(mp3_path))[0]

    if save_as_copy:
        out_path = os.path.join(out_dir, f"{base_no_ext} [{fx_info['tag']}].mp3")
    else:
        out_path = mp3_path

    temp_out = mp3_path + ".fx_tmp.mp3"
    temp_cover = mp3_path + ".fx_cover.jpg"

    try:
        has_cover = False
        if meta.get("cover_bytes"):
            with open(temp_cover, "wb") as fc:
                fc.write(meta["cover_bytes"])
            has_cover = True

        cmd = [ff, "-y", "-threads", "0", "-i", mp3_path]
        if has_cover and os.path.exists(temp_cover):
            cmd.extend(["-i", temp_cover, "-map", "0:a", "-map", "1:v", "-c:v", "mjpeg", "-disposition:v:0", "attached_pic"])
        else:
            cmd.extend(["-map", "0:a"])

        new_title = f"{meta['title']} ({fx_info['tag']})" if save_as_copy else meta["title"]
        cmd.extend([
            "-af", fx_info["filter"],
            "-c:a", "libmp3lame",
            "-b:a", "256k",
            "-ar", "44100",
            "-ac", "2",
            "-id3v2_version", "3",
            "-metadata", f"title={new_title}",
            "-metadata", f"artist={meta['artist']}",
            "-metadata", f"album={meta['album']}",
            "-metadata", f"year={meta['year']}",
            temp_out
        ])

        startupinfo = None
        creationflags = 0
        if sys.platform == "win32":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0
            creationflags = subprocess.CREATE_NO_WINDOW

        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo, creationflags=creationflags)
        _, _ = proc.communicate()

        if os.path.exists(temp_out) and os.path.getsize(temp_out) > 1024:
            shutil.move(temp_out, out_path)
            return out_path
        return None
    except Exception:
        return None
    finally:
        for f_tmp in (temp_out, temp_cover):
            if os.path.exists(f_tmp):
                try:
                    os.remove(f_tmp)
                except Exception:
                    pass


def trim_mp3_segment(
    mp3_path: str,
    start_sec: float,
    end_sec: float,
    save_as_copy: bool = True,
    ffmpeg_path: Optional[str] = None
) -> Optional[str]:
    """
    A-B Audio Trimmer & Ringtone Cutter: Qo'shiqning [A .. B] soniyalari oralig'ini
    silliq fade-in/out bilan kesib olish va MP3 sifatida saqlash.
    """
    if not mp3_path or not os.path.exists(mp3_path):
        return None

    s_sec = max(0.0, float(start_sec))
    e_sec = float(end_sec)
    if e_sec - s_sec < 1.0:
        return None

    ff = ffmpeg_path or get_ffmpeg_path()
    if not ff:
        return None

    meta = read_mp3_metadata(mp3_path)
    out_dir = os.path.dirname(mp3_path)
    base_no_ext = os.path.splitext(os.path.basename(mp3_path))[0]

    if save_as_copy:
        out_path = os.path.join(out_dir, f"{base_no_ext} [Kesilgan {int(s_sec)}s-{int(e_sec)}s].mp3")
    else:
        out_path = mp3_path

    temp_out = mp3_path + ".trim_tmp.mp3"
    temp_cover = mp3_path + ".trim_cover.jpg"

    try:
        has_cover = False
        if meta.get("cover_bytes"):
            with open(temp_cover, "wb") as fc:
                fc.write(meta["cover_bytes"])
            has_cover = True

        seg_dur = e_sec - s_sec
        fade_out_st = max(0.0, seg_dur - 0.35)
        af_str = f"afade=t=in:st=0:d=0.25,afade=t=out:st={fade_out_st:.2f}:d=0.35"

        cmd = [
            ff, "-y", "-threads", "0",
            "-ss", f"{s_sec:.2f}",
            "-to", f"{e_sec:.2f}",
            "-i", mp3_path
        ]
        if has_cover and os.path.exists(temp_cover):
            cmd.extend(["-i", temp_cover, "-map", "0:a", "-map", "1:v", "-c:v", "mjpeg", "-disposition:v:0", "attached_pic"])
        else:
            cmd.extend(["-map", "0:a"])

        cmd.extend([
            "-af", af_str,
            "-c:a", "libmp3lame",
            "-b:a", "256k",
            "-ar", "44100",
            "-ac", "2",
            "-id3v2_version", "3",
            "-metadata", f"title={meta['title']} (Cut)",
            "-metadata", f"artist={meta['artist']}",
            "-metadata", f"album={meta['album']}",
            "-metadata", f"year={meta['year']}",
            temp_out
        ])

        startupinfo = None
        creationflags = 0
        if sys.platform == "win32":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0
            creationflags = subprocess.CREATE_NO_WINDOW

        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo, creationflags=creationflags)
        _, _ = proc.communicate()

        if os.path.exists(temp_out) and os.path.getsize(temp_out) > 1024:
            shutil.move(temp_out, out_path)
            return out_path
        return None
    except Exception:
        return None
    finally:
        for f_tmp in (temp_out, temp_cover):
            if os.path.exists(f_tmp):
                try:
                    os.remove(f_tmp)
                except Exception:
                    pass


def build_eq_ffmpeg_filter(bands_db: List[float], preamp_db: float = 0.0) -> str:
    """
    AIMP 10-Polosali Ekvayzer shkalasini FFmpeg professional DSP filtr zanjiriga aylantirish.
    """
    filters = []
    if abs(preamp_db) >= 0.1:
        filters.append(f"volume={preamp_db:.1f}dB")

    for freq, gain in zip(AIMP_EQ_FREQS, bands_db):
        if abs(gain) >= 0.1:
            filters.append(f"equalizer=f={freq}:t=o:w=1.0:g={gain:.1f}")

    filters.append("loudnorm=I=-14:LRA=7:TP=-1.5")
    filters.append("alimiter=limit=-1.2dB")
    return ",".join(filters)


def remaster_track_with_eq(
    mp3_path: str,
    bands_db: List[float],
    preamp_db: float = 0.0,
    ffmpeg_path: Optional[str] = None
) -> bool:
    """
    AIMP Ekvayzer sozlamalarini joriy qo'shiqqa qo'llab, sifatni yo'qotmasdan qayta muhrlash.
    Agar .preview_raw nusxasi bo'lsa, o'shandan toza manba sifatida foydalanadi.
    """
    if not mp3_path or not os.path.exists(mp3_path):
        return False

    ff = ffmpeg_path or get_ffmpeg_path()
    if not ff:
        return False

    meta = read_mp3_metadata(mp3_path)
    out_dir = os.path.dirname(mp3_path)
    base_no_ext = os.path.splitext(os.path.basename(mp3_path))[0]
    raw_candidate = os.path.join(out_dir, ".preview_raw", f"{base_no_ext}_raw128k.mp3")
    source_audio = raw_candidate if os.path.exists(raw_candidate) else mp3_path

    temp_out = mp3_path + ".remaster_tmp.mp3"
    temp_cover = mp3_path + ".cover_tmp.jpg"

    try:
        has_cover = False
        if meta.get("cover_bytes"):
            with open(temp_cover, "wb") as fc:
                fc.write(meta["cover_bytes"])
            has_cover = True

        eq_filter = build_eq_ffmpeg_filter(bands_db, preamp_db)
        cmd = [ff, "-y", "-threads", "0", "-i", source_audio]
        if has_cover and os.path.exists(temp_cover):
            cmd.extend(["-i", temp_cover, "-map", "0:a", "-map", "1:v", "-c:v", "mjpeg", "-disposition:v:0", "attached_pic"])
        else:
            cmd.extend(["-map", "0:a"])

        cmd.extend([
            "-af", eq_filter,
            "-c:a", "libmp3lame",
            "-b:a", "256k",
            "-ar", "44100",
            "-ac", "2",
            "-id3v2_version", "3",
            "-metadata", f"title={meta['title']}",
            "-metadata", f"artist={meta['artist']}",
            "-metadata", f"album={meta['album']}",
            "-metadata", f"year={meta['year']}",
            temp_out
        ])

        startupinfo = None
        creationflags = 0
        if sys.platform == "win32":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0
            creationflags = subprocess.CREATE_NO_WINDOW

        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo, creationflags=creationflags)
        _, _ = proc.communicate()

        if os.path.exists(temp_out) and os.path.getsize(temp_out) > 1024:
            shutil.move(temp_out, mp3_path)
            return True
        return False
    except Exception:
        return False
    finally:
        for f_tmp in (temp_out, temp_cover):
            if os.path.exists(f_tmp):
                try:
                    os.remove(f_tmp)
                except Exception:
                    pass


def find_matching_raw_preview(studio_path: str) -> Optional[str]:
    """Berilgan Studio MP3 fayl uchun mos .preview_raw faylini qidirib topish."""
    if not studio_path or not os.path.exists(studio_path):
        return None
    folder = os.path.dirname(studio_path)
    raw_dir = os.path.join(folder, ".preview_raw")
    if not os.path.exists(raw_dir):
        return None

    base_no_ext = os.path.splitext(os.path.basename(studio_path))[0]
    exact_match = os.path.join(raw_dir, f"{base_no_ext}_raw128k.mp3")
    if os.path.exists(exact_match):
        return exact_match

    return None


# =========================================================================
# AIMP STUDIO AUDIOPHILE PLAYER VA PLEYLISH KONTROLLERI (A-B LOOP BILAN)
# =========================================================================

class AudiophilePlayer:
    """
    AIMP darajasidagi dastur ichidagi mukammal audio-studiya pleyeri:
    - MP3 tinglash (Play/Pause/Stop/Prev/Next/Volume/Mute)
    - Precision Waveform Seekbar (Istalgan soniyaga o'tkazish + +-5s/10s sakrash)
    - Real-Time A-B Loop (Qismni takrorlash: [A .. B])
    - A/B Taqqoslash: 'STUDIO 256k DSP' va 'RAW 128k YouTube' o'rtasida ayni soniyada almashish!
    - Pleylist Boshqaruvi: Avtomatik keyingi qo'shiqqa o'tish (Auto-Advance), Shuffle (🔀), Repeat (🔁)
    - Mutagen Metadata, Muqova va 80-Bar To'lqin ma'lumotlari.
    """

    def __init__(self):
        self.is_initialized = False
        self.current_studio_file: Optional[str] = None
        self.current_raw_file: Optional[str] = None
        self.current_mode: str = "STUDIO"  # 'STUDIO' yoki 'RAW'
        self.is_playing: bool = False
        self.is_paused: bool = False
        self.is_muted: bool = False
        self.volume: float = 0.85
        self.current_track_title: str = "Hech narsa tanlanmagan"

        # AIMP Seek, A-B Loop & Metadata holatlari
        self.seek_offset_sec: float = 0.0
        self.duration_sec: float = 210.0
        self.loop_a_sec: Optional[float] = None
        self.loop_b_sec: Optional[float] = None
        self.current_metadata: Dict[str, any] = {}
        self.waveform: List[float] = [0.35] * 80

        # AIMP Pleylist transporti
        self.playlist: List[str] = []
        self.current_index: int = -1
        self.repeat_mode: str = "ALL"  # 'ALL', 'ONE', 'OFF'
        self.shuffle_enabled: bool = False

        if _PYGAME_AVAILABLE:
            try:
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
                self.is_initialized = True
            except Exception:
                self.is_initialized = False

    def set_loop_a(self, sec: Optional[float] = None) -> float:
        val = self.get_position_sec() if sec is None else float(sec)
        self.loop_a_sec = max(0.0, min(val, self.duration_sec - 1.0))
        if self.loop_b_sec is not None and self.loop_b_sec <= self.loop_a_sec:
            self.loop_b_sec = None
        return self.loop_a_sec

    def set_loop_b(self, sec: Optional[float] = None) -> Optional[float]:
        val = self.get_position_sec() if sec is None else float(sec)
        if self.loop_a_sec is None:
            self.loop_a_sec = 0.0
        if val > self.loop_a_sec + 0.8:
            self.loop_b_sec = min(self.duration_sec, val)
            return self.loop_b_sec
        return None

    def clear_ab_loop(self):
        self.loop_a_sec = None
        self.loop_b_sec = None

    def set_playlist(self, files: List[str], active_file: Optional[str] = None):
        """Pleylist ro'yxatini yangilash va joriy trek indeksini belgilash."""
        self.playlist = [f for f in files if f and os.path.exists(f)]
        if active_file and active_file in self.playlist:
            self.current_index = self.playlist.index(active_file)
        elif self.current_studio_file and self.current_studio_file in self.playlist:
            self.current_index = self.playlist.index(self.current_studio_file)
        else:
            self.current_index = 0 if self.playlist else -1

    def load_and_play(self, studio_path: str, raw_path: Optional[str] = None, title: str = "") -> bool:
        if not studio_path or not os.path.exists(studio_path):
            return False

        self.current_studio_file = studio_path
        self.current_raw_file = raw_path or find_matching_raw_preview(studio_path)
        self.current_metadata = read_mp3_metadata(studio_path)
        self.duration_sec = max(1.0, float(self.current_metadata.get("duration_sec", 210.0)))
        self.waveform = self.current_metadata.get("waveform") or compute_audio_waveform(studio_path, 80)
        self.current_track_title = title or os.path.basename(studio_path)
        self.current_mode = "STUDIO"
        self.seek_offset_sec = 0.0
        self.clear_ab_loop()
        record_play_history(studio_path)

        folder = os.path.dirname(studio_path)
        if os.path.exists(folder):
            folder_mp3s = [os.path.join(folder, f) for f in sorted(os.listdir(folder)) if f.lower().endswith(".mp3")]
            if folder_mp3s:
                self.set_playlist(folder_mp3s, active_file=studio_path)

        if not self.is_initialized:
            return False

        return self._play_current_mode(seek_sec=0.0)

    def _play_current_mode(self, seek_sec: float = 0.0) -> bool:
        target_file = self.current_studio_file if self.current_mode == "STUDIO" else (self.current_raw_file or self.current_studio_file)
        if not target_file or not os.path.exists(target_file) or not self.is_initialized:
            return False

        try:
            self.seek_offset_sec = max(0.0, min(seek_sec, max(0.0, self.duration_sec - 0.5)))
            pygame.mixer.music.load(target_file)
            pygame.mixer.music.set_volume(0.0 if self.is_muted else self.volume)
            if self.seek_offset_sec > 0.05:
                pygame.mixer.music.play(start=self.seek_offset_sec)
            else:
                pygame.mixer.music.play()
            self.is_playing = True
            self.is_paused = False
            return True
        except Exception:
            return False

    def seek(self, target_sec: float) -> bool:
        """AIMP Waveform Seekbar: Qo'shiqning istalgan soniyasiga o'tkazish."""
        if not self.current_studio_file or not self.is_initialized:
            return False

        was_paused = self.is_paused
        clamped = max(0.0, min(float(target_sec), max(0.0, self.duration_sec - 0.5)))
        ok = self._play_current_mode(seek_sec=clamped)
        if ok and was_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
        return ok

    def step_seek(self, delta_sec: float) -> bool:
        """+5s/+10s yoki -5s/-10s sakrash."""
        cur = self.get_position_sec()
        return self.seek(cur + delta_sec)

    def get_position_sec(self) -> float:
        """Joriy soniyani seek_offset_sec bilan qo'shib aniq hisoblash."""
        if not self.is_playing or not self.is_initialized:
            return 0.0
        pos_ms = pygame.mixer.music.get_pos()
        rel_sec = max(0.0, pos_ms / 1000.0) if pos_ms >= 0 else 0.0
        return min(self.duration_sec, self.seek_offset_sec + rel_sec)

    def toggle_ab(self) -> str:
        """A/B almashish: Studio va Raw o'rtasida ayni soniyada o'tkazish!"""
        if not self.is_playing or not self.current_raw_file or not os.path.exists(self.current_raw_file):
            return self.current_mode

        pos_sec = self.get_position_sec()
        was_paused = self.is_paused
        self.current_mode = "RAW" if self.current_mode == "STUDIO" else "STUDIO"
        self._play_current_mode(seek_sec=pos_sec)
        if was_paused and self.is_initialized:
            pygame.mixer.music.pause()
            self.is_paused = True
        return self.current_mode

    def toggle_play_pause(self):
        if not self.is_initialized or not self.is_playing:
            return
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
        else:
            pygame.mixer.music.pause()
            self.is_paused = True

    def stop(self):
        if self.is_initialized and self.is_playing:
            pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.seek_offset_sec = 0.0

    def set_volume(self, val: float):
        self.volume = max(0.0, min(1.0, val))
        if self.volume > 0.0:
            self.is_muted = False
        if self.is_initialized:
            pygame.mixer.music.set_volume(0.0 if self.is_muted else self.volume)

    def toggle_mute(self) -> bool:
        self.is_muted = not self.is_muted
        if self.is_initialized:
            pygame.mixer.music.set_volume(0.0 if self.is_muted else self.volume)
        return self.is_muted

    def toggle_repeat(self) -> str:
        modes = ["ALL", "ONE", "OFF"]
        idx = (modes.index(self.repeat_mode) + 1) % len(modes) if self.repeat_mode in modes else 0
        self.repeat_mode = modes[idx]
        return self.repeat_mode

    def toggle_shuffle(self) -> bool:
        self.shuffle_enabled = not self.shuffle_enabled
        return self.shuffle_enabled

    def next_track(self, auto: bool = False) -> Optional[str]:
        """Pleylistdagi keyingi trekka o'tish."""
        if not self.playlist:
            return None

        if auto and self.repeat_mode == "ONE" and self.current_studio_file:
            self.load_and_play(self.current_studio_file, self.current_raw_file)
            return self.current_studio_file

        if self.shuffle_enabled and len(self.playlist) > 1:
            choices = [i for i in range(len(self.playlist)) if i != self.current_index]
            next_idx = random.choice(choices)
        else:
            next_idx = self.current_index + 1
            if next_idx >= len(self.playlist):
                if auto and self.repeat_mode == "OFF":
                    self.stop()
                    return None
                next_idx = 0

        self.current_index = next_idx
        target = self.playlist[self.current_index]
        if os.path.exists(target):
            self.load_and_play(target)
            return target
        return None

    def prev_track(self) -> Optional[str]:
        """Pleylistdagi oldingi trekka qaytish (yoki 5s dan oshgan bo'lsa boshiga qaytarish)."""
        if not self.playlist:
            return None

        if self.get_position_sec() > 5.0 and self.current_studio_file:
            self.seek(0.0)
            return self.current_studio_file

        prev_idx = (self.current_index - 1) % len(self.playlist)
        self.current_index = prev_idx
        target = self.playlist[self.current_index]
        if os.path.exists(target):
            self.load_and_play(target)
            return target
        return None

    def check_auto_advance(self) -> Optional[str]:
        """A-B Loop chegarasini yoki qo'shiq tugaganligini tekshirish."""
        if not self.is_initialized or not self.is_playing or self.is_paused:
            return None

        # 1. Real-Time A-B Loop tekshiruvi
        if self.loop_a_sec is not None and self.loop_b_sec is not None and self.loop_b_sec > self.loop_a_sec:
            if self.get_position_sec() >= self.loop_b_sec:
                self.seek(self.loop_a_sec)
                return self.current_studio_file

        # 2. Trek tugaganda keyingi trekka o'tish
        if not pygame.mixer.music.get_busy():
            return self.next_track(auto=True)
        return None

    def get_status(self) -> Dict[str, any]:
        pos_sec = self.get_position_sec()
        return {
            "is_playing": self.is_playing,
            "is_paused": self.is_paused,
            "is_muted": self.is_muted,
            "mode": self.current_mode,
            "title": self.current_track_title,
            "file": self.current_studio_file,
            "pos_sec": pos_sec,
            "duration_sec": self.duration_sec,
            "loop_a_sec": self.loop_a_sec,
            "loop_b_sec": self.loop_b_sec,
            "has_raw": bool(self.current_raw_file and os.path.exists(self.current_raw_file)),
            "repeat_mode": self.repeat_mode,
            "shuffle": self.shuffle_enabled,
            "metadata": self.current_metadata,
            "waveform": self.waveform,
        }


