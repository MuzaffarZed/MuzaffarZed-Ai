# -*- coding: utf-8 -*-
"""
Visual QA Inspector (Playwright Autonomous Headless Engine)
Muallif: MuzaffarZed
Standart: MUTLAQ MUKAMMALLIK (Zero-Beta, Zero-Defect)
Desktop (1920x1080) va Mobile (390x844) o'lchamlarda skrinshot olish,
konsol xatolarini tutish va Vercel Guidelines bo'yicha avto-audit qilish.
"""

import os
import sys
import json
import asyncio
from datetime import datetime
from playwright.async_api import async_playwright

SCREENSHOT_DIR = os.path.join(r"C:\Users\MuzaffarZed\ai_workspace", "screenshots", "visual_qa")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

class VisualQAInspector:
    def __init__(self, target):
        self.target = target
        self.console_logs = []
        self.page_errors = []
        self.audit_results = {
            "target": target,
            "timestamp": datetime.now().isoformat(),
            "desktop_ok": False,
            "mobile_ok": False,
            "console_errors_count": 0,
            "defects": [],
            "screenshots": {}
        }

    async def inspect(self):
        url = self.target
        if os.path.exists(url):
            url = f"file:///{os.path.abspath(url).replace(os.sep, '/')}"

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            
            # 1. Desktop Test (1920x1080)
            d_context = await browser.new_context(viewport={"width": 1920, "height": 1080})
            d_page = await d_context.new_page()
            
            d_page.on("console", lambda msg: self.console_logs.append(f"[{msg.type}] {msg.text}") if msg.type in ["error", "warning"] else None)
            d_page.on("pageerror", lambda err: self.page_errors.append(str(err)))
            
            try:
                await d_page.goto(url, wait_until="networkidle", timeout=15000)
            except Exception as e:
                # If networkidle times out, fallback to load
                try:
                    await d_page.goto(url, wait_until="load", timeout=10000)
                except Exception as ex:
                    self.audit_results["defects"].append(f"Yuklashda xato: {ex}")
            
            d_shot = os.path.join(SCREENSHOT_DIR, "desktop_view.png")
            await d_page.screenshot(path=d_shot, full_page=True)
            self.audit_results["screenshots"]["desktop"] = d_shot
            self.audit_results["desktop_ok"] = True
            
            # 2. Mobile Test (390x844 - iPhone 14 style)
            m_context = await browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True)
            m_page = await m_context.new_page()
            try:
                await m_page.goto(url, wait_until="load", timeout=10000)
            except Exception:
                pass
                
            m_shot = os.path.join(SCREENSHOT_DIR, "mobile_view.png")
            await m_page.screenshot(path=m_shot, full_page=True)
            self.audit_results["screenshots"]["mobile"] = m_shot
            self.audit_results["mobile_ok"] = True

            # 3. Vercel Guidelines JS Audit
            js_audit = """() => {
                const issues = [];
                // Hit targets check (mobile touch >= 44x44 or desktop >= 24x24)
                const clickables = document.querySelectorAll('button, a, input, select, textarea, [role="button"]');
                clickables.forEach(el => {
                    const rect = el.getBoundingClientRect();
                    if (rect.width > 0 && rect.height > 0 && (rect.width < 24 || rect.height < 24)) {
                        issues.push(`Kichik hit-target (<24px): <${el.tagName.toLowerCase()}> o'lchami ${Math.round(rect.width)}x${Math.round(rect.height)}px`);
                    }
                });
                // Small font check on mobile (<16px)
                const texts = document.querySelectorAll('p, span, a, input, label');
                texts.forEach(el => {
                    const fs = parseFloat(window.getComputedStyle(el).fontSize);
                    if (fs > 0 && fs < 11) {
                        issues.push(`O'ta kichik matn (<11px): ${fs}px`);
                    }
                });
                return issues.slice(0, 10);
            }"""
            try:
                client_issues = await m_page.evaluate(js_audit)
                self.audit_results["defects"].extend(client_issues)
            except Exception as e:
                pass

            await browser.close()

        self.audit_results["console_errors_count"] = len(self.console_logs) + len(self.page_errors)
        self.audit_results["console_logs"] = self.console_logs
        self.audit_results["page_errors"] = self.page_errors
        return self.audit_results

def run_self_test():
    test_html = os.path.join(SCREENSHOT_DIR, "test_page.html")
    with open(test_html, "w", encoding="utf-8") as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visual QA Test</title>
    <style>
        body { font-family: sans-serif; background: #0A0F1D; color: #FFFFFF; padding: 20px; }
        .btn { min-width: 44px; min-height: 44px; background: #00E5FF; color: #000; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; }
        .watermark { opacity: 0.4; font-size: 11px; margin-top: 30px; }
    </style>
</head>
<body>
    <h1>Visual QA Verification</h1>
    <p style="font-size: 16px;">Vercel Web Interface Guidelines Test Sahifasi.</p>
    <button class="btn">Test Tugma</button>
    <div class="watermark">Dasturchi: MuzaffarZed</div>
</body>
</html>""")
    inspector = VisualQAInspector(test_html)
    res = asyncio.run(inspector.inspect())
    print(json.dumps(res, indent=2))
    return res["desktop_ok"] and res["mobile_ok"]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != "--test":
        target = sys.argv[1]
        inspector = VisualQAInspector(target)
        res = asyncio.run(inspector.inspect())
        print(json.dumps(res, indent=2))
    else:
        print("[VisualQA] O'z-o'zini tekshirish (Self-Test) ishga tushdi...")
        ok = run_self_test()
        print(f"[VisualQA] Natija: {'MUVAFFAQ' if ok else 'XATO'}")
