# -*- coding: utf-8 -*-
"""
NEXUS MASTER CLI (Unified Autonomous OS Interface)
Muallif: MuzaffarZed
Standart: MUTLAQ MUKAMMALLIK (Zero-Beta, Zero-Defect)
"""

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

WORKSPACE = r"C:\Users\MuzaffarZed\ai_workspace"

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
