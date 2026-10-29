# -*- coding: utf-8 -*-
"""
Hardware Guard (RAM/CPU & Zombie Process Manager)
Muallif: MuzaffarZed
Standart: MUTLAQ MUKAMMALLIK (Zero-Beta, Zero-Defect)
"""

import os
import psutil

class HardwareGuard:
    def get_system_load(self):
        cpu = psutil.cpu_percent(interval=0.1)
        ram = psutil.virtual_memory().percent
        return {"cpu_percent": cpu, "ram_percent": ram}

    def cleanup_zombies(self):
        """Osilib qolgan headless chrome yoki ffmpeg jarayonlarini tozalash"""
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
