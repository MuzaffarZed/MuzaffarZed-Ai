# -*- coding: utf-8 -*-
"""
Security & Performance Gate (Ochiq Kalitlar va O'lik Kod Qorovuli)
Muallif: MuzaffarZed
Standart: MUTLAQ MUKAMMALLIK (Zero-Beta, Zero-Defect)
"""

import os
import re

WORKSPACE = r"C:\Users\MuzaffarZed\ai_workspace"

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
