with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. cacheDom additions
old_cache_dom_marker = "this.ctxPip = document.getElementById('ctx-pip');"
new_cache_dom_additions = """this.ctxPip = document.getElementById('ctx-pip');

      // 2x Speed Pill & Notifications & Profile
      this.speed2xPill = document.getElementById('speed-2x-pill');
      this.btnNotifications = document.getElementById('btn-notifications');
      this.notificationsDropdown = document.getElementById('notifications-dropdown');
      this.btnCloseNotif = document.getElementById('btn-close-notif');
      this.userProfileTrigger = document.getElementById('user-profile-menu-trigger');
      this.userProfileDropdown = document.getElementById('user-profile-dropdown');"""

if old_cache_dom_marker in code and "this.speed2xPill" not in code:
    code = code.replace(old_cache_dom_marker, new_cache_dom_additions, 1)
    print("Added v4 elements to cacheDom!")

# 2. bindEvents calls
old_bind_calls = "this.initPlayerWheelVolume();"
new_bind_calls = """this.initPlayerWheelVolume();
      this.init2xSpeedHold();
      this.initNotificationsEvents();
      this.initUserProfileEvents();
      this.initKeyboardShortcutsGlobal();"""

if old_bind_calls in code and "this.init2xSpeedHold()" not in code:
    code = code.replace(old_bind_calls, new_bind_calls, 1)
    print("Added v4 initialization calls to bindEvents!")

# 3. Add Shorts Progress Bar in renderShorts
old_reel_markup = """        reel.innerHTML = `
          ${mediaHtml}"""

new_reel_markup = """        reel.innerHTML = `
          ${mediaHtml}
          <div class="yt-short-progress"><div class="yt-short-progress-fill"></div></div>"""

if old_reel_markup in code and "yt-short-progress" not in code:
    code = code.replace(old_reel_markup, new_reel_markup, 1)
    print("Added Shorts progress bar markup!")

old_short_video_timeupdate = """        const video = reel.querySelector('video');
        if (video) {
          video.muted = true;"""

new_short_video_timeupdate = """        const video = reel.querySelector('video');
        if (video) {
          video.muted = true;
          const progFill = reel.querySelector('.yt-short-progress-fill');
          video.addEventListener('timeupdate', () => {
            if (video.duration && progFill) {
              progFill.style.width = ((video.currentTime / video.duration) * 100) + '%';
            }
          });"""

if old_short_video_timeupdate in code and "progFill" not in code:
    code = code.replace(old_short_video_timeupdate, new_short_video_timeupdate, 1)
    print("Wired Shorts progress bar live timeupdate!")

# 4. Methods to inject
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
        // Do not trigger if clicking controls or interactive buttons
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

          // Clear red dot on notification button
          const redDot = this.btnNotifications.querySelector('span');
          if (redDot) redDot.style.display = 'none';
        });
      }

      if (this.btnCloseNotif) {
        this.btnCloseNotif.addEventListener('click', () => {
          if (this.notificationsDropdown) this.notificationsDropdown.style.display = 'none';
        });
      }

      // Handle clicking notification item
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

# Inject new methods right before formatNumber
fn_marker = "formatNumber(num) {"
pos = code.find(fn_marker)
if pos != -1 and "init2xSpeedHold" not in code:
    code = code[:pos] + new_v4_methods + "\n    " + code[pos:]
    print("Injected v4 methods before formatNumber!")

with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("patch_app_v4.py completed!")
