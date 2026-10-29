"""
scratch/live_torture_test.py — Live Real-Time Torture & Endurance Test on Windows OS
Runs actual live system commands without mocks to verify 100% operational resilience.
"""

import sys
import time
from pathlib import Path

if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        ctypes.windll.kernel32.SetConsoleCP(65001)
    except Exception:
        pass
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

# Ensure project root in sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from bridge.windows_controller import WindowsController

def run_live_torture():
    print("=" * 80)
    print("       JARVIS LIVE RESILIENCE & OS ENDURANCE TORTURE TEST")
    print("=" * 80)
    
    controller = WindowsController()
    
    # 1. High-frequency telemetry polling
    print("\n[TEST 1/6] 10x Tezkor Telemetriya So'rovi...")
    t0 = time.time()
    for i in range(10):
        t = controller.get_system_telemetry()
        assert t["cpu_percent"] >= 0.0
        assert t["ram_percent"] > 0.0
    elapsed = time.time() - t0
    print(f"  --> MUVAFFAQ QILINDI! (10 ta so'rov {elapsed:.2f} soniyada yakunlandi)")
    print(f"      Hozirgi holat: CPU {t['cpu_percent']}%, RAM {t['ram_percent']}%, Batareya {t['battery_percent']}%")

    # 2. Window enumeration and active window verification
    print("\n[TEST 2/6] Real Ish Stoli Oynalarini Qayta-Qayta Tahlil Qilish...")
    t0 = time.time()
    for i in range(5):
        wins = controller.list_windows()
        assert len(wins) > 0, "Hech bo'lmasa 1 ta oyna topilishi kerak edi!"
    elapsed = time.time() - t0
    active = controller.get_active_window()
    print(f"  --> MUVAFFAQ QILINDI! ({len(wins)} ta oyna topildi, vaqt: {elapsed:.2f}s)")
    print(f"      Faol oyna: '{active.title if active else 'Yoq'}' (PID: {active.pid if active else 0})")

    # 3. Phantom window resistance
    print("\n[TEST 3/6] Mavjud Bo'lmagan Oynalar Bilan Siklik Sinov...")
    ghost_ok = controller.focus_window("Mavjud_Bolmagan_Arvoh_Oyna_99999")
    assert ghost_ok is False, "Mavjud bo'lmagan oyna topilmasligi kerak!"
    ghost_close = controller.close_window("Mavjud_Bolmagan_Arvoh_Oyna_99999")
    assert ghost_close is False, "Mavjud bo'lmagan oyna yopilmasligi kerak!"
    print("  --> MUVAFFAQ QILINDI! Xatoliklar xavfsiz filtrlandi.")

    # 4. Unicode & Clipboard Safety
    print("\n[TEST 4/6] O'zbek Tili Diakritik Harflari va Unicode Xavfsizligi...")
    test_text = "O‘zbekiston kelajagi buyuk davlat! G‘alaba, shiddat, cho‘qqi, mo‘jiza. 🎯🚀"
    type_ok = controller.type_text(test_text)
    assert type_ok is True
    import pyperclip
    clip_content = pyperclip.paste()
    assert clip_content == test_text, f"Clipboard buzildi: {clip_content}"
    print(f"  --> MUVAFFAQ QILINDI! Matn 100% o'zgarmasdan saqlandi: '{clip_content[:45]}...'")

    # 5. Live Screen Perception
    print("\n[TEST 5/6] Jonli Ekranni Suratga Olish (DPI-Aware Capture)...")
    t0 = time.time()
    res = controller.capture_screen()
    assert res["success"] is True, f"Ekran olinmadi: {res}"
    elapsed = time.time() - t0
    print(f"  --> MUVAFFAQ QILINDI! Ekran o'lchami: {res['width']}x{res['height']}, Vaqt: {elapsed:.2f}s")
    print(f"      Fayl: {res['file_path']}")

    # 6. PowerShell Execution
    print("\n[TEST 6/6] PowerShell Tizim Integratsiyasi...")
    ps_res = controller.run_powershell("Get-Date -Format 'yyyy-MM-dd HH:mm:ss'")
    assert ps_res["success"] is True
    print(f"  --> MUVAFFAQ QILINDI! Windows vaqti: {ps_res['stdout']}")

    print("\n" + "=" * 80)
    print("🎉 BARCHA JONLI SINTOVLAR 100% NUQSONSIZ VA BENUQSON YAKUNLANDI!")
    print("=" * 80)

if __name__ == "__main__":
    run_live_torture()
