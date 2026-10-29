---
name: visual-qa-playwright
description: Autonomous Playwright visual QA console checks and layout bug inspection.
---

# Visual QA Playwright Master Skill

## 1. Avtonom Vizual Tekshiruv Ish Tartibi
- Har qanday veb yoki GUI interfeys yaratilganda foydalanuvchiga taqdim etishdan oldin Playwright orqali tekshiriladi:
  `python nexus_core/visual_qa_inspector.py <url_yoki_html_fayl>`
- **Ikki O'lchamli Sinov**:
  - Desktop: 1920x1080 (HD / 4K ko'rinish)
  - Mobile: 390x844 (iPhone 14 / zamonaviy smartfon)

## 2. Zero-Defect Kriteriyalari
- **Console Errors**: Brauzer konsolida 0 ta xato (`page.on('console', ...)` va `pageerror`).
- **Touch-Targets**: Barcha button va linklar o'lchami standartga mos (≥24px desktop, ≥44px mobil).
- **Font Scale**: Mobil o'lchamda 16px dan kichik bo'lmagan matnlar.
- **Skrinshot Tasdig'i**: `screenshots/visual_qa/` papkasiga olingan skrinshotlar orqali vizual nuqsonsizlik tasdiqlanadi.

*Dasturchi: MuzaffarZed*
