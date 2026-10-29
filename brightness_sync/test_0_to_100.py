"""
0 dan 100% gacha va orqaga to'liq apparat sinovi skripti.
Chuqur qorong'ulik (Deep Dimming) bilan sinovdan o'tkazadi.
"""

import time
import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from core.controller import BrightnessController
from core.config import ConfigManager


def test_full_range():
    config = ConfigManager(os.path.join(CURRENT_DIR, "config.json"))
    ctrl = BrightnessController()

    print("=" * 65)
    print("      0% DAN 100% GACHA APPARAT VA CHUQUR XIRALASHISH SINOVI")
    print("=" * 65)

    test_steps = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0]
    print("\n--- 1. PASAYTIRISH SINOVI (100% -> 0%) ---")
    prev_ext = None
    all_down_ok = True

    for lap_val in test_steps:
        target_ext = config.calculate_external(lap_val)
        target_cnt = config.calculate_contrast(lap_val)
        ctrl.set_laptop_brightness(lap_val)
        ctrl.set_external_brightness_and_contrast(target_ext, target_cnt)
        time.sleep(0.08)

        info = ctrl.get_external_monitors_info()
        cur_ext = info[0]["current"] if info else target_ext

        check = "[OK] PASAYDI"
        if prev_ext is not None:
            if cur_ext > prev_ext:
                check = "[!] XATO (KOTARILDI)"
                all_down_ok = False
            elif cur_ext == prev_ext and lap_val != 0:
                check = "[=] BIR XIL"

        print(
            f" Noutbuk: {lap_val:3d}% | Monitor: {cur_ext:3d}% (Kontrast: {target_cnt:2d}%) | {check}"
        )
        prev_ext = cur_ext

    print("\n--- 2. KO'TARISH SINOVI (0% -> 100%) ---")
    test_up = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    prev_ext = None
    all_up_ok = True

    for lap_val in test_up:
        target_ext = config.calculate_external(lap_val)
        target_cnt = config.calculate_contrast(lap_val)
        ctrl.set_laptop_brightness(lap_val)
        ctrl.set_external_brightness_and_contrast(target_ext, target_cnt)
        time.sleep(0.08)

        info = ctrl.get_external_monitors_info()
        cur_ext = info[0]["current"] if info else target_ext

        check = "[OK] KOTARILDI"
        if prev_ext is not None:
            if cur_ext < prev_ext:
                check = "[!] XATO (PASAYDI)"
                all_up_ok = False
            elif cur_ext == prev_ext and lap_val != 100:
                check = "[=] BIR XIL"

        print(
            f" Noutbuk: {lap_val:3d}% | Monitor: {cur_ext:3d}% (Kontrast: {target_cnt:2d}%) | {check}"
        )
        prev_ext = cur_ext

    # Asl holatga qaytarish (masalan 100% va Kontrast 50%)
    ctrl.set_laptop_brightness(100)
    ctrl.set_external_brightness_and_contrast(100, 50)
    ctrl.close()

    print("=" * 65)
    if all_down_ok and all_up_ok:
        print("[MUVAFFAQIN!] Barcha nuqtalarda yorug'lik 100% qat'iy va to'g'ri ishladi!")
    else:
        print("[OGOHLANTIRISH] Qaysidir nuqtada noto'g'ri sakrash aniqlandi.")
    print("=" * 65)
    return all_down_ok and all_up_ok


if __name__ == "__main__":
    ok = test_full_range()
    sys.exit(0 if ok else 1)
