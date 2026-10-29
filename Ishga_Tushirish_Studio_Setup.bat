@echo off
chcp 65001 >nul
title Muzaffar Studio OS - 1-Click Setup
color 0b

echo ===================================================================
echo     MUZAFFAR STUDIO OS - 1-CLICK POST-FLASH PROVISIONER
echo     Samsung Galaxy Tab A (SM-T295) Maxsus Studio Tizimi
echo ===================================================================
echo.
echo Proshivkadan so'ng planshet yoqilgach, USB kabelni ulang.
echo "USB sozlash" (USB debugging) ruxsati berilganligiga ishonch hosil qiling.
echo.
pause

C:\Users\MuzaffarZed\ai_workspace\venv\Scripts\python.exe C:\Users\MuzaffarZed\ai_workspace\setup_muzaffar_studio.py

echo.
echo Yakunlandi. Davom etish uchun ixtiyoriy tugmani bosing...
pause >nul
