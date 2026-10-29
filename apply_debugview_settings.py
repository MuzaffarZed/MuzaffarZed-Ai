import winreg
import struct
import subprocess
import time
import psutil

print("1. Oldingi Dbgview jarayonlarini to'xtatish...")
for p in psutil.process_iter(['pid', 'name']):
    if 'dbgview' in p.info['name'].lower():
        print(f"To'xtatildi: PID {p.info['pid']}")
        try:
            p.kill()
        except Exception as e:
            print(f"Xato: {e}")

time.sleep(1)

print("2. Mukammal sozlamalarni Registry ga yozish...")

# 552 baytlik Settings strukturasi
blob = bytearray(552)
struct.pack_into('<I', blob, 0x00, 0x193) # Magic / Version (403)
struct.pack_into('<i', blob, 0x04, 80)    # Window X
struct.pack_into('<i', blob, 0x08, 60)    # Window Y
struct.pack_into('<i', blob, 0x0c, 1550)  # Window Width (keng va qulay)
struct.pack_into('<i', blob, 0x10, 880)   # Window Height (keng)

# Ustunlar kengligi (Columns Width)
struct.pack_into('<I', blob, 0x14, 75)    # Col 0: # (Qator raqami - 75px, hech qachon '...' bo'lmaydi)
struct.pack_into('<I', blob, 0x18, 130)   # Col 1: Time (Vaqt millisekundlari bilan - 130px)
struct.pack_into('<I', blob, 0x1c, 80)    # Col 2: PID (Jarayon IDsi - 80px)
struct.pack_into('<I', blob, 0x20, 1200)  # Col 3: Debug Print (Log matni - 1200px)

# Tarix buferi (History Depth)
struct.pack_into('<I', blob, 0x24, 100000) # 100,000 qator saqlanadi

# Bayroqlar (Options Flags)
blob[0x28] = 1 # Auto Scroll (Avtomatik pastga surish)
blob[0x29] = 1 # Clock Time (Mahalliy real soat vaqti)
blob[0x2a] = 1 # Show Milliseconds (Millisekundlargacha aniqlik)
blob[0x2b] = 1 # Show Win32 PIDs (PID ko'rinishi)
blob[0x2c] = 1 # Force Carriage Returns (Satrlarni to'g'ri sindirish)
blob[0x2d] = 0 # Hide When Minimized

# Dasturchilar shrifti: Consolas (10.5 pt, ClearType)
struct.pack_into('<i', blob, 0x30, -14) # lfHeight
struct.pack_into('<i', blob, 0x40, 400) # lfWeight FW_NORMAL
blob[0x4a] = 5  # CLEARTYPE_QUALITY
blob[0x4b] = 49 # FIXED_PITCH | FF_MODERN
font_bytes = b'Consolas\x00'
blob[0x4c:0x4c+len(font_bytes)] = font_bytes

# Capture bayroqlari
struct.pack_into('<I', blob, 0x6c, 0x01010100)

# Ranglar palitrasi (BGR format):
# Slot 1: Qizil (Xatoliklar, Error, Crash, Fail)
struct.pack_into('<I', blob, 0x70, 0x00FFFFFF) # Matn: Oq
struct.pack_into('<I', blob, 0x84, 0x002020DC) # Fon: Qizil (Crimson Red)

# Slot 2: Sariq / Zarg‘aldoq (Ogohlantirishlar, Warn, Timeout)
struct.pack_into('<I', blob, 0x74, 0x00FFFFFF) # Matn: Oq
struct.pack_into('<I', blob, 0x88, 0x00008CE0) # Fon: Yorqin Amber / To'q sariq

# Slot 3: Zumrad Yashil (Muvaffaqiyat, Success, OK, Connected)
struct.pack_into('<I', blob, 0x78, 0x00000000) # Matn: Qora
struct.pack_into('<I', blob, 0x8c, 0x0032CD32) # Fon: Lime Green

# Slot 4: Moviy / Havorang (Hodisalar, Device, PnP, Display)
struct.pack_into('<I', blob, 0x7c, 0x00FFFFFF) # Matn: Oq
struct.pack_into('<I', blob, 0x90, 0x00D07010) # Fon: Moviy / Royal Blue

# Slot 5: To‘q Binafsha (Debug, Trace, Init)
struct.pack_into('<I', blob, 0x80, 0x00FFFFFF) # Matn: Oq
struct.pack_into('<I', blob, 0x94, 0x00800080) # Fon: Magenta / Purple

blob[0x98] = 1 # Highlight funksiyasi faol
struct.pack_into('<I', blob, 0x9c, 0)
struct.pack_into('<H', blob, 0xa0, 0x0100) # Win32 Capture
blob[0xa1] = 1 # Global Win32 Capture (barcha sessiyalar va xizmatlar)

# Qo'shimcha slotlar 6..10
for off in [0x1a8, 0x1ac, 0x1b0, 0x1b4, 0x1b8]:
    struct.pack_into('<I', blob, off, 0x00000000)
struct.pack_into('<I', blob, 0x1bc, 0x00E6D8AD)
struct.pack_into('<I', blob, 0x1c0, 0x0098FB98)
struct.pack_into('<I', blob, 0x1c4, 0x00E0FFFF)
struct.pack_into('<I', blob, 0x1c8, 0x00D8BFD8)
struct.pack_into('<I', blob, 0x1cc, 0x00E0EEEE)
blob[0x1d0] = 1

# Filtrlash sozlamalari
in_filters = b'*\x00\x00'
ex_filters = b'\x00'

hi_filters = (
    b'*error*;*fail*;*exception*;*crash*;*fatal*;*denied*\x00'
    b'*warn*;*warning*;*missing*;*timeout*\x00'
    b'*success*;*ok*;*loaded*;*ready*;*started*;*connected*\x00'
    b'*device*;*event*;*status*;*pnp*;*display*\x00'
    b'*debug*;*trace*;*init*\x00\x00'
)

slots = [
    b'*error*;*fail*;*exception*;*crash*;*fatal*;*denied*',
    b'*warn*;*warning*;*missing*;*timeout*',
    b'*success*;*ok*;*loaded*;*ready*;*started*;*connected*',
    b'*device*;*event*;*status*;*pnp*;*display*',
    b'*debug*;*trace*;*init*',
    b'',
    b'',
    b'',
    b'',
    b''
]
hi_cur_filters = b'\x00'.join(slots) + b'\x00\x00'

key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r'Software\Sysinternals\DbgView')
winreg.SetValueEx(key, 'EulaAccepted', 0, winreg.REG_DWORD, 1)
winreg.SetValueEx(key, 'Settings', 0, winreg.REG_BINARY, bytes(blob))
winreg.SetValueEx(key, 'InFilters', 0, winreg.REG_BINARY, in_filters)
winreg.SetValueEx(key, 'ExFilters', 0, winreg.REG_BINARY, ex_filters)
winreg.SetValueEx(key, 'HiFilters', 0, winreg.REG_BINARY, hi_filters)
winreg.SetValueEx(key, 'HiCurFilters', 0, winreg.REG_BINARY, hi_cur_filters)
winreg.CloseKey(key)

print("Registry muvaffaqiyatli yangilandi!")

print("3. DebugView ni yangi sozlamalar bilan ishga tushirish...")
dbgview_exe = r'C:\Users\Public\Downloads\DebugView\Dbgview.exe'
# Start-Process orqali fon loglash va global rejimda ishga tushirish
ps_script = f'Start-Process -FilePath "{dbgview_exe}" -ArgumentList "/t /g /l C:\\Users\\Public\\Downloads\\Debugview.log"'
subprocess.run(['powershell', '-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass', '-Command', ps_script])

time.sleep(2)
print("Bajarildi!")
