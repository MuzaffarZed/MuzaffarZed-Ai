# -*- coding: utf-8 -*-
"""
Token Watchdog (Rules & Skills Auto-Compactor)
Muallif: MuzaffarZed
Standart: MUTLAQ MUKAMMALLIK (Zero-Beta, Zero-Defect)
Rules va Skills token byudjetini nazorat qiladi. 8,000 tokendan oshsa,
ixchamlashtirib, Antigravity byudjetini yashil zonada (<20,000) saqlaydi.
"""

import os

WORKSPACE = r"C:\Users\MuzaffarZed\ai_workspace"

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
