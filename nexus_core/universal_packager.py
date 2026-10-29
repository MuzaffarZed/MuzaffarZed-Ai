# -*- coding: utf-8 -*-
"""
Universal Packager (Tayyor Mahsulot Zavodi)
Muallif: MuzaffarZed
Standart: MUTLAQ MUKAMMALLIK (Zero-Beta, Zero-Defect)
Python dasturlarni .exe faylga aylantiradi va blueprints saqlaydi.
"""

import os
import sys
import subprocess

BLUEPRINTS_DIR = os.path.join(r"C:\Users\MuzaffarZed\ai_workspace", "blueprints")
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
            f.write(f"# Blueprint: {bp_type}\n# Dasturchi: MuzaffarZed\n\ndef main():\n    print('Nexus Blueprint {bp_type} faol!')\n\nif __name__ == '__main__':\n    main()\n")
        return t_path

if __name__ == "__main__":
    up = UniversalPackager()
    bp = up.init_blueprint("cli_pro", "demo_cli")
    print(f"[UniversalPackager] Blueprint yaratildi: {bp}")
    print("*Dasturchi: MuzaffarZed*")
