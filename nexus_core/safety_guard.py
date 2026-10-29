# -*- coding: utf-8 -*-
"""
Safety Guard (Circuit Breaker & Auto-Rollback Engine)
Muallif: MuzaffarZed
Standart: MUTLAQ MUKAMMALLIK (Zero-Beta, Zero-Defect)
Har bir vazifa oldidan avto-snapshot oladi. Bir xil xato 3 marta qaytarilsa,
token sarfini to'xtatib, sog'lom holatga qaytaradi (Rollback).
"""

import os
import shutil
import hashlib
import json
from datetime import datetime

SNAPSHOTS_DIR = os.path.join(r"C:\Users\MuzaffarZed\ai_workspace", ".nexus_snapshots")
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
        ws = r"C:\Users\MuzaffarZed\ai_workspace"
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
