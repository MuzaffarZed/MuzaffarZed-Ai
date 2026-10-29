@echo off
chcp 65001 >nul
title CALL OF DUTY: MODERN WARFARE 3D // SPECIAL OPS
color 0a

echo ================================================================
echo    CALL OF DUTY: MODERN WARFARE 3D // SPECIAL OPS
echo    Taktik 3D FPS Harbiy Simulyator
echo    Bosh Muhandis: Janob Muzaffar
echo ================================================================
echo.

cd /d "%~dp0"

echo [1/2] O'yin resurslari va 3D muhit tekshirilmoqda...
if not exist "cod_modern_war\index.html" (
    echo [XATO] cod_modern_war\index.html fayli topilmadi!
    pause
    exit /b 1
)

echo [2/2] Call of Duty 3D brauzerda ishga tushirilmoqda...
echo.
echo Boshqaruv eslatmasi:
echo  * Sichqonchaning chap tugmasi: O't ochish
echo  * Sichqonchaning o'ng tugmasi: ADS (Nishonga olish)
echo  * W, A, S, D: Harakatlanish
echo  * Shift: Sprint (Tez yugurish)
echo  * Space: Sakrash
echo  * R: Qurolni qayta o'qlash
echo  * 1 / 2: M4A1 / AWP qurollari
echo.

start "" "%~dp0cod_modern_war\index.html"

echo O'yin muvaffaqiyatli ishga tushirildi!
echo Ushbu oynani yopishingiz mumkin.
timeout /t 5 >nul
exit /b 0
