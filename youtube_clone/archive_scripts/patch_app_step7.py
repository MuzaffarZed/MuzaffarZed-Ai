with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'r', encoding='utf-8') as f:
    c = f.read().replace('\r\n', '\n')

# 1. Update renderVideos card.innerHTML and event listeners
target_render = """      videos.forEach(video => {
        const card = document.createElement('div');
        card.className = 'yt-card';
        card.innerHTML = `
          <div class="yt-thumbnail-wrapper">
            <img src="${video.thumbnail}" class="yt-thumbnail-img" alt="${video.title}">
            <span class="yt-duration-badge">${video.duration}</span>
          </div>
          <div class="yt-card-info">
            <img src="${video.channel.avatar}" class="yt-channel-avatar" alt="${video.channel.name}">
            <div class="yt-card-details">
              <h3 class="yt-card-title">${video.title}</h3>
              <div class="yt-card-channel-name">${video.channel.name}</div>
              <div class="yt-card-meta">${video.views} • ${video.timestamp}</div>
            </div>
          </div>
        `;
        card.querySelector('.yt-thumbnail-wrapper').addEventListener('click', () => this.openWatch(video));
        card.querySelector('.yt-card-title').addEventListener('click', () => this.openWatch(video));
        card.querySelector('.yt-channel-avatar').addEventListener('click', (e) => {
          e.stopPropagation();
          this.openChannelPage(video.channel);
        });
        card.querySelector('.yt-card-channel-name').addEventListener('click', (e) => {
          e.stopPropagation();
          this.openChannelPage(video.channel);
        });"""

replacement_render = """      videos.forEach(video => {
        const card = document.createElement('div');
        card.className = 'yt-card';
        card.innerHTML = `
          <div class="yt-thumbnail-wrapper">
            <img src="${video.thumbnail}" class="yt-thumbnail-img" alt="${video.title}">
            <span class="yt-duration-badge">${video.duration}</span>
            <div class="yt-thumb-quick-actions">
              <button class="yt-thumb-quick-btn btn-quick-watch-later" title="Keyinroq ko'rish">
                <i data-lucide="clock" style="width: 16px; height: 16px;"></i>
              </button>
            </div>
          </div>
          <div class="yt-card-info">
            <img src="${video.channel.avatar}" class="yt-channel-avatar" alt="${video.channel.name}">
            <div class="yt-card-details">
              <h3 class="yt-card-title">${video.title}</h3>
              <div class="yt-card-channel-name">${video.channel.name}</div>
              <div class="yt-card-meta">${video.views} • ${video.timestamp}</div>
            </div>
            <button class="yt-card-more-btn" title="Harakatlar">
              <i data-lucide="more-vertical" style="width: 18px; height: 18px;"></i>
            </button>
          </div>
        `;
        card.querySelector('.yt-thumbnail-wrapper').addEventListener('click', () => this.openWatch(video));
        card.querySelector('.yt-card-title').addEventListener('click', () => this.openWatch(video));
        card.querySelector('.yt-channel-avatar').addEventListener('click', (e) => {
          e.stopPropagation();
          this.openChannelPage(video.channel);
        });
        card.querySelector('.yt-card-channel-name').addEventListener('click', (e) => {
          e.stopPropagation();
          this.openChannelPage(video.channel);
        });
        const quickWl = card.querySelector('.btn-quick-watch-later');
        if (quickWl) {
          quickWl.addEventListener('click', (e) => {
            e.stopPropagation();
            this.addToWatchLater(video);
          });
        }
        const moreBtn = card.querySelector('.yt-card-more-btn');
        if (moreBtn) {
          moreBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.openCardContextMenu(e, video, card);
          });
        }"""

if target_render in c:
    c = c.replace(target_render, replacement_render)
    print("SUCCESS: renderVideos replaced!")
else:
    print("FAILED: target_render not found")

# 2. Add methods for card context menu, watch later, and network watcher
methods_to_add = """
    // ------------------------------------------------------------------------
    // VIDEO CARD CONTEXT MENU & QUICK ACTIONS
    // ------------------------------------------------------------------------
    initCardContextMenu() {
      this.cardContextMenu = document.getElementById('card-context-menu');
      this.currentContextVideo = null;
      this.currentContextCard = null;

      if (!this.cardContextMenu) return;

      const btnWl = document.getElementById('card-ctx-watch-later');
      const btnPl = document.getElementById('card-ctx-playlist');
      const btnCopy = document.getElementById('card-ctx-copy-link');
      const btnHide = document.getElementById('card-ctx-hide');

      if (btnWl) {
        btnWl.addEventListener('click', () => {
          if (this.currentContextVideo) {
            this.addToWatchLater(this.currentContextVideo);
          }
          this.hideCardContextMenu();
        });
      }

      if (btnPl) {
        btnPl.addEventListener('click', () => {
          if (this.currentContextVideo) {
            this.currentVideo = this.currentContextVideo;
            this.openPlaylistModal();
          }
          this.hideCardContextMenu();
        });
      }

      if (btnCopy) {
        btnCopy.addEventListener('click', () => {
          if (this.currentContextVideo) {
            const url = `${window.location.origin}/?v=${this.currentContextVideo.id}`;
            navigator.clipboard.writeText(url).then(() => {
              this.showToast("Video havolasi nusxalandi!");
            });
          }
          this.hideCardContextMenu();
        });
      }

      if (btnHide) {
        btnHide.addEventListener('click', () => {
          if (this.currentContextCard) {
            this.currentContextCard.style.transition = 'all 0.3s cubic-bezier(0.16, 1, 0.3, 1)';
            this.currentContextCard.style.opacity = '0';
            this.currentContextCard.style.transform = 'scale(0.85)';
            setTimeout(() => this.currentContextCard.remove(), 300);
            this.showToast("Video tavsiyalardan olib tashlandi");
          }
          this.hideCardContextMenu();
        });
      }

      document.addEventListener('click', (e) => {
        if (this.cardContextMenu && this.cardContextMenu.style.display !== 'none') {
          if (!this.cardContextMenu.contains(e.target)) {
            this.hideCardContextMenu();
          }
        }
      });
    }

    openCardContextMenu(e, video, card) {
      if (!this.cardContextMenu) return;
      this.currentContextVideo = video;
      this.currentContextCard = card;

      const rect = e.currentTarget.getBoundingClientRect();
      let left = rect.left - 180;
      let top = rect.bottom + 6;

      if (left < 10) left = 10;
      if (top + 180 > window.innerHeight) top = rect.top - 180;

      this.cardContextMenu.style.left = `${left}px`;
      this.cardContextMenu.style.top = `${top}px`;
      this.cardContextMenu.style.display = 'block';
      this.refreshIcons();
    }

    hideCardContextMenu() {
      if (this.cardContextMenu) {
        this.cardContextMenu.style.display = 'none';
      }
    }

    async addToWatchLater(video) {
      if (!video) return;
      try {
        await fetch(`${API_BASE}/api/playlists/add`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            playlist_id: 'pl-watch-later',
            video_id: video.id,
            title: video.title,
            thumbnail: video.thumbnail
          })
        });
        this.showToast(`"${video.title.substring(0, 30)}..." Keyinroq ko'rishga qo'shildi!`);
      } catch (e) {
        this.showToast("Keyinroq ko'rishga saqlandi (Kesh)");
      }
    }

    // ------------------------------------------------------------------------
    // NETWORK CONNECTIVITY GUARDIAN (OFFLINE / ONLINE DETECTOR)
    // ------------------------------------------------------------------------
    initNetworkStatusWatcher() {
      this.networkStatusPill = document.getElementById('network-status-pill');
      this.netStatusText = document.getElementById('net-status-text');

      window.addEventListener('offline', () => {
        this.showNetworkPill(false, "Internet aloqasi uzildi — Oflayn rejimdasiz");
      });

      window.addEventListener('online', () => {
        this.showNetworkPill(true, "Internet aloqasi qayta tiklandi");
        setTimeout(() => {
          if (this.networkStatusPill) this.networkStatusPill.classList.remove('show');
        }, 3000);
      });
    }

    showNetworkPill(isOnline, message) {
      if (!this.networkStatusPill) return;
      this.networkStatusPill.className = `yt-network-status-pill ${isOnline ? 'online' : 'offline'} show`;
      if (this.netStatusText) this.netStatusText.textContent = message;
    }
"""

# Inject before initPlayerWheelVolume()
target_wheel = "    initPlayerWheelVolume() {"
if target_wheel in c:
    c = c.replace(target_wheel, methods_to_add + "\n    initPlayerWheelVolume() {")
    print("SUCCESS: methods injected!")
else:
    print("FAILED: target_wheel not found")

# 3. Call in bindEvents
target_bind = "      this.initPlayerWheelVolume();"
replacement_bind = """      this.initPlayerWheelVolume();
      this.initCardContextMenu();
      this.initNetworkStatusWatcher();"""

if target_bind in c:
    c = c.replace(target_bind, replacement_bind)
    print("SUCCESS: bindEvents hooked!")
else:
    print("FAILED: target_bind not found")

with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'w', encoding='utf-8') as f:
    f.write(c)
