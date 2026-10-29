with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'r', encoding='utf-8') as f:
    code = f.read()

new_v4_methods = """
    // ------------------------------------------------------------------------
    // PRESS-AND-HOLD FOR 2X SPEED (YOUTUBE 2026 SIGNATURE)
    // ------------------------------------------------------------------------
    init2xSpeedHold() {
      if (!this.playerContainer || !this.videoElement) return;

      this.is2xActive = false;
      this.savedPlaybackRate = 1.0;
      this.holdTimer = null;

      const startHold = (e) => {
        if (e.target.closest('.yt-player-controls') || e.target.closest('.yt-dropdown-menu') || e.target.closest('.yt-modal-card')) {
          return;
        }
        if (this.videoElement.paused) return;

        this.savedPlaybackRate = this.videoElement.playbackRate || 1.0;
        clearTimeout(this.holdTimer);
        this.holdTimer = setTimeout(() => {
          if (!this.videoElement.paused) {
            this.is2xActive = true;
            this.videoElement.playbackRate = 2.0;
            if (this.speed2xPill) this.speed2xPill.classList.add('show');
          }
        }, 320);
      };

      const endHold = () => {
        clearTimeout(this.holdTimer);
        if (this.is2xActive) {
          this.is2xActive = false;
          this.videoElement.playbackRate = this.savedPlaybackRate || 1.0;
          if (this.speed2xPill) this.speed2xPill.classList.remove('show');
        }
      };

      this.playerContainer.addEventListener('mousedown', startHold);
      this.playerContainer.addEventListener('mouseup', endHold);
      this.playerContainer.addEventListener('mouseleave', endHold);

      this.playerContainer.addEventListener('touchstart', startHold, { passive: true });
      this.playerContainer.addEventListener('touchend', endHold);
      this.playerContainer.addEventListener('touchcancel', endHold);
    }

    // ------------------------------------------------------------------------
    // NOTIFICATIONS CENTER
    // ------------------------------------------------------------------------
    initNotificationsEvents() {
      if (this.btnNotifications && this.notificationsDropdown) {
        this.btnNotifications.addEventListener('click', (e) => {
          e.stopPropagation();
          const isShown = this.notificationsDropdown.style.display === 'flex';
          this.notificationsDropdown.style.display = isShown ? 'none' : 'flex';
          if (this.userProfileDropdown) this.userProfileDropdown.style.display = 'none';

          const redDot = this.btnNotifications.querySelector('span');
          if (redDot) redDot.style.display = 'none';
          this.refreshIcons();
        });
      }

      if (this.btnCloseNotif) {
        this.btnCloseNotif.addEventListener('click', () => {
          if (this.notificationsDropdown) this.notificationsDropdown.style.display = 'none';
        });
      }

      if (this.notificationsDropdown) {
        this.notificationsDropdown.querySelectorAll('.yt-notif-item').forEach(item => {
          item.addEventListener('click', () => {
            const vidId = item.getAttribute('data-vid');
            item.classList.remove('unread');
            const found = this.videos.find(v => v.id === vidId);
            if (found) {
              this.openWatch(found);
            }
            this.notificationsDropdown.style.display = 'none';
          });
        });
      }

      document.addEventListener('click', (e) => {
        if (this.notificationsDropdown && !this.notificationsDropdown.contains(e.target) && !this.btnNotifications.contains(e.target)) {
          this.notificationsDropdown.style.display = 'none';
        }
      });
    }

    // ------------------------------------------------------------------------
    // USER PROFILE / ACCOUNT MENU CARD
    // ------------------------------------------------------------------------
    initUserProfileEvents() {
      if (this.userProfileTrigger && this.userProfileDropdown) {
        this.userProfileTrigger.addEventListener('click', (e) => {
          e.stopPropagation();
          const isShown = this.userProfileDropdown.style.display === 'flex';
          this.userProfileDropdown.style.display = isShown ? 'none' : 'flex';
          if (this.notificationsDropdown) this.notificationsDropdown.style.display = 'none';
          this.refreshIcons();
        });
      }

      const menuMyChannel = document.getElementById('menu-my-channel');
      if (menuMyChannel) {
        menuMyChannel.addEventListener('click', () => {
          this.openChannelPage('ch-muzaffarzed');
          this.userProfileDropdown.style.display = 'none';
        });
      }

      const menuStudio = document.getElementById('menu-studio');
      if (menuStudio) {
        menuStudio.addEventListener('click', () => {
          this.uploadModal.classList.add('open');
          this.userProfileDropdown.style.display = 'none';
        });
      }

      const menuPremiumPerks = document.getElementById('menu-premium-perks');
      if (menuPremiumPerks) {
        menuPremiumPerks.addEventListener('click', () => {
          this.showToast("💎 YouTube Pro Premium: 0 Reklama, 4K UHD va 300% Boost cheksiz faol!");
          this.userProfileDropdown.style.display = 'none';
        });
      }

      const menuSwitchTheme = document.getElementById('menu-switch-theme');
      if (menuSwitchTheme) {
        menuSwitchTheme.addEventListener('click', () => {
          this.btnToggleTheme.click();
          this.userProfileDropdown.style.display = 'none';
        });
      }

      const menuSwitchLang = document.getElementById('menu-switch-lang');
      if (menuSwitchLang) {
        menuSwitchLang.addEventListener('click', () => {
          this.btnToggleLang.click();
          this.userProfileDropdown.style.display = 'none';
        });
      }

      const menuShortcuts = document.getElementById('menu-shortcuts');
      if (menuShortcuts) {
        menuShortcuts.addEventListener('click', () => {
          this.shortcutsModal.classList.add('open');
          this.userProfileDropdown.style.display = 'none';
        });
      }

      const menuSignout = document.getElementById('menu-signout');
      if (menuSignout) {
        menuSignout.addEventListener('click', () => {
          this.showToast("MuzaffarZed hisobi tizimda xavfsiz qoldi.");
          this.userProfileDropdown.style.display = 'none';
        });
      }

      document.addEventListener('click', (e) => {
        if (this.userProfileDropdown && !this.userProfileDropdown.contains(e.target) && !this.userProfileTrigger.contains(e.target)) {
          this.userProfileDropdown.style.display = 'none';
        }
      });
    }

    // ------------------------------------------------------------------------
    // GLOBAL KEYBOARD SHORTCUTS (?)
    // ------------------------------------------------------------------------
    initKeyboardShortcutsGlobal() {
      document.addEventListener('keydown', (e) => {
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
        if (e.key === '?' || (e.shiftKey && e.key === '/')) {
          e.preventDefault();
          if (this.shortcutsModal) {
            this.shortcutsModal.classList.toggle('open');
          }
        }
      });
    }
"""

fn_marker = "formatNumber(num) {"
pos = code.find(fn_marker)
if pos != -1 and "init2xSpeedHold() {" not in code:
    code = code[:pos] + new_v4_methods + "\n    " + code[pos:]
    print("Injected v4 method definitions!")

with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Saved app.js!")
