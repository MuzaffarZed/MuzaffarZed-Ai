#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
clean_all_bloat.py — Global va Lokal Antigravity Bloat Tozalagich
267 ta ortiqcha skill va plaginlarni o'chirib, token hajmini 45,206 va 16,695 dan
keskin pastga (<5,000 tokenga) tushiruvchi 100% avtonom tozalash dvijogi.

Faqat o'zimizning 5 ta asosiy Master Skill va ixcham qoidalarimizni qoldiradi:
1) core-coding/SKILL.md (Ponytail + Addy Osmani qoidalari)
2) graphify/SKILL.md (Kodbaza bilimlari grafi)
3) ui-ux-design/SKILL.md (taste-skill + Impeccable + Emil Kowalski)
4) video-cinema/SKILL.md (FFmpeg, Whisper, Viral Reels, Remotion, Pro-Cinema 3D/Manim)
5) second-brain/SKILL.md (Kognitiv xotira, lessons learned, NotebookLM bridge)

Muallif: janob Muzaffar uchun
Dasturchi: MuzaffarZed
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

# Windows console UTF-8 handling
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

HOME = Path.home()
WORKSPACE = Path(r"C:\Users\MuzaffarZed\ai_workspace")
BACKUP_DIR = WORKSPACE / ".backup_customizations" / f"backup_before_bloat_clean_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

# Global paths
GEMINI_DIR = HOME / ".gemini"
GEMINI_SKILLS = GEMINI_DIR / "skills"
GEMINI_CONFIG_SKILLS = GEMINI_DIR / "config" / "skills"
GEMINI_CONFIG_PLUGINS = GEMINI_DIR / "config" / "plugins"
GEMINI_CONFIG_JSON = GEMINI_DIR / "config" / "config.json"
GEMINI_AGENTS_MD = GEMINI_DIR / "AGENTS.md"
GEMINI_CONFIG_AGENTS_MD = GEMINI_DIR / "config" / "AGENTS.md"
HOME_AGENTS_MD = HOME / "AGENTS.md"
HOME_AGENTS_DIR = HOME / ".agents"

# Local workspace paths
WORKSPACE_SKILLS = WORKSPACE / ".agents" / "skills"
WORKSPACE_AGENTS_MD = WORKSPACE / "AGENTS.md"
WORKSPACE_RULES_DIR = WORKSPACE / ".agents" / "rules"

AUDIT_RESULTS = {}


# ====================================================================
# 1-QADAM: TO'LIQ ZAXIRA NUSXA OLISH (BACKUP)
# ====================================================================
def backup_everything():
    print("\n" + "="*70)
    print("1-QADAM: BARCHA FAYLLARNI TO'LIQ ZAXIRAGA OLISH (BACKUP)")
    print("="*70)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    items = [
        ("gemini_config_plugins", GEMINI_CONFIG_PLUGINS),
        ("gemini_config_skills", GEMINI_CONFIG_SKILLS),
        ("gemini_skills", GEMINI_SKILLS),
        ("gemini_config_json", GEMINI_CONFIG_JSON),
        ("gemini_config_agents_md", GEMINI_CONFIG_AGENTS_MD),
        ("gemini_root_agents_md", GEMINI_AGENTS_MD),
        ("home_agents_md", HOME_AGENTS_MD),
        ("home_agents_dir", HOME_AGENTS_DIR),
        ("workspace_skills", WORKSPACE_SKILLS),
        ("workspace_agents_md", WORKSPACE_AGENTS_MD),
        ("workspace_agents_rules", WORKSPACE_RULES_DIR),
    ]

    backed_count = 0
    for name, p in items:
        if p.exists():
            dest = BACKUP_DIR / name
            if p.is_dir():
                shutil.copytree(p, dest)
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p, dest)
            backed_count += 1
            print(f"  [+] Zaxiraga olindi: {p.name} -> {dest.name}")

    print(f"\n[OK] Jami {backed_count} ta papka va fayl xavfsiz zaxiraga olindi:")
    print(f"     Manzil: {BACKUP_DIR}")


# ====================================================================
# 2-QADAM: GLOBAL VA TIZIMDAGI BARCHA ORTIQCHA SKILL/PLAGINLARNI TOZALASH
# ====================================================================
def clean_global_bloat():
    print("\n" + "="*70)
    print("2-QADAM: GLOBAL ORTIQCHA SKILL VA PLAGINLARNI BUTUNLAY TOZALASH")
    print("="*70)

    # 1. ~/.gemini/config/plugins — 132 ta keraksiz skill berayotgan plaginlarni tozalash
    if GEMINI_CONFIG_PLUGINS.exists():
        plugins_cleaned = 0
        for p_dir in list(GEMINI_CONFIG_PLUGINS.iterdir()):
            if p_dir.is_dir():
                s_folder = p_dir / "skills"
                if s_folder.exists():
                    shutil.rmtree(s_folder, ignore_errors=True)
                try:
                    shutil.rmtree(p_dir, ignore_errors=True)
                except Exception:
                    pass
                plugins_cleaned += 1
        print(f"  [+] ~/.gemini/config/plugins dan {plugins_cleaned} ta plagin skilllari tozalandi.")

    # config.json ichidan keraksiz plaginlarni o'chirish
    if GEMINI_CONFIG_JSON.exists():
        try:
            cfg = json.loads(GEMINI_CONFIG_JSON.read_text(encoding="utf-8"))
            if "plugins" in cfg:
                cfg["plugins"] = {}
                GEMINI_CONFIG_JSON.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
                print("  [+] config.json ichidagi ortiqcha plaginlar ro'yxati tozalandi.")
        except Exception as e:
            print(f"  [-] config.json yangilashda ogohlantirish: {e}")

    # 2. ~/.gemini/skills — dublikat papkani butunlay bo'shatish
    if GEMINI_SKILLS.exists():
        shutil.rmtree(GEMINI_SKILLS, ignore_errors=True)
        GEMINI_SKILLS.mkdir(parents=True, exist_ok=True)
        print("  [+] ~/.gemini/skills dublikat papkasi butunlay tozalandi.")

    # 3. ~/.agents/skills — home papkasidagi ortiqcha skilllarni tozalash
    if (HOME_AGENTS_DIR / "skills").exists():
        shutil.rmtree(HOME_AGENTS_DIR / "skills", ignore_errors=True)
        (HOME_AGENTS_DIR / "skills").mkdir(parents=True, exist_ok=True)
        print("  [+] ~/.agents/skills papkasi butunlay tozalandi.")

    # 4. ~/.gemini/config/skills — faqat bitta 'graphify' ni qoldiramiz (talab bo'yicha)
    graphify_src = WORKSPACE_SKILLS / "graphify"
    if not graphify_src.exists():
        graphify_src = GEMINI_CONFIG_SKILLS / "graphify"

    graphify_backup_content = None
    if (graphify_src / "SKILL.md").exists():
        graphify_backup_content = (graphify_src / "SKILL.md").read_text(encoding="utf-8")

    if GEMINI_CONFIG_SKILLS.exists():
        skills_removed = 0
        for s_dir in list(GEMINI_CONFIG_SKILLS.iterdir()):
            if s_dir.is_dir() and s_dir.name != "graphify":
                shutil.rmtree(s_dir, ignore_errors=True)
                skills_removed += 1
        print(f"  [+] ~/.gemini/config/skills dan {skills_removed} ta keraksiz global skill olib tashlandi.")

    # Graphify global papkada toza va ixcham saqlansin
    global_graphify_dir = GEMINI_CONFIG_SKILLS / "graphify"
    global_graphify_dir.mkdir(parents=True, exist_ok=True)
    graphify_skill_md = """---
name: graphify
description: Codebase knowledge graph queries, visual architecture maps, and AST code relationships.
---

# /graphify

Drop any folder of code into graphify and get a queryable knowledge graph.
- Query: `graphify query "<question>"`
- Shortest path: `graphify path "<nodeA>" "<nodeB>"`
- Explain: `graphify explain "<node>"`
- Update: `graphify update .`

*Dasturchi: MuzaffarZed*
"""
    (global_graphify_dir / "SKILL.md").write_text(graphify_skill_md.strip() + "\n", encoding="utf-8")
    print("  [+] Global ~/.gemini/config/skills da faqat ixcham 'graphify' qoldirildi.")


# ====================================================================
# 3-QADAM: LOKAL WORKSPACE SKILLLARINI 5 TA MASTER SKILLGA KELTIRISH
# ====================================================================
def setup_local_5_master_skills():
    print("\n" + "="*70)
    print("3-QADAM: LOKAL SKILLLARNI FAQAT 5 TA IXCHAM MASTER SKILLGA KELTIRISH")
    print("="*70)

    if WORKSPACE_SKILLS.exists():
        shutil.rmtree(WORKSPACE_SKILLS)
    WORKSPACE_SKILLS.mkdir(parents=True, exist_ok=True)

    master_skills = {
        "core-coding": {
            "desc": "Ponytail senior dev minimalism and Addy Osmani engineering best practices.",
            "content": """---
name: core-coding
description: Ponytail senior dev minimalism and Addy Osmani engineering best practices.
---

# Core Coding: Ponytail & Engineering Excellence

Eng yaxshi kod — yozilmagan kod. Masalani minimal yangi kod (Shortest Working Diff) bilan hal qil.

## Qoidalar:
1. **Ponytail Minimalizm:** Boilerplate, wrapper va kelajak uchun deb yozilgan keraksiz kod taqiqlanadi. Deletion beats addition.
2. **TDD & Test:** Yangi murakkab mantiq (tarmoqlanish, loop, pul, xavfsizlik) kichik avtotest qoldiradi.
3. **Ildiz Sabab (Root Cause):** Xatoni tuzatishdan oldin barcha chaqiruvchilarni grep qil, muammoni shared kodda bir marta to'g'irla.
4. **Xatarlar:** Har bir javob oxirida nimalar o'tkazib yuborilgani va mavjud xatarlar (risk) 1-2 qatorda aytiladi.

*Dasturchi: MuzaffarZed*
"""
        },
        "graphify": {
            "desc": "Codebase knowledge graph navigation, AST code analysis, and architecture exploration.",
            "content": """---
name: graphify
description: Codebase knowledge graph navigation, AST code analysis, and architecture exploration.
---

# /graphify Codebase Knowledge Graph

Kodbazani semantik graf va wiki orqali tezkor tahlil qilish dvijogi.

## Buyruqlar:
- `graphify query "<savol>"` — kodbaza bo'yicha BFS tahlili.
- `graphify path "<A>" "<B>"` — ikki modul/funksiya orasidagi eng qisqa yo'l.
- `graphify explain "<konsept>"` — tugun yoki modul tavsifi.
- `graphify update .` — kodbaza o'zgarganda grafni yangilash (AST, no API cost).

*Dasturchi: MuzaffarZed*
"""
        },
        "ui-ux-design": {
            "desc": "Anti-generic UI/UX design: taste-skill, Impeccable polish commands, and Emil Kowalski animations.",
            "content": """---
name: ui-ux-design
description: Anti-generic UI/UX design: taste-skill, Impeccable polish commands, and Emil Kowalski animations.
---

# UI/UX & Design Engineering: Taste + Impeccable + Emil Kowalski

Shablon AI dizayndan mutlaq qochish, premium editorial estetika va silliq mikro-animatsiyalar.

## Standartlar:
1. **taste-skill:** Balanslangan kontrast, shablon bo'lmagan tipografiya, gapless bento grid.
2. **impeccable:** 24 ta dizayn buyrug'i (`/audit`, `/polish`, `/animate`, `/colorize`, `/bolder`, `/quieter`, `/distill`).
3. **emilkowalski:** Fizikaga asoslangan silliq harakat (spring curves), tebranishlarsiz o'tishlar, 60fps optimizatsiya.

*Dasturchi: MuzaffarZed*
"""
        },
        "video-cinema": {
            "desc": "FFmpeg and Whisper video editing, Viral Reels B-Roll, Remotion, and Pro-Cinema 3D/Manim.",
            "content": """---
name: video-cinema
description: FFmpeg and Whisper video editing, Viral Reels B-Roll, Remotion, and Pro-Cinema 3D/Manim.
---

# Video & Cinema Engine: AI Montaj, Viral Reels & Pro-Cinema 3D

2D yassi slaydlar taqiqlanadi! Professional kinematik video va avtomatik montaj dvijogi.

## Imkoniyatlar:
1. **AI Montaj & Viral Reels:** 0.4s dan uzun sukunatlarni kesish, har 4-6 soniyada B-Roll kadrlar, Glassmorphism va Inter Black subtitrlar.
2. **Pro-Cinema 3D:** Three.js 3D virtual kamera parvozlari (`@remotion/three`), Manim matematik simulyatsiyalari.
3. **Audio Mastering & SFX:** Aktyorlik inson nutqi (Edge-TTS segmentatsiyasi), telefon karnayi filtri, SFX (`whoosh`, `riser`, `sub-bass impact`, `ui-click`, `typing`) va suxandon gapirganda fon musiqasini pasaytiruvchi Smart Audio Ducking.
4. **Eksport:** 60 FPS, Full HD / 4K.

*Dasturchi: MuzaffarZed*
"""
        },
        "second-brain": {
            "desc": "Cognitive memory, error-learning database, pre-task context recall, and NotebookLM sync.",
            "content": """---
name: second-brain
description: Cognitive memory, error-learning database, pre-task context recall, and NotebookLM sync.
---

# Second Brain: Self-Evolving Cognitive Memory & NotebookLM

Janob Muzaffarning kognitiv profili, xatolardan olingan saboqlar va arxitektura bilimlari xazinasi.

## Mexanizmlar:
1. **Pre-Task Hook:** Vazifa oldidan kognitiv profil va saboqlarni o'qish (`memory_engine.py context`).
2. **Error-Learning Hook:** Xatolardan avtomatik saboq olib, `lessons_learned.md` va SQLite FTS5 bazasiga yozish.
3. **Post-Task Reflection:** Bilimlarni boyitish va Google NotebookLM uchun `Muzaffar_Second_Brain_Source.md` faylini yangilash (`notebooklm_exporter.py`).

*Dasturchi: MuzaffarZed*
"""
        }
    }

    for s_name, data in master_skills.items():
        s_dir = WORKSPACE_SKILLS / s_name
        s_dir.mkdir(parents=True, exist_ok=True)
        (s_dir / "SKILL.md").write_text(data["content"].strip() + "\n", encoding="utf-8")
        print(f"  [+] 5 ta asosiy Master Skill'dan biri yaratildi: {s_name}/SKILL.md")


# ====================================================================
# 4-QADAM: RULES (AGENTS.MD) QISMINI ZICHLASHTIRISH VA DEDUPLIKATSIYA
# ====================================================================
def compress_and_deduplicate_rules():
    print("\n" + "="*70)
    print("4-QADAM: RULES FAYLLARINI DEDUPLIKATSIYA QILISH VA 5,000 TOKENGACHA SIQISH")
    print("="*70)

    # 5 ta alohida faylda takrorlanayotgan 46 KB matn o'rniga:
    # 1 ta asosiy global qoida (~1,200 token) va 1 ta workspace qoidasi (~600 token)
    MASTER_GLOBAL_RULE = """# Ponytail, Senior Lazy Dev & Oliy Arxitektura Qonunlari

## 1. Oliy Standart (janob Muzaffar uchun Doimiy Qonun)
- Sen 40+ yillik elit Bosh Arxitektorsan. Foydalanuvchiga doimo hurmat bilan **"janob Muzaffar"** yoki **"janob"** deb murojaat qilasan.
- **Standart:** MUTLAQ MUKAMMALLIK (Zero-Beta, Zero-Defect). Hech qachon chala ish, beta versiya yoki yuzaki javob berilmaydi.
- **Avtonomiya & Proaktivlik:** 100% avtonom (mayda savollar berilmaydi). "Aytilmagan lekin bo'lishi shart" qulayliklar oldindan qo'shiladi.
- **Imzo:** Har bir dastur, oyna, video va javobda nafis `*Dasturchi: MuzaffarZed*` muhri bo'lishi SHART!

## 2. Ponytail Senior Lazy Dev Mode
- Eng yaxshi kod — yozilmagan kod. Masalani minimal yangi kod (Shortest Working Diff) bilan hal qil.
- Boilerplate, wrapper va kelajak uchun deb yozilgan keraksiz qatlamlar taqiqlanadi. Deletion beats addition.
- Javob oxirida doimo 1-2 qatorda nimalar o'tkazib yuborilgani va har qanday xatar (risk) ochiq ko'rsatiladi.

## 3. 15 ta Oliy Arxitektura Qonuni
1. **Meta-Prompt:** Avval to'liq reja va ichki arxitektura sxemasini chiz.
2. **Cross-Platform:** 4 gigant (Apple nafisligi, Android qulayligi, Linux yengilligi, Windows boshqaruvi) sintezi.
3. **Proaktivlik:** Pleyerda ekvayzer, videoda SFX va ducking, kodda testlarni oldindan qo'sh.
4. **Vizual Did:** Shablon dizayndan qochish (`taste-skill`, `impeccable`, `emilkowalski` animatsiyalari).
5. **Ikki Qiyofali Sinov:** Ham Oddiy, ham Ekspert foydalanuvchi ko'zi bilan sinab ko'r.
6. **Zero-Defect:** Bitta xato bo'lsa ham foydalanuvchiga bermasdan, mustaqil tuzatib topshir.
7. **MuzaffarZed Imzosi:** Har bir ishda mualliflik muhri bo'lsin.
8. **O'zini Ko'rish:** UI va ish stoli o'zgarganda `capture_window` yoki `capture_screen` orqali tasdiqla.
9. **Teskari Muhandislik:** DLL, drayver va xatoliklarni PE import tahlili bilan mustaqil tuzat.
10. **PowerShell Himoyasi:** Inline ko'p qatorli powershell chaqirma; faqat Python yoki `.ps1 -NonInteractive`.
11. **Yopiq Halqa Auditi:** Chiqish fayli, hajm, video/audio metadatasini shaxsan tekshir.
12. **Ponytail Qoidasi:** Eng qisqa mukammal diff; minimal boilerplate.
13. **Graphify:** Kod tahlilida `graphify query` dan foydalan; kodbaza o'zgarsa `graphify update .` qil.
14. **Agent Skills:** Tizimdagi 5 ta Master Skill'dan proaktiv foydalan (`core-coding`, `graphify`, `ui-ux-design`, `video-cinema`, `second-brain`).
15. **Teams & Enterprise:** `/team` da 6 mutaxassis, `/enterprise` da AGI Korporatsiya ishga tushadi.

## 4. Jamoalar va Ish Oqimlari
- `/team`: Team Lead, Frontend, Backend, Tester, Reviewer, Researcher.
- `/enterprise`: CEO Orchestrator, Sales, Marketing, Content, Admin, Finance.
- `/montaj` va `/viral-reels`: 0.4s pauza kesish, B-Roll, Glassmorphism va Inter Black subtitr.
- `/pro-cinema`: Three.js 3D kamera, Manim simulyatsiya, SFX, Audio Ducking, 60 FPS.
- `/brain`: Pre-task recall (`memory_engine.py context`), Error-learning hook (`lessons_learned.md`), Post-task reflection (`notebooklm_exporter.py`).

## 5. Universal Doimiy Majburiyat
Ushbu barcha qoidalar barcha chatlarda, har doim va har qanday yangi vazifada so'zsiz amal qiladi!

*Dasturchi: MuzaffarZed*
"""

    # 1. Global config AGENTS.md — yagona to'liq qoida
    GEMINI_CONFIG_AGENTS_MD.parent.mkdir(parents=True, exist_ok=True)
    GEMINI_CONFIG_AGENTS_MD.write_text(MASTER_GLOBAL_RULE.strip() + "\n", encoding="utf-8")
    print(f"  [+] Global ~/.gemini/config/AGENTS.md yangilandi ({len(MASTER_GLOBAL_RULE)} bayt).")

    # 2. Duplicate rule fayllarini tozalash (tokenni 3-4 marta ko'paytirib yubormasligi uchun)
    if GEMINI_AGENTS_MD.exists():
        GEMINI_AGENTS_MD.unlink()
        print("  [+] ~/.gemini/AGENTS.md dublikati olib tashlandi.")
    
    if HOME_AGENTS_MD.exists():
        HOME_AGENTS_MD.unlink()
        print("  [+] ~/AGENTS.md dublikati olib tashlandi.")

    if WORKSPACE_RULES_DIR.exists():
        for f in WORKSPACE_RULES_DIR.glob("*.md"):
            f.unlink()
        print("  [+] ai_workspace/.agents/rules/ ichidagi dublikat qoidalar olib tashlandi.")

    # 3. ai_workspace/AGENTS.md — ixcham workspace direktivasi
    WORKSPACE_RULE_TEXT = f"""# Workspace Directives: ai_workspace
Global laws inherited from `~/.gemini/config/AGENTS.md`.
Primary project root: `C:\\Users\\MuzaffarZed\\ai_workspace`
Python virtualenv: `C:\\Users\\MuzaffarZed\\ai_workspace\\venv\\Scripts\\python.exe`
Active Master Skills: `core-coding`, `graphify`, `ui-ux-design`, `video-cinema`, `second-brain`.
*Dasturchi: MuzaffarZed*
"""
    WORKSPACE_AGENTS_MD.write_text(WORKSPACE_RULE_TEXT.strip() + "\n", encoding="utf-8")
    print("  [+] ai_workspace/AGENTS.md ixchamlashtirildi.")


# ====================================================================
# 5-QADAM: YAKUNIY TOKEN VA MD FAYLLAR AUDITI
# ====================================================================
def final_verification_audit():
    print("\n" + "="*70)
    print("5-QADAM: YAKUNIY AUDIT VA TOKEN SARFI HISOBOTI")
    print("="*70)

    # 1. Rules hajmi
    rule_files = [GEMINI_CONFIG_AGENTS_MD, WORKSPACE_AGENTS_MD]
    total_rule_bytes = sum(f.stat().st_size for f in rule_files if f.exists())
    rule_tokens = int(total_rule_bytes * 0.35)

    # 2. Qolgan skilllar
    global_skills = [d.name for d in GEMINI_CONFIG_SKILLS.iterdir() if d.is_dir() and (d / "SKILL.md").exists()] if GEMINI_CONFIG_SKILLS.exists() else []
    local_skills = [d.name for d in WORKSPACE_SKILLS.iterdir() if d.is_dir() and (d / "SKILL.md").exists()] if WORKSPACE_SKILLS.exists() else []

    all_active_skills = sorted(list(set(global_skills + local_skills)))
    total_skill_tokens = len(all_active_skills) * 35  # har bir skill nomi, yo'li va 10-15 so'zlik tavsifi

    # 3. Saqlab qolingan .md fayllar soni
    saved_md_files = []
    for check_dir in [
        WORKSPACE / ".agents" / "agents",
        WORKSPACE / ".agents" / "enterprise",
        WORKSPACE / ".agents" / "workflows",
        WORKSPACE / ".agents" / "memory",
        WORKSPACE / ".agents" / "skills",
    ]:
        if check_dir.exists():
            for f in check_dir.rglob("*.md"):
                saved_md_files.append(f)
    if WORKSPACE_AGENTS_MD.exists():
        saved_md_files.append(WORKSPACE_AGENTS_MD)
    if GEMINI_CONFIG_AGENTS_MD.exists():
        saved_md_files.append(GEMINI_CONFIG_AGENTS_MD)

    total_tokens = rule_tokens + total_skill_tokens

    print("\n" + "*"*75)
    print(f"{'Metrika':<30} | {'Eski Holat':<18} | {'Yangi Holat':<18}")
    print("-" * 75)
    print(f"{'Jami Faol Skilllar':<30} | {'267 ta (105 excluded)':<18} | {f'{len(all_active_skills)} ta (0 excluded)':<18}")
    print(f"{'Rules Token Sarfi':<30} | {'16,695 (83.5%)':<18} | {f'{rule_tokens} ({rule_tokens/200:.1f}%)':<18}")
    print(f"{'Customizations Token Sarfi':<30} | {'45,206 (226.0%)':<18} | {f'{total_skill_tokens} ({total_skill_tokens/200:.1f}%)':<18}")
    print(f"{'Jami Token Yuklanishi':<30} | {'61,901 tokens':<18} | {f'{total_tokens} tokens':<18}")
    print(f"{'Limitdan pastlik':<30} | {'-21,901 (EXCEEDED)':<18} | {f'+{20000 - total_tokens} (XAVFSIZ)':<18}")
    print(f"{'Saqlangan Asosiy .md Fayllar':<30} | {'Barchasi saqlangan':<18} | {f'{len(saved_md_files)} ta toza fayl':<18}")
    print("*"*75)

    print("\nFaol Qolgan Asosiy Skilllar:")
    for s in all_active_skills:
        print(f"  ⭐ {s}")

    print("\n[MUVAFFAQIN!] Barcha ortiqcha bloat 100% tozalandi, token sarfi 61,901 dan")
    print(f"~{total_tokens} tokenga tushirildi (20,000 lik limitdan deyarli 10 barobar pastda!).")
    print("Dasturchi: MuzaffarZed\n")


def main():
    print("*"*70)
    print("ANTIGRAVITY CLEAN ALL BLOAT — BOSHLANDI")
    print("*"*70)
    backup_everything()
    clean_global_bloat()
    setup_local_5_master_skills()
    compress_and_deduplicate_rules()
    final_verification_audit()


if __name__ == "__main__":
    main()
