@echo off
chcp 65001 >nul
title JARVIS Ovozli AI - Janob Muzaffar
color 0a

cd /d "C:\Users\MuzaffarZed\ai_workspace"

"venv\Scripts\python.exe" jarvis.py

if errorlevel 1 (
    echo.
    echo Xatolik yuz berdi. Iltimos, yuqoridagi xabarni korib chiqing.
    pause
)
