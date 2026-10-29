@echo off
chcp 65001 >nul
title J.A.R.V.I.S — Resident Background Daemon
echo ================================================================================
echo           J.A.R.V.I.S — ELEVATED RESIDENT OS DAEMON (v3.0)
echo         Bosh Muhandis: Janob Muzaffar ^| Windows 10 / 11 Autonomiya
echo ================================================================================
echo.
echo [1] Fonda bevosita ishga tushirish (Foreground / Console)
echo [2] Windows Task Scheduler ga o'rnatish (Avtomatik Elevated Startup)
echo [3] Xizmatni to'xtatish
echo [4] Chiqish
echo.
set /p choice="Tanlovingizni kiriting [1-4]: "

if "%choice%"=="1" (
    echo.
    echo [+] JARVIS Daemon ishga tushmoqda: http://127.0.0.1:8765 ...
    .\venv\Scripts\python.exe daemon\elevated_server.py
)
if "%choice%"=="2" (
    echo.
    echo [+] Windows Task Scheduler ga o'rnatilmoqda...
    .\venv\Scripts\python.exe daemon\service_installer.py
    pause
)
if "%choice%"=="3" (
    echo.
    echo [+] Xizmat to'xtatilmoqda...
    .\venv\Scripts\python.exe daemon\service_installer.py stop
    pause
)
