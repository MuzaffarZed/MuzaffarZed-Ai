with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. cacheDom additions
cache_anchor = "this.btnManageSubsPage = document.getElementById('btn-manage-subs-page');"
cache_new = """this.btnManageSubsPage = document.getElementById('btn-manage-subs-page');

      // V6 Components: Subtitles Menu, Channel Tabs & Search, History Search, Sound Modal
      this.subtitlesLangMenu = document.getElementById('subtitles-lang-menu');
      this.tabChannelShorts = document.getElementById('tab-channel-shorts');
      this.tabChannelPlaylists = document.getElementById('tab-channel-playlists');
      this.channelSearchInput = document.getElementById('channel-search-input');
      this.channelAboutSection = document.getElementById('channel-about-section');
      this.historySearchInput = document.getElementById('history-search-input');
      this.btnPauseHistory = document.getElementById('btn-pause-history');
      this.pauseHistoryLabel = document.getElementById('pause-history-label');
      this.shortsSoundModal = document.getElementById('shorts-sound-modal');
      this.btnCloseSoundModal = document.getElementById('btn-close-sound-modal');
      this.soundModalTitle = document.getElementById('sound-modal-title');
      this.soundModalAuthor = document.getElementById('sound-modal-author');
      this.btnUseSound = document.getElementById('btn-use-sound');"""

if cache_anchor in code and "this.subtitlesLangMenu" not in code:
    code = code.replace(cache_anchor, cache_new, 1)
    print("Added v6 elements to cacheDom!")

# 2. bindEvents calls
bind_anchor = "this.initRecentSearches();"
bind_new = """this.initRecentSearches();
      this.initSubtitlesMenuEvents();
      this.initChannelPageEvents();
      this.initHistoryPageEvents();
      this.initShortsSoundModalEvents();"""

if bind_anchor in code and "this.initSubtitlesMenuEvents()" not in code:
    code = code.replace(bind_anchor, bind_new, 1)
    print("Added v6 calls to bindEvents!")

# 3. Upgrade openChannelPage
old_open_channel = """    openChannelPage(channel) {
      this.currentChannel = channel;
      this.switchView('channel');

      this.channelPageAvatar.src = channel.avatar;
      this.channelPageTitle.textContent = channel.name;
      this.channelPageMeta.textContent = `@${channel.name.toLowerCase().replace(/\\s+/g, '')} ? ${channel.subscribers || '1.2M obunachi'} ? MuzaffarZed Verified`;
      
      const isSub = this.subscribedChannels.has(channel.id);
      this.btnChannelPageSub.textContent = isSub ? "Obuna bo'lindi" : "Obuna bo'lish";
      this.btnChannelPageSub.className = `yt-subscribe-btn ${isSub ? 'subscribed' : ''}`;

      const channelVideos = this.videos.filter(v => v.channel.name === channel.name || v.channel.id === channel.id);
      this.channelVideosGrid.innerHTML = '';
      if (channelVideos.length === 0) {
        this.channelVideosGrid.innerHTML = '<p style="color: var(--yt-text-secondary); padding: 40px;">Bu kanalda hali videolar yo\\'q.</p>';
      } else {
        channelVideos.forEach(v => {
          const card = document.createElement('div');
          card.className = 'yt-card';
          card.innerHTML = `
            <div class="yt-thumbnail-wrapper">
              <img src="${v.thumbnail}" class="yt-thumbnail-img" alt="${v.title}">
              <span class="yt-duration-badge">${v.duration}</span>
            </div>
            <div class="yt-card-details">
              <div class="yt-card-meta">
                <h3 class="yt-card-title">${v.title}</h3>
                <div class="yt-card-views">${v.views} • ${v.timestamp}</div>
              </div>
            </div>
          `;
          card.addEventListener('click', () => this.openWatch(v));
          this.channelVideosGrid.appendChild(card);
        });
      }
      this.refreshIcons();
    }"""

# Let's inspect exact text of openChannelPage to make sure it matches
idx_ch = code.find("openChannelPage(channel) {")
end_ch = code.find("openHistoryView() {", idx_ch)
if idx_ch != -1 and end_ch != -1:
    print("Found exact openChannelPage block!")
    new_open_channel = """openChannelPage(channel) {
      if (typeof channel === 'string') {
        const foundVid = this.videos.find(v => v.channel && (v.channel.id === channel || v.channel.name.toLowerCase().includes(channel.toLowerCase())));
        if (foundVid) channel = foundVid.channel;
        else channel = { id: channel, name: "MuzaffarZed Tech", avatar: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80", subscribers: "1.4M obunachi" };
      }

      this.currentChannel = channel;
      this.switchView('channel');

      if (this.channelAboutSection) this.channelAboutSection.style.display = 'none';
      if (this.channelVideosGrid) this.channelVideosGrid.style.display = 'grid';

      this.channelPageAvatar.src = channel.avatar;
      this.channelPageTitle.textContent = channel.name;
      this.channelPageMeta.textContent = `@${channel.name.toLowerCase().replace(/\\s+/g, '')} • ${channel.subscribers || '1.2M obunachi'} • MuzaffarZed Verified`;
      
      const isSub = this.subscribedChannels.has(channel.id);
      this.btnChannelPageSub.textContent = isSub ? "Obuna bo'lindi" : "Obuna bo'lish";
      this.btnChannelPageSub.className = `yt-subscribe-btn ${isSub ? 'subscribed' : ''}`;

      const channelVideos = this.videos.filter(v => v.channel && (v.channel.name === channel.name || v.channel.id === channel.id));
      this.renderChannelVideosList(channelVideos);
      this.refreshIcons();
    }

    renderChannelVideosList(videos) {
      this.channelVideosGrid.innerHTML = '';
      if (videos.length === 0) {
        this.channelVideosGrid.innerHTML = '<p style="color: var(--yt-text-secondary); padding: 40px;">Bu kanalda hali videolar yo\\'q.</p>';
      } else {
        videos.forEach(v => {
          const card = document.createElement('div');
          card.className = 'yt-card';
          card.innerHTML = `
            <div class="yt-thumbnail-wrapper">
              <img src="${v.thumbnail}" class="yt-thumbnail-img" alt="${v.title}">
              <span class="yt-duration-badge">${v.duration}</span>
            </div>
            <div class="yt-card-details">
              <div class="yt-card-meta">
                <h3 class="yt-card-title">${v.title}</h3>
                <div class="yt-card-views">${v.views} • ${v.timestamp}</div>
              </div>
            </div>
          `;
          card.addEventListener('click', () => this.openWatch(v));
          this.channelVideosGrid.appendChild(card);
        });
      }
    }

    """
    code = code[:idx_ch] + new_open_channel + code[end_ch:]
    print("Replaced openChannelPage with enhanced version!")

# 4. Upgrade openHistoryView to support remove item button and pause state
idx_hist = code.find("openHistoryView() {")
end_hist = code.find("setSleepTimer(", idx_hist)
if idx_hist != -1 and end_hist != -1:
    new_open_history = """openHistoryView() {
      this.switchView('history');
      this.renderHistoryList();
    }

    renderHistoryList(filterQuery = '') {
      const historyIds = this.watchHistory;
      let historyVideos = historyIds.map(id => this.videos.find(v => v.id === id)).filter(Boolean);

      if (filterQuery) {
        const q = filterQuery.toLowerCase();
        historyVideos = historyVideos.filter(v => v.title.toLowerCase().includes(q) || v.channel.name.toLowerCase().includes(q));
      }

      this.historyVideosGrid.innerHTML = '';
      if (historyVideos.length === 0) {
        this.historyVideosGrid.innerHTML = '<p style="color: var(--yt-text-secondary); padding: 40px;">Ko\\'rishlar tarixi bo\\'sh.</p>';
      } else {
        historyVideos.forEach(v => {
          const card = document.createElement('div');
          card.className = 'yt-card';
          card.style.position = 'relative';
          card.innerHTML = `
            <div class="yt-thumbnail-wrapper">
              <img src="${v.thumbnail}" class="yt-thumbnail-img" alt="${v.title}">
              <span class="yt-duration-badge">${v.duration}</span>
              <button class="yt-history-card-remove" title="Tarixdan o'chirish">✕</button>
            </div>
            <div class="yt-card-details">
              <div class="yt-card-meta">
                <h3 class="yt-card-title">${v.title}</h3>
                <div class="yt-card-channel-name">${v.channel.name}</div>
                <div class="yt-card-views">${v.views} • ${v.timestamp}</div>
              </div>
            </div>
          `;

          const removeBtn = card.querySelector('.yt-history-card-remove');
          removeBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.watchHistory = this.watchHistory.filter(id => id !== v.id);
            localStorage.setItem('yt_history', JSON.stringify(this.watchHistory));
            card.remove();
            this.showToast("Video tarixdan o'chirildi!");
          });

          card.addEventListener('click', () => this.openWatch(v));
          this.historyVideosGrid.appendChild(card);
        });
      }
      this.refreshIcons();
    }

    """
    code = code[:idx_hist] + new_open_history + code[end_hist:]
    print("Replaced openHistoryView with enhanced filter and remove buttons!")

# 5. Methods to inject before formatNumber
v6_methods = """
    // ------------------------------------------------------------------------
    // SUBTITLES LANGUAGE SELECTOR & REAL-TIME TRANSLATION
    // ------------------------------------------------------------------------
    initSubtitlesMenuEvents() {
      if (this.btnCcToggle && this.subtitlesLangMenu) {
        this.btnCcToggle.addEventListener('contextmenu', (e) => {
          e.preventDefault();
          this.subtitlesLangMenu.style.display = this.subtitlesLangMenu.style.display === 'block' ? 'none' : 'block';
        });

        this.subtitlesLangMenu.querySelectorAll('.yt-dropdown-item').forEach(item => {
          item.addEventListener('click', () => {
            const lang = item.getAttribute('data-sublang');
            this.subtitlesLangMenu.style.display = 'none';

            if (lang === 'off') {
              this.ccActive = false;
              this.subtitlesOverlay.style.display = 'none';
              this.btnCcToggle.style.color = '#fff';
              this.showToast("Subtitrlar o'chirildi");
            } else {
              this.ccActive = true;
              this.subtitlesOverlay.style.display = 'block';
              this.btnCcToggle.style.color = 'var(--yt-blue)';
              
              const langLabels = { uz: "O'zbekcha", en: "English", ru: "Русский", tr: "Türkçe" };
              const langCaptions = {
                uz: "MuzaffarZed Engine: Zamonaviy sun'iy intellekt arxitekturasi va neyron tarmoqlar tahlili...",
                en: "MuzaffarZed Engine: Modern artificial intelligence architecture and deep neural networks analysis...",
                ru: "MuzaffarZed Engine: Архитектура современного искусственного интеллекта и нейронных сетей...",
                tr: "MuzaffarZed Engine: Modern yapay zeka mimarisi ve sinir aglari analizi..."
              };

              if (this.subtitlesText) {
                this.subtitlesText.textContent = langCaptions[lang] || langCaptions['uz'];
              }
              this.showToast(`Subtitr tili: ${langLabels[lang] || lang}`);
            }
          });
        });
      }
    }

    // ------------------------------------------------------------------------
    // CHANNEL PAGE TABS & SEARCH
    // ------------------------------------------------------------------------
    initChannelPageEvents() {
      if (this.tabChannelShorts) {
        this.tabChannelShorts.addEventListener('click', () => {
          document.querySelectorAll('.yt-channel-tab').forEach(t => t.classList.remove('active'));
          this.tabChannelShorts.classList.add('active');
          if (this.channelAboutSection) this.channelAboutSection.style.display = 'none';
          if (this.channelVideosGrid) {
            this.channelVideosGrid.style.display = 'grid';
            this.channelVideosGrid.innerHTML = '';
            this.shorts.forEach(s => {
              const card = document.createElement('div');
              card.className = 'yt-card';
              card.innerHTML = `
                <div class="yt-thumbnail-wrapper" style="aspect-ratio: 9/16; border-radius: 12px; overflow: hidden;">
                  <img src="${s.avatar}" style="width: 100%; height: 100%; object-fit: cover;">
                  <span class="yt-duration-badge" style="background: var(--yt-red);">SHORTS</span>
                </div>
                <div class="yt-card-details">
                  <h4 style="font-size: 13px; font-weight: 600; margin-top: 6px;">${s.title}</h4>
                </div>
              `;
              card.addEventListener('click', () => {
                this.switchView('shorts');
              });
              this.channelVideosGrid.appendChild(card);
            });
          }
        });
      }

      if (this.tabChannelPlaylists) {
        this.tabChannelPlaylists.addEventListener('click', () => {
          document.querySelectorAll('.yt-channel-tab').forEach(t => t.classList.remove('active'));
          this.tabChannelPlaylists.classList.add('active');
          if (this.channelAboutSection) this.channelAboutSection.style.display = 'none';
          if (this.channelVideosGrid) {
            this.channelVideosGrid.style.display = 'grid';
            this.channelVideosGrid.innerHTML = `
              <div class="yt-card" style="cursor: pointer;" id="channel-playlist-card-demo">
                <div class="yt-thumbnail-wrapper" style="background: linear-gradient(135deg, #1e3a8a, #000); display: flex; align-items: center; justify-content: center; height: 160px; border-radius: 12px;">
                  <i data-lucide="list-music" style="width: 48px; height: 48px; color: white;"></i>
                </div>
                <h4 style="font-size: 14px; font-weight: 700; margin-top: 8px;">Barcha Masterklasslar Playlisti</h4>
                <div style="font-size: 12px; color: var(--yt-text-secondary);">12 ta video • Yangilangan</div>
              </div>
            `;
            this.refreshIcons();
            const card = document.getElementById('channel-playlist-card-demo');
            if (card) card.addEventListener('click', () => this.openPlaylistView('pl-masterclass'));
          }
        });
      }

      const tabAbout = document.getElementById('tab-channel-about');
      if (tabAbout) {
        tabAbout.addEventListener('click', () => {
          document.querySelectorAll('.yt-channel-tab').forEach(t => t.classList.remove('active'));
          tabAbout.classList.add('active');
          if (this.channelVideosGrid) this.channelVideosGrid.style.display = 'none';
          if (this.channelAboutSection) this.channelAboutSection.style.display = 'block';
        });
      }

      const tabVideos = document.getElementById('tab-channel-videos');
      if (tabVideos) {
        tabVideos.addEventListener('click', () => {
          document.querySelectorAll('.yt-channel-tab').forEach(t => t.classList.remove('active'));
          tabVideos.classList.add('active');
          if (this.channelAboutSection) this.channelAboutSection.style.display = 'none';
          if (this.channelVideosGrid) {
            this.channelVideosGrid.style.display = 'grid';
            if (this.currentChannel) {
              const vids = this.videos.filter(v => v.channel && (v.channel.name === this.currentChannel.name || v.channel.id === this.currentChannel.id));
              this.renderChannelVideosList(vids);
            }
          }
        });
      }

      if (this.channelSearchInput) {
        this.channelSearchInput.addEventListener('input', (e) => {
          const q = e.target.value.toLowerCase().trim();
          if (this.currentChannel) {
            let vids = this.videos.filter(v => v.channel && (v.channel.name === this.currentChannel.name || v.channel.id === this.currentChannel.id));
            if (q) vids = vids.filter(v => v.title.toLowerCase().includes(q));
            this.renderChannelVideosList(vids);
          }
        });
      }
    }

    // ------------------------------------------------------------------------
    // HISTORY PAGE SEARCH & PAUSE
    // ------------------------------------------------------------------------
    initHistoryPageEvents() {
      if (this.historySearchInput) {
        this.historySearchInput.addEventListener('input', (e) => {
          this.renderHistoryList(e.target.value.trim());
        });
      }

      if (this.btnPauseHistory) {
        this.historyPaused = false;
        this.btnPauseHistory.addEventListener('click', () => {
          this.historyPaused = !this.historyPaused;
          if (this.pauseHistoryLabel) {
            this.pauseHistoryLabel.textContent = this.historyPaused ? "Tarixni yoqish" : "Tarixni pauzalash";
          }
          this.showToast(this.historyPaused ? "Ko'rishlar tarixi pauza qilindi" : "Ko'rishlar tarixi davom ettirilmoqda");
        });
      }
    }

    // ------------------------------------------------------------------------
    // SHORTS SOUND MODAL
    // ------------------------------------------------------------------------
    initShortsSoundModalEvents() {
      if (this.btnCloseSoundModal) {
        this.btnCloseSoundModal.addEventListener('click', () => {
          if (this.shortsSoundModal) this.shortsSoundModal.classList.remove('open');
        });
      }

      if (this.btnUseSound) {
        this.btnUseSound.addEventListener('click', () => {
          if (this.shortsSoundModal) this.shortsSoundModal.classList.remove('open');
          this.uploadModal.classList.add('open');
          this.showToast("Audio tanlandi! Yangi Short rolik yuklashingiz mumkin.");
        });
      }
    }

    openShortsSoundModal(soundName, authorName) {
      if (!this.shortsSoundModal) return;
      if (this.soundModalTitle) this.soundModalTitle.textContent = soundName || "Original Audio";
      if (this.soundModalAuthor) this.soundModalAuthor.textContent = authorName || "MuzaffarZed Studio";
      this.shortsSoundModal.classList.add('open');
      this.refreshIcons();
    }
"""

pos_fn = code.find("formatNumber(num) {")
if pos_fn != -1 and "initSubtitlesMenuEvents() {" not in code:
    code = code[:pos_fn] + v6_methods + "\n    " + code[pos_fn:]
    print("Injected v6 methods before formatNumber!")

# 6. Wire sound tag in renderShorts to open sound modal
old_sound_markup = """            <div style="display: flex; align-items: center; gap: 6px; font-size: 12px; color: #ccc;">
              <i data-lucide="music" style="width: 14px; height: 14px;"></i>
              <span>${s.sound || 'Original Audio'}</span>
            </div>"""

new_sound_markup = """            <div class="yt-short-sound-tag" style="display: flex; align-items: center; gap: 6px; font-size: 12px; color: #ccc; cursor: pointer;">
              <i data-lucide="music" style="width: 14px; height: 14px; color: var(--yt-blue);"></i>
              <span>${s.sound || 'Original Audio'}</span>
            </div>"""

if old_sound_markup in code and "yt-short-sound-tag" not in code:
    code = code.replace(old_sound_markup, new_sound_markup, 1)
    print("Added sound tag class in renderShorts!")

old_sound_wire = """const soundBtn = reel.querySelector('.btn-short-sound');"""
new_sound_wire = """const soundTag = reel.querySelector('.yt-short-sound-tag');
        if (soundTag) {
          soundTag.addEventListener('click', (e) => {
            e.stopPropagation();
            this.openShortsSoundModal(s.sound, s.channel);
          });
        }
        const soundBtn = reel.querySelector('.btn-short-sound');"""

if old_sound_wire in code and "soundTag" not in code:
    code = code.replace(old_sound_wire, new_sound_wire, 1)
    print("Wired sound tag click in renderShorts!")

with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("patch_app_v6.py complete!")
