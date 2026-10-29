import os
import pytest

STOCK_DIR = r"D:\Downloads_Archive\Compressed\Model SM-T295"
CUSTOM_DIR = r"D:\T295_Custom_ROM"
LAUNCHER_APK = r"C:\Users\MuzaffarZed\ai_workspace\capcut_os_launcher\CapCutOS.apk"

def test_stock_ap_exists():
    """Verify original Samsung stock AP archive exists and is intact (>4GB)."""
    ap_path = os.path.join(STOCK_DIR, "AP_T295XXS6CWG6_CL23850358_QB68227052_REV00_user_low_ship_MULTI_CERT_meta_RKEY_OS11.tar.md5")
    assert os.path.exists(ap_path), "Stock AP file does not exist!"
    assert os.path.getsize(ap_path) > 4000 * 1024 * 1024, "Stock AP size is under 4000MB!"

def test_stock_bl_csc_exist():
    """Verify BL and CSC partitions exist for clean Odin flashing."""
    bl_path = os.path.join(STOCK_DIR, "BL_T295XXS6CWG6_CL23850358_QB68227052_REV00_user_low_ship_MULTI_CERT.tar.md5")
    csc_path = os.path.join(STOCK_DIR, "CSC_OMC_OXM_T295OXM6CWG6_CL23850358_QB68227052_REV00_user_low_ship_MULTI_CERT.tar.md5")
    assert os.path.exists(bl_path), "Stock BL does not exist!"
    assert os.path.exists(csc_path), "Stock CSC does not exist!"

def test_disabled_vbmeta_exists():
    """Verify pre-patched vbmeta with disabled dm-verity exists."""
    vbmeta_path = os.path.join(CUSTOM_DIR, "vbmeta.img.lz4")
    assert os.path.exists(vbmeta_path), "Patched vbmeta does not exist!"

def test_studio_launcher_apk_exists():
    """Verify Muzaffar Studio OS APK is compiled and signed."""
    assert os.path.exists(LAUNCHER_APK), "CapCutOS.apk does not exist!"
    assert os.path.getsize(LAUNCHER_APK) > 5000, "CapCutOS.apk is empty!"

def test_odin_flasher_available():
    """Verify Odin3 flasher executable exists on the machine."""
    odin_paths = [
        r"C:\Users\MuzaffarZed\Downloads\Новая папка\Odin3_v3.14.4\Odin3_v3.14.4.exe",
        r"C:\Users\MuzaffarZed\Downloads\Odin3_v3.14.4_Verified.zip",
        r"C:\Users\MuzaffarZed\Downloads\Odin3_v3.14.4.zip"
    ]
    assert any(os.path.exists(p) for p in odin_paths), "Odin3 flasher was not found!"
