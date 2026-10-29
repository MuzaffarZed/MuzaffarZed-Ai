@echo off
title Usta Master 1171 - Rasmiy Telegram Bot
chcp 65001 > nul
cls
echo ========================================================
echo    USTA MASTER 1171 - RASMIY TELEGRAM NAZORATCHI BOT
echo    Muallif: janob Muzaffar
echo    Dasturchi: MuzaffarZed
echo ========================================================
echo.

cd /d "%~dp0"
"C:\Users\MuzaffarZed\ai_workspace\venv\Scripts\python.exe" usta_master_bot.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [!] Bot to'xtadi yoki xatolik yuz berdi.
    pause
)
