@echo off
title MuzaffarZed Antigravity Restore Engine
color 0A
echo ======================================================================
echo    MUZAFFARZED ANTIGRAVITY AVTOMATIK TIKLASH (1-CLICK RESTORE)
echo ======================================================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [DIQQAT] Python topilmadi. Iltimos, avval Python o'rnating.
    pause
    exit /b 1
)

python "%~dp0bootstrap_new_pc.py"

echo.
echo ======================================================================
echo Tayyor! Istalgan tugmani bosing...
pause >nul
