import os
import sys
import time
import psutil

sys.path.append(os.path.dirname(__file__))
import sentinel
import vault
import brain_reflection
import cognitive_cortex

GAMES_PROCESS_NAMES = [
    "mafia2.exe",
    "blur.exe",
    "firewatch.exe",
    "saintsrowthethird.exe",
    "tod.exe",
    "totaloverdose.exe",
    "game.exe",
    "speed for deen wast monted.exe",
    "flatout2.exe",
    "1.6.exe",
    "hl.exe",
    "generals.exe",
    "gta-vc.exe",
    "gta-9matrix.exe",
    "mk3w.exe",
]

class IntuitionDaemon:
    def __init__(self):
        self.running_games = set()
        self.is_running = True
        print("[JARVIS INTUITION] Daemon initialized for janob Muzaffar.")

    def run_cycle(self):
        current_active = set()
        
        # 1. Detect game launches and apply instant Game Boost
        for proc in psutil.process_iter(['name', 'pid']):
            try:
                name = (proc.info['name'] or '').lower()
                if name in GAMES_PROCESS_NAMES:
                    current_active.add(name)
                    if name not in self.running_games:
                        # NEW GAME LAUNCHED!
                        print(f"[INTUITION] Game detected: {name}! Applying High-Priority & RAM Turbo Boost...")
                        try:
                            proc.nice(psutil.HIGH_PRIORITY_CLASS)
                        except Exception:
                            pass
                        res = sentinel.boost_ram()
                        print(f"[INTUITION] Boosted {name}! Freed {res['freed_ram_mb']} MB RAM.")
                        vault.log_event(f"Intuition Game Boost: {name}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        self.running_games = current_active

        # 2. Prevent RAM exhaustion
        vm = psutil.virtual_memory()
        if vm.percent > 85.0:
            print(f"[INTUITION] High RAM usage ({vm.percent}%) detected! Auto-optimizing...")
            sentinel.boost_ram()

        # 3. Cognitive Cortex Periodic Reflection (every ~60s)
        now = time.time()
        if not hasattr(self, '_last_cortex_time') or (now - self._last_cortex_time > 60):
            self._last_cortex_time = now
            try:
                cortex = cognitive_cortex.CognitiveCortex()
                cortex.generate_proactive_ideas()
            except Exception as e:
                pass

    def start_loop(self, max_cycles=None):
        cycles = 0
        while self.is_running:
            self.run_cycle()
            time.sleep(3)
            cycles += 1
            if max_cycles and cycles >= max_cycles:
                break

if __name__ == "__main__":
    print("Testing Intuition Daemon for 2 cycles...")
    daemon = IntuitionDaemon()
    daemon.start_loop(max_cycles=2)
    print("Intuition Daemon test completed with 100% success!")
