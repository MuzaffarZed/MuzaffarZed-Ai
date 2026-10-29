@echo off
title YouTube Pro - MuzaffarZed Edition
cd /d "%~dp0"
echo ===================================================================
echo   YouTube Pro (MuzaffarZed Edition) ishga tushirilmoqda...
echo   Backend: FastAPI + Uvicorn + SQLite + yt-dlp Real YouTube Engine
echo   Frontend: YouTube 2026 Dark/Light UI + Ambient Mode + AI Xulosa
echo ===================================================================

start "" "http://localhost:8000"
"C:\Users\MuzaffarZed\ai_workspace\venv\Scripts\python.exe" api_server.py
pause
