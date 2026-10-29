# -*- coding: utf-8 -*-
import sys
import os
import shutil
import asyncio
from playwright.async_api import async_playwright

ARTIFACT_DIR = r"C:\Users\MuzaffarZed\.gemini\antigravity\brain\72c2b0f2-6160-4256-88c8-75c12871d9f5"
SCREENSHOT_PATH = r"C:\Users\MuzaffarZed\ai_workspace\youtube_clone\youtube_pro_phone_qr_modal.png"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        print("[TEST] Navigating to http://localhost:8000 ...", flush=True)
        await page.goto("http://localhost:8000", wait_until="domcontentloaded")
        await page.wait_for_timeout(1500)

        # Check btn-connect-phone exists
        btn_phone = page.locator("#btn-connect-phone")
        assert await btn_phone.is_visible(), "btn-connect-phone not visible!"
        print("[TEST] #btn-connect-phone is visible in header.", flush=True)

        # Click phone connect button
        await btn_phone.click()
        await page.wait_for_timeout(1000)

        # Check modal is open
        modal = page.locator("#connect-phone-modal")
        classes = await modal.get_attribute("class")
        assert "open" in classes, f"connect-phone-modal did not get 'open' class: {classes}"
        print("[TEST] #connect-phone-modal is open.", flush=True)

        # Check IP link
        ip_link = page.locator("#phone-modal-ip-link")
        ip_text = await ip_link.text_content()
        print(f"[TEST] Phone IP Link: {ip_text}", flush=True)
        assert "192.168" in ip_text or "8000" in ip_text, f"Unexpected IP link: {ip_text}"

        # Check mDNS link
        mdns_link = page.locator("#phone-modal-mdns-link")
        mdns_text = await mdns_link.text_content()
        print(f"[TEST] mDNS Link: {mdns_text}", flush=True)
        assert "local:8000" in mdns_text, f"Unexpected mDNS link: {mdns_text}"

        # Check Cloudflare Global Link
        cf_link = page.locator("#phone-modal-cf-link")
        cf_text = await cf_link.text_content()
        print(f"[TEST] Cloudflare Global Link: {cf_text}", flush=True)
        assert "trycloudflare.com" in cf_text, f"Unexpected Cloudflare link: {cf_text}"

        # Check QR code img src
        qr_img = page.locator("#phone-modal-qr-img")
        qr_src = await qr_img.get_attribute("src")
        print(f"[TEST] QR Image Src: {qr_src}", flush=True)
        assert "api.qrserver.com" in qr_src, f"Unexpected QR src: {qr_src}"

        # Click Copy Cloudflare button
        btn_copy_cf = page.locator("#btn-copy-cf-link")
        await btn_copy_cf.click()
        await page.wait_for_timeout(500)

        # Capture screenshot of the modal
        await page.screenshot(path=SCREENSHOT_PATH)
        print(f"[TEST] Saved screenshot: {SCREENSHOT_PATH}", flush=True)

        # Copy to artifact dir
        dest_artifact = os.path.join(ARTIFACT_DIR, "youtube_pro_phone_qr_modal.png")
        shutil.copy2(SCREENSHOT_PATH, dest_artifact)
        print(f"[TEST] Copied screenshot to artifact directory: {dest_artifact}", flush=True)

        # Test Escape key dismissal
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(500)
        classes_after_esc = await modal.get_attribute("class")
        assert "open" not in classes_after_esc, f"Modal did not close on Escape: {classes_after_esc}"
        print("[TEST] Modal closed cleanly on Escape key!", flush=True)

        await browser.close()
        print("[TEST] ALL TESTS PASSED! ZERO DEFECT!", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
