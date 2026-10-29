"""
================================================================================
MUZAFFARZED ANTIGRAVITY AUTO-SYNC & CLOUD BACKUP MASTER ENGINE
================================================================================
Barcha loyihalar, Second Brain kognitiv xotirasi, 40+ skills va qoidalarni
avtomatik ravishda Cloud (GitHub) va Offline Portable ZIP ga zaxirala beruvchi
bosh arxitektura skripti.

Muallif: MuzaffarZed
Standart: Oliy Arxitektura Kodeksi (Zero-Defect)
"""

import os
import sys
import shutil
import zipfile
import subprocess
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(r"C:\Users\MuzaffarZed\ai_workspace")
GEMINI_CONFIG = Path.home() / ".gemini" / "config"
BACKUP_GEMINI = WORKSPACE / ".gemini_backup"
BACKUPS_DIR = WORKSPACE / "backups"
GITHUB_REPO_URL = "https://github.com/MuzaffarZed/MuzaffarZed-Ai.git"

def log(msg):
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] {msg}")

def sync_gemini_config():
    log("1. .gemini/config (Skills, Rules, Agents) zaxiralanmoqda...")
    if not GEMINI_CONFIG.exists():
        log("[!] .gemini/config topilmadi.")
        return

    os.makedirs(BACKUP_GEMINI, exist_ok=True)
    ignore_patterns = shutil.ignore_patterns(
        "node_modules", ".migrated", "backup_shortcuts", "*.tmp",
        "auth.json", "*.auth.json", "*.key", "*.token", ".env*"
    )
    
    for item in os.listdir(GEMINI_CONFIG):
        if item in ["node_modules", ".migrated", "backup_shortcuts"]:
            continue
        s = GEMINI_CONFIG / item
        d = BACKUP_GEMINI / item
        if s.is_dir():
            shutil.copytree(s, d, dirs_exist_ok=True, ignore=ignore_patterns)
        else:
            if not any(pat in item.lower() for pat in ["auth.json", ".key", ".token", ".env"]):
                shutil.copy2(s, d)

    # Clean any accidental auth.json in backup
    for f in list(BACKUP_GEMINI.rglob("*auth*.json")):
        try:
            f.unlink()
        except Exception:
            pass

    log("[+] .gemini/config muvaffaqiyatli .gemini_backup jildiga sinxronlandi (xavfsiz holda).")

def sync_second_brain():
    log("2. Second Brain va NotebookLM sinxronizatsiyasi...")
    exporter = WORKSPACE / ".agents" / "memory" / "notebooklm_exporter.py"
    if exporter.exists():
        try:
            subprocess.run([sys.executable, str(exporter)], capture_output=True, text=True, timeout=10)
            log("[+] NotebookLM manbasi yangilandi.")
        except Exception as e:
            log(f"[!] NotebookLM sinxronida xatolik: {e}")

def create_portable_zip():
    log("3. Offline Portable ZIP zaxira to'plami yaratilmoqda...")
    os.makedirs(BACKUPS_DIR, exist_ok=True)
    zip_path = BACKUPS_DIR / "MuzaffarZed_Antigravity_Portable_Backup.zip"

    # Muhim fayllarni arxivlash
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # 1. .gemini_backup
        if BACKUP_GEMINI.exists():
            for root, dirs, files in os.walk(BACKUP_GEMINI):
                for f in files:
                    fp = Path(root) / f
                    arc = fp.relative_to(WORKSPACE)
                    zf.write(fp, arc)
        
        # 2. .agents (Second brain)
        agents_dir = WORKSPACE / ".agents"
        if agents_dir.exists():
            for root, dirs, files in os.walk(agents_dir):
                for f in files:
                    fp = Path(root) / f
                    arc = fp.relative_to(WORKSPACE)
                    zf.write(fp, arc)

        # 3. Bootstrap scripts
        for s in ["bootstrap_new_pc.py", "bootstrap_new_pc.bat", "AGENTS.md", "GEMINI.md", "DESIGN.md"]:
            sp = WORKSPACE / s
            if sp.exists():
                zf.write(sp, s)

    log(f"[+] Portable ZIP tayyor: {zip_path.stat().st_size / (1024*1024):.2f} MB")

def sync_git():
    log("4. Git va GitHub Cloud sinxronizatsiyasi...")
    # Remote tekshirish
    remotes = subprocess.run(["git", "remote"], cwd=WORKSPACE, capture_output=True, text=True).stdout
    if "origin" not in remotes:
        subprocess.run(["git", "remote", "add", "origin", GITHUB_REPO_URL], cwd=WORKSPACE)
        log(f"[+] Remote 'origin' qo'shildi: {GITHUB_REPO_URL}")

    # Add & Commit
    subprocess.run(["git", "add", ".gitignore", ".gemini_backup", ".agents", "bootstrap_new_pc.*", "sync_master.py", "*.md", "*.py", "*.bat"], cwd=WORKSPACE)
    commit_msg = f"Auto-Sync: MuzaffarZed Second Brain, Skills & Projects [{datetime.now().strftime('%Y-%m-%d %H:%M')}]"
    
    commit_res = subprocess.run(["git", "commit", "-m", commit_msg], cwd=WORKSPACE, capture_output=True, text=True)
    if "nothing to commit" in commit_res.stdout:
        log("[i] Barcha o'zgarishlar allaqachon commit qilingan.")
    else:
        log(f"[+] Yangi commit yaratildi: {commit_msg}")

    # Push to dedicated branch workspace-main to ensure zero conflicts
    log("[*] GitHub bulutiga yuklanmoqda (branch: workspace-main)...")
    push_res = subprocess.run(["git", "push", "-u", "origin", "HEAD:workspace-main"], cwd=WORKSPACE, capture_output=True, text=True, timeout=60)
    if push_res.returncode == 0:
        log("[MUVAFFAQIYAT] Barcha loyihalar, xotira va skills GitHub'ga yuklandi!")
    else:
        log(f"[!] Push natijasi: {push_res.stderr.strip()[:200]}")

def main():
    print("=" * 70)
    print("   MUZAFFARZED ANTIGRAVITY AUTO-SYNC & CLOUD BACKUP MASTER   ")
    print("=" * 70)
    sync_gemini_config()
    sync_second_brain()
    create_portable_zip()
    sync_git()
    print("=" * 70)
    print("   BARCHA VARIANTLAR (GITHUB + OFFLINE ZIP + BOOTSTRAP) TAYYOR!   ")
    print("=" * 70)

if __name__ == "__main__":
    main()
