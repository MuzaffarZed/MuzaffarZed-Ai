---
name: tester
description: test-driven-development va debugging-and-error-recovery orqali avtomatik testlar o'tkazish va xatolarni tuzattirish ish oqimi.
---

# Workflow: Autonomous Testing & Self-Healing

Avtomatlashtirilgan sinov va xatolarni mustaqil bartaraf etish jarayoni.

## Bosqichlar:
1. **`test-driven-development`**:
   - `tests/` papkasida `pytest` yoki `unittest` sinov fayllarini shakllantirish.
   - Har bir asosiy funksiya, chegara holatlari (edge cases) va API larni to'liq qamrab olish.
2. **Ishga Tushirish**: Testlarni terminalda ishga tushirish (`pytest tests/ -v`).
3. **`debugging-and-error-recovery` (Avtonom Tuzatish Halqasi)**:
   - Agar biron test yiqilsa (Failed):
     - Foydalanuvchini aralashtirmay xato sababini aniqlash.
     - `backend` yoki `frontend` kodidagi xatoni tuzatish.
     - Testlarni qayta ishga tushirish.
   - Bu jarayon barcha testlar 100% muvaffaqiyatli o'tgunga qadar avtonom davom etadi.
4. **Tasdiqlash**: Zero-Defect darajasidagi yashil natijani `reviewer`ga uzatish.

*Dasturchi: MuzaffarZed*
