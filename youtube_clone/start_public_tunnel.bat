@echo off
title YouTube Pro - Cloudflare Bepul Global Tunnel (MuzaffarZed)
color 0A
chcp 65001 > nul
cls
echo ==============================================================================
echo        YOUTUBE PRO — CLOUDFLARE BEPUL GLOBAL TUNNEL (MuzaffarZed)
echo ==============================================================================
echo.
echo  [1] Ushbu tunnel kompyuteringizdagi YouTube Pro (http://127.0.0.1:8000) ni
echo      butun dunyo bo'ylab BEPUL, tezkor va shifrlangan HTTPS havolaga aylantiradi!
echo.
echo  [2] Hech qanday to'lov yo'q ($0), ro'yxatdan o'tish yoki karta kiritish shart emas!
echo.
echo  [3] Telefoningizda (Wi-Fi bo'lmasa ham, 4G/5G mobil internetda) ochishingiz mumkin.
echo.
echo  Tunnel ishga tushirilmoqda...
echo  Quyida "https://xxxxxxxx.trycloudflare.com" ko'rinishidagi havola paydo bo'ladi.
echo ==============================================================================
echo.
"%~dp0cloudflared.exe" tunnel --url http://127.0.0.1:8000
pause
