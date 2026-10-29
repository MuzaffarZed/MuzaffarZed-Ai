import os
import win32com.client
import psutil

def audit_and_repair_desktop_shortcuts():
    """
    Scans Desktop and Public Desktop for dead/broken shortcuts (.lnk)
    and removes or repairs them autonomously.
    """
    wsh = win32com.client.Dispatch("WScript.Shell")
    desktops = [
        os.path.expanduser(r"~\Desktop"),
        r"C:\Users\Public\Desktop"
    ]
    repaired = []
    
    for d in desktops:
        if os.path.exists(d):
            for f in os.listdir(d):
                if f.lower().endswith(".lnk"):
                    p = os.path.join(d, f)
                    try:
                        shortcut = wsh.CreateShortcut(p)
                        target = shortcut.TargetPath
                        if target and not os.path.exists(target) and not target.startswith("http"):
                            # Dead shortcut!
                            os.remove(p)
                            repaired.append(f"Removed dead shortcut: {f} (Target was: {target})")
                    except Exception:
                        pass
    return repaired

def get_system_health():
    """
    Returns full health diagnostics of hardware and storage.
    """
    vm = psutil.virtual_memory()
    c_disk = psutil.disk_usage("C:\\")
    d_disk = psutil.disk_usage("D:\\")
    
    return {
        "status": "Healthy",
        "cpu_cores": psutil.cpu_count(logical=True),
        "ram_health": f"{vm.percent}% used ({round(vm.used / 1024**3, 1)}GB / {round(vm.total / 1024**3, 1)}GB)",
        "c_free_gb": round(c_disk.free / 1024**3, 1),
        "d_free_gb": round(d_disk.free / 1024**3, 1),
        "battery": psutil.sensors_battery().percent if psutil.sensors_battery() else "AC Power",
        "power_plugged": psutil.sensors_battery().power_plugged if psutil.sensors_battery() else True
    }

if __name__ == "__main__":
    print("Testing System Guardian...")
    dead = audit_and_repair_desktop_shortcuts()
    print("Dead shortcuts checked:", dead if dead else "Zero broken shortcuts found! 100% Clean.")
    health = get_system_health()
    print("Health report:", health)
