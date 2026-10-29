@echo off
chcp 65001 >nul
title JARVIS - Peak-Level Multimodal Autonomous Assistant (v3.0)
color 0b

echo ================================================================
echo    JARVIS -- PEAK-LEVEL AUTONOMOUS MULTIMODAL AGENT (v3.0)
echo    ReAct Loop -- 3-Tier OS Control -- Hybrid Vision -- Barge-In
echo    Bosh Muhandis: Janob Muzaffar
echo ================================================================
echo.

cd /d "%~dp0"

set "PY_EXE="
if exist "venv\Scripts\python.exe" (
    set "PY_EXE=venv\Scripts\python.exe"
) else if exist "C:\Users\MuzaffarZed\ai_workspace\venv\Scripts\python.exe" (
    set "PY_EXE=C:\Users\MuzaffarZed\ai_workspace\venv\Scripts\python.exe"
) else (
    set "PY_EXE=python"
)

if not "%1"=="" (
    "%PY_EXE%" main.py %*
    goto end
)

:menu
echo Rejimni tanlang:
echo  [1] Matnli ReAct rejimi (Interaktiv Peak-Level konsol boshqaruvi)
echo  [2] Ovozli rejim (Barge-in qo'llab-quvvatlanuvchi mikrofon)
echo  [3] Murakkab topshiriq sinovi (ReAct avtonom tsikli)
echo  [4] Tizim avtotestlarini tekshirish (pytest)
echo  [0] Chiqish
echo.
set /p choice="Tanlovingiz (1/2/3/4/0): "

if "%choice%"=="1" (
    "%PY_EXE%" main.py --text
) else if "%choice%"=="2" (
    "%PY_EXE%" main.py --voice
) else if "%choice%"=="3" (
    "%PY_EXE%" main.py --once "tizim holatini ko'r va hisobot ber" --react
) else if "%choice%"=="4" (
    "%PY_EXE%" -m pytest tests/ -v
) else if "%choice%"=="0" (
    exit /b 0
) else (
    echo Standart matnli rejim ochilmoqda...
    "%PY_EXE%" main.py --text
)

:end
pause
