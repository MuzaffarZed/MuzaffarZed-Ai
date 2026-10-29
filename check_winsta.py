import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32
hwinsta = user32.GetProcessWindowStation()
buff = ctypes.create_unicode_buffer(256)
user32.GetUserObjectInformationW(hwinsta, 2, buff, 256, None) # 2 = UOI_NAME
print("Current Process WindowStation:", buff.value)

hdesk = user32.GetThreadDesktop(ctypes.windll.kernel32.GetCurrentThreadId())
buff2 = ctypes.create_unicode_buffer(256)
user32.GetUserObjectInformationW(hdesk, 2, buff2, 256, None)
print("Current Thread Desktop:", buff2.value)
