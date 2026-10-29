# NovaBlocks — Dinamik Blokli Zamonaviy Ish Maydoni (Workspace)

> **Muallif va Bosh Arxitektor:** MuzaffarZed  
> **Standart:** Mutlaq Mukammallik (Zero-Beta, Zero-Defect)  
> **Versiya:** v3.0 Ultra  

---

## 🌟 Umumiy Tavsif
**NovaBlocks** — bu ekran bo'ylab to'liq erkin harakatlanuvchi, o'lchami dinamik o'zgaruvchi va har bir bloki shaxsiy fon rasmlari hamda qoraytirish effektlari bilan boyitilgan eng zamonaviy veb-ish maydoni (Interactive Block-Based Canvas OS).

Ushbu tizim Apple nafisligi (silliq glassmorphism, blur effektlari), Android moslashuvchanligi (boy oflayn imkoniyatlar), Linux yengilligi (nol ortiqcha kutubxona, toza Vanilla JS) hamda Windows flagmanlari qulayligini (magnit setka, qaynoq tugmalar, ko'p qatlamli z-index boshqaruvi) o'zida mujassam etgan.

---

## ⚡ Asosiy Imkoniyatlar va Yangi Ilg'or Funksiyalar (v3.0 Ultra)

### 1. 🧲 Magnit Setka va Intellektual Yo'naltiruvchi Chiziqlar (Magnetic Snapping & Smart Guides)
- **16px Magnit Setka:** Bloklar ko'chirilganda va o'lchami o'zgartirilganda 16px li ko'rinmas panjaraga aniq yopishadi.
- **Figma-darajasidagi Smart Alignment Guides:** Blok boshqa bir blokning chap, o'ng, tepa, pastki chegarasi yoki markaziga yaqinlashganda ekranda avtomatik ravishda neon-binafsharang chiziqlar va piksel ko'rsatkichli nishonlar (`Chap`, `O'ng`, `Markaz X`, `Tepa`, `Past`) paydo bo'ladi.
- **Top Bar Toggle Switch:** Yuqori asboblar panelida macOS/iOS uslubidagi silliq "Setka" almashtirgich (toggle switch) orqali tizimni bir zumda yoqish yoki o'chirish mumkin (`G` qaynoq tugmasi).

### 2. ✍️ Suzuvchi Matn Formatlash Paneli (Floating Typography Toolbar)
- Matn maydoniga bosilganda yoki fokus berilganda faol blok tepasida zamonaviy suzuvchi formatlash pulti paydo bo'ladi.
- **Shriftlar to'plami:** *Inter (Sans)*, *Playfair Display (Klassik Serif)*, *Fira Code (Dasturchi Monospace)*, *Plus Jakarta Sans (Nafis Geometrik)*.
- **Shrift o'lchamlari:** `S (12px)`, `M (14px)`, `L (16px)`, `XL (20px)`.
- **Matn rangi:** Tayyor rang palitrasi (Oq, To'q Slate, Moviy, Zumrad, Oltin, Atirgul) hamda cheksiz HTML5 rang tanlagich (`<input type="color">`).
- **Qalin va Qiya matn:** Bir bosishda `B` (Bold) va `I` (Italic) rejimlari.
- **Gorizontal va Vertikal Tekislash:** Matnni chapga, markazga, o'ngga surish hamda blok ichida vertikal (tepaga, o'rtaga, pastga) joylashtirish.
- **Tipografiya xotirasi:** Har bir blokning individual shrift va uslublari avtomatik ravishda `localStorage`da saqlanadi.

### 3. 📸 Toza PNG Tasvir va PDF Hujjat Eksporti (Clean Canvas Export)
- Yuqori panelda **"Eksport"** tugmasi va menyusi:
  - 🖼️ **Download as PNG:** Butun kanvasni 2x Retina sifatidagi tiniq rasm sifatida yuklab olish.
  - 📄 **Download as PDF:** Ish maydonini chop etishga tayyor professional PDF hujjatiga aylantirish.
  - 💾 **Download as JSON:** Butun tizim ma'lumotlarini zaxira fayl qilib olish.
- **Toza Tasvir Kafolati:** Eksport jarayonida barcha boshqaruv tugmalari (o'chirish, o'lcham tutqichlari, suzuvchi panellar, yo'naltiruvchi chiziqlar) avtomatik ravishda yashiriladi va faqat chiroyli tayyor bloklar tasvirga tushadi.

### 4. 🖼️ Shaxsiy Fon Rasmlari va Effektlar (Custom Background Engine)
- Mahalliy rasm yuklash (Offline FileReader API) yoki internetdan URL qo'yish.
- Overlay Opacity (0% dan 95% gacha qoraytirish) va Backdrop Blur (oynasimon xiralashtirish).
- Rangli tuslar (Qora, Safir, Zumrad, Oltin, Muzdek oq).

### 5. 💾 Avtomatik Saqlash va Zaxira (Persistence)
- Barcha koordinatalar, o'lchamlar, matnlar, tipografiya va fonlar uzluksiz `localStorage`ga yozib boriladi.
- Sahifa yangilanganda yoki brauzer qayta ochilganda barcha ish joyingiz 100% tiklanadi.

---

## ⌨️ Tezkor Qaynoq Tugmalar
| Tugmalar | Vazifasi |
| :--- | :--- |
| `Ctrl + N` | Yangi blok qo'shish |
| `Ctrl + D` | Tanlangan blokdan nusxa olish |
| `G` | Magnit setka va yo'naltiruvchilarni yoqish / o'chirish |
| `T` | Blok sarlavhasidagi T tugmasi orqali suzuvchi formatlash panelini ochish |
| `Del / Backspace` | Tanlangan blokni o'chirish |
| `Space + Drag` | Kanvasni erkin surish (Pan) |
| `Ctrl + G'ildirak` | Masshtabni kattalashtirish / kichiklashtirish (50% - 175%) |
| `Esc` | Barcha ochiq pult va menyularni yopish |

---

*Dasturchi: MuzaffarZed*
