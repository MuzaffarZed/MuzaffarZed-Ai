# -*- coding: utf-8 -*-
import os

index_path = r"C:\Users\MuzaffarZed\ai_workspace\youtube_clone\index.html"
with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add header button before #btn-install-pwa
btn_target = '<!-- Install PWA App Button -->'
new_btn = """<!-- Phone Connect QR Code Button -->
      <button class="yt-icon-btn yt-phone-connect-btn" id="btn-connect-phone" title="Telefonga ulash (QR Kod va Wi-Fi)">
        <i data-lucide="smartphone" style="width: 16px; height: 16px;"></i>
        <span>Telefonga ulash</span>
      </button>

      """
if 'btn-connect-phone' not in content:
    content = content.replace(btn_target, new_btn + btn_target)
    print("Added btn-connect-phone to header")
else:
    print("btn-connect-phone already present")

# 2. Add menu item in #user-profile-dropdown
menu_target = '<div class="yt-user-menu-item" id="menu-my-channel">'
new_menu_item = """<div class="yt-user-menu-item" id="menu-connect-phone">
      <i data-lucide="qr-code" style="width: 18px; height: 18px; color: #10b981;"></i>
      <span>Telefonda ochish (QR Kod)</span>
    </div>
    """
if 'menu-connect-phone' not in content:
    content = content.replace(menu_target, new_menu_item + menu_target)
    print("Added menu-connect-phone to user dropdown")
else:
    print("menu-connect-phone already present")

# 3. Add #connect-phone-modal before </body>
modal_target = '</body>'
modal_html = """  <!-- Phone Connect & Network Discovery Modal -->
  <div class="yt-modal-backdrop" id="connect-phone-modal">
    <div class="yt-modal-card" style="max-width: 460px; text-align: center; position: relative;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; border-bottom: 1px solid var(--yt-border); padding-bottom: 10px;">
        <h3 style="font-size: 17px; font-weight: 700; display: flex; align-items: center; gap: 8px; margin: 0;">
          <i data-lucide="smartphone" style="width: 20px; height: 20px; color: #10b981;"></i>
          <span>Telefonga Ulash &amp; QR Kod</span>
        </h3>
        <button class="yt-icon-btn" id="btn-close-phone-modal" title="Yopish" style="width: 28px; height: 28px;">
          <i data-lucide="x" style="width: 18px; height: 18px;"></i>
        </button>
      </div>

      <div style="background: #ffffff; border-radius: 16px; padding: 12px; display: inline-block; box-shadow: 0 8px 24px rgba(0,0,0,0.25); margin: 4px auto 12px;">
        <img id="phone-modal-qr-img" src="" alt="QR Kod yuklanmoqda..." style="width: 210px; height: 210px; display: block; border-radius: 8px;">
      </div>

      <p style="font-size: 13px; color: var(--yt-text-secondary); margin: 0 0 14px; line-height: 1.4;">
        Telefon kamerangizni QR kodga qarating — YouTube Pro hech qanday IP yozmasdan ochiladi!
      </p>

      <div style="display: flex; flex-direction: column; gap: 10px; text-align: left; background: var(--yt-surface); border: 1px solid var(--yt-border); border-radius: 12px; padding: 12px 14px;">
        <!-- Wi-Fi Direct IP Address -->
        <div style="display: flex; align-items: center; justify-content: space-between; gap: 8px;">
          <div style="overflow: hidden;">
            <div style="font-size: 11px; font-weight: 700; color: var(--yt-text-secondary); text-transform: uppercase;">1. Wi-Fi manzili (Telefon uchun):</div>
            <a id="phone-modal-ip-link" href="#" target="_blank" style="font-size: 13px; font-weight: 600; color: var(--yt-blue); text-decoration: none; word-break: break-all;">
              Yuklanmoqda...
            </a>
          </div>
          <button class="yt-btn-secondary" id="btn-copy-ip-link" style="padding: 5px 10px; font-size: 11px; border-radius: 8px; display: flex; align-items: center; gap: 4px; white-space: nowrap;">
            <i data-lucide="copy" style="width: 13px; height: 13px;"></i>
            <span>Nusxa</span>
          </button>
        </div>

        <!-- mDNS Hostname Address -->
        <div style="display: flex; align-items: center; justify-content: space-between; gap: 8px; border-top: 1px solid var(--yt-border); padding-top: 8px;">
          <div style="overflow: hidden;">
            <div style="font-size: 11px; font-weight: 700; color: var(--yt-text-secondary); text-transform: uppercase;">2. IP raqamsiz manzil (mDNS):</div>
            <a id="phone-modal-mdns-link" href="#" target="_blank" style="font-size: 13px; font-weight: 600; color: var(--yt-blue); text-decoration: none; word-break: break-all;">
              Yuklanmoqda...
            </a>
          </div>
          <button class="yt-btn-secondary" id="btn-copy-mdns-link" style="padding: 5px 10px; font-size: 11px; border-radius: 8px; display: flex; align-items: center; gap: 4px; white-space: nowrap;">
            <i data-lucide="copy" style="width: 13px; height: 13px;"></i>
            <span>Nusxa</span>
          </button>
        </div>

        <!-- Cloudflare Global Tunnel Option -->
        <div style="display: flex; align-items: center; justify-content: space-between; gap: 8px; border-top: 1px solid var(--yt-border); padding-top: 8px;">
          <div style="overflow: hidden;">
            <div style="font-size: 11px; font-weight: 700; color: #10b981; text-transform: uppercase;">3. Dunyo bo'ylab (Wi-Fi'siz / 4G):</div>
            <span style="font-size: 12px; color: var(--yt-text-secondary);">start_public_tunnel.bat orqali bepul HTTPS</span>
          </div>
          <button class="yt-btn-secondary" id="btn-info-cloudflare" style="padding: 5px 10px; font-size: 11px; border-radius: 8px; display: flex; align-items: center; gap: 4px; white-space: nowrap; color: #10b981; border-color: rgba(16,185,129,0.3);">
            <i data-lucide="globe" style="width: 13px; height: 13px;"></i>
            <span>Ma'lumot</span>
          </button>
        </div>
      </div>

      <div style="margin-top: 14px; font-size: 12px; color: var(--yt-text-secondary); display: flex; align-items: center; justify-content: center; gap: 6px;">
        <i data-lucide="shield-check" style="width: 15px; height: 15px; color: #10b981;"></i>
        <span>Shifrlangan mahalliy tarmoq • 0 so'm xarajat • MuzaffarZed</span>
      </div>
    </div>
  </div>

"""
if 'connect-phone-modal' not in content:
    content = content.replace(modal_target, modal_html + modal_target)
    print("Added connect-phone-modal to index.html")
else:
    print("connect-phone-modal already present")

with open(index_path, "w", encoding="utf-8") as f:
    f.write(content)
print("index.html updated successfully!")
