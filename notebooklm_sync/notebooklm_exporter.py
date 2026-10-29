#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
notebooklm_exporter.py — NotebookLM Master Source Exporter
.agents/memory/ dagi barcha fikrlar, xatolardan olingan saboqlar,
Graphify kodbaza hisobotlari va loyiha tarixini Google NotebookLM uchun
eng ideal, chuqur strukturalangan "Muzaffar_Second_Brain_Source.md" fayliga
avtomatik birlashtiradi.

Dasturchi: MuzaffarZed
"""

import sys
import os
import shutil
import sqlite3
from pathlib import Path
from datetime import datetime

# Windows UTF-8 console output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

WORKSPACE_ROOT = Path(r"C:\Users\MuzaffarZed\ai_workspace")
MEMORY_DIR = WORKSPACE_ROOT / ".agents" / "memory"
SYNC_DIR = WORKSPACE_ROOT / "notebooklm_sync"
OUTPUT_SYNC_FILE = SYNC_DIR / "Muzaffar_Second_Brain_Source.md"
OUTPUT_WORKSPACE_FILE = WORKSPACE_ROOT / "Muzaffar_Second_Brain_Source.md"

PROFILE_MD = MEMORY_DIR / "cognitive_profile.md"
LESSONS_MD = MEMORY_DIR / "lessons_learned.md"
KNOWLEDGE_MD = MEMORY_DIR / "knowledge_vault.md"
DB_PATH = MEMORY_DIR / "memory.db"
AGENTS_MD = WORKSPACE_ROOT / "AGENTS.md"


def read_file_safely(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return ""


def get_db_stats() -> dict:
    if not DB_PATH.exists():
        return {"total": 0}
    try:
        con = sqlite3.connect(str(DB_PATH))
        cur = con.cursor()
        cur.execute("SELECT category, COUNT(*) as cnt FROM memories GROUP BY category")
        stats = {row[0]: row[1] for row in cur.fetchall()}
        cur.execute("SELECT COUNT(*) FROM memories")
        stats["total"] = cur.fetchone()[0]
        con.close()
        return stats
    except Exception:
        return {"total": 0}


def get_recent_memories(limit: int = 15) -> list:
    if not DB_PATH.exists():
        return []
    try:
        con = sqlite3.connect(str(DB_PATH))
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT category, title, content, created_at FROM memories ORDER BY id DESC LIMIT ?", (limit,))
        rows = [dict(r) for r in cur.fetchall()]
        con.close()
        return rows
    except Exception:
        return []


def generate_master_source() -> str:
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    profile_content = read_file_safely(PROFILE_MD)
    lessons_content = read_file_safely(LESSONS_MD)
    knowledge_content = read_file_safely(KNOWLEDGE_MD)
    agents_content = read_file_safely(AGENTS_MD)
    stats = get_db_stats()
    recent = get_recent_memories()

    doc = []
    # Title & Metadata
    doc.append("# Muzaffar Second Brain: Master Knowledge & Cognitive Architecture Source")
    doc.append(f"> **Hujjat turi:** Google NotebookLM Master Source (Deep Memory & Cognitive Context)")
    doc.append(f"> **Muallif va Egasi:** janob Muzaffar (MuzaffarZed)")
    doc.append(f"> **Sinxronizatsiya vaqti:** {now_str}")
    doc.append(f"> **Arxitektura:** Self-Evolving Cognitive Memory (SQLite FTS5 + Observer Hooks)")
    doc.append(f"> **Faol Xotiralar soni:** {stats.get('total', 0)} ta indekslangan yozuv")
    doc.append("\n---\n")

    # Table of Contents
    doc.append("## Mundarija (Table of Contents)")
    doc.append("1. [Ikkinchi Miya va Kognitiv Xotira Arxitekturasi](#1-ikkinchi-miya-va-kognitiv-xotira-arxitekturasi)")
    doc.append("2. [Janob Muzaffarning Kognitiv Profili va Did Standartlari](#2-janob-muzaffarning-kognitiv-profili-va-did-standartlari)")
    doc.append("3. [Xatolar va Olingan Saboqlar Bazasi (Root Cause Database)](#3-xatolar-va-olingan-saboqlar-bazasi-root-cause-database)")
    doc.append("4. [Bilimlar Xazinasi va Muhandislik Arxitekturasi](#4-bilimlar-xazinasi-va-muhandislik-arxitekturasi)")
    doc.append("5. [Amaldagi Ishchi Qoidalar (AGENTS.md Directives)](#5-amaldagi-ishchi-qoidalar-agentsmd-directives)")
    doc.append("6. [Texnologik Stack va O'rnatilgan Dvijoklar](#6-texnologik-stack-va-ornatilgan-dvijoklar)")
    doc.append("7. [Xotira Dvijogi Statistikasi va Oxirgi Xotiralar](#7-xotira-dvijogi-statistikasi-va-oxirgi-xotiralar)")
    doc.append("\n---\n")

    # Section 1: Overview
    doc.append("## 1. Ikkinchi Miya va Kognitiv Xotira Arxitekturasi")
    doc.append("""
Ushbu tizim janob Muzaffarning `C:\\Users\\MuzaffarZed\\ai_workspace` muhitida AI agentlarining xotirasini uzluksiz rivojlantirib borish uchun qurilgan.
U uchta asosiy halqa (Observer Hooks) asosida ishlaydi:
- **Pre-Task Hook:** Yangi vazifa boshlanganda `memory_engine.py context` orqali tegishli profil, oldingi xatolar va bilimlarni o'qiydi.
- **Error-Learning Hook:** Kod yoki terminalda xato yuz berganda uning ildiz sababi (Root Cause) va oltin qoidasi darhol `lessons_learned.md` hamda SQLite FTS5 bazasiga yoziladi.
- **Post-Task Reflection:** Har bir vazifa yakunlangach, yangi bilimlar `knowledge_vault.md` ga kiritiladi va ushbu `Muzaffar_Second_Brain_Source.md` NotebookLM manbasi avtomatik yangilanadi.
""")
    doc.append("\n---\n")

    # Section 2: Cognitive Profile
    doc.append("## 2. Janob Muzaffarning Kognitiv Profili va Did Standartlari")
    if profile_content:
        doc.append(profile_content)
    else:
        doc.append("*Profil fayli hali shakllantirilmoqda.*")
    doc.append("\n---\n")

    # Section 3: Lessons Learned
    doc.append("## 3. Xatolar va Olingan Saboqlar Bazasi (Root Cause Database)")
    if lessons_content:
        doc.append(lessons_content)
    else:
        doc.append("*Saboqlar fayli hali bo'sh.*")
    doc.append("\n---\n")

    # Section 4: Knowledge Vault
    doc.append("## 4. Bilimlar Xazinasi va Muhandislik Arxitekturasi")
    if knowledge_content:
        doc.append(knowledge_content)
    else:
        doc.append("*Bilimlar xazinasi shakllantirilmoqda.*")
    doc.append("\n---\n")

    # Section 5: AGENTS.md Rules
    doc.append("## 5. Amaldagi Ishchi Qoidalar (AGENTS.md Directives)")
    if agents_content:
        doc.append(agents_content)
    else:
        doc.append("*AGENTS.md mavjud emas.*")
    doc.append("\n---\n")

    # Section 6: Tech Stack
    doc.append("## 6. Texnologik Stack va O'rnatilgan Dvijoklar")
    doc.append("""
- **Asosiy Til va Virtual Muhit:** Python 3.12 (`C:\\Users\\MuzaffarZed\\ai_workspace\\venv`)
- **Ma'lumotlar Bazasi:** SQLite3 FTS5 Full-Text Search Engine
- **Audio-Video Montaj:** FFmpeg (Static build), faster-whisper, edge-tts, MoviePy
- **Kinematik 3D & Simulyatsiya:** Three.js, React Three Fiber (`@remotion/three`, `@react-three/drei`), Manim Community, Remotion
- **UI/UX Stack:** `taste-skill`, `pbakaus/impeccable`, `emilkowalski/skills`, `hyperframes`, `remotion-video`
- **Kodbaza Grafi:** Graphify (Persistent AST-based Knowledge Graph)
- **Avtonom Jamoa:** Claude Code Agent Teams (Team Lead, Frontend, Backend, Tester, Reviewer, Researcher)
- **Desktop Avtomatizatsiyasi:** `bridge/windows_controller.py`, Win32 API (`ctypes.windll.user32`), Telegram Desktop Automation
""")
    doc.append("\n---\n")

    # Section 7: Stats and Recent Memories
    doc.append("## 7. Xotira Dvijogi Statistikasi va Oxirgi Xotiralar")
    doc.append(f"**Jami Indekslangan Yozuvlar:** {stats.get('total', 0)}")
    for cat, count in stats.items():
        if cat != "total":
            doc.append(f"- **{cat.capitalize()}:** {count} ta")

    if recent:
        doc.append("\n### Oxirgi Xotira Yozuvlari:")
        for r in recent:
            doc.append(f"- **[{r['category'].upper()}] {r['title']}** ({r['created_at']})")
            doc.append(f"  > {r['content'][:180].replace(chr(10), ' ')}...")

    doc.append("\n---\n")
    doc.append("### Yakuniy Mualliflik Imzosi")
    doc.append("*Ushbu master manba Google NotebookLM uchun tayyorlangan bo'lib, Audio Overview (podkast generatsiya), savol-javob va chuqur tahlil uchun 100% optimallashtirilgan.*")
    doc.append("\n*Dasturchi: MuzaffarZed*")

    return "\n".join(doc)


def main():
    SYNC_DIR.mkdir(parents=True, exist_ok=True)
    master_content = generate_master_source()

    # 1. Sync papkasiga yozish
    OUTPUT_SYNC_FILE.write_text(master_content, encoding="utf-8")
    print(f"[OK] NotebookLM Master Source yaratildi: {OUTPUT_SYNC_FILE}")

    # 2. Workspace asosiy papkasiga nusxalash
    OUTPUT_WORKSPACE_FILE.write_text(master_content, encoding="utf-8")
    print(f"[OK] Workspace asosiy manziliga nusxalandi: {OUTPUT_WORKSPACE_FILE}")

    size_kb = len(master_content.encode("utf-8")) / 1024
    lines = len(master_content.splitlines())
    print(f"Hajmi: {size_kb:.2f} KB | Qatorlar soni: {lines}")


if __name__ == "__main__":
    main()
