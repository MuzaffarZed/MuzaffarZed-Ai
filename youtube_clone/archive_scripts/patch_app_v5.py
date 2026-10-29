with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. cacheDom
cache_anchor = "this.userProfileDropdown = document.getElementById('user-profile-dropdown');"
cache_new = """this.userProfileDropdown = document.getElementById('user-profile-dropdown');
      this.sleepTimerDropdown = document.getElementById('sleep-timer-dropdown');
      this.viewSubscriptions = document.getElementById('view-subscriptions');
      this.subsChannelsRow = document.getElementById('subs-channels-row');
      this.subsFilterChips = document.getElementById('subs-filter-chips');
      this.subsVideoGrid = document.getElementById('subs-video-grid');
      this.btnManageSubsPage = document.getElementById('btn-manage-subs-page');"""

if cache_anchor in code and "this.viewSubscriptions" not in code:
    code = code.replace(cache_anchor, cache_new, 1)
    print("Added Subscriptions & Sleep Timer to cacheDom!")

# 2. switchView
switch_anchor = "if (this.viewPlaylist) this.viewPlaylist.style.display = viewName === 'playlist' ? 'block' : 'none';"
switch_new = """if (this.viewPlaylist) this.viewPlaylist.style.display = viewName === 'playlist' ? 'block' : 'none';
      if (this.viewSubscriptions) this.viewSubscriptions.style.display = viewName === 'subscriptions' ? 'block' : 'none';"""

if switch_anchor in code and "this.viewSubscriptions.style.display" not in code:
    code = code.replace(switch_anchor, switch_new, 1)
    print("Updated switchView with subscriptions!")

# 3. Sidebar Nav for subscriptions
old_subs_nav = """} else if (targetNav === 'subscriptions') {
            this.switchView('home');
            this.filterSubscriptions();
          }"""

new_subs_nav = """} else if (targetNav === 'subscriptions') {
            this.openSubscriptionsView();
          }"""

if old_subs_nav in code:
    code = code.replace(old_subs_nav, new_subs_nav, 1)
    print("Updated sidebar subscriptions navigation!")

# 4. Bind events calls
bind_anchor = "this.initKeyboardShortcutsGlobal();"
bind_new = """this.initKeyboardShortcutsGlobal();
      this.initSleepTimerDropdown();
      this.initRecentSearches();"""

if bind_anchor in code and "this.initSleepTimerDropdown()" not in code:
    code = code.replace(bind_anchor, bind_new, 1)
    print("Added v5 calls to bindEvents!")

# 5. Methods to add
v5_methods = """
    // ------------------------------------------------------------------------
    // DEDICATED SUBSCRIPTIONS FEED HUB
    // ------------------------------------------------------------------------
    openSubscriptionsView() {
      this.switchView('subscriptions');
      this.renderSubscribedChannels();
      this.renderSubscriptionsFeed('all');

      if (this.subsFilterChips) {
        this.subsFilterChips.querySelectorAll('.yt-chip').forEach(chip => {
          chip.addEventListener('click', () => {
            this.subsFilterChips.querySelectorAll('.yt-chip').forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
            const filter = chip.getAttribute('data-subfilter') || 'all';
            this.renderSubscriptionsFeed(filter);
          });
        });
      }

      if (this.btnManageSubsPage) {
        this.btnManageSubsPage.addEventListener('click', () => {
          this.showToast("Barcha obunalar boshqaruv holatida!");
        });
      }
    }

    renderSubscribedChannels() {
      if (!this.subsChannelsRow) return;

      const channels = [
        { id: "ch-muzaffarzed", name: "MuzaffarZed Tech", avatar: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80", unread: true },
        { id: "ch-webdev", name: "Web Dev Pro", avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80", unread: true },
        { id: "ch-cosmic", name: "Cosmic Cosmos", avatar: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80", unread: false },
        { id: "ch-lofi", name: "Lofi Beats", avatar: "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=150&auto=format&fit=crop&q=80", unread: false },
        { id: "ch-nature", name: "Nature 4K", avatar: "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=150&auto=format&fit=crop&q=80", unread: true }
      ];

      this.subsChannelsRow.innerHTML = channels.map(c => `
        <div class="yt-subs-channel-item" data-id="${c.id}" title="${c.name}">
          <div class="yt-subs-avatar-wrap">
            <img src="${c.avatar}" alt="${c.name}">
            ${c.unread ? '<span class="yt-subs-unread-dot"></span>' : ''}
          </div>
          <span class="yt-subs-channel-name">${c.name}</span>
        </div>
      `).join('');

      this.subsChannelsRow.querySelectorAll('.yt-subs-channel-item').forEach(item => {
        item.addEventListener('click', () => {
          this.subsChannelsRow.querySelectorAll('.yt-subs-channel-item').forEach(i => i.classList.remove('active'));
          item.classList.add('active');
          const chId = item.getAttribute('data-id');
          this.openChannelPage(chId);
        });
      });
    }

    renderSubscriptionsFeed(filter) {
      if (!this.subsVideoGrid) return;
      this.subsVideoGrid.innerHTML = '';

      let list = this.videos;
      if (filter === 'today') {
        list = list.slice(0, 4);
      } else if (filter === 'unwatched') {
        list = list.filter(v => !this.watchHistory.includes(v.id));
      } else if (filter === 'live') {
        list = list.filter(v => v.duration === 'LIVE' || v.category === 'Music');
      }

      if (list.length === 0) {
        this.subsVideoGrid.innerHTML = `
          <div style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--yt-text-secondary);">
            <i data-lucide="bell-off" style="width: 48px; height: 48px; margin-bottom: 12px;"></i>
            <h3 style="color: var(--yt-text-primary);">Yangi videolar topilmadi</h3>
            <p>Boshqa filtrlarni tekshirib ko'ring.</p>
          </div>
        `;
        this.refreshIcons();
        return;
      }

      list.forEach(video => {
        const card = document.createElement('div');
        card.className = 'yt-card';
        card.innerHTML = `
          <div class="yt-thumbnail-wrapper">
            <img src="${video.thumbnail}" class="yt-thumbnail-img" alt="${video.title}">
            <span class="yt-duration-badge">${video.duration}</span>
          </div>
          <div class="yt-card-details">
            <img src="${video.channel.avatar}" class="yt-channel-avatar" alt="${video.channel.name}">
            <div class="yt-card-meta">
              <h3 class="yt-card-title">${video.title}</h3>
              <div class="yt-channel-title">
                <span>${video.channel.name}</span>
                ${video.channel.verified ? '<i data-lucide="check-circle" style="width: 12px; height: 12px; fill: currentColor; color: var(--yt-text-secondary);"></i>' : ''}
              </div>
              <div class="yt-card-views">
                <span>${video.views}</span> • <span>${video.timestamp}</span>
              </div>
            </div>
          </div>
        `;
        card.addEventListener('click', () => this.openWatch(video));
        this.subsVideoGrid.appendChild(card);
      });

      this.refreshIcons();
    }

    // ------------------------------------------------------------------------
    // SLEEP TIMER PRESETS DROPDOWN
    // ------------------------------------------------------------------------
    initSleepTimerDropdown() {
      if (this.btnSleepTimer && this.sleepTimerDropdown) {
        this.btnSleepTimer.addEventListener('click', (e) => {
          e.stopPropagation();
          const isShow = this.sleepTimerDropdown.style.display === 'block';
          this.sleepTimerDropdown.style.display = isShow ? 'none' : 'block';
          if (this.notificationsDropdown) this.notificationsDropdown.style.display = 'none';
          if (this.userProfileDropdown) this.userProfileDropdown.style.display = 'none';
        });

        this.sleepTimerDropdown.querySelectorAll('.yt-dropdown-item').forEach(item => {
          item.addEventListener('click', () => {
            const val = item.getAttribute('data-timer');
            this.sleepTimerDropdown.style.display = 'none';
            if (val === '0') {
              this.setSleepTimer(0);
            } else if (val === 'end') {
              this.showToast("Taymer: Video tugashi bilan o'chadi");
              if (this.sleepTimerBadge) {
                this.sleepTimerBadge.textContent = 'End';
                this.sleepTimerBadge.style.display = 'inline-block';
              }
            } else {
              this.setSleepTimer(parseInt(val));
            }
          });
        });

        document.addEventListener('click', (e) => {
          if (this.sleepTimerDropdown && !this.sleepTimerDropdown.contains(e.target) && !this.btnSleepTimer.contains(e.target)) {
            this.sleepTimerDropdown.style.display = 'none';
          }
        });
      }
    }

    // ------------------------------------------------------------------------
    // RECENT SEARCHES AUTOCOMPLETE
    // ------------------------------------------------------------------------
    initRecentSearches() {
      if (!this.searchInput || !this.suggestionsDropdown) return;

      this.searchInput.addEventListener('focus', () => {
        if (!this.searchInput.value.trim()) {
          this.renderRecentSearches();
        }
      });

      this.searchInput.addEventListener('input', () => {
        if (!this.searchInput.value.trim()) {
          this.renderRecentSearches();
        }
      });
    }

    renderRecentSearches() {
      const recents = JSON.parse(localStorage.getItem('yt_recent_searches') || '["AGI", "MuzaffarZed", "Dasturlash", "Web Development", "AI"]');
      if (recents.length === 0) {
        this.suggestionsDropdown.style.display = 'none';
        return;
      }

      this.suggestionsDropdown.innerHTML = `
        <div style="font-size: 11px; font-weight: 700; color: var(--yt-text-secondary); padding: 8px 12px; border-bottom: 1px solid var(--yt-border);">
          OXIRGI QIDIRUVLAR
        </div>
      `;

      recents.forEach(term => {
        const row = document.createElement('div');
        row.className = 'yt-recent-search-row';
        row.innerHTML = `
          <div class="yt-recent-search-left">
            <i data-lucide="clock" style="width: 15px; height: 15px; color: var(--yt-text-secondary);"></i>
            <span>${term}</span>
          </div>
          <button class="yt-btn-remove-recent" title="Tarixdan o'chirish">O'chirish</button>
        `;

        row.querySelector('.yt-recent-search-left').addEventListener('click', () => {
          this.searchInput.value = term;
          this.searchQuery = term;
          this.suggestionsDropdown.style.display = 'none';
          this.switchView('home');
          this.performSearch(term);
        });

        row.querySelector('.yt-btn-remove-recent').addEventListener('click', (e) => {
          e.stopPropagation();
          const updated = recents.filter(t => t !== term);
          localStorage.setItem('yt_recent_searches', JSON.stringify(updated));
          this.renderRecentSearches();
        });

        this.suggestionsDropdown.appendChild(row);
      });

      this.suggestionsDropdown.style.display = 'block';
      this.refreshIcons();
    }
"""

fn_marker = "formatNumber(num) {"
pos = code.find(fn_marker)
if pos != -1 and "openSubscriptionsView() {" not in code:
    code = code[:pos] + v5_methods + "\n    " + code[pos:]
    print("Injected v5 methods before formatNumber!")

with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("patch_app_v5.py completed!")
