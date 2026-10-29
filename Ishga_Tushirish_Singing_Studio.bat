@echo off
chcp 65001 >nul
title JARVIS AI Singing Studio — Janob Muzaffar
color 0B

echo =====================================================================
echo           JARVIS AI SINGING STUDIO - YAGONA STUDIYA TIZIMI
echo             Muhtaram janob Muzaffar uchun maxsus tayyorlandi
echo =====================================================================
echo.
echo [1/3] Python virtual muhiti tekshirilmoqda...
set PYTHON_EXE="C:\Users\MuzaffarZed\ai_workspace\venv\Scripts\python.exe"

if not exist %PYTHON_EXE% (
    echo [!] XATOLIK: Python virtual muhiti topilmadi: %PYTHON_EXE%
    pause
    exit /b 1
)

echo [2/3] FFmpeg va audio modullar tekshirilmoqda...
where ffmpeg >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] DIQQAT: FFmpeg topilmadi. Audio ishlashida xatolik bolishi mumkin.
) else (
    echo [OK] FFmpeg tizimda mavjud va tayyor!
)

echo.
echo [3/3] Studiya serveri ishga tushirilmoqda: http://127.0.0.1:7860
echo Brauzer avtomatik ravishda ochiladi...
echo.

start "" http://127.0.0.1:7860

cd /d "C:\Users\MuzaffarZed\ai_workspace\singing_studio"
%PYTHON_EXE% app.py

pause
