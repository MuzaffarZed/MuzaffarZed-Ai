# 🤖 J.A.R.V.I.S Pro Native — Mukammal Loyiha Pasporti va Migratsiya Manfesti
> **Bosh Arxitektor:** Janob Muzaffar | **Dasturchi:** MuzaffarZed  
> **Versiya:** `v12.0 QUANTUM-APEX` (Zero-Beta, Zero-Defect)  
> **Antigravity Boshlang'ich Chat ID:** `conversation://e5c21327-3ca5-4acd-92d1-8b0b219000dd`  
> **Sana:** 2026-10-13  

---

## 📌 1. YANGI CHATDA DAVOM ETTIRISHNING 3 TA OSON USULI

### ⚡ 1-USUL: Antigravity Cross-Conversation Link (Eng qulay va tezkor)
Yangi ochgan chatingizga quyidagi matnni nusxalab jo'natsangiz kifoya:
```text
Oldingi chatimizdagi J.A.R.V.I.S Pro Native loyihamizni davom ettiramiz. 
Chat tarixi va arxitektura havolasi: conversation://e5c21327-3ca5-4acd-92d1-8b0b219000dd
Loyiha pasporti: C:\Users\MuzaffarZed\ai_workspace\JARVIS_PROJECT_PASSPORT.md
Iltimos, shu manzil va pasportni to'liq o'rganib chiqib, ishni uzluksiz davom ettir.
```
*Antigravity yangi chat ichidan turib avvalgi chatning `transcript.jsonl` va `transcript_full.jsonl` fayllarini to'liq o'qib, barcha qilingan ishlarni 100% xotirasida tiklaydi.*

---

### 📂 2-USUL: Loyiha Fayllari va Holatini Yangi Loyihaga Nusxalash
Agar yangi chat boshqa bir maxsus papkada ochilgan bo'lsa (masalan, `C:\Users\MuzaffarZed\yangi_loyiha`), quyidagi buyruq orqali butun kod bazasi yangi katalogga o'tkaziladi:
```powershell
# Manba papkasidan yangi loyihaga nusxalash:
Copy-Item -Path "C:\Users\MuzaffarZed\ai_workspace\JarvisNativePro" -Destination "SIZNING_YANGI_PAPKA\JarvisNativePro" -Recurse -Force
```
*Dasturning barcha sozlamalari, muloqot tarixi, xazinasi va ovoz sozlamalari `C:\Users\MuzaffarZed\AppData\Local\JarvisNativePro\jarvis_state_v11.json` faylida saqlangani sababli, dastur qayerga ko'chsa ham xotirasi o'chib ketmaydi!*

---

## 🗺️ 2. FAYLLAR VA KATALOGLAR XARITASI (EXACT PATHS)

| Qism | To'liq Manzil | Tavsif |
| :--- | :--- | :--- |
| **Boshlang'ich Chat Loglari** | `C:\Users\MuzaffarZed\.gemini\antigravity\brain\e5c21327-3ca5-4acd-92d1-8b0b219000dd` | Ushbu suhbatdagi barcha qadamlar, buyruqlar va xotira |
| **C# Bosh Loyiha** | `C:\Users\MuzaffarZed\ai_workspace\JarvisNativePro` | To'liq C# .NET 10 WinForms + WebView2 GPU loyihasi |
| **Yakka-Fayl Ish stolidagi EXE** | `C:\Users\MuzaffarZed\Desktop\JARVIS_Pro.exe` | Barcha DLL'lari ichiga joylangan mustaqil tayyor dastur |
| **HTML / CSS / JS UI Kodlari** | `C:\Users\MuzaffarZed\ai_workspace\JarvisNativePro\ui` | `index.html`, `styles.css`, `app.js` (8 ta tab, 5 ta tema) |
| **Dastur Xotirasi va Holati** | `C:\Users\MuzaffarZed\AppData\Local\JarvisNativePro\jarvis_state_v11.json` | Chat tarixi, Smart Vault, mavzu, API kalit, ovoz teglari |
| **Avtomatlashtirilgan Testlar** | `C:\Users\MuzaffarZed\ai_workspace\tests\test_jarvis_native_pro.py` | 8 ta kompleks pytest sinovi (100% Yashil) |
| **Python Virtual Muhiti** | `C:\Users\MuzaffarZed\ai_workspace\venv\Scripts\python.exe` | Test va qo'shimcha skriptlar muhiti |

---

## 🏗️ 3. TEXNOLOGIK ARXITEKTURA VA IMKONIYATLAR

1. **Yadro va Backend (C# .NET 10 + DirectX 12):**
   - [`Program.cs`](file:///C:/Users/MuzaffarZed/ai_workspace/JarvisNativePro/Program.cs): 3-bosqichli WebView2 GPU Failover (`0x800700AA` immuniteti), Win32 `ShowWindow(SW_SHOWNORMAL)` va `SetForegroundWindow` integratsiyasi.
   - [`JarvisEngine.cs`](file:///C:/Users/MuzaffarZed/ai_workspace/JarvisNativePro/JarvisEngine.cs):
     - Kognitiv 3-bosqichli AI (Gemini 2.5/Flash + Ollama + C# Oflayn Regex/Math).
     - PC Manager 3-in-1 Super-Boost (RAM EmptyWorkingSet + Temp tozalash + DNS Flush).
     - Multimodal Vision tahlili (GDI+ Skrinshot + Hybrid OCR/Vision).
     - Everything uslubidagi millisekundli fayl qidiruvchi.
     - Microsoft Edge Neural TTS (O'zbekcha `uz-UZ-MadinaNeural` va `uz-UZ-SardorNeural`) + MP3 eksport.
     - Smart Clipboard Vault & Snippets tizimi.
     - Anti-Clutter Workspace Radari va 1-bosishda Yuklamalarni avto-tartiblovchi (`organize_downloads`).
   - [`LocalJarvisServer.cs`](file:///C:/Users/MuzaffarZed/ai_workspace/JarvisNativePro/LocalJarvisServer.cs): Yuqori tezlikdagi nolinchi-kechikishli mahalliy HTTP server (`/api/bootstrap`, `/api/command`, `/api/macro`, `/api/vault`, `/api/tts`, `/api/files`, `/api/windows`, `/api/processes`).

2. **Frontend & UI (Bento-Grid + Sci-Fi Cyber HUD):**
   - **8 ta To'liq Bo'lim:**
     1. `tab-cockpit` — 3D Gologramma Yadro (Arc Reactor), Jonli Telemetriya, Muloqot Markazi.
     2. `tab-apps` — Kompyuterdagi barcha dasturlar va yorliqlar markazi (Studio, AI, Office, System).
     3. `tab-vault` — Aqlli Bufer, Kod parchalari va Yuklamalarni 1-bosishda toifalarga saralovchi Anti-Clutter Radar.
     4. `tab-missions` — Avtonom Super-Boost, Skrinshot, Ovozli diktor MP3 eksporti, PowerShell.
     5. `tab-system` — Jarayonlar boshqaruvi va ochiq oynalar pulti.
     6. `tab-vision` — Multimodal AI Vision galereyasi va tahlili.
     7. `tab-files` — Tezkor fayl qidiruvchi.
     8. `tab-settings` — Ovozlar, ekvayzer, API kalitlar va xotira boshqaruvi.
   - **Qaynoq tugmalar:** `Ctrl+K` (Universal Palitra), `F2` (Ovozli buyruq), `Ctrl+F` (Qidiruv), `Esc` (To'xtatish), `F1..F8` (Bo'limlar).
   - **5 ta Elita Mavzu:** Onyx (Kiber-Qora), Oltin (Stark Gold), Zumrad (Cyber Emerald), Sport (Neon Sport), Kristal (Yorug'lik).
   - **WebAudio DSP:** 5 polosali Ekvayzer va 4 xil Binaural Fokus Sintezatori (`40Hz Gamma`, `10Hz Alpha`, `Stark Lab`, `Rain`).

---

## 🛠️ 4. QAYTA YIG'ISH VA TEST BUYRUQLARI
Yangi chatda dasturga yangi funksiyalar qo'shilgach, yagona buyruq orqali yig'ish va sinovdan o'tkazish mumkin:
```powershell
# 1. Yig'ish va Desktop'ga nusxalash:
cd "C:\Users\MuzaffarZed\ai_workspace\JarvisNativePro"
Get-Process JARVIS_Pro -ErrorAction SilentlyContinue | Stop-Process -Force
dotnet publish -c Release -o .\publish
Copy-Item .\publish\JARVIS_Pro.exe "C:\Users\MuzaffarZed\Desktop\JARVIS_Pro.exe" -Force

# 2. 8 ta kompleks testni ishga tushirish:
C:\Users\MuzaffarZed\ai_workspace\venv\Scripts\python.exe -m pytest C:\Users\MuzaffarZed\ai_workspace\tests\test_jarvis_native_pro.py -v
```

---
*Dasturchi: MuzaffarZed | Janob Muzaffar uchun yaratildi.*
