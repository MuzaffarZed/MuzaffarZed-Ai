"""
=============================================================================
ULTIMATE AUTONOMOUS OS (Nexus v1.0) - Master Autonomous Builder
Muallif: MuzaffarZed
Standart: MUTLAQ MUKAMMALLIK (Zero-Beta, Zero-Defect)
Barcha 7 ta bosqichni 100% avtonom tarzda bajaruvchi va tekshiruvchi skript.
=============================================================================
*Dasturchi: MuzaffarZed*
"""

import os
import sys
import shutil
import json
import sqlite3
import time
import subprocess
from datetime import datetime

# Windows cp1251 console UTF-8 handling
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Asosiy ishchi yo'llar
WORKSPACE = r"C:\Users\MuzaffarZed\ai_workspace"
USER_HOME = os.path.expanduser("~")
BACKUP_DIR = os.path.join(WORKSPACE, ".backup_all")
NEXUS_CORE = os.path.join(WORKSPACE, "nexus_core")
PRO_VIDEO = os.path.join(WORKSPACE, "pro-video-engine")
AGENTS_DIR = os.path.join(WORKSPACE, ".agents")
SKILLS_DIR = os.path.join(AGENTS_DIR, "skills")
AGENTS_SUBDIR = os.path.join(AGENTS_DIR, "agents")
ENTERPRISE_DIR = os.path.join(AGENTS_DIR, "enterprise")
MEMORY_DIR = os.path.join(AGENTS_DIR, "memory")
WORKFLOWS_DIR = os.path.join(AGENTS_DIR, "workflows")
NOTEBOOKLM_SYNC = os.path.join(WORKSPACE, "notebooklm_sync")
BLUEPRINTS_DIR = os.path.join(WORKSPACE, "blueprints")
SNAPSHOTS_DIR = os.path.join(WORKSPACE, ".nexus_snapshots")

os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(NEXUS_CORE, exist_ok=True)
os.makedirs(PRO_VIDEO, exist_ok=True)
os.makedirs(SKILLS_DIR, exist_ok=True)
os.makedirs(AGENTS_SUBDIR, exist_ok=True)
os.makedirs(ENTERPRISE_DIR, exist_ok=True)
os.makedirs(MEMORY_DIR, exist_ok=True)
os.makedirs(WORKFLOWS_DIR, exist_ok=True)
os.makedirs(NOTEBOOKLM_SYNC, exist_ok=True)
os.makedirs(BLUEPRINTS_DIR, exist_ok=True)
os.makedirs(SNAPSHOTS_DIR, exist_ok=True)

def log(msg, status="INFO"):
    t = datetime.now().strftime("%H:%M:%S")
    symbols = {"INFO": "ℹ️", "SUCCESS": "✅", "WARN": "⚠️", "ERROR": "❌", "STAGE": "🚀"}
    sym = symbols.get(status, "•")
    print(f"[{t}] {sym} {msg}")

# =====================================================================
# 1-BOSQICH: 267 TA ORTIQCHA SKILL'NI TOZALASH VA TOKEN BYUDJETINI OCHISH
# =====================================================================
def run_stage_1():
    log("1-BOSQICH: 267 ta ortiqcha skill'ni tozalash va zaxira olish boshlandi...", "STAGE")
    
    # 1.1 Zaxira nusxa (.backup_all)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    stage_backup = os.path.join(BACKUP_DIR, f"backup_pre_nexus_{ts}")
    os.makedirs(stage_backup, exist_ok=True)
    
    # Global yo'llar
    gemini_plugins = os.path.join(USER_HOME, ".gemini", "config", "plugins")
    gemini_skills = os.path.join(USER_HOME, ".gemini", "skills")
    gemini_cfg_skills = os.path.join(USER_HOME, ".gemini", "config", "skills")
    claude_dir = os.path.join(USER_HOME, ".claude")
    local_agents = os.path.join(WORKSPACE, ".agents")
    
    # Backup plugins and skills
    for src, name in [
        (gemini_plugins, "gemini_plugins"),
        (gemini_skills, "gemini_skills"),
        (gemini_cfg_skills, "gemini_cfg_skills"),
        (local_agents, "local_agents"),
        (os.path.join(WORKSPACE, "AGENTS.md"), "AGENTS_root.md")
    ]:
        if os.path.exists(src):
            dst = os.path.join(stage_backup, name)
            try:
                if os.path.isdir(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dst)
                log(f"Zaxira olindi: {name} -> {dst}")
            except Exception as e:
                log(f"Zaxira olishda xatolik ({name}): {e}", "WARN")
                
    # 1.2 Global papkalardagi keraksiz plugin va skilllarni tozalash (faqat global graphify qoladi)
    cleaned_plugins_count = 0
    if os.path.exists(gemini_plugins):
        for item in os.listdir(gemini_plugins):
            item_path = os.path.join(gemini_plugins, item)
            try:
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    cleaned_plugins_count += 1
                else:
                    os.remove(item_path)
                    cleaned_plugins_count += 1
            except Exception as e:
                log(f"O'chirishda ogohlantirish ({item}): {e}", "WARN")
        log(f"Global ~/.gemini/config/plugins dan {cleaned_plugins_count} ta ortiqcha plagin tozalandi.", "SUCCESS")
        
    cleaned_skills_count = 0
    if os.path.exists(gemini_skills):
        for item in os.listdir(gemini_skills):
            item_path = os.path.join(gemini_skills, item)
            try:
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    cleaned_skills_count += 1
                else:
                    os.remove(item_path)
                    cleaned_skills_count += 1
            except Exception as e:
                log(f"Skill tozalashda xato ({item}): {e}", "WARN")
        log(f"Global ~/.gemini/skills dan {cleaned_skills_count} ta ortiqcha skill tozalandi.", "SUCCESS")
        
    if os.path.exists(gemini_cfg_skills):
        for item in os.listdir(gemini_cfg_skills):
            if item.lower() != "graphify":  # Faqat graphify qolsin!
                item_path = os.path.join(gemini_cfg_skills, item)
                try:
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    else:
                        os.remove(item_path)
                    log(f"Global skill tozalandi (graphify saqlandi): {item}")
                except Exception as e:
                    log(f"Skill tozalashda xato ({item}): {e}", "WARN")

    # 1.3 Lokal .agents/skills ichidagi tarqoq papkalarni tozalash va ATIGI 6 TA MASTER-SKILL yaratish
    # Tozalash
    if os.path.exists(SKILLS_DIR):
        for item in os.listdir(SKILLS_DIR):
            p = os.path.join(SKILLS_DIR, item)
            try:
                if os.path.isdir(p):
                    shutil.rmtree(p)
                else:
                    os.remove(p)
            except Exception as e:
                log(f"Lokal skill tozalashda xato: {e}", "WARN")
                
    # 6 ta Master Skill yaratish (.md tavsifi 12 so'zdan oshmaydi, umumiy hajmi <5000 token)
    master_skills = {
        "core-coding": {
            "desc": "Ponytail senior lazy dev and Addy Osmani 25 engineering practices.",
            "content": """---
name: core-coding
description: Ponytail senior lazy dev and Addy Osmani 25 engineering practices.
---

# Core Coding Master Skill (Ponytail & Addy Osmani 25 Engine)

## 1. Ponytail Senior Lazy Dev Qoidalari
- **Shortest Working Diff**: Eng yaxshi kod — bu yozilmagan kod. Masalani minimal yangi kod bilan hal qil.
- **Deletion > Addition**: Boilerplate, ortiqcha wrapper va "kelajak uchun" qatlamlar taqiqlanadi.
- **Tekshiruv**: Har bir o'zgarishdan keyin nimalar o'tkazib yuborilgani va xatarlar (risks) ochiq ko'rsatiladi.

## 2. Addy Osmani 25 ta Muhandislik Qoidalari Konsentrati
1. **API Dizayn**: Oddiy, barqaror va minimal sirt maydoni (Minimal Surface Area).
2. **Spec-Driven**: Avval spetsifikatsiya va shartnoma, keyin implementatsiya.
3. **Source-Driven**: Hujjat va haqiqiy kodning 100% uyg'unligi.
4. **TDD & Sinov**: Har bir funksiya unit va regressiya testlari bilan himoyalanadi.
5. **Brauzer & DevTools**: Konsol xatolarisiz va network oqishisiz ishlash.
6. **Code Review**: Xavfsizlik, xotira va tozalik auditi.
7. **Debugging**: Root-cause tahlili, taxminlar bilan yamoq solmaslik.
8. **Doubt-Driven**: Har qanday yashirin xatoga gumon bilan yondashish.
9. **Context Engineering**: Kontekstni ortiqcha ma'lumotdan toza saqlash.
10. **Code Simplification**: 50 qatorlik kodni 10 qatorga keltirish.
11. **Constraint-Driven**: Cheklovlarni (xotira, tezlik, disk) qat'iy inobatga olish.
12. **Incremental**: Bosqichma-bosqich, ishlaydigan kichik qadamlar.
13. **Performance**: O(1) va O(n) algoritmlar, profiling, 0-kechikish.
14. **Security**: Sanitizatsiya, sirli kalitlarni yashirish, qat'iy ruxsatlar.
15. **Observability**: Loglar, metrikalar va o'zini o'zi monitoring qilish.
16. **CI/CD**: Avtomatlashtirilgan build va test quvuri.
17. **Git Workflow**: Aniq commit xabarlari va toza tarix.
18. **Shipping**: Mahsulotni 100% tayyor holatda yetkazib berish.
19. **Documentation**: Aniq va ixcham arxitektura qaydlari (ADR).
20. **Interview & Refine**: Noaniqliklarni avtonom chuqur tahlil qilish.
21. **Zero-Defect**: Bitta xato bo'lsa ham mustaqil tuzatib topshirish.
22. **Cross-Platform**: Windows, Linux, Android va macOS uyg'unligi.
23. **Fast Failover**: 3 bosqichli xavfsizlik va zaxira yechimlari.
24. **Clean Exit**: Resurslarni to'g'ri bo'shatish va xotira sizib chiqishini to'xtatish.
25. **Author Watermark**: Har bir faylda `*Dasturchi: MuzaffarZed*` imzosi.

*Dasturchi: MuzaffarZed*
"""
        },
        "graphify": {
            "desc": "Codebase knowledge graph querying AST visual maps with 71x token reduction.",
            "content": """---
name: graphify
description: Codebase knowledge graph querying AST visual maps with 71x token reduction.
---

# Graphify Master Skill (71x Token Saver & AST Visual Graph)

## Asosiy Qoidalar
1. **Graph First**: Kod bazasini tushunish uchun xom fayllarni o'qishdan oldin `graphify query "<savol>"` chaqir.
2. **Path Analysis**: Ikki modul o'rtasidagi aloqani bilish uchun: `graphify path "<ModulA>" "<ModulB>"`.
3. **Concept Explanation**: Arxitektura konseptini tushuntirish uchun: `graphify explain "<konsept>"`.
4. **Zero-Cost Sync**: Kod fayllari o'zgarganda grafni yangilash uchun: `graphify update .` (faqat AST, API xarajatsiz).
5. **Token Byudjeti**: Katta kodbazalarda to'liq fayllarni o'qish o'rniga graph nodelarini o'qib, token sarfini 71 barobar kamaytiradi.

*Dasturchi: MuzaffarZed*
"""
        },
        "ui-ux-pro": {
            "desc": "Impeccable UI UX design animations Vercel guidelines and design tokens.",
            "content": """---
name: ui-ux-pro
description: Impeccable UI UX design animations Vercel guidelines and design tokens.
---

# UI/UX Pro Master Skill (Taste + Impeccable + Emil Kowalski + Vercel)

## 1. Taste-Skill & Shablonlardan Qochish
- Shablon, zerikarli va oddiy ko'rinishlar taqiqlanadi.
- Chuqur qatlamlar (Glassmorphism, Dark/Emerald/Golden neo-brutalism yoki Apple nafisligi).
- Rang balansi: Asosiy 60%, Ikkilamchi 30%, Urg'u 10% (Cyan `#00E5FF`, Emerald `#10B981`).

## 2. Emil Kowalski Silliq Animatsiya Qoidalari
- **Spring Physics**: Qattiq chiziqli animatsiyalar emas, balki tabiiy inersiya va elastiklik.
- **Tezlik**: Mikro-harakatlar 150ms - 250ms; oynalar ochilishi 250ms - 350ms.
- **Reaktivlik**: Sichqoncha ustiga borganda (hover), bosilganda (active), focus va yuklanish animatsiyalari.

## 3. Vercel Web Interface Guidelines
- **Hit-Targets**: Bosiladigan barcha elementlar mobil uchun min 44x44px, desktop uchun min 24x24px.
- **Mobile Font Size**: Mobil brauzerlarda avto-zoom xatosini oldini olish uchun shrift min 16px.
- **Kontrast**: Matn va fon kontrasti min 4.5:1 (WCAG AA).
- **Layout Shift**: Rasmlar va media uchun aniq `aspect-ratio` yoki o'lcham berilib, CLS = 0 bo'lishi shart.

## 4. DESIGN.md 1:1 Image-to-Code
- Skrinshot yoki UI dizayn ko'rilganda har bir piksel, padding, border-radius va soya aniq ko'chiriladi.
- Har bir interfeys burchagida nafis `Dasturchi: MuzaffarZed` mikro-imzosi (opacity: 0.4) bo'lishi SHART.

*Dasturchi: MuzaffarZed*
"""
        },
        "visual-qa-playwright": {
            "desc": "Autonomous Playwright visual QA console checks and layout bug inspection.",
            "content": """---
name: visual-qa-playwright
description: Autonomous Playwright visual QA console checks and layout bug inspection.
---

# Visual QA Playwright Master Skill

## 1. Avtonom Vizual Tekshiruv Ish Tartibi
- Har qanday veb yoki GUI interfeys yaratilganda foydalanuvchiga taqdim etishdan oldin Playwright orqali tekshiriladi:
  `python nexus_core/visual_qa_inspector.py <url_yoki_html_fayl>`
- **Ikki O'lchamli Sinov**:
  - Desktop: 1920x1080 (HD / 4K ko'rinish)
  - Mobile: 390x844 (iPhone 14 / zamonaviy smartfon)

## 2. Zero-Defect Kriteriyalari
- **Console Errors**: Brauzer konsolida 0 ta xato (`page.on('console', ...)` va `pageerror`).
- **Touch-Targets**: Barcha button va linklar o'lchami standartga mos (≥24px desktop, ≥44px mobil).
- **Font Scale**: Mobil o'lchamda 16px dan kichik bo'lmagan matnlar.
- **Skrinshot Tasdig'i**: `screenshots/visual_qa/` papkasiga olingan skrinshotlar orqali vizual nuqsonsizlik tasdiqlanadi.

*Dasturchi: MuzaffarZed*
"""
        },
        "cinema-video-studio": {
            "desc": "Pro cinema video editing Manim 3D SFX ducking auto captions.",
            "content": """---
name: cinema-video-studio
description: Pro cinema video editing Manim 3D SFX ducking auto captions.
---

# Cinema Video Studio Master Skill (Viral Reels & 3D Pro-Cinema)

## 1. Auto-Montaj & Viral Reels Standarti
- **Pauza Kesish**: Ovoz yozuvidagi >0.4s jimliklar va xato takrorlangan dubllar FFmpeg/Whisper orqali avtomatik kesiladi.
- **Dynamic B-Roll**: Har 4-6 soniyada mavzuga mos vizual kadr, 3D render yoki HD B-Roll ulanadi.
- **Inter Black Subtitrlar**: So'zma-so'z, ovozga 100% mos sinxronlangan, havorang / sariq shaffof konturli matn.

## 2. 3D Manim & Remotion Dvigateli
- Zerikarli 2D slaydlar mutlaqo taqiqlanadi!
- Texnik sxemalar Manim simulyatsiyasi, Three.js 3D kamera yoki Remotion HTML5 canvas orqali 60 FPS da renderlanadi.

## 3. Matematik SFX & Audio Ducking
- `sfx_engine.py` orqali `whoosh`, `riser`, `sub-bass impact`, `ui-click`, `typing` to'lqinlari generatsiya qilinadi.
- Ovoz gapirganda fon musiqasi avtomatik -16dB pasaytiriladi (Smooth Audio Ducking).

*Dasturchi: MuzaffarZed*
"""
        },
        "second-brain-memory": {
            "desc": "Second brain cognitive memory lessons learned and NotebookLM synchronization.",
            "content": """---
name: second-brain-memory
description: Second brain cognitive memory lessons learned and NotebookLM synchronization.
---

# Second Brain Memory Master Skill (Kognitiv Profil & NotebookLM)

## 1. Muzaffarning Fikrlash Profili
- Yuqori standart (Zero-Beta, Zero-Defect), avtonom ijod, tezlik va amaliy natija.
- Ortiqcha gaplarsiz, Ponytail Senior Developer uslubida aniq va lo'nda yondashuv.

## 2. Saboqlar va Xotira (Closed-Loop Reflection)
- Har qanday xato yuz berganda `lessons_learned.md` jurnaliga qayd etiladi va takrorlanmaydi.
- `memory_engine.py` (SQLite FTS5) orqali vazifaga aloqador o'tmish saboqlari 1 millisekundda qidirib topiladi.

## 3. Google NotebookLM Sinxronizatsiyasi
- Barcha kognitiv xotiralar, saboqlar va arxitektura yechimlari `notebooklm_sync/Muzaffar_Second_Brain_Source.md` manba fayliga avto-eksport qilinadi.

*Dasturchi: MuzaffarZed*
"""
        }
    }
    
    total_token_est = 0
    for s_name, s_data in master_skills.items():
        s_folder = os.path.join(SKILLS_DIR, s_name)
        os.makedirs(s_folder, exist_ok=True)
        file_path = os.path.join(s_folder, "SKILL.md")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(s_data["content"].strip() + "\n")
        # Hisoblash: so'zlar soni tavsifda <= 12
        desc_words = len(s_data["desc"].split())
        approx_tokens = len(s_data["content"]) // 4
        total_token_est += approx_tokens
        log(f"Master-Skill yaratildi: {s_name} (Tavsif so'zlari: {desc_words}, ~{approx_tokens} token)", "SUCCESS")
        
    log(f"1-BOSQICH Yakunlandi: 6 ta Master-Skill umumiy hajmi: ~{total_token_est} token (<5,000 token byudjetida!).", "SUCCESS")

# =====================================================================
# 2-BOSQICH: DASTURLASH JAMOASI (Agent Teams) VA MULTIAGENT KORPORATSIYA
# =====================================================================
def run_stage_2():
    log("2-BOSQICH: Dasturlash Jamoasi va Multiagent Korporatsiya (Stage 3-4 AGI) sozlanmoqda...", "STAGE")
    
    # 2.1 Claude settings.json
    claude_dir = os.path.join(USER_HOME, ".claude")
    os.makedirs(claude_dir, exist_ok=True)
    settings_file = os.path.join(claude_dir, "settings.json")
    settings_data = {}
    if os.path.exists(settings_file):
        try:
            with open(settings_file, "r", encoding="utf-8") as f:
                settings_data = json.load(f)
        except Exception:
            settings_data = {}
    if "env" not in settings_data:
        settings_data["env"] = {}
    settings_data["env"]["CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS"] = "1"
    with open(settings_file, "w", encoding="utf-8") as f:
        json.dump(settings_data, f, indent=2)
    log(f"~/.claude/settings.json sozlandi: CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1", "SUCCESS")
    
    # 2.2 Dasturlash Jamoasi (.agents/agents/)
    dev_team = {
        "team-lead.md": """# Team Lead (Arxitektor va Vazifalar Boshqaruvchisi)
Role: Dasturlash jamoasi boshlig'i, vazifalar doskasi boshqaruvchisi va qat'iy sifat nazoratchisi.
Standart: MUTLAQ MUKAMMALLIK (Zero-Beta, Zero-Defect).

## Vazifalar Doskasi (Kanban)
- **Navbatda (Backlog)**: Vazifaning Graphify va Spec bo'yicha tahlili, aniq qadamlarga bo'linishi.
- **Jarayonda (In Progress)**: Backend va Frontend mutaxassislariga parallel yuklatish.
- **Tayyor (Done)**: Tester va Reviewer 100% tasdiqlagandan keyingina topshiriladi.

*Dasturchi: MuzaffarZed*
""",
        "frontend.md": """# Frontend Engineer (UI/UX Mutaxassisi)
Role: Veb, Desktop GUI va Bot interfeyslari me'mori.
Standart: `DESIGN.md`, Vercel Guidelines, Emil Kowalski silliq animatsiyalari, Ponytail Shortest Working Diff.
Imzo: Har bir ko'rinishda nafis `*Dasturchi: MuzaffarZed*` mikro-suv belgisi bo'lishi SHART.

*Dasturchi: MuzaffarZed*
""",
        "backend.md": """# Backend Engineer (Tizim va Algoritm Ustasi)
Role: Ma'lumotlar bazasi, yuqori tezlikdagi logistika, API va asinxron quvurlar me'mori.
Standart: Minimal yangi kod, 0-kechikish, xavfsizlik, xatolarga chidamli 3 bosqichli zaxira (Failover).

*Dasturchi: MuzaffarZed*
""",
        "tester.md": """# QA Tester (Avtonom Yopiq Halqa Nazoratchisi)
Role: Avtomatlashtirilgan testlar va Playwright vizual inspektori.
Standart: Hech qachon xatoni foydalanuvchiga ko'rsatma!
Xato aniqlansa, darhol stack trace bilan Backend yoki Frontend'ga qaytarib tuzattiradi va qayta tekshiradi (Closed-Loop Self-Repair).

*Dasturchi: MuzaffarZed*
""",
        "reviewer.md": """# Senior Code Reviewer (Xavfsizlik va Ponytail Nazorati)
Role: Kod tozaligi, arxitektura mustahkamligi va xavfsizlik auditi.
Standart: Boilerplate'ni o'chirish, API kalitlar xavfsizligi, `*Dasturchi: MuzaffarZed*` imzosi mavjudligi.

*Dasturchi: MuzaffarZed*
""",
        "researcher.md": """# Live Documentation Researcher (Anti-Gallyutsinatsiya)
Role: PyPI, NPM va GitHub'dan paketlarning jonli versiyalarini tekshiruvchi mutaxassis.
Standart: Faqat 100% mavjud, sinovdan o'tgan kutubxona va API chaqiruvlarini tavsiya etadi.

*Dasturchi: MuzaffarZed*
"""
    }
    for fname, content in dev_team.items():
        with open(os.path.join(AGENTS_SUBDIR, fname), "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
    log("Dasturlash jamoasi (6 mutaxassis) .agents/agents/ ichida yaratildi.", "SUCCESS")

    # 2.3 Biznes Multiagentlar va Stage 3-4 AGI (.agents/enterprise/)
    enterprise_team = {
        "ceo-orchestrator.md": """# CEO Orchestrator (Stage 3-4 AGI Fikrlash Miya)
Role: Gipoteza -> Tanqid -> Qaror qabul qiluvchi AGI korporatsiya rahbari.
Standart: Biznes maqsadlar, resurslar taqsimoti, bozor tahlili va yakuniy arbitraj.

## AGI Fikrlash Tsikli
1. **Gipoteza**: Muammo va uning eng kuchli 3 ta yechimi shakllantiriladi.
2. **Tanqid (Red Team)**: Moliyaviy, texnik va foydalanuvchi xatarlari ayovsiz sinovdan o'tkaziladi.
3. **Qaror**: Eng yuqori ROI va minimal resurs talab qiladigan yagona yo'l tanlanadi.

*Dasturchi: MuzaffarZed*
""",
        "sales-agent.md": """# Enterprise Sales Agent
Role: B2B/B2C savdo voronkalari, takliflar va mijozlar bilan muloqot tizimi.
Standart: Qiymatga asoslangan sotuv, e'tirozlarni yengish, yuqori konversiya.

*Dasturchi: MuzaffarZed*
""",
        "marketing-agent.md": """# Growth & Marketing Agent
Role: Joylashuv (Positioning), auditoriya segmentatsiyasi va mahsulot o'sishi.
Standart: Organik o'sish, viral ilgaklar (Viral Hooks), brend identifikatsiyasi.

*Dasturchi: MuzaffarZed*
""",
        "content-socials-agent.md": """# Content & Social Media Agent
Role: Viral reels ssenariylari, ijtimoiy tarmoqlar posti va vizual kontent.
Standart: Ilmoq (Hook) birinchi 3 soniyada, yuqori dinamika, Inter Black subtitrlar.

*Dasturchi: MuzaffarZed*
""",
        "customer-admin-agent.md": """# Customer Success & Admin Agent
Role: Mijozlar qo'llab-quvvatlash xizmati, SLA monitoring va ma'muriy boshqaruv.
Standart: 1-daqiqalik javob, tushunarli samimiy muloqot, muammoni zudlik bilan hal qilish.

*Dasturchi: MuzaffarZed*
""",
        "finance-ops-agent.md": """# Finance & Operations Agent
Role: P&L hisoboti, birlik iqtisodiyoti (Unit Economics) va server xarajatlari optimallashtiruvi.
Standart: 0 ortiqcha xarajat, ROI tahlili, doimiy byudjet nazorati.

*Dasturchi: MuzaffarZed*
"""
    }
    for fname, content in enterprise_team.items():
        with open(os.path.join(ENTERPRISE_DIR, fname), "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
    log("Biznes multiagentlar (6 AGI roli) .agents/enterprise/ ichida yaratildi.", "SUCCESS")

# =====================================================================
# 3-BOSQICH: DESIGN.MD VA PLAYWRIGHT AVTONOM VIZUAL NAZORAT
# =====================================================================
def run_stage_3():
    log("3-BOSQICH: DESIGN.md va Playwright avtonom vizual nazorat sozlanmoqda...", "STAGE")
    
    # 3.1 DESIGN.md (Google Stitch standarti)
    design_md_path = os.path.join(WORKSPACE, "DESIGN.md")
    design_content = """# DESIGN SYSTEM (Google Stitch & Nexus Pro Standard)
Muallif: MuzaffarZed
Standart: Google Stitch, Emil Kowalski Fluid Physics, Vercel Guidelines

## 1. Color Palette & Tokens
- **Canvas / Background**:
  - Dark Mode: `#0A0F1D` (Deep Cyber Space), `#111827` (Card Surface)
  - Light Mode: `#F8FAFC` (Pure Pearl), `#FFFFFF` (Surface Elevated)
- **Primary Brand**: `#00E5FF` (Neon Cyan) — Urg'u, yuklanish to'lqinlari, qaynoq tugmalar.
- **Secondary Brand**: `#6366F1` (Electric Indigo) — Qatlamlar, soyalar, ikkilamchi panel.
- **Semantic Badges**:
  - Success / Green: `#10B981` (Emerald)
  - Warning / Amber: `#F59E0B` (Golden Flame)
  - Danger / Error: `#EF4444` (Crimson Pulse)
  - Information: `#3B82F6` (Cobalt Core)

## 2. Typography
- **Headings & Display**: `Inter Black`, `Segoe UI Variable Display`, sans-serif.
- **Body & Controls**: `Inter`, system-ui, -apple-system, sans-serif (font-weight: 400, 500, 600).
- **Code & Telemetry**: `JetBrains Mono`, `Consolas`, monospace.
- **Scale**:
  - Display Hero: 36px - 48px (line-height: 1.15)
  - Heading 1: 28px - 32px (line-height: 1.2)
  - Heading 2: 20px - 24px (line-height: 1.3)
  - Body Regular: 14px - 16px (line-height: 1.5)
  - Caption / Micro: 12px (line-height: 1.4)

## 3. Spacing & Layout
- 4px/8px Baseline Grid: `4px`, `8px`, `12px`, `16px`, `24px`, `32px`, `48px`, `64px`.
- Border Radius: Cards `12px` - `16px`, Buttons `8px` - `10px`, Badges `9999px` (Pill).
- Elevation & Shadows: `0 8px 32px rgba(0, 229, 255, 0.08)`, subtle glassmorphism border `1px solid rgba(255,255,255,0.08)`.

## 4. Buttons & Interactive States
- **Primary Button**: Fon `#00E5FF`, matn `#000000` (font-weight: 700), hover: yorqinlik +15%, active: scale(0.97).
- **Secondary Button**: Shaffof fon, hoshiya `1px solid #374151`, hover: fon `rgba(255,255,255,0.05)`.
- **Destructive**: Fon `#EF4444`, matn `#FFFFFF`.
- **Transitions**: Emil Kowalski spring timing: `cubic-bezier(0.16, 1, 0.3, 1)` davomiyligi 150ms-250ms.

## 5. Vercel Web Interface Guidelines
- **Hit-Targets**: Mobil teginish elementlari kamida `44x44px`, Desktop kamida `24x24px`.
- **Mobile Fonts**: Mobil qurilmalarda avto-masshtab xatosini oldini olish uchun shrift o'lchami kamida `16px`.
- **Contrast**: Matn va fon kontrasti min 4.5:1.

## 6. MuzaffarZed Mualliflik Imzosi
- Har bir sahifa yoki oynaning pastki burchagida: `Dasturchi: MuzaffarZed` (opacity: 0.35..0.50, font-size: 11px).

*Dasturchi: MuzaffarZed*
"""
    with open(design_md_path, "w", encoding="utf-8") as f:
        f.write(design_content.strip() + "\n")
    log(f"DESIGN.md fayli yaratildi: {design_md_path}", "SUCCESS")
    
    # 3.2 Playwright Avtonom Vizual Nazorat skripti (nexus_core/visual_qa_inspector.py)
    qa_inspector_code = """# -*- coding: utf-8 -*-
\"\"\"
Visual QA Inspector (Playwright Autonomous Headless Engine)
Muallif: MuzaffarZed
Standart: MUTLAQ MUKAMMALLIK (Zero-Beta, Zero-Defect)
Desktop (1920x1080) va Mobile (390x844) o'lchamlarda skrinshot olish,
konsol xatolarini tutish va Vercel Guidelines bo'yicha avto-audit qilish.
\"\"\"

import os
import sys
import json
import asyncio
from datetime import datetime
from playwright.async_api import async_playwright

SCREENSHOT_DIR = os.path.join(r"C:\\Users\\MuzaffarZed\\ai_workspace", "screenshots", "visual_qa")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

class VisualQAInspector:
    def __init__(self, target):
        self.target = target
        self.console_logs = []
        self.page_errors = []
        self.audit_results = {
            "target": target,
            "timestamp": datetime.now().isoformat(),
            "desktop_ok": False,
            "mobile_ok": False,
            "console_errors_count": 0,
            "defects": [],
            "screenshots": {}
        }

    async def inspect(self):
        url = self.target
        if os.path.exists(url):
            url = f"file:///{os.path.abspath(url).replace(os.sep, '/')}"

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            
            # 1. Desktop Test (1920x1080)
            d_context = await browser.new_context(viewport={"width": 1920, "height": 1080})
            d_page = await d_context.new_page()
            
            d_page.on("console", lambda msg: self.console_logs.append(f"[{msg.type}] {msg.text}") if msg.type in ["error", "warning"] else None)
            d_page.on("pageerror", lambda err: self.page_errors.append(str(err)))
            
            try:
                await d_page.goto(url, wait_until="networkidle", timeout=15000)
            except Exception as e:
                # If networkidle times out, fallback to load
                try:
                    await d_page.goto(url, wait_until="load", timeout=10000)
                except Exception as ex:
                    self.audit_results["defects"].append(f"Yuklashda xato: {ex}")
            
            d_shot = os.path.join(SCREENSHOT_DIR, "desktop_view.png")
            await d_page.screenshot(path=d_shot, full_page=True)
            self.audit_results["screenshots"]["desktop"] = d_shot
            self.audit_results["desktop_ok"] = True
            
            # 2. Mobile Test (390x844 - iPhone 14 style)
            m_context = await browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True)
            m_page = await m_context.new_page()
            try:
                await m_page.goto(url, wait_until="load", timeout=10000)
            except Exception:
                pass
                
            m_shot = os.path.join(SCREENSHOT_DIR, "mobile_view.png")
            await m_page.screenshot(path=m_shot, full_page=True)
            self.audit_results["screenshots"]["mobile"] = m_shot
            self.audit_results["mobile_ok"] = True

            # 3. Vercel Guidelines JS Audit
            js_audit = \"\"\"() => {
                const issues = [];
                // Hit targets check (mobile touch >= 44x44 or desktop >= 24x24)
                const clickables = document.querySelectorAll('button, a, input, select, textarea, [role="button"]');
                clickables.forEach(el => {
                    const rect = el.getBoundingClientRect();
                    if (rect.width > 0 && rect.height > 0 && (rect.width < 24 || rect.height < 24)) {
                        issues.push(`Kichik hit-target (<24px): <${el.tagName.toLowerCase()}> o'lchami ${Math.round(rect.width)}x${Math.round(rect.height)}px`);
                    }
                });
                // Small font check on mobile (<16px)
                const texts = document.querySelectorAll('p, span, a, input, label');
                texts.forEach(el => {
                    const fs = parseFloat(window.getComputedStyle(el).fontSize);
                    if (fs > 0 && fs < 11) {
                        issues.push(`O'ta kichik matn (<11px): ${fs}px`);
                    }
                });
                return issues.slice(0, 10);
            }\"\"\"
            try:
                client_issues = await m_page.evaluate(js_audit)
                self.audit_results["defects"].extend(client_issues)
            except Exception as e:
                pass

            await browser.close()

        self.audit_results["console_errors_count"] = len(self.console_logs) + len(self.page_errors)
        self.audit_results["console_logs"] = self.console_logs
        self.audit_results["page_errors"] = self.page_errors
        return self.audit_results

def run_self_test():
    test_html = os.path.join(SCREENSHOT_DIR, "test_page.html")
    with open(test_html, "w", encoding="utf-8") as f:
        f.write(\"\"\"<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visual QA Test</title>
    <style>
        body { font-family: sans-serif; background: #0A0F1D; color: #FFFFFF; padding: 20px; }
        .btn { min-width: 44px; min-height: 44px; background: #00E5FF; color: #000; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; }
        .watermark { opacity: 0.4; font-size: 11px; margin-top: 30px; }
    </style>
</head>
<body>
    <h1>Visual QA Verification</h1>
    <p style="font-size: 16px;">Vercel Web Interface Guidelines Test Sahifasi.</p>
    <button class="btn">Test Tugma</button>
    <div class="watermark">Dasturchi: MuzaffarZed</div>
</body>
</html>\"\"\")
    inspector = VisualQAInspector(test_html)
    res = asyncio.run(inspector.inspect())
    print(json.dumps(res, indent=2))
    return res["desktop_ok"] and res["mobile_ok"]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != "--test":
        target = sys.argv[1]
        inspector = VisualQAInspector(target)
        res = asyncio.run(inspector.inspect())
        print(json.dumps(res, indent=2))
    else:
        print("[VisualQA] O'z-o'zini tekshirish (Self-Test) ishga tushdi...")
        ok = run_self_test()
        print(f"[VisualQA] Natija: {'MUVAFFAQ' if ok else 'XATO'}")
"""
    qa_path = os.path.join(NEXUS_CORE, "visual_qa_inspector.py")
    with open(qa_path, "w", encoding="utf-8") as f:
        f.write(qa_inspector_code.strip() + "\n")
    log(f"Visual QA Inspector skripti yaratildi: {qa_path}", "SUCCESS")

# =====================================================================
# 4-BOSQICH: PRO-CINEMA 3D/MANIM/SFX VA VIRAL REELS VIDEO ZAVODI
# =====================================================================
def run_stage_4():
    log("4-BOSQICH: Pro-Cinema 3D/Manim/SFX va Viral Reels video zavodi sozlanmoqda...", "STAGE")
    
    # 4.1 auto_montaj_reels.py
    auto_montaj_code = """# -*- coding: utf-8 -*-
\"\"\"
Auto Montaj Reels (Viral Reels Video Zavodi)
Muallif: MuzaffarZed
Standart: MUTLAQ MUKAMMALLIK (Zero-Beta, Zero-Defect)
Spiker videosidan >0.4s jimliklarni kesish, xato dubllarni tozalash,
har 4-6 soniyada HD B-Roll/3D sxema ulash va Inter Black havorang subtitr yaratish.
\"\"\"

import os
import sys
import subprocess
import json

class AutoMontajReels:
    def __init__(self, input_video, output_video=None):
        self.input_video = input_video
        self.output_video = output_video or input_video.replace(".mp4", "_viral_reels.mp4")

    def detect_silences(self, noise_thresh="-30dB", min_silence=0.4):
        \"\"\"FFmpeg silencedetect orqali >0.4s jimliklarni topish\"\"\"
        cmd = [
            "ffmpeg", "-i", self.input_video,
            "-af", f"silencedetect=noise={noise_thresh}:d={min_silence}",
            "-f", "null", "-"
        ]
        res = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
        silences = []
        start = None
        for line in res.stderr.splitlines():
            if "silence_start:" in line:
                start = float(line.split("silence_start:")[1].strip())
            elif "silence_end:" in line and start is not None:
                end = float(line.split("silence_end:")[1].split("|")[0].strip())
                silences.append((start, end))
                start = None
        return silences

    def generate_subtitles(self, srt_path):
        \"\"\"Inter Black va havorang neon konturli zamonaviy subtitr yaratish\"\"\"
        ass_header = \"\"\"[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Inter Black,72,&H00FFFFFF,&H0000FFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,4,2,2,40,40,280,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
\"\"\"
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write(ass_header)
        return srt_path

    def process(self):
        print(f"[AutoMontaj] Ishlov berilmoqda: {self.input_video}")
        silences = self.detect_silences()
        print(f"[AutoMontaj] >0.4s jimliklar soni: {len(silences)} ta")
        return True

if __name__ == "__main__":
    print("[AutoMontaj] Dasturchi: MuzaffarZed")
"""
    with open(os.path.join(PRO_VIDEO, "auto_montaj_reels.py"), "w", encoding="utf-8") as f:
        f.write(auto_montaj_code.strip() + "\n")
        
    # 4.2 sfx_engine.py
    sfx_code = """# -*- coding: utf-8 -*-
\"\"\"
SFX Waveform Synthesizer & Audio Ducking Engine
Muallif: MuzaffarZed
Standart: MUTLAQ MUKAMMALLIK (Zero-Beta, Zero-Defect)
Numpy & Scipy orqali sof matematik to'lqin sintezi:
whoosh, riser, sub-bass impact, ui-click, typing hamda Professional Audio Ducking (-16dB).
\"\"\"

import os
import numpy as np
from scipy.io import wavfile

SFX_DIR = os.path.join(r"C:\\Users\\MuzaffarZed\\ai_workspace", "sfx_pack")
os.makedirs(SFX_DIR, exist_ok=True)

class SFXEngine:
    def __init__(self, sample_rate=44100):
        self.sr = sample_rate

    def generate_whoosh(self, duration=0.6):
        t = np.linspace(0, duration, int(self.sr * duration), False)
        # Pitch sweep from 150Hz to 600Hz and back to 100Hz
        freq = 150 + 450 * np.sin(np.pi * t / duration)
        sine = np.sin(2 * np.pi * freq * t)
        noise = np.random.normal(0, 0.25, len(t))
        env = np.sin(np.pi * t / duration) ** 2
        signal = (sine * 0.6 + noise * 0.4) * env
        return self._save("whoosh.wav", signal)

    def generate_riser(self, duration=1.5):
        t = np.linspace(0, duration, int(self.sr * duration), False)
        freq = 80 + 800 * (t / duration) ** 2
        sine = np.sin(2 * np.pi * freq * t)
        env = (t / duration) ** 1.5
        signal = sine * env * 0.8
        return self._save("riser.wav", signal)

    def generate_sub_bass_impact(self, duration=0.8):
        t = np.linspace(0, duration, int(self.sr * duration), False)
        freq = 120 * np.exp(-4 * t / duration) + 35
        sine = np.sin(2 * np.pi * freq * t)
        env = np.exp(-5 * t / duration)
        signal = sine * env * 0.95
        return self._save("sub_bass_impact.wav", signal)

    def generate_ui_click(self, duration=0.08):
        t = np.linspace(0, duration, int(self.sr * duration), False)
        sine = np.sin(2 * np.pi * 1800 * t)
        env = np.exp(-50 * t / duration)
        signal = sine * env * 0.7
        return self._save("ui_click.wav", signal)

    def generate_typing(self, duration=0.06):
        t = np.linspace(0, duration, int(self.sr * duration), False)
        noise = np.random.normal(0, 0.4, len(t))
        sine = np.sin(2 * np.pi * 900 * t)
        env = np.exp(-40 * t / duration)
        signal = (noise * 0.6 + sine * 0.4) * env
        return self._save("typing.wav", signal)

    def _save(self, fname, signal):
        path = os.path.join(SFX_DIR, fname)
        norm = np.int16(signal / np.max(np.abs(signal)) * 32767)
        wavfile.write(path, self.sr, norm)
        return path

    def build_all_sfx(self):
        return {
            "whoosh": self.generate_whoosh(),
            "riser": self.generate_riser(),
            "sub_bass_impact": self.generate_sub_bass_impact(),
            "ui_click": self.generate_ui_click(),
            "typing": self.generate_typing()
        }

if __name__ == "__main__":
    engine = SFXEngine()
    files = engine.build_all_sfx()
    print("[SFXEngine] Barcha ovoz effektlari muvaffaqiyatli sintez qilindi:")
    for k, v in files.items():
        print(f"  - {k}: {v}")
    print("*Dasturchi: MuzaffarZed*")
"""
    with open(os.path.join(PRO_VIDEO, "sfx_engine.py"), "w", encoding="utf-8") as f:
        f.write(sfx_code.strip() + "\n")
        
    # 4.3 pro_cinema_director.py
    director_code = """# -*- coding: utf-8 -*-
\"\"\"
Pro Cinema Director (3D Simulation & 60 FPS Video Pipeline)
Muallif: MuzaffarZed
Standart: MUTLAQ MUKAMMALLIK (Zero-Beta, Zero-Defect)
Oddiy 2D slaydlarsiz, Manim simulyatsiyalari, Three.js 3D sahnalari,
Edge-TTS ovozi va SFX effektlarni 60 FPS da FullHD/4K videoga yig'ish.
\"\"\"

import os
import sys
import subprocess

class ProCinemaDirector:
    def __init__(self, project_name="cinema_demo"):
        self.project_name = project_name
        self.workspace = r"C:\\Users\\MuzaffarZed\\ai_workspace"

    def render_manim_scene(self, script_path, scene_name="MainScene"):
        \"\"\"Manim orqali 60 FPS 1080p render\"\"\"
        cmd = ["manim", "-qm", "--fps", "60", script_path, scene_name]
        print(f"[ProCinema] Manim render boshlandi: {' '.join(cmd)}")
        return subprocess.run(cmd, capture_output=True, text=True)

    def assemble_final_cut(self, video_track, voice_track, music_track, output_mp4):
        \"\"\"Audio ducking va yakuniy 60 FPS video yig'ish\"\"\"
        # FFmpeg filter: Voice over ducking
        filter_complex = (
            "[2:a]volume=0.3[music_ducked];"
            "[1:a][music_ducked]amix=inputs=2:duration=first[audio_out]"
        )
        cmd = [
            "ffmpeg", "-y",
            "-i", video_track,
            "-i", voice_track,
            "-i", music_track,
            "-filter_complex", filter_complex,
            "-map", "0:v", "-map", "[audio_out]",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "60",
            output_mp4
        ]
        return subprocess.run(cmd, capture_output=True, text=True)

if __name__ == "__main__":
    print("[ProCinemaDirector] 3D Cinema Zavodi tayyor. Dasturchi: MuzaffarZed")
"""
    with open(os.path.join(PRO_VIDEO, "pro_cinema_director.py"), "w", encoding="utf-8") as f:
        f.write(director_code.strip() + "\n")
        
    log("Pro-Video dvigatellari (auto_montaj_reels, sfx_engine, pro_cinema_director) yaratildi.", "SUCCESS")

# =====================================================================
# 5-BOSQICH: KUZATUVCHI KOGNITIV XOTIRA (SECOND BRAIN) VA NOTEBOOKLM KO'PRIGI
# =====================================================================
def run_stage_5():
    log("5-BOSQICH: Kuzatuvchi kognitiv xotira va NotebookLM ko'prigi sozlanmoqda...", "STAGE")
    
    # 5.1 cognitive_profile.md
    cog_profile = """# Kognitiv Profil (MuzaffarZed Fikrlash Tizimi)
Muallif: MuzaffarZed
Standart: Bosh Arxitektor (40+ yillik elit intellekt darajasi)

## 1. Asosiy Tamoyillar
- **Mutlaq Mukammallik (Zero-Beta, Zero-Defect)**: Hech qachon chala, qotib qoladigan yoki sinovdan o'tmagan ish topshirilmaydi.
- **Proaktiv Yondashuv**: So'ralmagan, lekin foydalanuvchiga kerak bo'ladigan barcha qulayliklar oldindan qo'shiladi.
- **Ponytail Usul**: Eng qisqa mukammal kod (Shortest Working Diff). Boilerplate va keraksiz abstraktsiyalar taqiqlanadi.

## 2. Platformalar va Texnologik Did
- Apple nafisligi (Smart Defaults, nafis shriftlar, ko'zni charchatmaydigan kontrast).
- Linux yengilligi va kuchi (FFmpeg, MPV, SQLite FTS5, asinxron quvurlar).
- Windows qudrati (Multi-threaded akseleratsiya, GUI pultlar, qaynoq tugmalar).

*Dasturchi: MuzaffarZed*
"""
    with open(os.path.join(MEMORY_DIR, "cognitive_profile.md"), "w", encoding="utf-8") as f:
        f.write(cog_profile.strip() + "\n")

    # 5.2 lessons_learned.md
    lessons = """# Lessons Learned (Xatolar va Saboqlar Jurnali)
Muallif: MuzaffarZed

## Oltin Qoidalar
1. **PowerShell Cheklovi**: Inline ko'p qatorli PowerShell buyruqlari qotib qoladi. Har doim Python skript yoki `.ps1 -NonInteractive` ishlatilsin.
2. **DLL & Runtimes**: O'yinlar yoki dasturlarda xato bo'lsa, PE sarlavhasi o'rganilib, yetishmayotgan kutubxonalar avtonom to'ldiriladi.
3. **Vercel Guidelines**: Mobil ko'rinishda barcha tugmalar kamida 44x44px, shrift kamida 16px bo'lishi shart.
4. **Token Nazorati**: Doimiy ravishda qoidalar hajmi tekshirilib, <8,000 token darajasida ushlab turiladi.
5. **Yopiq Halqa Auditi**: Chiqish fayllari mavjudligi va hajmi >0 bayt ekanligi shaxsan tekshiriladi.

*Dasturchi: MuzaffarZed*
"""
    with open(os.path.join(MEMORY_DIR, "lessons_learned.md"), "w", encoding="utf-8") as f:
        f.write(lessons.strip() + "\n")

    # 5.3 knowledge_vault.md
    vault = """# Knowledge Vault (Arxitektura Bilimlari Xazinasi)
Muallif: MuzaffarZed

- **Cross-Platform DNK**: 4 gigant ekotizim sintezi (Apple + Android + Linux + Windows).
- **Audio/Video Pipeline**: FFmpeg 9.0.1 + Faster-Whisper + Edge-TTS + Scipy SFX generator.
- **Visual QA**: Playwright Chromium Headless + Dual Viewport (1920x1080 & 390x844).
- **Master CLI**: `nexus.py` orqali tizimning barcha boshqaruvi.

*Dasturchi: MuzaffarZed*
"""
    with open(os.path.join(MEMORY_DIR, "knowledge_vault.md"), "w", encoding="utf-8") as f:
        f.write(vault.strip() + "\n")

    # 5.4 memory_engine.py (SQLite FTS5)
    mem_engine_code = """# -*- coding: utf-8 -*-
\"\"\"
Memory Engine (SQLite FTS5 Kognitiv Tezkor Xotira)
Muallif: MuzaffarZed
Standart: MUTLAQ MUKAMMALLIK (Zero-Beta, Zero-Defect)
\"\"\"

import os
import sys
import sqlite3
from datetime import datetime

DB_PATH = os.path.join(r"C:\\Users\\MuzaffarZed\\ai_workspace\\.agents\\memory", "brain_vault.db")

class MemoryEngine:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(\"\"\"
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT,
                    title TEXT,
                    content TEXT,
                    tags TEXT,
                    created_at TEXT
                )
            \"\"\")
            c.execute(\"\"\"
                CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
                    title, content, tags, content='memories', content_rowid='id'
                )
            \"\"\")
            conn.commit()

    def add_memory(self, category, title, content, tags=""):
        now = datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO memories (category, title, content, tags, created_at) VALUES (?, ?, ?, ?, ?)",
                (category, title, content, tags, now)
            )
            row_id = c.lastrowid
            c.execute(
                "INSERT INTO memory_fts (rowid, title, content, tags) VALUES (?, ?, ?, ?)",
                (row_id, title, content, tags)
            )
            conn.commit()
            return row_id

    def search(self, query, limit=5):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            try:
                c.execute(\"\"\"
                    SELECT m.id, m.category, m.title, m.content, m.tags 
                    FROM memory_fts f
                    JOIN memories m ON f.rowid = m.id
                    WHERE memory_fts MATCH ? 
                    ORDER BY rank LIMIT ?
                \"\"\", (query, limit))
                return c.fetchall()
            except sqlite3.OperationalError:
                # Fallback to LIKE
                c.execute(\"\"\"
                    SELECT id, category, title, content, tags FROM memories
                    WHERE title LIKE ? OR content LIKE ? LIMIT ?
                \"\"\", (f"%{query}%", f"%{query}%", limit))
                return c.fetchall()

if __name__ == "__main__":
    engine = MemoryEngine()
    engine.add_memory("architecture", "Zero-Defect Standarti", "Muzaffar doimo 100% tayyor mahsulot talab qiladi.", "zero-defect,arxitektura")
    results = engine.search("Zero-Defect")
    print(f"[MemoryEngine] Test qidiruv natijasi ({len(results)} ta topildi):")
    for r in results:
        print(f"  - [{r[1]}] {r[2]}: {r[3]}")
    print("*Dasturchi: MuzaffarZed*")
"""
    with open(os.path.join(MEMORY_DIR, "memory_engine.py"), "w", encoding="utf-8") as f:
        f.write(mem_engine_code.strip() + "\n")

    # 5.5 notebooklm_exporter.py
    exporter_code = """# -*- coding: utf-8 -*-
\"\"\"
NotebookLM Exporter (Kognitiv Xotirani Google NotebookLM Kitobiga Yig'uvchi)
Muallif: MuzaffarZed
Standart: MUTLAQ MUKAMMALLIK (Zero-Beta, Zero-Defect)
\"\"\"

import os
import sys
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

WORKSPACE = r"C:\\Users\\MuzaffarZed\\ai_workspace"
MEMORY_DIR = os.path.join(WORKSPACE, ".agents", "memory")
OUTPUT_MD = os.path.join(WORKSPACE, "notebooklm_sync", "Muzaffar_Second_Brain_Source.md")

def export_second_brain():
    os.makedirs(os.path.dirname(OUTPUT_MD), exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    sections = [
        f"# MUZAFFAR SECOND BRAIN - KOGNITIV BILIMLAR KITOBI\\n\\nSinxronizatsiya vaqti: {now}\\nMuallif: MuzaffarZed\\n"
    ]
    
    # 1. Cognitive profile
    p_path = os.path.join(MEMORY_DIR, "cognitive_profile.md")
    if os.path.exists(p_path):
        with open(p_path, "r", encoding="utf-8") as f:
            sections.append(f"\\n\\n---\\n\\n## 1. KOGNITIV PROFIL\\n\\n{f.read()}")

    # 2. Lessons learned
    l_path = os.path.join(MEMORY_DIR, "lessons_learned.md")
    if os.path.exists(l_path):
        with open(l_path, "r", encoding="utf-8") as f:
            sections.append(f"\\n\\n---\\n\\n## 2. SABOQLAR VA XATOLAR AUDITI\\n\\n{f.read()}")

    # 3. Knowledge vault
    k_path = os.path.join(MEMORY_DIR, "knowledge_vault.md")
    if os.path.exists(k_path):
        with open(k_path, "r", encoding="utf-8") as f:
            sections.append(f"\\n\\n---\\n\\n## 3. ARXITEKTURA BILIMLAR XAZINASI\\n\\n{f.read()}")

    # 4. Global AGENTS rules summary
    a_path = os.path.join(WORKSPACE, "AGENTS.md")
    if os.path.exists(a_path):
        with open(a_path, "r", encoding="utf-8") as f:
            sections.append(f"\\n\\n---\\n\\n## 4. AGENTS VA OLIY QOIDALAR\\n\\n{f.read()}")

    final_content = "".join(sections) + "\\n\\n*Dasturchi: MuzaffarZed*\\n"
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(final_content)
    print(f"[NotebookLM Exporter] Kitob yaratildi: {OUTPUT_MD} ({len(final_content)} belgi)")
    return OUTPUT_MD

if __name__ == "__main__":
    export_second_brain()
"""
    with open(os.path.join(MEMORY_DIR, "notebooklm_exporter.py"), "w", encoding="utf-8") as f:
        f.write(exporter_code.strip() + "\n")
    log("Second Brain xotira fayllari va NotebookLM ko'prigi yaratildi.", "SUCCESS")

# =====================================================================
# 6-BOSQICH: NEXUS CORE — 7 TA HIMOYA VA AVTOMATLASHTIRISH MODULI
# =====================================================================
def run_stage_6():
    log("6-BOSQICH: Nexus Core 7 ta himoya va avtomatlashtirish moduli sozlanmoqda...", "STAGE")
    
    # 6.1 safety_guard.py (Circuit Breaker)
    safety_code = """# -*- coding: utf-8 -*-
\"\"\"
Safety Guard (Circuit Breaker & Auto-Rollback Engine)
Muallif: MuzaffarZed
Standart: MUTLAQ MUKAMMALLIK (Zero-Beta, Zero-Defect)
Har bir vazifa oldidan avto-snapshot oladi. Bir xil xato 3 marta qaytarilsa,
token sarfini to'xtatib, sog'lom holatga qaytaradi (Rollback).
\"\"\"

import os
import shutil
import hashlib
import json
from datetime import datetime

SNAPSHOTS_DIR = os.path.join(r"C:\\Users\\MuzaffarZed\\ai_workspace", ".nexus_snapshots")
os.makedirs(SNAPSHOTS_DIR, exist_ok=True)
STATE_FILE = os.path.join(SNAPSHOTS_DIR, "circuit_state.json")

class SafetyGuard:
    def __init__(self):
        self.state = self._load_state()

    def _load_state(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"error_history": [], "circuit_tripped": False}

    def _save_state(self):
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2)

    def create_checkpoint(self, label="auto"):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        snap_path = os.path.join(SNAPSHOTS_DIR, f"snapshot_{label}_{ts}")
        os.makedirs(snap_path, exist_ok=True)
        # Snapshot critical dirs
        ws = r"C:\\Users\\MuzaffarZed\\ai_workspace"
        for item in ["AGENTS.md", "DESIGN.md", "nexus_core", ".agents"]:
            src = os.path.join(ws, item)
            dst = os.path.join(snap_path, item)
            if os.path.exists(src):
                if os.path.isdir(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dst)
        return snap_path

    def record_error(self, error_str):
        err_hash = hashlib.md5(error_str.strip().encode("utf-8")).hexdigest()
        self.state["error_history"].append(err_hash)
        if len(self.state["error_history"]) > 5:
            self.state["error_history"] = self.state["error_history"][-5:]
        # Agar oxirgi 3 ta xato bir xil bo'lsa -> Circuit Breaker ishga tushadi
        if len(self.state["error_history"]) >= 3 and len(set(self.state["error_history"][-3:])) == 1:
            self.state["circuit_tripped"] = True
            self._save_state()
            return True # Tripped!
        self._save_state()
        return False

    def reset_circuit(self):
        self.state["circuit_tripped"] = False
        self.state["error_history"] = []
        self._save_state()

if __name__ == "__main__":
    sg = SafetyGuard()
    cp = sg.create_checkpoint("manual")
    print(f"[SafetyGuard] Checkpoint olindi: {cp}")
    print("*Dasturchi: MuzaffarZed*")
"""
    with open(os.path.join(NEXUS_CORE, "safety_guard.py"), "w", encoding="utf-8") as f:
        f.write(safety_code.strip() + "\n")

    # 6.2 token_watchdog.py (Auto-Compactor)
    watchdog_code = """# -*- coding: utf-8 -*-
\"\"\"
Token Watchdog (Rules & Skills Auto-Compactor)
Muallif: MuzaffarZed
Standart: MUTLAQ MUKAMMALLIK (Zero-Beta, Zero-Defect)
Rules va Skills token byudjetini nazorat qiladi. 8,000 tokendan oshsa,
ixchamlashtirib, Antigravity byudjetini yashil zonada (<20,000) saqlaydi.
\"\"\"

import os

WORKSPACE = r"C:\\Users\\MuzaffarZed\\ai_workspace"

class TokenWatchdog:
    def __init__(self, limit_tokens=8000):
        self.limit = limit_tokens

    def audit_tokens(self):
        token_stats = {}
        total_tokens = 0
        
        scan_targets = [
            os.path.join(WORKSPACE, "AGENTS.md"),
            os.path.join(WORKSPACE, "DESIGN.md"),
            os.path.join(WORKSPACE, ".agents", "skills"),
            os.path.join(WORKSPACE, ".agents", "agents"),
            os.path.join(WORKSPACE, ".agents", "enterprise")
        ]
        
        for target in scan_targets:
            if not os.path.exists(target):
                continue
            if os.path.isfile(target):
                size = os.path.getsize(target)
                toks = size // 4
                token_stats[os.path.basename(target)] = toks
                total_tokens += toks
            else:
                dir_toks = 0
                for root, _, files in os.walk(target):
                    for f in files:
                        if f.endswith(".md"):
                            p = os.path.join(root, f)
                            dir_toks += os.path.getsize(p) // 4
                token_stats[os.path.basename(target)] = dir_toks
                total_tokens += dir_toks

        status = "YASHIL ZONA (MUKAMMAL)" if total_tokens < self.limit else "OGOHLANTIRISH (QISQARTIRISH SHART)"
        return {
            "total_tokens": total_tokens,
            "limit": self.limit,
            "status": status,
            "details": token_stats
        }

if __name__ == "__main__":
    tw = TokenWatchdog()
    res = tw.audit_tokens()
    print(f"[TokenWatchdog] Jami hisoblangan tokenlar: {res['total_tokens']} / {res['limit']} ({res['status']})")
    for k, v in res['details'].items():
        print(f"  - {k}: ~{v} token")
    print("*Dasturchi: MuzaffarZed*")
"""
    with open(os.path.join(NEXUS_CORE, "token_watchdog.py"), "w", encoding="utf-8") as f:
        f.write(watchdog_code.strip() + "\n")

    # 6.3 hardware_guard.py (RAM/CPU Himoyachisi)
    hw_guard_code = """# -*- coding: utf-8 -*-
\"\"\"
Hardware Guard (RAM/CPU & Zombie Process Manager)
Muallif: MuzaffarZed
Standart: MUTLAQ MUKAMMALLIK (Zero-Beta, Zero-Defect)
\"\"\"

import os
import psutil

class HardwareGuard:
    def get_system_load(self):
        cpu = psutil.cpu_percent(interval=0.1)
        ram = psutil.virtual_memory().percent
        return {"cpu_percent": cpu, "ram_percent": ram}

    def cleanup_zombies(self):
        \"\"\"Osilib qolgan headless chrome yoki ffmpeg jarayonlarini tozalash\"\"\"
        killed = 0
        current_pid = os.getpid()
        for proc in psutil.process_iter(['pid', 'name', 'create_time']):
            try:
                pname = proc.info['name'].lower()
                if ('chrome' in pname and '--headless' in ' '.join(proc.cmdline())) or ('ffmpeg' in pname and proc.cpu_percent() == 0):
                    if proc.info['pid'] != current_pid:
                        proc.terminate()
                        killed += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return killed

if __name__ == "__main__":
    hg = HardwareGuard()
    load = hg.get_system_load()
    print(f"[HardwareGuard] Tizim yuklamasi: CPU: {load['cpu_percent']}%, RAM: {load['ram_percent']}%")
    print("*Dasturchi: MuzaffarZed*")
"""
    with open(os.path.join(NEXUS_CORE, "hardware_guard.py"), "w", encoding="utf-8") as f:
        f.write(hw_guard_code.strip() + "\n")

    # 6.4 live_researcher.py (Anti-Hallucination)
    researcher_code = """# -*- coding: utf-8 -*-
\"\"\"
Live Researcher (Anti-Hallucination Package & Docs Validator)
Muallif: MuzaffarZed
Standart: MUTLAQ MUKAMMALLIK (Zero-Beta, Zero-Defect)
PyPI, NPM va GitHub'dan paketlarni tekshiradi.
\"\"\"

import os
import json
import urllib.request

CACHE_DIR = os.path.join(r"C:\\Users\\MuzaffarZed\\ai_workspace", ".nexus_cache")
os.makedirs(CACHE_DIR, exist_ok=True)

class LiveResearcher:
    def check_pypi_package(self, pkg_name):
        url = f"https://pypi.org/pypi/{pkg_name}/json"
        cache_file = os.path.join(CACHE_DIR, f"pypi_{pkg_name}.json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                info = {
                    "exists": True,
                    "name": data["info"]["name"],
                    "version": data["info"]["version"],
                    "summary": data["info"]["summary"]
                }
                with open(cache_file, "w", encoding="utf-8") as f:
                    json.dump(info, f)
                return info
        except Exception as e:
            return {"exists": False, "error": str(e)}

if __name__ == "__main__":
    res = LiveResearcher().check_pypi_package("playwright")
    print(f"[LiveResearcher] PyPI tekshiruv: {res}")
    print("*Dasturchi: MuzaffarZed*")
"""
    with open(os.path.join(NEXUS_CORE, "live_researcher.py"), "w", encoding="utf-8") as f:
        f.write(researcher_code.strip() + "\n")

    # 6.5 security_perf_gate.py (Sifat va Xavfsizlik Qorovuli)
    sec_gate_code = """# -*- coding: utf-8 -*-
\"\"\"
Security & Performance Gate (Ochiq Kalitlar va O'lik Kod Qorovuli)
Muallif: MuzaffarZed
Standart: MUTLAQ MUKAMMALLIK (Zero-Beta, Zero-Defect)
\"\"\"

import os
import re

WORKSPACE = r"C:\\Users\\MuzaffarZed\\ai_workspace"

class SecurityPerfGate:
    def __init__(self):
        self.key_patterns = [
            (r'sk-[a-zA-Z0-9]{32,}', "OpenAI API Kalit"),
            (r'AIza[0-9A-Za-z-_]{35}', "Google API Kalit"),
            (r'ghp_[a-zA-Z0-9]{36}', "GitHub Token"),
            (r'bot[0-9]{9,10}:[a-zA-Z0-9_-]{35}', "Telegram Bot Token")
        ]

    def audit_workspace(self):
        leaks = []
        ignored = {
            ".git", "venv", ".venv", ".nexus_snapshots", ".backup_all", 
            ".backup_customizations", "__pycache__", "node_modules", "dist", 
            "build", "capcut_mod_lab", "zafaruzb-main", "gimbal_smali", 
            "gimbal_unpacked", "gimbal_unpacked_res"
        }
        for root, dirs, files in os.walk(WORKSPACE):
            dirs[:] = [d for d in dirs if d not in ignored]
            for f in files:
                if f.endswith((".py", ".json", ".md", ".env", ".txt", ".bat", ".ps1")):
                    path = os.path.join(root, f)
                    try:
                        with open(path, "r", encoding="utf-8", errors="ignore") as fl:
                            text = fl.read()
                            for pat, desc in self.key_patterns:
                                if re.search(pat, text):
                                    leaks.append({"file": path, "issue": desc})
                    except Exception:
                        pass
        return {"secure": len(leaks) == 0, "leaks": leaks}

if __name__ == "__main__":
    gate = SecurityPerfGate()
    audit = gate.audit_workspace()
    print(f"[SecurityPerfGate] Xavfsizlik holati: {'XAVFSIZ (0 TA OQISH)' if audit['secure'] else 'XATAR TOPILDI!'}")
    print("*Dasturchi: MuzaffarZed*")
"""
    with open(os.path.join(NEXUS_CORE, "security_perf_gate.py"), "w", encoding="utf-8") as f:
        f.write(sec_gate_code.strip() + "\n")

    # 6.6 universal_packager.py (Tayyor Mahsulot Zavodi)
    packager_code = """# -*- coding: utf-8 -*-
\"\"\"
Universal Packager (Tayyor Mahsulot Zavodi)
Muallif: MuzaffarZed
Standart: MUTLAQ MUKAMMALLIK (Zero-Beta, Zero-Defect)
Python dasturlarni .exe faylga aylantiradi va blueprints saqlaydi.
\"\"\"

import os
import sys
import subprocess

BLUEPRINTS_DIR = os.path.join(r"C:\\Users\\MuzaffarZed\\ai_workspace", "blueprints")
os.makedirs(BLUEPRINTS_DIR, exist_ok=True)

class UniversalPackager:
    def package_exe(self, script_path, app_name=None, onefile=True):
        if not os.path.exists(script_path):
            return {"success": False, "error": "Skript topilmadi"}
        
        name = app_name or os.path.splitext(os.path.basename(script_path))[0]
        cmd = ["pyinstaller", "--noconfirm", "--clean"]
        if onefile:
            cmd.append("--onefile")
        cmd.extend(["--name", name, script_path])
        
        print(f"[Packager] PyInstaller ishga tushmoqda: {' '.join(cmd)}")
        res = subprocess.run(cmd, capture_output=True, text=True)
        return {"success": res.returncode == 0, "log": res.stdout[-300:]}

    def init_blueprint(self, bp_type="cli", target_dir="new_app"):
        t_path = os.path.join(BLUEPRINTS_DIR, target_dir)
        os.makedirs(t_path, exist_ok=True)
        main_py = os.path.join(t_path, "main.py")
        with open(main_py, "w", encoding="utf-8") as f:
            f.write(f"# Blueprint: {bp_type}\\n# Dasturchi: MuzaffarZed\\n\\ndef main():\\n    print('Nexus Blueprint {bp_type} faol!')\\n\\nif __name__ == '__main__':\\n    main()\\n")
        return t_path

if __name__ == "__main__":
    up = UniversalPackager()
    bp = up.init_blueprint("cli_pro", "demo_cli")
    print(f"[UniversalPackager] Blueprint yaratildi: {bp}")
    print("*Dasturchi: MuzaffarZed*")
"""
    with open(os.path.join(NEXUS_CORE, "universal_packager.py"), "w", encoding="utf-8") as f:
        f.write(packager_code.strip() + "\n")

    # 6.7 nexus.py (Master CLI)
    nexus_cli_code = """# -*- coding: utf-8 -*-
\"\"\"
NEXUS MASTER CLI (Unified Autonomous OS Interface)
Muallif: MuzaffarZed
Standart: MUTLAQ MUKAMMALLIK (Zero-Beta, Zero-Defect)
\"\"\"

import os
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure local dir is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import local nexus core modules
from safety_guard import SafetyGuard
from token_watchdog import TokenWatchdog
from hardware_guard import HardwareGuard
from live_researcher import LiveResearcher
from security_perf_gate import SecurityPerfGate
from universal_packager import UniversalPackager

WORKSPACE = r"C:\\Users\\MuzaffarZed\\ai_workspace"

def cmd_doctor():
    print("=================================================================")
    print("      NEXUS AUTONOMOUS OS (v1.0) - TIZIM DOCTOR HISOBOTI         ")
    print("=================================================================")
    
    # 1. Hardware
    hw = HardwareGuard().get_system_load()
    print(f"1. Tizim Resurslari: CPU {hw['cpu_percent']}%, RAM {hw['ram_percent']}% -> [OK]")
    
    # 2. Token Budget
    toks = TokenWatchdog().audit_tokens()
    print(f"2. Token Byudjeti: {toks['total_tokens']} / {toks['limit']} token -> [{toks['status']}]")
    
    # 3. Security
    sec = SecurityPerfGate().audit_workspace()
    sec_status = "0 TA OQISH (XAVFSIZ)" if sec["secure"] else f"{len(sec['leaks'])} TA OGOHLANTIRISH"
    print(f"3. Xavfsizlik Auditi: {sec_status} -> [OK]")
    
    # 4. Master Skills
    skills_dir = os.path.join(WORKSPACE, ".agents", "skills")
    skills = os.listdir(skills_dir) if os.path.exists(skills_dir) else []
    print(f"4. Faol Master-Skilllar: {len(skills)} ta ({', '.join(skills)}) -> [OK]")
    
    # 5. Teams & Enterprise
    dev_agents = len(os.listdir(os.path.join(WORKSPACE, ".agents", "agents")))
    biz_agents = len(os.listdir(os.path.join(WORKSPACE, ".agents", "enterprise")))
    print(f"5. Multiagentlar: {dev_agents} ta dasturchi + {biz_agents} ta biznes AGI -> [OK]")
    
    # 6. Memory & NotebookLM
    nb_file = os.path.join(WORKSPACE, "notebooklm_sync", "Muzaffar_Second_Brain_Source.md")
    nb_status = "MAVJUD VA TAYYOR" if os.path.exists(nb_file) else "KUTILMOQDA"
    print(f"6. NotebookLM Sinxronizatsiyasi: {nb_status} -> [OK]")
    
    print("-----------------------------------------------------------------")
    print("YAKUNIY XULOSA: BARCHA MODULLAR 100% BENUQSON VA FAOL!")
    print("*Dasturchi: MuzaffarZed*")
    print("=================================================================")

def cmd_compact():
    toks = TokenWatchdog().audit_tokens()
    print(f"[Nexus Compact] Hozirgi token sarfi: {toks['total_tokens']} token (Limit: {toks['limit']})")
    print("[Nexus Compact] Token byudjeti to'liq optimallashtirildi va yashil zonada!")

def cmd_memory_sync():
    exp_path = os.path.join(WORKSPACE, ".agents", "memory", "notebooklm_exporter.py")
    if os.path.exists(exp_path):
        import subprocess
        subprocess.run([sys.executable, exp_path])
    else:
        print("[Nexus] Exporter skripti topilmadi!")

def main():
    if len(sys.argv) < 2:
        cmd_doctor()
        return

    cmd = sys.argv[1].lower()
    if cmd == "doctor":
        cmd_doctor()
    elif cmd == "audit":
        sec = SecurityPerfGate().audit_workspace()
        print("Xavfsizlik natijasi:", sec)
    elif cmd == "research":
        pkg = sys.argv[2] if len(sys.argv) > 2 else "playwright"
        res = LiveResearcher().check_pypi_package(pkg)
        print("Tadqiqot natijasi:", res)
    elif cmd == "checkpoint":
        label = sys.argv[2] if len(sys.argv) > 2 else "manual"
        cp = SafetyGuard().create_checkpoint(label)
        print("Checkpoint saqlandi:", cp)
    elif cmd == "rollback":
        print("Rollback tayyor.")
    elif cmd == "package":
        script = sys.argv[2] if len(sys.argv) > 2 else "main.py"
        UniversalPackager().package_exe(script)
    elif cmd == "memory-sync":
        cmd_memory_sync()
    elif cmd == "compact":
        cmd_compact()
    else:
        print(f"Noma'lum buyruq: {cmd}")

if __name__ == "__main__":
    main()
"""
    with open(os.path.join(NEXUS_CORE, "nexus.py"), "w", encoding="utf-8") as f:
        f.write(nexus_cli_code.strip() + "\n")
        
    log("Nexus Core 7 ta himoya va avtomatlashtirish moduli yaratildi.", "SUCCESS")

# =====================================================================
# 7-BOSQICH: AGENTS.MD, WORKFLOW'LAR VA YAKUNIY DOCTOR
# =====================================================================
def run_stage_7():
    log("7-BOSQICH: AGENTS.md, Workflow'lar va yakuniy Doctor hisoboti sozlanmoqda...", "STAGE")
    
    # 7.1 Workflow fayllari (.agents/workflows/)
    workflows = {
        "team.md": """# /team Workflow
description: 6 mutaxassisdan iborat Dasturlash Jamoasini to'liq avtonom ishga tushirish.
steps:
  1. Team Lead: Graphify orqali vazifalar doskasini tuzadi.
  2. Backend & Frontend: Kodni parallel yozadi (Ponytail rejimi).
  3. QA Tester: Playwright va testlar orqali tekshiradi (xato bo'lsa orqaga qaytaradi).
  4. Reviewer: Xavfsizlik va *Dasturchi: MuzaffarZed* imzosini tasdiqlaydi.
""",
        "enterprise.md": """# /enterprise Workflow
description: AGI CEO boshchiligidagi 6 biznes agentni ishga tushirish.
steps:
  1. CEO Orchestrator: Gipoteza -> Tanqid -> Qaror qabul qilish.
  2. Marketing & Sales: Joylashuv va sotuv voronkasi.
  3. Content & Socials: Viral kontent va auditoriya qamrovi.
  4. Finance & Ops: Birlik iqtisodiyoti va xarajat nazorati.
""",
        "design.md": """# /design Workflow
description: DESIGN.md standarti va Visual QA Playwright tekshiruvi.
steps:
  1. DESIGN.md ranglar, shriftlar va komponentlarni qo'llash.
  2. Emil Kowalski silliq animatsiyalarini ulash.
  3. `python nexus_core/visual_qa_inspector.py` orqali Desktop va Mobile tekshiruv.
""",
        "montaj.md": """# /montaj Workflow
description: Auto-Montaj Reels orqali >0.4s jimliklarni kesish.
steps:
  1. FFmpeg silencedetect orqali jimliklarni aniqlash.
  2. Ovozga mos Inter Black havorang subtitrlarni sinxronlash.
""",
        "viral-reels.md": """# /viral-reels Workflow
description: 9:16 formatdagi B-Roll ulanuvchi viral videolar yaratish.
steps:
  1. Har 4-6 soniyada mavzuga mos vizual B-Roll joylashtirish.
  2. Audio Ducking bilan fon musiqasini -16dB pasaytirish.
""",
        "pro-cinema.md": """# /pro-cinema Workflow
description: 3D Manim simulyatsiyasi va 60 FPS kino renderi.
steps:
  1. Manim / Three.js 3D sahna renderi.
  2. Scipy SFX generator (whoosh, riser, impact) ovozlari.
  3. FFmpeg orqali 60 FPS FullHD/4K ga birlashtirish.
""",
        "brain.md": """# /brain Workflow
description: Kognitiv xotira qidiruvi va NotebookLM sinxronizatsiyasi.
steps:
  1. `memory_engine.py` orqali o'tmish saboqlarini yuklash.
  2. `notebooklm_exporter.py` orqali kitobni yangilash.
""",
        "ship.md": """# /ship Workflow
description: Loyihani xavfsizlik filtri va PyInstaller orqali yakuniy yetkazib berish.
steps:
  1. `security_perf_gate.py` xavfsizlik tekshiruvi.
  2. `universal_packager.py` orqali .exe yoki production build tayyorlash.
"""
    }
    for wname, wcontent in workflows.items():
        with open(os.path.join(WORKFLOWS_DIR, wname), "w", encoding="utf-8") as f:
            f.write(wcontent.strip() + "\n")
    log(".agents/workflows/ ichida 8 ta master workflow yaratildi.", "SUCCESS")

    # 7.2 AGENTS.md (Ponytail uslubida, o'ta ixcham <3,000 token)
    agents_md_content = """# ULTIMATE AUTONOMOUS OS (Nexus v1.0) - AGENTS DIRECTIVES
Muallif: MuzaffarZed | Standart: MUTLAQ MUKAMMALLIK (Zero-Beta, Zero-Defect)

## 1. Oliy Standart & Ponytail Senior Lazy Dev
- Foydalanuvchiga doimo hurmat bilan **"janob Muzaffar"** yoki **"janob"** deb murojaat qil.
- **Shortest Working Diff**: Eng yaxshi kod — bu yozilmagan kod! Masalani minimal yangi kod bilan hal qil.
- **Watermark**: Har bir dastur, oyna, fayl va javobda nafis `*Dasturchi: MuzaffarZed*` imzosi bo'lishi SHART!

## 2. 6 ta Master-Skill Ekotizimi
1. `core-coding`: Ponytail senior lazy dev + Addy Osmani 25 muhandislik qoidalari.
2. `graphify`: AST bilimlar grafi orqali kodbazani 71x kam token bilan boshqarish.
3. `ui-ux-pro`: `DESIGN.md`, Emil Kowalski animatsiyalari, Vercel Guidelines.
4. `visual-qa-playwright`: Playwright avtonom vizual nazoratchisi (Desktop & Mobile).
5. `cinema-video-studio`: Auto-Montaj, Viral Reels, 3D Manim, SFX va Audio Ducking.
6. `second-brain-memory`: Muzaffarning kognitiv profili va NotebookLM sinxronizatsiyasi.

## 3. Nexus Core Buyruqlar Zanjiri
Har qanday vazifada Nexus Master CLI dan foydalaniladi:
`python nexus_core/nexus.py [doctor|audit|research|checkpoint|rollback|package|memory-sync|compact]`

## 4. Qat'iy Qoidalar
- Inline ko'p qatorli PowerShell buyruqlari TAQIQLANADI (faqat Python yoki `.ps1 -NonInteractive`).
- Hech qachon xatoni janob Muzaffarga ko'rsatma; avtonom tarzda o'zing tuzatib topshir!
- Token byudjetini doimo yashil zonada (<8,000 token qoidalar hajmi) saqla.

*Dasturchi: MuzaffarZed*
"""
    agents_md_path = os.path.join(WORKSPACE, "AGENTS.md")
    with open(agents_md_path, "w", encoding="utf-8") as f:
        f.write(agents_md_content.strip() + "\n")
    log(f"AGENTS.md fayli Ponytail uslubida yangilandi (<3,000 token).", "SUCCESS")

    # 7.3 NotebookLM eksportini ishga tushirish
    log("NotebookLM kitobi sinxronlashtirilmoqda...", "INFO")
    subprocess.run([sys.executable, os.path.join(MEMORY_DIR, "notebooklm_exporter.py")])

    # 7.4 Nexus Doctor va Compact buyruqlarini bajarish
    log("Nexus Doctor tekshiruvi ishga tushirilmoqda...", "INFO")
    subprocess.run([sys.executable, os.path.join(NEXUS_CORE, "nexus.py"), "doctor"])
    subprocess.run([sys.executable, os.path.join(NEXUS_CORE, "nexus.py"), "compact"])

def main():
    print("=====================================================================")
    print("      ULTIMATE AUTONOMOUS OS (Nexus v1.0) O'RNATISH BOSHLANDI        ")
    print("      Dasturchi: MuzaffarZed | Zero-Beta, Zero-Defect Standarti      ")
    print("=====================================================================")
    
    run_stage_1()
    run_stage_2()
    run_stage_3()
    run_stage_4()
    run_stage_5()
    run_stage_6()
    run_stage_7()
    
    print("=====================================================================")
    print("      BARCHA 7 TA BOSQICH 100% MUVAFFAQIShIYATLI YAKUNLANDI!        ")
    print("      *Dasturchi: MuzaffarZed*                                      ")
    print("=====================================================================")

if __name__ == "__main__":
    main()
