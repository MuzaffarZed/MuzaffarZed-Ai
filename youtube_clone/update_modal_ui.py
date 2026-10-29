# -*- coding: utf-8 -*-

index_path = r"C:\Users\MuzaffarZed\ai_workspace\youtube_clone\index.html"
with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

# Replace Option 3 in #connect-phone-modal
old_opt3 = """        <!-- Cloudflare Global Tunnel Option -->
        <div style="display: flex; align-items: center; justify-content: space-between; gap: 8px; border-top: 1px solid var(--yt-border); padding-top: 8px;">
          <div style="overflow: hidden;">
            <div style="font-size: 11px; font-weight: 700; color: #10b981; text-transform: uppercase;">3. Dunyo bo'ylab (Wi-Fi'siz / 4G):</div>
            <span style="font-size: 12px; color: var(--yt-text-secondary);">start_public_tunnel.bat orqali bepul HTTPS</span>
          </div>
          <button class="yt-btn-secondary" id="btn-info-cloudflare" style="padding: 5px 10px; font-size: 11px; border-radius: 8px; display: flex; align-items: center; gap: 4px; white-space: nowrap; color: #10b981; border-color: rgba(16,185,129,0.3);">
            <i data-lucide="globe" style="width: 13px; height: 13px;"></i>
            <span>Ma'lumot</span>
          </button>
        </div>"""

new_opt3 = """        <!-- Cloudflare Global Tunnel Option -->
        <div style="display: flex; align-items: center; justify-content: space-between; gap: 8px; border-top: 1px solid var(--yt-border); padding-top: 8px;">
          <div style="overflow: hidden;">
            <div style="font-size: 11px; font-weight: 700; color: #10b981; text-transform: uppercase;">3. Dunyo bo'ylab (Wi-Fi'siz / 4G):</div>
            <a id="phone-modal-cf-link" href="#" target="_blank" style="font-size: 13px; font-weight: 600; color: #10b981; text-decoration: none; word-break: break-all;">
              Yuklanmoqda...
            </a>
          </div>
          <button class="yt-btn-secondary" id="btn-copy-cf-link" style="padding: 5px 10px; font-size: 11px; border-radius: 8px; display: flex; align-items: center; gap: 4px; white-space: nowrap; color: #10b981; border-color: rgba(16,185,129,0.3);">
            <i data-lucide="copy" style="width: 13px; height: 13px;"></i>
            <span>Nusxa</span>
          </button>
        </div>"""

if old_opt3 in html:
    html = html.replace(old_opt3, new_opt3)
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html updated with phone-modal-cf-link!")
else:
    print("Option 3 pattern not found or already updated")
