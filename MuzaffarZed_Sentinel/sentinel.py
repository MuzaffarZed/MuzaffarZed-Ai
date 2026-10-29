import os
import psutil
import ctypes
import shutil

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

def boost_ram():
    """
    Trims memory of all processes using Windows EmptyWorkingSet API.
    Cleans up user temporary files.
    """
    freed_mb = 0
    initial_ram = psutil.virtual_memory().used
    
    # 1. EmptyWorkingSet across accessible processes
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            handle = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, proc.info['pid'])
            if handle:
                ctypes.windll.psapi.EmptyWorkingSet(handle)
                ctypes.windll.kernel32.CloseHandle(handle)
        except Exception:
            pass
            
    final_ram = psutil.virtual_memory().used
    freed_mb = max(0, round((initial_ram - final_ram) / (1024 * 1024), 1))
    
    # 2. Clean temporary files in %TEMP%
    temp_dir = os.environ.get("TEMP")
    cleaned_files = 0
    if temp_dir and os.path.exists(temp_dir):
        for f in os.listdir(temp_dir):
            if f.endswith(('.tmp', '.log', '.bak')):
                fp = os.path.join(temp_dir, f)
                try:
                    if os.path.isfile(fp):
                        os.remove(fp)
                        cleaned_files += 1
                except Exception:
                    pass
                    
    return {
        "status": "success",
        "freed_ram_mb": freed_mb,
        "current_ram_percent": psutil.virtual_memory().percent,
        "cleaned_temp_files": cleaned_files
    }

def get_system_telemetry():
    vm = psutil.virtual_memory()
    disk = psutil.disk_usage("D:\\")
    active_games = []
    for proc in psutil.process_iter(['name', 'pid']):
        pname = (proc.info['name'] or '').lower()
        if pname in GAMES_PROCESS_NAMES:
            active_games.append(proc.info['name'])
            
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "ram_percent": vm.percent,
        "ram_used_gb": round(vm.used / (1024**3), 2),
        "ram_total_gb": round(vm.total / (1024**3), 2),
        "disk_free_gb": round(disk.free / (1024**3), 1),
        "active_games": active_games
    }

def boost_active_games():
    """
    Sets running games to High Priority class for 60 FPS performance.
    """
    boosted = []
    for proc in psutil.process_iter(['name', 'pid']):
        pname = (proc.info['name'] or '').lower()
        if pname in GAMES_PROCESS_NAMES:
            try:
                proc.nice(psutil.HIGH_PRIORITY_CLASS)
                boosted.append(proc.info['name'])
            except Exception:
                pass
    return boosted

if __name__ == "__main__":
    print("Testing Sentinel Telemetry & Auto-Boost...")
    tel = get_system_telemetry()
    print("Telemetry:", tel)
    res = boost_ram()
    print("RAM Boost Result:", res)
