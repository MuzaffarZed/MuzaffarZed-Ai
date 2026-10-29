#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bootstrap_memory.py — Kognitiv Xotirani Dastlabki To'ldirish (Bootstrap)
Ponytail, Graphify, 25 ta Agent Skills, Agent Teams, Pro-Cinema va
Muzaffarning "Oliy Mukammallik va 100% Avtonomlik" falsafasini
xotira bazasiga va NotebookLM Master Source'ga kiritadi.

Dasturchi: MuzaffarZed
"""

import sys
import os
from pathlib import Path

# Add current dir to sys.path
current_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(current_dir))

from memory_engine import MemoryEngine

def bootstrap():
    engine = MemoryEngine()
    print("=== 1. Markdown fayllardan xotiralarni sinxronlash ===")
    counts = engine.sync_from_markdown()
    print(f"Markdown sinxronlash natijasi: {counts}")

    print("\n=== 2. Dastlabki Oltin Xotiralarni (Golden Memories) kiritish ===")
    bootstrap_entries = [
        {
            "category": "profile",
            "title": "Janob Muzaffarning Asosiy Talabi: Mutlaq Mukammallik (Zero-Beta)",
            "content": "Janob Muzaffar 'oddiy narsa emas, eng mukammal va 100% avtonom tizim bo'lsin' tamoyili bilan ishlaydi. Hech qachon chala namuna, beta versiya yoki 'aytilganini qildim-ku' degan yuzaki natija qabul qilinmaydi. Har bir ish o'zini o'zi to'liq tekshirib (closed-loop verification), zero-defect holatida topshiriladi.",
            "tags": "muzaffar,mindset,zero_defect,autonomous,philosophy"
        },
        {
            "category": "profile",
            "title": "Aytilmagan Lekin Bo'lishi Shart (Proactive Expansion)",
            "content": "Foydalanuvchi vazifa berganda har bir detalni bittalab aytishini kutmaslik; loyiha o'z sohasining eng professional cho'qqisida nimalarga ega bo'lishi kerak bo'lsa (masalan audio pleyerda ekvayzer, videoda SFX va ducking, kodda test va xavfsizlik), barchasini proaktiv ravishda o'z tashabbusi bilan qo'shish.",
            "tags": "proactivity,smart_defaults,excellence"
        },
        {
            "category": "knowledge",
            "title": "Ponytail Senior Lazy Dev Framework",
            "content": "Eng yaxshi kod — bu yozilmagan kod. Butun muammoni minimal miqdordagi yangi kod bilan hal qilish. Platforma, standart kutubxona va o'rnatilgan paketlardan maksimal foydalanish. Keraksiz wrapper, boilerplate, type conversion va 'kelajak uchun' degan ortiqcha kodlardan mutlaq voz kechish.",
            "tags": "ponytail,lazy_dev,clean_code,minimal_diff"
        },
        {
            "category": "knowledge",
            "title": "Graphify Knowledge Graph & Wiki Architecture",
            "content": "AST (Abstract Syntax Tree) asosida butun kodbazani semantik bilimlar grafi va wiki hujjatlariga aylantiruvchi tizim. Xom fayllarni o'qib kontekstni to'ldirmasdan, graphify query orqali mantiqiy bog'liqliklar va funksiyalar chaqiruvlarini bir lahzada aniqlash imkonini beradi.",
            "tags": "graphify,knowledge_graph,ast,architecture"
        },
        {
            "category": "knowledge",
            "title": "Addy Osmani 25+ Professional Agent Skills",
            "content": "Muhandislikning 6 ta ustuni: API va interfeys dizayni, test-driven development, debugging va xatolarni tiklash, kodni soddalashtirish, optimallash, xavfsizlik, CI/CD va arxitektura hujjatlari. Har bir qadamda tegishli skill avtonom chaqiriladi.",
            "tags": "agent_skills,engineering,best_practices,quality"
        },
        {
            "category": "knowledge",
            "title": "Autonomous Agent Teams (6-Specialist Hierarchy)",
            "content": "Foydalanuvchi /team buyrug'ini berganda Team Lead boshchiligida ishga tushuvchi tuzilma: Team Lead (Kanban doska), Frontend (UI/UX), Backend (API & baza), Tester (avtomatik sinov), Reviewer (sifat va xavfsizlik) va Researcher (texnologik tahlil).",
            "tags": "agent_teams,multi_agent,collaboration,kanban"
        },
        {
            "category": "knowledge",
            "title": "Pro-Cinema 3D / Manim / SFX Video Engine",
            "content": "Oddiy 2D slaydlar mutlaq taqiqlanadi! Remotion + Three.js (@remotion/three) orqali 3D fazoviy sahnalar, virtual kamera harakati, Manim simulyatsiyalari, SFX (whoosh, riser, impact), suxandon ovoziga mos Smart Audio Ducking, Multi-Voice aktyorlik ovozi va Inter Black dinamik subtitrlari.",
            "tags": "pro_cinema,video_engine,threejs,manim,sfx,audio_ducking"
        },
        {
            "category": "knowledge",
            "title": "Self-Evolving Cognitive Memory (Second Brain) & NotebookLM Bridge",
            "content": "Lokal SQLite FTS5 asosidagi xotira dvijogi. Pre-task recall (vazifa oldidan kontekstni olish), Error-learning hook (xatolarni avtomatik o'rganish) va Post-task reflection (bilimlarni NotebookLM Master Source'ga sinxronlash) orqali agent doimiy ravishda o'zini o'zi rivojlantirib boradi.",
            "tags": "second_brain,cognitive_memory,fts5,notebooklm,self_evolving"
        }
    ]

    for entry in bootstrap_entries:
        mid = engine.add_memory(
            category=entry["category"],
            title=entry["title"],
            content=entry["content"],
            tags=entry["tags"],
            source_file="bootstrap_memory.py"
        )
        print(f"  [+] Saqlandi #{mid}: {entry['title']}")

    print("\n=== 3. Xotira Statistikasi ===")
    stats = engine.get_stats()
    for cat, cnt in stats.items():
        print(f"  - {cat}: {cnt}")

    print("\n=== 4. Google NotebookLM Master Source faylini yangilash ===")
    exporter_path = current_dir.parent.parent / "notebooklm_sync" / "notebooklm_exporter.py"
    if exporter_path.exists():
        import subprocess
        result = subprocess.run([sys.executable, str(exporter_path)], capture_output=True, text=True, encoding="utf-8")
        print(result.stdout)
        if result.stderr:
            print("Stderr:", result.stderr)
    print("\n=== Bootstrap Muvaffaqiyatli Yakunlandi! ===")

if __name__ == "__main__":
    bootstrap()
