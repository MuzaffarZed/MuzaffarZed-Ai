import os
import json
from datetime import datetime

VAULT_PATH = os.path.expanduser(r"~/.gemini/config/muzaffarzed_vault.json")

DEFAULT_VAULT = {
    "architect": "MuzaffarZed",
    "user_title": "janob Muzaffar",
    "standard": "Zero-Beta, Zero-Defect",
    "signature": "by MuzaffarZed",
    "games": [
        {"name": "Mafia 2", "exe": r"D:\KANPIYUTER O'YINLARI\Mafia 2\pc\mafia2.exe"},
        {"name": "Blur", "exe": r"D:\KANPIYUTER O'YINLARI\Blur\Blur.exe"},
        {"name": "Firewatch", "exe": r"D:\KANPIYUTER O'YINLARI\Firewatch\Firewatch.exe"},
        {"name": "Saints Row: The Third", "exe": r"D:\KANPIYUTER O'YINLARI\Saints Row The Third\saintsrowthethird.exe"},
        {"name": "Total Overdose", "exe": r"D:\KANPIYUTER O'YINLARI\Total Overdose\TOD.exe"},
        {"name": "Euro Truck Simulator", "exe": r"D:\KANPIYUTER O'YINLARI\Euro Truck Simulator\game.exe"},
        {"name": "Need for Speed: Most Wanted", "exe": r"D:\KANPIYUTER O'YINLARI\Speed rof Deen Wast Monted\Speed for Deen Wast Monted.exe"},
        {"name": "FlatOut 2", "exe": r"D:\KANPIYUTER O'YINLARI\FlatOut2\FlatOut2.exe"},
        {"name": "Counter-Strike 1.6", "exe": r"D:\KANPIYUTER O'YINLARI\CS 1.6 Champ\CS 1.6\1.6.exe"},
        {"name": "Generals - Reloaded Fire", "exe": r"D:\KANPIYUTER O'YINLARI\ReloadedFire\generals.exe"},
        {"name": "GTA Vice City (Deluxe)", "exe": r"D:\KANPIYUTER O'YINLARI\GTA Vice City - Deluxe\gta-vc.exe"},
        {"name": "GTA Vice City (Matrix)", "exe": r"D:\KANPIYUTER O'YINLARI\GTA-Vice City MATRIX\GTA-9MATRIX.exe"},
        {"name": "Mortal Kombat 3", "exe": r"D:\KANPIYUTER O'YINLARI\Mortol  kombat\MK3W.EXE"},
    ],
    "learned_lessons": [
        "Never leave broken white sheet icons on Desktop",
        "Clean all cartoon casual games as per user's strict taste",
        "Never run multi-line powershell -Command that hangs on stdin (Use NonInteractive or Python)",
        "Always verify Desktop with windows_capture_screen before reporting completion",
        "Always address as janob Muzaffar and include by MuzaffarZed signature"
    ],
    "history": []
}

def load_vault():
    if os.path.exists(VAULT_PATH):
        try:
            with open(VAULT_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    save_vault(DEFAULT_VAULT)
    return DEFAULT_VAULT

def save_vault(data):
    os.makedirs(os.path.dirname(VAULT_PATH), exist_ok=True)
    with open(VAULT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def log_event(event_text):
    vault = load_vault()
    entry = {
        "timestamp": datetime.now().isoformat(),
        "event": event_text
    }
    vault["history"].append(entry)
    save_vault(vault)

if __name__ == "__main__":
    v = load_vault()
    print("MuzaffarZed Vault initialized successfully!")
    print(f"Total Games tracked: {len(v['games'])}")
    print(f"Lessons memorized: {len(v['learned_lessons'])}")
