@echo off
title Windows Bilan Birga Ishga Tushirishni O'rnatish
echo =======================================================
echo   AVTOMATIK ISHGA TUSHIRISHNI SOZLASH
echo =======================================================

set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT_PATH=%STARTUP_FOLDER%\BrightnessSync.lnk"
set "TARGET_SCRIPT=C:\Users\MuzaffarZed\ai_workspace\brightness_sync\Orqa_Fonda_Ishga_Tushirish.vbs"

powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%SHORTCUT_PATH%'); $s.TargetPath = '%TARGET_SCRIPT%'; $s.WorkingDirectory = 'C:\Users\MuzaffarZed\ai_workspace\brightness_sync'; $s.Save()"

if exist "%SHORTCUT_PATH%" (
    echo [OK] Windows Startup papkasiga yorliq muvaffaqiyatli qoshildi!
    echo Endi kompyuter yoqilganda xizmat orqa fonda avtomatik ishga tushadi.
) else (
    echo [!] Yorliq yaratishda xatolik yuz berdi.
)

echo =======================================================
pause
