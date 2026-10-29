@echo off
title MuzaffarDub To'xtatish - Dasturchi MuzaffarZed
chcp 65001 >nul
echo Port 8989 tekshirilmoqda...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8989 ^| findstr LISTENING') do (
    echo MuzaffarDub jarayoni topildi (PID: %%a). To'xtatilmoqda...
    taskkill /f /pid %%a >nul 2>&1
)
echo Server to'xtatildi!
timeout /t 2 >nul
