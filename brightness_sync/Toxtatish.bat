@echo off
title Yorug'lik Sinxronizatorini To'xtatish
powershell -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*service.py*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force; Write-Host ('[OK] Jarayon toxtatildi: PID ' + $_.ProcessId) }"
echo =======================================================
echo   Sinxronizatsiya xizmati to'xtatildi.
echo =======================================================
ping 127.0.0.1 -n 2 > nul
