schtasks /create /tn "MuzaffarZed_Lock_UTC5" /tr "C:\Users\MuzaffarZed\ai_workspace\lock_tz_utc5.cmd" /sc HOURLY /ru "SYSTEM" /f > "C:\Users\MuzaffarZed\ai_workspace\create_task.log" 2>&1
