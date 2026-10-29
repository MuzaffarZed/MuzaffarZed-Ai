import ctypes
from ctypes import wintypes
import time

winmm = ctypes.windll.winmm

class JOYCAPSW(ctypes.Structure):
    _fields_ = [
        ('wMid', wintypes.WORD),
        ('wPid', wintypes.WORD),
        ('szPname', wintypes.WCHAR * 32),
        ('wXmin', wintypes.UINT),
        ('wXmax', wintypes.UINT),
        ('wYmin', wintypes.UINT),
        ('wYmax', wintypes.UINT),
        ('wZmin', wintypes.UINT),
        ('wZmax', wintypes.UINT),
        ('wNumButtons', wintypes.UINT),
        ('wPeriodMin', wintypes.UINT),
        ('wPeriodMax', wintypes.UINT),
        ('wRmin', wintypes.UINT),
        ('wRmax', wintypes.UINT),
        ('wUmin', wintypes.UINT),
        ('wUmax', wintypes.UINT),
        ('wVmin', wintypes.UINT),
        ('wVmax', wintypes.UINT),
        ('wCaps', wintypes.UINT),
        ('wMaxAxes', wintypes.UINT),
        ('wNumAxes', wintypes.UINT),
        ('wMaxButtons', wintypes.UINT),
        ('szRegKey', wintypes.WCHAR * 32),
        ('szOEMVxD', wintypes.WCHAR * 260)
    ]

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

num_devs = winmm.joyGetNumDevs()
print(f"joyGetNumDevs reported: {num_devs} devices supported")

for i in range(min(num_devs, 16)):
    caps = JOYCAPSW()
    res = winmm.joyGetDevCapsW(i, ctypes.byref(caps), ctypes.sizeof(caps))
    if res == 0:
        print(f"\n--- Joystick ID {i} ---")
        print(f"Name: {caps.szPname}")
        print(f"Mid: {caps.wMid}, Pid: {caps.wPid}")
        print(f"Buttons: {caps.wNumButtons}, Axes: {caps.wNumAxes}")
        
        info = JOYINFOEX()
        info.dwSize = ctypes.sizeof(info)
        info.dwFlags = 0xFF # JOY_RETURNALL
        res_pos = winmm.joyGetPosEx(i, ctypes.byref(info))
        if res_pos == 0:
            print(f"Current State -> X: {info.dwXpos}, Y: {info.dwYpos}, Z: {info.dwZpos}, R: {info.dwRpos}, Buttons: {bin(info.dwButtons)}, POV: {info.dwPOV}")
        else:
            print(f"joyGetPosEx error: {res_pos}")
