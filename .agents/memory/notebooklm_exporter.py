# -*- coding: utf-8 -*-
"""
NotebookLM Exporter (Kognitiv Xotirani Google NotebookLM Kitobiga Yig'uvchi)
Muallif: MuzaffarZed
Standart: MUTLAQ MUKAMMALLIK (Zero-Beta, Zero-Defect)
"""

import os
import sys
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

WORKSPACE = r"C:\Users\MuzaffarZed\ai_workspace"
MEMORY_DIR = os.path.join(WORKSPACE, ".agents", "memory")
OUTPUT_MD = os.path.join(WORKSPACE, "notebooklm_sync", "Muzaffar_Second_Brain_Source.md")

def export_second_brain():
    os.makedirs(os.path.dirname(OUTPUT_MD), exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    sections = [
        f"# MUZAFFAR SECOND BRAIN - KOGNITIV BILIMLAR KITOBI\n\nSinxronizatsiya vaqti: {now}\nMuallif: MuzaffarZed\n"
    ]
    
    # 1. Cognitive profile
    p_path = os.path.join(MEMORY_DIR, "cognitive_profile.md")
    if os.path.exists(p_path):
        with open(p_path, "r", encoding="utf-8") as f:
            sections.append(f"\n\n---\n\n## 1. KOGNITIV PROFIL\n\n{f.read()}")

    # 2. Lessons learned
    l_path = os.path.join(MEMORY_DIR, "lessons_learned.md")
    if os.path.exists(l_path):
        with open(l_path, "r", encoding="utf-8") as f:
            sections.append(f"\n\n---\n\n## 2. SABOQLAR VA XATOLAR AUDITI\n\n{f.read()}")

    # 3. Knowledge vault
    k_path = os.path.join(MEMORY_DIR, "knowledge_vault.md")
    if os.path.exists(k_path):
        with open(k_path, "r", encoding="utf-8") as f:
            sections.append(f"\n\n---\n\n## 3. ARXITEKTURA BILIMLAR XAZINASI\n\n{f.read()}")

    # 4. Global AGENTS rules summary
    a_path = os.path.join(WORKSPACE, "AGENTS.md")
    if os.path.exists(a_path):
        with open(a_path, "r", encoding="utf-8") as f:
            sections.append(f"\n\n---\n\n## 4. AGENTS VA OLIY QOIDALAR\n\n{f.read()}")

    final_content = "".join(sections) + "\n\n*Dasturchi: MuzaffarZed*\n"
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(final_content)
    print(f"[NotebookLM Exporter] Kitob yaratildi: {OUTPUT_MD} ({len(final_content)} belgi)")
    return OUTPUT_MD

if __name__ == "__main__":
    export_second_brain()
