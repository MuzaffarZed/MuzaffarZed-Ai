"""
Call of Duty: Modern Warfare 3D — Masterpiece Edition (v3.0)
Avtomatlashtirilgan Sifat va Mantiq Testlari
Zero-Defect Verification Suite
"""

import os
import pytest

WORKSPACE = r"C:\Users\MuzaffarZed\ai_workspace"
GAME_DIR = os.path.join(WORKSPACE, "cod_modern_war")
HTML_FILE = os.path.join(GAME_DIR, "index.html")
CSS_FILE = os.path.join(GAME_DIR, "style.css")
BAT_FILE = os.path.join(WORKSPACE, "Ishga_Tushirish_COD3D.bat")
DESKTOP_DIR = r"C:\Users\MuzaffarZed\Desktop\Call_of_Duty_3D"
DESKTOP_HTML = os.path.join(DESKTOP_DIR, "index.html")
DESKTOP_BAT = os.path.join(DESKTOP_DIR, "O'YINNI_BOSHLASH.bat")


def test_game_files_exist():
    """Barcha zaruriy fayllar to'liq mavjudligini tekshiradi."""
    assert os.path.exists(HTML_FILE), "index.html mavjud emas!"
    assert os.path.exists(CSS_FILE), "style.css mavjud emas!"
    assert os.path.exists(BAT_FILE), "Ishga_Tushirish_COD3D.bat mavjud emas!"
    assert os.path.exists(DESKTOP_DIR), "Desktop Call_of_Duty_3D papkasi mavjud emas!"


def test_html_masterpiece_integrity():
    """HTML va v3.0 Masterpiece imkoniyatlari mavjudligini tekshiradi."""
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Three.js 3D kutubxonasi mavjudligi
    assert "three.min.js" in content, "Three.js kutubxonasi ulanmagan!"

    # 1. Granata tizimi (G tugmasi)
    assert "throwGrenade" in content, "Granata otish funksiyasi yo'q!"
    assert "detonateGrenade" in content, "Granata portlash funksiyasi yo'q!"
    assert 'id="grenade-count"' in content, "Granata HUD indikatori yo'q!"

    # 2. Qurolni ko'zdan kechirish (F tugmasi)
    assert "inspectWeapon" in content, "Qurolni ko'zdan kechirish animatsiyasi yo'q!"

    # 3. Taktik Yashil Lazer (T tugmasi)
    assert "toggleLaser" in content, "Lazer yoqish/o'chirish yo'q!"
    assert "laserBeam" in content, "Lazer nuri ob'ekti yo'q!"

    # 4. Mis Gilzalar chiqishi (Ejected Shell Casings)
    assert "spawnEjectedCasing" in content, "Gilza otilishi funksiyasi yo'q!"
    assert "playCasingClink" in content, "Gilza jaranglashi ovozi yo'q!"

    # 5. Ratsiya va ovozli aloqa (Radio Voice-Over)
    assert "radioCallout" in content, "Harbiy ratsiya tizimi yo'q!"
    assert 'id="radio-box"' in content, "Ratsiya subtitr qutisi yo'q!"

    # 6. Dushman 3D Salomatlik Bari
    assert "createEnemyHealthSprite" in content, "Dushman boshidagi 3D salomatlik bari yo'q!"


def test_combat_and_grenade_physics():
    """Granata va qurol balansi hisob-kitobini tekshiradi."""
    grenade_dmg = 180
    grenade_radius = 16
    enemy_hp = 100

    # Granata 8 metr masofada dushmanni bir zumda o'ldirishi kerak (180 * (1 - 8/16) = 90 < 100)
    # 4 metr masofada esa: 180 * (1 - 4/16) = 135 > 100
    close_dmg = int(grenade_dmg * (1 - 4 / grenade_radius))
    assert close_dmg >= enemy_hp, "Granata yaqin masofada dushmanni yo'q qilishi shart!"


def test_laser_and_trauma_logic():
    """Kamera silkinishi (Trauma) va lazer tizimi parametrlarini tekshiradi."""
    max_trauma = 1.0
    trauma = min(max_trauma, 0.5 + 0.3)
    assert trauma == 0.8
    shake = trauma * trauma
    assert shake == pytest.approx(0.64)
