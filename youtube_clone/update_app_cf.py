# -*- coding: utf-8 -*-

app_path = r"C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js"
with open(app_path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update cacheDom
old_cache = "this.btnInfoCloudflare = document.getElementById('btn-info-cloudflare');"
new_cache = """this.btnInfoCloudflare = document.getElementById('btn-info-cloudflare');
      this.phoneModalCfLink = document.getElementById('phone-modal-cf-link');
      this.btnCopyCfLink = document.getElementById('btn-copy-cf-link');"""

if old_cache in code:
    code = code.replace(old_cache, new_cache)
    print("cacheDom updated with phoneModalCfLink")

# 2. Update initPhoneConnect logic
old_fetch = """            if (this.phoneModalQrImg && this.networkInfoData.local_url) {
              this.phoneModalQrImg.src = `https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=${encodeURIComponent(this.networkInfoData.local_url)}`;
            }"""

new_fetch = """            if (this.networkInfoData.public_tunnel_url && this.phoneModalCfLink) {
              this.phoneModalCfLink.textContent = this.networkInfoData.public_tunnel_url;
              this.phoneModalCfLink.href = this.networkInfoData.public_tunnel_url;
            }
            const activeQrUrl = this.networkInfoData.public_tunnel_url || this.networkInfoData.local_url;
            if (this.phoneModalQrImg && activeQrUrl) {
              this.phoneModalQrImg.src = `https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=${encodeURIComponent(activeQrUrl)}`;
            }"""

if old_fetch in code:
    code = code.replace(old_fetch, new_fetch)
    print("initPhoneConnect updated with activeQrUrl and phoneModalCfLink")

# 3. Add btnCopyCfLink listener
old_btn = """      if (this.btnInfoCloudflare) {
        this.btnInfoCloudflare.addEventListener('click', () => {
          this.showToast("start_public_tunnel.bat faylini bosing — bepul HTTPS beradi! 🌐");
        });
      }"""

new_btn = """      if (this.btnCopyCfLink) {
        this.btnCopyCfLink.addEventListener('click', () => {
          const url = (this.phoneModalCfLink && this.phoneModalCfLink.href && this.phoneModalCfLink.href !== '#') 
            ? this.phoneModalCfLink.href 
            : (this.networkInfoData ? this.networkInfoData.public_tunnel_url : '');
          if (url) {
            navigator.clipboard.writeText(url).then(() => {
              this.showToast("Dunyo bo'ylab global HTTPS havola nusxalandi! 🌐");
            }).catch(() => {
              this.showToast(url);
            });
          }
        });
      }"""

if old_btn in code:
    code = code.replace(old_btn, new_btn)
    print("btnCopyCfLink handler added")

with open(app_path, "w", encoding="utf-8") as f:
    f.write(code)
print("app.js updated successfully!")
