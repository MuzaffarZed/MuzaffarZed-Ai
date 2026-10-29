# -*- coding: utf-8 -*-

app_js_path = r"C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js"
with open(app_js_path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update API_BASE
old_api_base = 'const API_BASE = "http://localhost:8000";'
new_api_base = 'const API_BASE = (window.location.origin && window.location.origin.startsWith("http")) ? window.location.origin : "http://localhost:8000";'

if old_api_base in code:
    code = code.replace(old_api_base, new_api_base)
    print("API_BASE updated to dynamic origin")
else:
    print("API_BASE already updated or not found")

# 2. Add to cacheDom()
dom_target = 'this.btnInstallPwa = document.getElementById(\'btn-install-pwa\');'
new_dom = """this.btnConnectPhone = document.getElementById('btn-connect-phone');
      this.menuConnectPhone = document.getElementById('menu-connect-phone');
      this.connectPhoneModal = document.getElementById('connect-phone-modal');
      this.btnClosePhoneModal = document.getElementById('btn-close-phone-modal');
      this.phoneModalQrImg = document.getElementById('phone-modal-qr-img');
      this.phoneModalIpLink = document.getElementById('phone-modal-ip-link');
      this.phoneModalMdnsLink = document.getElementById('phone-modal-mdns-link');
      this.btnCopyIpLink = document.getElementById('btn-copy-ip-link');
      this.btnCopyMdnsLink = document.getElementById('btn-copy-mdns-link');
      this.btnInfoCloudflare = document.getElementById('btn-info-cloudflare');
      this.networkInfoData = null;

      """
if 'btnConnectPhone' not in code:
    code = code.replace(dom_target, new_dom + dom_target)
    print("Added phone connect DOM references in cacheDom")
else:
    print("btnConnectPhone already in cacheDom")

# 3. Add to bindEvents()
bind_target = 'this.initShortsSoundModalEvents();'
new_bind = """this.initShortsSoundModalEvents();
      this.initPhoneConnect();"""
if 'this.initPhoneConnect();' not in code:
    code = code.replace(bind_target, new_bind)
    print("Added this.initPhoneConnect() to bindEvents")
else:
    print("initPhoneConnect already in bindEvents")

# 4. Add to Escape key listener
esc_target = 'if (this.voiceSearchModal) this.voiceSearchModal.classList.remove(\'open\');'
new_esc = """if (this.voiceSearchModal) this.voiceSearchModal.classList.remove('open');
          if (this.connectPhoneModal) this.connectPhoneModal.classList.remove('open');"""
if 'if (this.connectPhoneModal) this.connectPhoneModal.classList.remove(\'open\');' not in code:
    code = code.replace(esc_target, new_esc)
    print("Added Escape key dismiss for connectPhoneModal")
else:
    print("Escape key dismiss for connectPhoneModal already present")

# 5. Add method initPhoneConnect() before the end of YouTubeApp class
method_marker = '    initPlayerWheelVolume() {'
phone_method = """    initPhoneConnect() {
      const fetchNetworkInfo = async () => {
        try {
          const res = await fetch(`${API_BASE}/api/network-info`);
          if (res.ok) {
            this.networkInfoData = await res.json();
            if (this.phoneModalIpLink && this.networkInfoData.local_url) {
              this.phoneModalIpLink.textContent = this.networkInfoData.local_url;
              this.phoneModalIpLink.href = this.networkInfoData.local_url;
            }
            if (this.phoneModalMdnsLink && this.networkInfoData.mdns_url) {
              this.phoneModalMdnsLink.textContent = this.networkInfoData.mdns_url;
              this.phoneModalMdnsLink.href = this.networkInfoData.mdns_url;
            }
            if (this.phoneModalQrImg && this.networkInfoData.local_url) {
              this.phoneModalQrImg.src = `https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=${encodeURIComponent(this.networkInfoData.local_url)}`;
            }
          }
        } catch (err) {
          console.warn("[Network Info] Fetch failed:", err);
        }
      };

      fetchNetworkInfo();

      const openModal = async () => {
        if (!this.networkInfoData) await fetchNetworkInfo();
        if (this.userProfileDropdown) this.userProfileDropdown.style.display = 'none';
        if (this.connectPhoneModal) {
          this.connectPhoneModal.classList.add('open');
          this.refreshIcons();
        }
      };

      const closeModal = () => {
        if (this.connectPhoneModal) this.connectPhoneModal.classList.remove('open');
      };

      if (this.btnConnectPhone) {
        this.btnConnectPhone.addEventListener('click', (e) => {
          e.stopPropagation();
          openModal();
        });
      }

      if (this.menuConnectPhone) {
        this.menuConnectPhone.addEventListener('click', (e) => {
          e.stopPropagation();
          openModal();
        });
      }

      if (this.btnClosePhoneModal) {
        this.btnClosePhoneModal.addEventListener('click', closeModal);
      }

      if (this.connectPhoneModal) {
        this.connectPhoneModal.addEventListener('click', (e) => {
          if (e.target === this.connectPhoneModal) closeModal();
        });
      }

      if (this.btnCopyIpLink) {
        this.btnCopyIpLink.addEventListener('click', () => {
          const url = (this.phoneModalIpLink && this.phoneModalIpLink.href) ? this.phoneModalIpLink.href : '';
          if (url) {
            navigator.clipboard.writeText(url).then(() => {
              this.showToast("Wi-Fi IP manzili buferga nusxalandi! 📋");
            }).catch(() => {
              this.showToast(url);
            });
          }
        });
      }

      if (this.btnCopyMdnsLink) {
        this.btnCopyMdnsLink.addEventListener('click', () => {
          const url = (this.phoneModalMdnsLink && this.phoneModalMdnsLink.href) ? this.phoneModalMdnsLink.href : '';
          if (url) {
            navigator.clipboard.writeText(url).then(() => {
              this.showToast("mDNS manzili buferga nusxalandi! 📋");
            }).catch(() => {
              this.showToast(url);
            });
          }
        });
      }

      if (this.btnInfoCloudflare) {
        this.btnInfoCloudflare.addEventListener('click', () => {
          this.showToast("start_public_tunnel.bat faylini bosing — bepul HTTPS beradi! 🌐");
        });
      }
    }

"""
if 'initPhoneConnect() {' not in code:
    code = code.replace(method_marker, phone_method + method_marker)
    print("Added initPhoneConnect() method to YouTubeApp")
else:
    print("initPhoneConnect() method already present")

with open(app_js_path, "w", encoding="utf-8") as f:
    f.write(code)
print("app.js updated successfully!")
