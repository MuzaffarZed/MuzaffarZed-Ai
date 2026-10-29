# J.A.R.V.I.S — Multimodal Autonomous System (v2.0)

**Bosh Muhandis:** Janob Muzaffar  
**Loyiha ildizi:** `C:\Users\MuzaffarZed\ai_workspace`  
**Virtual Muhit:** `C:\Users\MuzaffarZed\ai_workspace\venv`  
**Qo'llab-quvvatlanuvchi OT:** Windows 10 / Windows 11

---

## 🏛️ 4 Asosiy Ustunga Asoslangan Modulli Arxitektura

### 1. 👁️ Kompyuter nigohi (Vision / Screen-Awareness — `vision/`)
- **`vision/screen_capture.py`**: DPI-aware (yuqori masshtabli displeylarda ham aniq), ko'p monitorli virtual ish stoli yoki ma'lum sohadan skrinshot olish, xotirada bayt yoki base64 ko'rinishida siqish.
- **`vision/coordinate_mapper.py`**: Multimodal model tomonidan `[0, 1000]` shkalasida aniqlangan koordinata yoki bounding box `[ymin, xmin, ymax, xmax]` markazini ekranning real jismoniy piksellariga `(x, y)` aylantirish va ekran chegaralaridan chiqib ketmaslik (clamping).
- **`vision/screen_analyzer.py`**: `google-genai` (Gemini 2.5 Flash, 2.0 Flash) orqali multimodal vizual fikrlash. Ekranni umumiy tahlil qilish hamda kerakli tugma, belgi, oyna va matnlarni qidirish.
- **`vision/vision_engine.py`**: Barcha vizual imkoniyatlarni birlashtiruvchi markaziy fasad.

### 2. 🖱️ Tizim va GUI boshqaruvi (OS & GUI Automation — `actions/`)
- **`actions/gui_actions.py`**: `PyAutoGUI` vositasida sichqoncha va klaviatura harakatlari:
  - Sichqoncha: `move_to(x, y)`, `click(x, y)`, `double_click(x, y)`, `right_click(x, y)`, `drag_to(x, y)`, `scroll(clicks)`.
  - Klaviatura: O'zbek tilidagi `o‘`, `g‘`, `sh`, `ch` harflarini buzilmasdan xatosiz yozish uchun avtomatik Clipboard (Unicode-safe) orqali matn terish (`type_text`), tezkor kombinatsiyalar (`press_hotkey('alt', 'f4')`, `press_hotkey('ctrl', 'c')`).
  - **Favqulodda to'xtatish (Fail-safe)**: `pyautogui.FAILSAFE = True` faollashtirilgan. Kursor chap yuqori burchakka olib borilganda jarayon zudlik bilan to'xtaydi.
- **`actions/system_actions.py`**: Ilovalarni tezkor ishga tushirish (Chrome, Telegram, VS Code, Bloknot, Terminal, Taskmgr, Explorer), Win32 tizim ovozi va media nazorati, apparat telemetriyasi (`psutil`).

### 3. 🎙️ Kiruvchi buyruqlar (Dual Input — `senses/` va `main.py`)
- **Matnli rejim**: Interaktiv buyruqlar qatori orqali yozma boshqarish (`--text`).
- **Ovozli rejim**: `SpeechRecognition` orqali mikrofondan kelayotgan o'zbek tilidagi nutqni shovqindan tozalab, aniq matnga aylantirish (`--voice`).

### 4. 🔊 Chiquvchi javoblar (Feedback — `senses/voice.py`)
- **Tabiiy ovozli hisobot**: Microsoft `edge-tts` orqali tiniq, ravon va tabiiy o'zbek tilida gapirish (`uz-UZ-MadinaNeural` / `uz-UZ-SardorNeural`).
- **Offline zaxira**: Favqulodda internet yo'qolganda `pyttsx3` offline ovoz tizimi.
- **Fon ijrosi**: Windows Multimedia (`WinMM`) orqali keraksiz oyna yoki popuplarsiz fonda audio ijro.
- **Akustik signallar**: `winsound` orqali tinglash boshlanishi, buyruq qabul qilinishi va tugallanish signallari.

---

## 🤖 Antigravity Subagenti
Tizim Antigravity muhiti ichida orqa fonda parallel vazifalarni bajaruvchi maxsus subagentga ega:
- Fayl joylashuvi: `.agents/agents/jarvis-controller.md`

---

## 🚀 Ishga Tushirish

### 1. Interaktiv Menyu orqali:
`Ishga_Tushirish.bat` faylini bosing.
- `1` — Matnli rejim
- `2` — Ovozli rejim
- `3` — Tizim avtotestlari (`pytest`)

### 2. PowerShell / Terminal orqali:
```powershell
# Virtual muhit orqali bitta buyruq bajarish:
.\venv\Scripts\python.exe main.py --once "Vaqt necha bo'ldi?"
.\venv\Scripts\python.exe main.py --once "Tizim holati qanday?"
.\venv\Scripts\python.exe main.py --once "Ekranga qara"

# Matnli interaktiv konsol:
.\venv\Scripts\python.exe main.py --text

# Ovozli rejim:
.\venv\Scripts\python.exe main.py --voice

# Barcha avtotestlarni tekshirish:
.\venv\Scripts\python.exe -m pytest tests/ -v
```
