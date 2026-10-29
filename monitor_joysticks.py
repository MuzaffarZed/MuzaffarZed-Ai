import ctypes
from ctypes import wintypes
import time

winmm = ctypes.windll.winmm

class JOYINFOEX(ctypes.Structure):
    _fields_ = [
        ('dwSize', wintypes.DWORD),
        ('dwFlags', wintypes.DWORD),
        ('dwXpos', wintypes.DWORD),
        ('dwYpos', wintypes.DWORD),
        ('dwZpos', wintypes.DWORD),
        ('dwRpos', wintypes.DWORD),
        ('dwUpos', wintypes.DWORD),
        ('dwVpos', wintypes.DWORD),
        ('dwButtons', wintypes.DWORD),
        ('dwButtonNumber', wintypes.DWORD),
        ('dwPOV', wintypes.DWORD),
        ('dwReserved1', wintypes.DWORD),
        ('dwReserved2', wintypes.DWORD)
    ]

def monitor():
    print("Monitoring Joystick 0 and Joystick 1 for 3 seconds...")
    info0 = JOYINFOEX()
    info0.dwSize = ctypes.sizeof(info0)
    info0.dwFlags = 0xFF

    info1 = JOYINFOEX()
    info1.dwSize = ctypes.sizeof(info1)
    info1.dwFlags = 0xFF

    start = time.time()
    changes = []
    
    last_b0 = None
    last_b1 = None

    while time.time() - start < 3.0:
        res0 = winmm.joyGetPosEx(0, ctypes.byref(info0))
        res1 = winmm.joyGetPosEx(1, ctypes.byref(info1))
        
        if res0 == 0 and info0.dwButtons != last_b0:
            changes.append(f"Joy 0 Button change: {bin(info0.dwButtons)}")
            last_b0 = info0.dwButtons
        if res1 == 0 and info1.dwButtons != last_b1:
            changes.append(f"Joy 1 Button change: {bin(info1.dwButtons)}")
            last_b1 = info1.dwButtons
        time.sleep(0.05)

    print(f"Monitoring finished. Changes detected: {len(changes)}")
    for c in changes:
        print(c)

if __name__ == '__main__':
    monitor()
