import subprocess
import shutil
import re
from typing import Dict, List, Optional
from dataclasses import dataclass

DEFAULT_ADB = r"C:\Users\MuzaffarZed\AppData\Local\Android\Sdk\platform-tools\adb.exe"

@dataclass
class AndroidDevice:
    serial: str
    model: str
    device_name: str
    role: str  # 'sender' (Phone) or 'receiver' (Tablet)
    android_version: str
    free_storage: str
    battery_level: int
    is_ready: bool

class DeviceDetector:
    def __init__(self, adb_path: Optional[str] = None):
        self.adb = adb_path or (DEFAULT_ADB if shutil.which(DEFAULT_ADB) else "adb")

    def _run_adb(self, *args, serial: Optional[str] = None) -> str:
        cmd = [self.adb]
        if serial:
            cmd.extend(["-s", serial])
        cmd.extend(args)
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=15)
            return res.stdout.strip()
        except Exception as e:
            return ""

    def list_connected_serials(self) -> List[str]:
        output = self._run_adb("devices")
        serials = []
        for line in output.splitlines():
            line = line.strip()
            if not line or line.startswith("*") or line.startswith("List of devices"):
                continue
            parts = line.split()
            if len(parts) >= 2 and parts[1] == "device":
                serials.append(parts[0])
        return serials

    def inspect_device(self, serial: str) -> AndroidDevice:
        model = self._run_adb("shell", "getprop", "ro.product.model", serial=serial) or "Unknown"
        version = self._run_adb("shell", "getprop", "ro.build.version.release", serial=serial) or "?"
        
        # Free storage check on /sdcard
        df_out = self._run_adb("shell", "df", "-h", "/sdcard", serial=serial)
        free_storage = "Noma'lum"
        for line in df_out.splitlines():
            if "/storage" in line or "/dev/fuse" in line or "/data" in line:
                cols = line.split()
                if len(cols) >= 4:
                    free_storage = cols[3]
                    break

        # Battery check
        batt_out = self._run_adb("shell", "dumpsys", "battery", serial=serial)
        batt_level = 100
        for line in batt_out.splitlines():
            if "level:" in line:
                match = re.search(r"\d+", line)
                if match:
                    batt_level = int(match.group())
                break

        # Determine role: S908 = S22 Ultra (Sender/Camera), T295 = Tab A (Receiver/Tablet)
        model_upper = model.upper()
        if "S908" in model_upper or "S22" in model_upper or "ULTRA" in model_upper:
            role = "sender"
            dev_name = "Samsung Galaxy S22 Ultra (Kamera)"
        elif "T295" in model_upper or "TAB" in model_upper:
            role = "receiver"
            dev_name = "Samsung Galaxy Tab A (Planshet)"
        else:
            role = "unknown"
            dev_name = f"Android Qurilma ({model})"

        return AndroidDevice(
            serial=serial,
            model=model,
            device_name=dev_name,
            role=role,
            android_version=version,
            free_storage=free_storage,
            battery_level=batt_level,
            is_ready=True
        )

    def detect_pair(self) -> Dict[str, Optional[AndroidDevice]]:
        serials = self.list_connected_serials()
        devices = [self.inspect_device(s) for s in serials]

        sender = next((d for d in devices if d.role == "sender"), None)
        receiver = next((d for d in devices if d.role == "receiver"), None)

        # Fallback if names are slightly different but 2 devices connected
        if not sender and len(devices) >= 2:
            sender = devices[0]
            sender.role = "sender"
        if not receiver and len(devices) >= 2:
            receiver = devices[1]
            receiver.role = "receiver"

        return {
            "sender": sender,
            "receiver": receiver,
            "all": devices
        }
