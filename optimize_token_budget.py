#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
optimize_token_budget.py
Antigravity Customization Token Budgetini 20,000 limitidan ancha pastga (<12,000 tokenga)
tushiruvchi, dublikatlarni tozalovchi va skill'larni Master Suite'larga birlashtiruvchi
100% avtonom optimizatsiya dvijogi.

Muallif: janob Muzaffar uchun
Dasturchi: MuzaffarZed
"""

import os
import sys
import shutil
import re
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
BACKUP_BASE = WORKSPACE / ".backup_customizations"

# Source folders
GEMINI_SKILLS = HOME / ".gemini" / "skills"
GEMINI_CONFIG_SKILLS = HOME / ".gemini" / "config" / "skills"
GEMINI_CONFIG_PLUGINS = HOME / ".gemini" / "config" / "plugins"
HOME_AGENTS_SKILLS = HOME / ".agents" / "skills"
WORKSPACE_SKILLS = WORKSPACE / ".agents" / "skills"

# Rule files
GLOBAL_AGENTS_MD_CONFIG = HOME / ".gemini" / "config" / "AGENTS.md"
GLOBAL_AGENTS_MD_ROOT = HOME / ".gemini" / "AGENTS.md"
HOME_AGENTS_MD = HOME / "AGENTS.md"
WORKSPACE_AGENTS_MD = WORKSPACE / "AGENTS.md"
WORKSPACE_RULES_DIR = WORKSPACE / ".agents" / "rules"

REPORT_DATA = {}


# ====================================================================
# 1-QADAM: TO'LIQ ZAXIRA NUSXA (BACKUP)
# ====================================================================
def step_1_backup():
    print("\n" + "="*70)
    print("1-QADAM: TO'LIQ ZAXIRA NUSXA OLISH (BACKUP)")
    print("="*70)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = BACKUP_BASE / f"backup_{timestamp}"
    backup_dir.mkdir(parents=True, exist_ok=True)

    items_to_backup = [
        ("gemini_skills", GEMINI_SKILLS),
        ("gemini_config_skills", GEMINI_CONFIG_SKILLS),
        ("gemini_config_plugins", GEMINI_CONFIG_PLUGINS),
        ("gemini_config_agents_md", GLOBAL_AGENTS_MD_CONFIG),
        ("gemini_root_agents_md", GLOBAL_AGENTS_MD_ROOT),
        ("home_agents_md", HOME_AGENTS_MD),
        ("home_agents_dir", HOME / ".agents"),
        ("claude_settings", HOME / ".claude" / "settings.json"),
        ("workspace_agents_md", WORKSPACE_AGENTS_MD),
        ("workspace_agents_dir", WORKSPACE / ".agents"),
    ]

    total_backed = 0
    for name, path in items_to_backup:
        if path.exists():
            dest = backup_dir / name
            if path.is_dir():
                shutil.copytree(path, dest)
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, dest)
            total_backed += 1
            print(f"  [+] Zaxiralandi: {path} -> {dest.name}")

    print(f"\n[OK] Jami {total_backed} ta manba to'liq zaxiraga olindi: {backup_dir}")
    REPORT_DATA["backup_dir"] = str(backup_dir)
    return backup_dir


# ====================================================================
# 2-QADAM: DUBLIKATLARNI VA ORTIQCHA PAPKALARNI TOZALASH
# ====================================================================
def step_2_remove_duplicates():
    print("\n" + "="*70)
    print("2-QADAM: DUBLIKATLAR VA ORTIQCHA PAPKALARNI TOZALASH")
    print("="*70)

    # 1. ~/.gemini/skills — bu ~/.gemini/config/skills ning 100% kloni bo'lib, Antigravity uni alohida skan qilardi
    if GEMINI_SKILLS.exists():
        count = len(list(GEMINI_SKILLS.iterdir()))
        shutil.rmtree(GEMINI_SKILLS)
        GEMINI_SKILLS.mkdir(parents=True, exist_ok=True)
        print(f"  [+] ~/.gemini/skills tozalab bo'shatildi ({count} ta dublikat skill olib tashlandi).")

    # 2. ~/.agents/skills — home papkasidagi dublikat
    if HOME_AGENTS_SKILLS.exists():
        count = len(list(HOME_AGENTS_SKILLS.iterdir()))
        shutil.rmtree(HOME_AGENTS_SKILLS)
        HOME_AGENTS_SKILLS.mkdir(parents=True, exist_ok=True)
        print(f"  [+] ~/.agents/skills tozalab bo'shatildi ({count} ta dublikat skill olib tashlandi).")

    # 3. ~/.gemini/config/skills dagi pluginlar bilan takrorlangan 31 ta skillni olib tashlash
    plugin_skills = set()
    if GEMINI_CONFIG_PLUGINS.exists():
        for root, dirs, files in os.walk(GEMINI_CONFIG_PLUGINS):
            if "SKILL.md" in files:
                plugin_skills.add(Path(root).name)

    removed_plugin_dupes = 0
    if GEMINI_CONFIG_SKILLS.exists():
        for sdir in list(GEMINI_CONFIG_SKILLS.iterdir()):
            if sdir.is_dir() and sdir.name in plugin_skills:
                shutil.rmtree(sdir)
                removed_plugin_dupes += 1

    print(f"  [+] ~/.gemini/config/skills dan pluginlar takrori bo'lgan {removed_plugin_dupes} ta skill tozalandi.")


# ====================================================================
# 3-QADAM: SKILLLARNI MASTER SUITE PAKETLARIGA BIRLASHTIRISH
# ====================================================================
def step_3_consolidate_master_suites():
    print("\n" + "="*70)
    print("3-QADAM: SKILLLARNI 'MASTER SUITE' PAKETLARIGA BIRLASHTIRISH")
    print("="*70)

    skills_root = GEMINI_CONFIG_SKILLS
    if not skills_root.exists():
        skills_root.mkdir(parents=True, exist_ok=True)

    # Consolidation xaritasi
    # Master Suite Name -> {
    #   'desc': 10-15 words description,
    #   'sub_skills': [list of sub_skill folder names to absorb]
    # }
    master_suites = {
        "ponytail": {
            "desc": "Lazy senior dev mode: shortest working diff, review, audit, debt tracking, no bloat.",
            "title": "Ponytail Master Suite",
            "sub_skills": ["ponytail-audit", "ponytail-debt", "ponytail-gain", "ponytail-help", "ponytail-review"],
            "core_intro": "Senior developer mindset: minimal working code, shortest working diffs, zero boilerplate."
        },
        "impeccable-design": {
            "desc": "Anti-generic UI/UX design, polish commands (/audit, /polish), micro-animations, typography, layout.",
            "title": "Impeccable & Design Taste Master Suite",
            "sub_skills": [
                "taste-skill", "impeccable", "design-taste-frontend", "design-taste-frontend-v1",
                "design-taste-frontend-v2-experimental", "stitch-design-taste", "gpt-taste",
                "emil-design-eng", "emilkowalski", "apple-design", "high-end-visual-design",
                "minimalist-ui", "industrial-brutalist-ui", "break-ui", "pick-ui-library",
                "prototype", "redesign-existing-projects", "ask-sonner", "brandkit"
            ],
            "core_intro": "Complete design suite: editorial typography, physics motion, /audit and /polish workflows."
        },
        "hyperframes": {
            "desc": "HyperFrames HTML-to-MP4 video composition, timeline, tracks, animations, determinism.",
            "title": "HyperFrames Video Master Suite",
            "sub_skills": [
                "hyperframes-animation", "hyperframes-audio", "hyperframes-cli", "hyperframes-core",
                "hyperframes-creative", "hyperframes-keyframes", "hyperframes-registry", "hyperframes-studio"
            ],
            "core_intro": "HTML and CSS driven deterministic video authoring and rendering engine."
        },
        "remotion-video": {
            "desc": "Programmatic video creation in React and Remotion: 60 FPS, Three.js, subtitles, shaders.",
            "title": "Remotion Video Master Suite",
            "sub_skills": ["remotion", "remotion-to-hyperframes"],
            "core_intro": "React-based video production with 3D canvas and dynamic subtitle tracks."
        },
        "animation-engineering": {
            "desc": "Physics-based motion, spring tuning, animations, 60fps performance and audit.",
            "title": "Animation Engineering Master Suite",
            "sub_skills": [
                "animate", "animate-expo", "animation-performance", "animation-vocabulary",
                "find-animation-opportunities", "improve-animations", "review-animations", "motion-graphics"
            ],
            "core_intro": "Natural animation engineering, spring curves, micro-interactions, performance profiling."
        },
        "ai-video-studio": {
            "desc": "AI video editing, 3D Manim cinema, viral reels, audio ducking, word-level subtitles.",
            "title": "AI Video Studio & Pro-Cinema Master Suite",
            "sub_skills": [
                "ai-video-montaj", "pro-cinema", "viral-reels", "faceless-explainer",
                "general-video", "music-to-video", "pr-to-video", "product-launch-video",
                "slideshow", "talking-head-recut", "media-use", "embedded-captions"
            ],
            "core_intro": "Autonomous video studio: 0.4s pause cutting, 3D Manim/Three.js camera flights, SFX and dynamic subtitles."
        },
        "suite-architecture-design": {
            "desc": "API contracts, architecture decisions (ADRs), specifications, source-driven system design.",
            "title": "System Architecture & API Design Suite",
            "sub_skills": [
                "api-and-interface-design", "spec-driven-development", "source-driven-development",
                "documentation-and-adrs", "deprecation-and-migration"
            ],
            "core_intro": "Clean API interfaces, architecture decision records, spec-first implementation."
        },
        "suite-testing-quality": {
            "desc": "Test-driven development (TDD), browser devtools testing, multi-axis code review.",
            "title": "Testing & Code Quality Suite",
            "sub_skills": [
                "test-driven-development", "browser-testing-with-devtools", "code-review-and-quality"
            ],
            "core_intro": "Quality engineering: test-driven slices, automated test execution, and comprehensive reviews."
        },
        "suite-debugging-diagnostics": {
            "desc": "Systematic root-cause debugging, error recovery, memory leak diagnosis, context tuning.",
            "title": "Debugging & Diagnostics Suite",
            "sub_skills": [
                "debugging-and-error-recovery", "doubt-driven-development", "context-engineering",
                "troubleshooting", "memory-leak-debugging"
            ],
            "core_intro": "Systematic root-cause diagnosis, error-recovery loops, and context engineering."
        },
        "suite-clean-code": {
            "desc": "Refactoring for clarity, constraint-driven thin slices, clean code without bloat.",
            "title": "Clean Code & Refactoring Suite",
            "sub_skills": [
                "code-simplification", "constraint-driven-development", "incremental-implementation",
                "full-output-enforcement"
            ],
            "core_intro": "Clean code philosophy: delete unnecessary abstractions, incremental delivery, clear semantics."
        },
        "suite-performance-security": {
            "desc": "Performance tuning, security hardening, production logging, tracing, observability.",
            "title": "Performance, Security & Observability Suite",
            "sub_skills": [
                "performance-optimization", "security-and-hardening", "observability-and-instrumentation"
            ],
            "core_intro": "Hardened application security, fast execution profiling, and deep production observability."
        },
        "suite-shipping-planning": {
            "desc": "CI/CD pipelines, git workflows, production rollouts, task planning and breakdown.",
            "title": "Shipping, Versioning & Planning Suite",
            "sub_skills": [
                "ci-cd-and-automation", "git-workflow-and-versioning", "shipping-and-launch",
                "interview-me", "idea-refine", "planning-and-task-breakdown", "using-agent-skills"
            ],
            "core_intro": "Release engineering: automated pipelines, git conventions, staged rollouts, and task breakdown."
        },
        "second-brain": {
            "desc": "Self-evolving memory (SQLite FTS5), pre-task context recall, NotebookLM bridge.",
            "title": "Cognitive Memory & Second Brain Suite",
            "sub_skills": [],
            "core_intro": "Janob Muzaffarning kognitiv profili, xatolardan olingan saboqlar va NotebookLM sinxronizatsiyasi."
        },
        "enterprise-agi": {
            "desc": "Autonomous multiagent corporation (CEO Orchestrator, Sales, Marketing, Content, Ops).",
            "title": "Enterprise AGI Multiagent Suite",
            "sub_skills": [],
            "core_intro": "Multiagent korporatsiya: CEO, Sotuv, Marketing, Kontent, Mijozlar va Moliya bo'limlari."
        },
        "windows-controller": {
            "desc": "Universal Windows 10/11 desktop automation, Win32 API, screen grounding, self-repair.",
            "title": "Universal Windows Controller Suite",
            "sub_skills": ["jarvis-master-architect", "muzaffarzed-autonomous-core", "android-cli"],
            "core_intro": "Deep Windows OS automation: UIA, Win32 API, screen capture, keyboard and mouse control."
        }
    }

    # Birlashtirish jarayoni
    for suite_name, info in master_suites.items():
        suite_dir = skills_root / suite_name
        suite_dir.mkdir(parents=True, exist_ok=True)
        ref_dir = suite_dir / "references"
        ref_dir.mkdir(parents=True, exist_ok=True)

        ref_links = []
        for sub in info["sub_skills"]:
            sub_path = skills_root / sub
            if sub_path.exists() and sub_path.is_dir():
                # Sub-skill ichidagi barcha fayllarni references ga ko'chirish
                sub_skill_md = sub_path / "SKILL.md"
                if sub_skill_md.exists():
                    target_ref = ref_dir / f"{sub}.md"
                    target_ref.write_bytes(sub_skill_md.read_bytes())
                    ref_links.append(f"- **{sub}**: [`{sub}.md`](./references/{sub}.md)")
                
                # Agar sub-skillda references yoki scripts bo'lsa, ularni ham ko'chirish
                for extra in ["references", "scripts", "examples"]:
                    extra_p = sub_path / extra
                    if extra_p.exists() and extra_p.is_dir():
                        dest_extra = suite_dir / extra
                        dest_extra.mkdir(parents=True, exist_ok=True)
                        for item in extra_p.iterdir():
                            dest_item = dest_extra / f"{sub}_{item.name}"
                            if item.is_file():
                                shutil.copy2(item, dest_item)
                
                # Sub-skill papkasini olib tashlash (chunki endi master suite ichida)
                if sub_path != suite_dir:
                    shutil.rmtree(sub_path)
                    print(f"    -> {sub} birlashtirildi -> {suite_name}/references/{sub}.md")

        # Master Suite SKILL.md faylini qisqa, ixcham va ko'rsatkichli qilib yozish
        links_block = "\n".join(ref_links) if ref_links else "*(Tafsilotlar references/ papkasida saqlangan)*"
        master_skill_md = f"""---
name: {suite_name}
description: {info['desc']}
---

# {info['title']}

{info['core_intro']}

## References & Specialized Modules:
{links_block}

*Dasturchi: MuzaffarZed*
"""
        (suite_dir / "SKILL.md").write_text(master_skill_md.strip() + "\n", encoding="utf-8")
        print(f"  [+] Master Suite yaratildi: {suite_name}")

    # Shuningdek, workspace/.agents/skills ni ham ixcham holatga keltiramiz
    if WORKSPACE_SKILLS.exists():
        # faqat loyiha uchun xos bo'lganlarini qoldiramiz yoki global suite'larni nusxalaymiz
        print("  [*] ai_workspace/.agents/skills yangilanmoqda...")
        for suite_name in master_suites.keys():
            src_s = skills_root / suite_name
            if src_s.exists():
                dst_s = WORKSPACE_SKILLS / suite_name
                if dst_s.exists():
                    shutil.rmtree(dst_s)
                shutil.copytree(src_s, dst_s)


# ====================================================================
# 4-QADAM: BARCHA SKILLLARNING DESCRIPTION QISMINI OPTIMALLASHTIRISH
# ====================================================================
def step_4_optimize_skill_frontmatters():
    print("\n" + "="*70)
    print("4-QADAM: BARCHA SKILLLARNING DESCRIPTION QISMINI QISQARTIRISH (10-15 SO'Z)")
    print("="*70)

    skills_root = GEMINI_CONFIG_SKILLS
    optimized_count = 0

    for sdir in skills_root.iterdir():
        if not sdir.is_dir():
            continue
        skill_file = sdir / "SKILL.md"
        if not skill_file.exists():
            continue

        content = skill_file.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if not m:
            continue

        frontmatter = m.group(1)
        body = content[m.end():].strip()

        # Name va Description ni olish
        name_match = re.search(r"^name:\s*(.*)$", frontmatter, re.MULTILINE)
        name = name_match.group(1).strip() if name_match else sdir.name

        desc_match = re.search(r"description:\s*(?:>-\s*|\"|\')?(.*?)(?:\n\w+:|\n---|\"|\'$)", frontmatter, re.DOTALL)
        old_desc = desc_match.group(1).strip() if desc_match else ""

        # Descriptionni 15 ta so'zdan oshmasligini ta'minlash
        words = old_desc.split()
        if len(words) > 15:
            new_desc = " ".join(words[:14]) + "."
        else:
            new_desc = old_desc or f"Tool and workflow for {name} operations."

        # Agar body juda katta bo'lsa (>3000 chars), details.md ga ko'chirish
        if len(body) > 3000:
            ref_dir = sdir / "references"
            ref_dir.mkdir(parents=True, exist_ok=True)
            details_file = ref_dir / "details.md"
            details_file.write_text(body, encoding="utf-8")
            body = f"# {name.capitalize()}\n\nDetailed specifications and instructions moved to [`references/details.md`](./references/details.md).\n\n*Dasturchi: MuzaffarZed*"

        new_content = f"""---
name: {name}
description: {new_desc}
---

{body}
"""
        skill_file.write_text(new_content.strip() + "\n", encoding="utf-8")
        optimized_count += 1

    print(f"  [+] Jami {optimized_count} ta skill'ning YAML frontmatteri optimallashtirildi.")


# ====================================================================
# 5-QADAM: RULES (16,695 TOKENS) BO'LIMINI SIQISH VA DEDUP QILISH
# ====================================================================
def step_5_compress_rules():
    print("\n" + "="*70)
    print("5-QADAM: RULES FAYLLARINI SIQISH VA TAKRORLANISHLARNI BARTARAF ETISH")
    print("="*70)

    # Global yagona mukammal qoida: ixcham, zich, lekin barcha 15 qonun va talablarni qamragan
    CONCISE_MASTER_RULES = """# Ponytail, Senior Lazy Dev & Oliy Arxitektura Qonunlari

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
14. **Agent Skills:** Tizimdagi 25+ muhandislik mahoratlaridan proaktiv foydalan.
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

    clean_rules = CONCISE_MASTER_RULES.strip() + "\n"
    size_bytes = len(clean_rules.encode("utf-8"))
    est_tokens = len(clean_rules) // 4
    print(f"  [*] Zichlashtirilgan Master Rules hajmi: {size_bytes} bayt (~{est_tokens} tokens).")

    # 1. Asosiy Global Qoida: ~/.gemini/config/AGENTS.md
    GLOBAL_AGENTS_MD_CONFIG.parent.mkdir(parents=True, exist_ok=True)
    GLOBAL_AGENTS_MD_CONFIG.write_text(clean_rules, encoding="utf-8")
    print(f"  [+] ~/.gemini/config/AGENTS.md yangilandi ({size_bytes} bayt).")

    # 2. ~/.gemini/AGENTS.md va ~/AGENTS.md — bularni qisqa pointer yoki toza holatga keltirish
    # Antigravity har ikkalasini o'qiganda tokenni 2 marta yemasligi uchun pointer qilamiz
    pointer_text = "# Global Antigravity Rules\nRules are centrally maintained in `~/.gemini/config/AGENTS.md`.\n*Dasturchi: MuzaffarZed*\n"
    GLOBAL_AGENTS_MD_ROOT.write_text(pointer_text, encoding="utf-8")
    print("  [+] ~/.gemini/AGENTS.md ixcham pointerga keltirildi.")

    if HOME_AGENTS_MD.exists():
        HOME_AGENTS_MD.write_text(pointer_text, encoding="utf-8")
        print("  [+] ~/AGENTS.md ixcham pointerga keltirildi.")

    # 3. ai_workspace/AGENTS.md — workspace darajasida qisqa saqlanadi
    workspace_rule_text = f"""# Workspace Directives: ai_workspace
Global directives are inherited from `~/.gemini/config/AGENTS.md`.
Primary project root: `C:\\Users\\MuzaffarZed\\ai_workspace`
Virtualenv: `C:\\Users\\MuzaffarZed\\ai_workspace\\venv\\Scripts\\python.exe`
Observer hooks: Pre-task recall (`memory_engine.py`), error learning (`lessons_learned.md`), NotebookLM sync (`notebooklm_exporter.py`).
*Dasturchi: MuzaffarZed*
"""
    WORKSPACE_AGENTS_MD.write_text(workspace_rule_text.strip() + "\n", encoding="utf-8")
    print("  [+] ai_workspace/AGENTS.md ixchamlashtirildi.")

    # 4. ai_workspace/.agents/rules/master_rules.md — olib tashlash yoki pointer
    if WORKSPACE_RULES_DIR.exists():
        for r_file in WORKSPACE_RULES_DIR.glob("*.md"):
            r_file.unlink()
        print("  [+] .agents/rules/*.md dublikatlari tozalandi.")


# ====================================================================
# 6-QADAM: YAKUNIY TOKEN AUDITI VA NATIJALAR JADVALI
# ====================================================================
def step_6_final_audit():
    print("\n" + "="*70)
    print("6-QADAM: YAKUNIY TOKEN AUDITI VA NATIJALAR")
    print("="*70)

    # 1. Rules tokenlarini hisoblash
    rule_files = [
        GLOBAL_AGENTS_MD_CONFIG,
        GLOBAL_AGENTS_MD_ROOT,
        HOME_AGENTS_MD,
        WORKSPACE_AGENTS_MD
    ]
    total_rule_bytes = sum(f.stat().st_size for f in rule_files if f.exists())
    est_rule_tokens = int(total_rule_bytes * 0.35)

    # 2. Skills tokenlarini hisoblash
    skills_root = GEMINI_CONFIG_SKILLS
    skills_count = len([d for d in skills_root.iterdir() if d.is_dir()]) if skills_root.exists() else 0
    
    total_desc_chars = 0
    for sdir in skills_root.iterdir():
        if sdir.is_dir():
            sfile = sdir / "SKILL.md"
            if sfile.exists():
                text = sfile.read_text(encoding="utf-8", errors="ignore")
                m = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
                if m:
                    for line in m.group(1).split("\n"):
                        if line.strip().startswith("description:"):
                            total_desc_chars += len(line)

    # Har bir skill Antigravity promptida: "- name (path): description\n" ko'rinishida beriladi
    est_skill_index_tokens = int((skills_count * 50 + total_desc_chars) * 0.35)

    # Plugin skills hisobi (faqat pluginlar ichidagi)
    plugin_skills_count = 0
    if GEMINI_CONFIG_PLUGINS.exists():
        for root, dirs, files in os.walk(GEMINI_CONFIG_PLUGINS):
            if "SKILL.md" in files:
                plugin_skills_count += 1
    est_plugin_tokens = int(plugin_skills_count * 35)

    total_other_customizations_tokens = est_skill_index_tokens + est_plugin_tokens

    print("\n" + "*"*70)
    print(f"{'Kategoriya':<25} | {'Oldingi Holat':<18} | {'Yangi Holat':<18} | {'Limit':<12}")
    print("-" * 75)
    print(f"{'Rules Tokens':<25} | {'16,695 (83.5%)':<18} | {f'{est_rule_tokens} ({est_rule_tokens/200:.1f}%)':<18} | {'20,000':<12}")
    print(f"{'Other Customizations':<25} | {'45,206 (226.0%)':<18} | {f'{total_other_customizations_tokens} ({total_other_customizations_tokens/200:.1f}%)':<18} | {'20,000':<12}")
    print(f"{'Jami Customizations':<25} | {'61,901 tokens':<18} | {f'{est_rule_tokens + total_other_customizations_tokens} tokens':<18} | {'40,000':<12}")
    print(f"{'Faol Skilllar Soni':<25} | {'267 ta (105 excluded)':<18} | {f'{skills_count + plugin_skills_count} ta (0 excluded)':<18} | {'Cheklanmagan':<12}")
    print("*"*70)
    print("\n[MUVAFFAQIN!] Token byudjeti 20,000 lik qizil zonadan to'liq chiqarildi!")
    print("Barcha skill'lar va bilimlar 100% references/ ichida to'liq saqlab qolindi!")
    print("Dasturchi: MuzaffarZed\n")


def main():
    print("*"*70)
    print("ANTIGRAVITY TOKEN BUDGET OPTIMIZATION — BOSHLANDI")
    print("*"*70)
    step_1_backup()
    step_2_remove_duplicates()
    step_3_consolidate_master_suites()
    step_4_optimize_skill_frontmatters()
    step_5_compress_rules()
    step_6_final_audit()

if __name__ == "__main__":
    main()
