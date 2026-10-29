"""
Brightness Sync Service Entrypoint.
Boshqaruv, Tizim Patnisi (Tray) va Fonda Ishga Tushirish skripti.
"""

import sys
import os
import argparse
import logging
import signal

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

# Ensure safe UTF-8 output and pythonw.exe compatibility
LOG_FILE = os.path.join(CURRENT_DIR, "brightness_sync.log")

if sys.platform == "win32":
    import io

    if sys.stdout is not None:
        try:
            sys.stdout = io.TextIOWrapper(
                sys.stdout.buffer, encoding="utf-8", errors="replace"
            )
        except Exception:
            pass
    else:
        sys.stdout = open(os.devnull, "w", encoding="utf-8")

    if sys.stderr is not None:
        try:
            sys.stderr = io.TextIOWrapper(
                sys.stderr.buffer, encoding="utf-8", errors="replace"
            )
        except Exception:
            pass
    else:
        sys.stderr = open(os.devnull, "w", encoding="utf-8")

from core.controller import BrightnessController
from core.sync_daemon import BrightnessSyncDaemon
from core.config import ConfigManager
from ui.tray import BrightnessTrayApp

CONFIG_FILE = os.path.join(CURRENT_DIR, "config.json")
ICON_FILE = os.path.join(CURRENT_DIR, "assets", "brightness.ico")


def setup_logger(verbose: bool = False):
    level = logging.DEBUG if verbose else logging.INFO
    handlers = [
        logging.FileHandler(LOG_FILE, encoding="utf-8", mode="a")
    ]
    # Agar haqiqiy konsol mavjud bo'lsa, konsolga ham chiqaramiz
    if sys.stderr is not None and hasattr(sys.stderr, "write"):
        handlers.append(logging.StreamHandler(sys.stderr))

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
        handlers=handlers,
    )


def show_status(controller: BrightnessController, config: ConfigManager):
    status = controller.get_status()
    print("=" * 60)
    print("             MONITOR YORUG'LIK HOLATI")
    print("=" * 60)

    laptop = status.get("laptop_brightness")
    print(
        f" [Noutbuk Ichki Ekrani] : {laptop}%"
        if laptop is not None
        else " [Noutbuk] : Aniqlanmadi"
    )

    externals = status.get("external_monitors", [])
    if externals:
        for ext in externals:
            print(
                f" [Tashqi Monitor #{ext['index'] + 1}]  : {ext['description']} -> {ext['current']}% (Min: {ext['min']}%, Max: {ext['max']}%)"
            )
    else:
        print(" [Tashqi Monitor]       : DDC/CI qo'llab-quvvatlovchi monitor topilmadi")

    in_sync = False
    if laptop is not None and externals:
        target_ext = config.calculate_external(laptop)
        in_sync = all(ext["current"] == target_ext for ext in externals)

    sync_str = "[OK] BIR XIL (Sinxron)" if in_sync else "[!] HAR XIL (Sinxron emas)"
    print(f" Holat                   : {sync_str}")
    print(f" Avtomatik Sinxronlash   : {'[YOQILGAN]' if config.get('sync_enabled', True) else '[OCHIRILGAN]'}")
    print(f" Rejim                   : {config.get('mode', 'mirror')} (Minimum: {config.get('min_brightness', 0)}%)")
    print(f" Mayin O'tish (Smooth)   : {'[HA]' if config.get('smooth_transition', False) else '[YOQ]'}")
    print("=" * 60)


def run_headless_daemon(controller: BrightnessController, config: ConfigManager):
    daemon = BrightnessSyncDaemon(
        config=config,
        controller=controller,
        on_sync_callback=lambda lvl, cnt: print(
            f"[SYNC] Noutbuk yorug'ligi {lvl}% -> Tashqi monitor yangilandi ({cnt} ta)."
        ),
    )

    def handle_exit(sig, frame):
        print("\n[STOP] To'xtatish buyrug'i qabul qilindi...")
        daemon.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    print("=======================================================")
    print("  NOUTBUK VA TASHQI MONITOR SINXRONIZATORI ISHGA TUSHDI")
    print("=======================================================")
    print(f" Tekshiruv intervali : {config.get('interval', 0.35)} soniya")
    print(" Noutbuk yorug'ligi o'zgarganda tashqi monitor birga o'zgaradi.")
    print(" To'xtatish uchun: Ctrl + C bosing.")
    print("-------------------------------------------------------")

    daemon.start(non_blocking=False)


def run_tray_app(controller: BrightnessController, config: ConfigManager):
    daemon = BrightnessSyncDaemon(
        config=config,
        controller=controller,
    )
    tray = BrightnessTrayApp(
        controller=controller,
        daemon=daemon,
        config=config,
        icon_path=ICON_FILE,
    )
    tray.run()


def main():
    parser = argparse.ArgumentParser(
        description="Noutbuk va tashqi monitor yorug'ligini avtomatik sinxronlash tizimi"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Hozirgi yorug'lik holatini ko'rsatish",
    )
    parser.add_argument(
        "--sync-now",
        action="store_true",
        help="Hozirning o'zida bir martalik sinxronizatsiya qilish",
    )
    parser.add_argument(
        "--set",
        type=int,
        metavar="LEVEL",
        help="Ikkala monitor yorug'ligini belgilangan foizga o'rnatish (0-100)",
    )
    parser.add_argument(
        "--daemon",
        action="store_true",
        help="Tray belgisisiz, faqat orqa fonda ishlash",
    )
    parser.add_argument(
        "--tray",
        action="store_true",
        help="Windows vazifalar panelida Tray belgisi bilan ishlash",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Batafsil loglarni chiqarish"
    )

    args = parser.parse_args()
    setup_logger(args.verbose)

    config = ConfigManager(CONFIG_FILE)
    controller = BrightnessController()

    if args.status:
        show_status(controller, config)
    elif args.sync_now:
        laptop_lvl = controller.get_laptop_brightness()
        if laptop_lvl is not None:
            target_ext = config.calculate_external(laptop_lvl)
            updated = controller.set_external_brightness(target_ext)
            print(
                f"[OK] Sinxronlandi: Noutbuk ({laptop_lvl}%) -> Tashqi monitor ({target_ext}%, {updated} ta)."
            )
        else:
            print("[!] Noutbuk yorug'ligini aniqlab bo'lmadi.")
    elif args.set is not None:
        lvl = max(0, min(100, args.set))
        controller.set_all_brightness(lvl)
        print(f"[OK] Ikkala monitor yorug'ligi {lvl}% ga muvaffaqiyatli o'rnatildi.")
    else:
        # Uzluksiz rejim (Daemon yoki Tray) uchun yagona nusxa (Single-Instance Mutex) tekshiruvi
        import win32event, win32api, winerror

        mutex = win32event.CreateMutex(
            None, False, "BrightnessSync_SingleInstance_Mutex"
        )
        if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
            print("[INFO] Xizmat allaqachon orqa fonda ishlab turibdi.")
            sys.exit(0)

        if args.daemon:
            run_headless_daemon(controller, config)
        else:
            run_tray_app(controller, config)


if __name__ == "__main__":
    main()
