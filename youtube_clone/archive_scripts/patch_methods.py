with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update renderComments to support sorting and clickable timestamps
old_render_comments = """    renderComments(video) {
      this.commentsList.innerHTML = '<p style="color: var(--yt-text-secondary); font-size: 14px;">Izohlar yuklanmoqda...</p>';

      let comments = video.comments || [];
      try {
        const res = await fetch(`${API_BASE}/api/comments/${video.id}`);
        const data = await res.json();
        if (data.success && data.comments.length > 0) {
          comments = [...data.comments, ...comments];
        }
      } catch (e) {}

      this.commentsTotalCount.textContent = `${comments.length} ta fikr`;
      this.commentsList.innerHTML = '';

      if (comments.length === 0) {
        this.commentsList.innerHTML = `
          <p style="color: var(--yt-text-secondary); font-size: 14px; margin-top: 10px;">Birinchi bo'lib fikr qoldiring!</p>
        `;
        return;
      }

      comments.forEach(c => {
        const item = document.createElement('div');
        item.className = 'yt-comment-item';
        item.innerHTML = `
          <img src="${c.avatar}" style="width: 36px; height: 36px; border-radius: 50%; object-fit: cover; flex-shrink: 0;" alt="${c.author}">
          <div class="yt-comment-body">
            <div class="yt-comment-author">
              <span>@${c.author}</span>
              <span class="yt-comment-time">${c.time}</span>
            </div>
            <div class="yt-comment-content">${c.text}</div>
            <div class="yt-comment-footer">
              <button class="yt-comment-btn btn-comment-like">
                <i data-lucide="thumbs-up" style="width: 14px; height: 14px;"></i>
                <span>${c.likes || 0}</span>
              </button>
              <button class="yt-comment-btn">
                <i data-lucide="thumbs-down" style="width: 14px; height: 14px;"></i>
              </button>
              <button class="yt-comment-btn" style="font-weight: 600;">Javob berish</button>
            </div>
          </div>
        `;

        const likeBtn = item.querySelector('.btn-comment-like');
        likeBtn.addEventListener('click', () => {
          c.likes = (c.likes || 0) + 1;
          likeBtn.querySelector('span').textContent = c.likes;
          likeBtn.style.color = 'var(--yt-blue)';
        });

        this.commentsList.appendChild(item);
      });

      this.refreshIcons();
    }"""

new_render_comments = """    renderComments(video) {
      this.commentsList.innerHTML = '<p style="color: var(--yt-text-secondary); font-size: 14px;">Izohlar yuklanmoqda...</p>';

      let comments = video.comments || [];
      try {
        const res = await fetch(`${API_BASE}/api/comments/${video.id}`);
        const data = await res.json();
        if (data.success && data.comments.length > 0) {
          comments = [...data.comments, ...comments];
        }
      } catch (e) {}

      // Apply Sort Mode
      if (this.commentsSortMode === 'top') {
        comments.sort((a, b) => (b.likes || 0) - (a.likes || 0));
      } else {
        comments.sort((a, b) => {
          if (a.time === 'Hozirgina') return -1;
          if (b.time === 'Hozirgina') return 1;
          return 0;
        });
      }

      this.commentsTotalCount.textContent = `${comments.length} ta fikr`;
      this.commentsList.innerHTML = '';

      if (comments.length === 0) {
        this.commentsList.innerHTML = `
          <p style="color: var(--yt-text-secondary); font-size: 14px; margin-top: 10px;">Birinchi bo'lib fikr qoldiring!</p>
        `;
        return;
      }

      comments.forEach(c => {
        const item = document.createElement('div');
        item.className = 'yt-comment-item';
        const formattedComment = this.formatTimestampsInText(c.text);

        item.innerHTML = `
          <img src="${c.avatar}" style="width: 36px; height: 36px; border-radius: 50%; object-fit: cover; flex-shrink: 0;" alt="${c.author}">
          <div class="yt-comment-body">
            <div class="yt-comment-author">
              <span>@${c.author}</span>
              <span class="yt-comment-time">${c.time}</span>
            </div>
            <div class="yt-comment-content">${formattedComment}</div>
            <div class="yt-comment-footer">
              <button class="yt-comment-btn btn-comment-like">
                <i data-lucide="thumbs-up" style="width: 14px; height: 14px;"></i>
                <span>${c.likes || 0}</span>
              </button>
              <button class="yt-comment-btn">
                <i data-lucide="thumbs-down" style="width: 14px; height: 14px;"></i>
              </button>
              <button class="yt-comment-btn" style="font-weight: 600;">Javob berish</button>
            </div>
          </div>
        `;

        const likeBtn = item.querySelector('.btn-comment-like');
        likeBtn.addEventListener('click', () => {
          c.likes = (c.likes || 0) + 1;
          likeBtn.querySelector('span').textContent = c.likes;
          likeBtn.style.color = 'var(--yt-blue)';
        });

        // Wire timestamp links in comments
        item.querySelectorAll('.yt-timestamp-link').forEach(link => {
          link.addEventListener('click', (e) => {
            e.stopPropagation();
            const sec = parseFloat(link.getAttribute('data-sec'));
            this.videoElement.currentTime = sec;
            if (this.videoElement.paused) this.videoElement.play();
            this.showToast(`Vaqtga sakrash: ${link.textContent}`);
          });
        });

        this.commentsList.appendChild(item);
      });

      this.refreshIcons();
    }"""

if old_render_comments in code:
    code = code.replace(old_render_comments, new_render_comments, 1)
    print("Upgraded renderComments successfully!")
else:
    print("Warning: old_render_comments not matched exactly!")

# 2. Update renderShorts comment button
old_short_action = """            <button class="yt-short-action-btn">
              <i data-lucide="message-square" style="width: 22px; height: 22px;"></i>
              <span class="yt-short-action-label">${s.comments || '1.2K'}</span>
            </button>"""

new_short_action = """            <button class="yt-short-action-btn btn-short-comment" title="Izohlar">
              <i data-lucide="message-square" style="width: 22px; height: 22px;"></i>
              <span class="yt-short-action-label">${s.comments || '1.2K'}</span>
            </button>"""

if old_short_action in code:
    code = code.replace(old_short_action, new_short_action, 1)
    print("Updated short comment button markup!")

# Add listener to comment button in renderShorts
old_like_wire = """        const likeBtn = reel.querySelector('.btn-short-like');
        likeBtn.addEventListener('click', () => {"""

new_comment_and_like_wire = """        const commentBtn = reel.querySelector('.btn-short-comment');
        if (commentBtn) {
          commentBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.openShortsComments(s);
          });
        }

        const likeBtn = reel.querySelector('.btn-short-like');
        likeBtn.addEventListener('click', () => {"""

if old_like_wire in code:
    code = code.replace(old_like_wire, new_comment_and_like_wire, 1)
    print("Wired short comment button click handler!")

# 3. New methods to inject before closing bracket of class YouTubeApp
new_methods = """
    // ------------------------------------------------------------------------
    // CENTER PLAY/PAUSE SPLASH HUD
    // ------------------------------------------------------------------------
    triggerCenterSplash(isPlaying) {
      if (!this.playerCenterSplash || !this.centerSplashIcon) return;
      this.centerSplashIcon.setAttribute('data-lucide', isPlaying ? 'play' : 'pause');
      this.refreshIcons();
      this.playerCenterSplash.classList.remove('animate');
      void this.playerCenterSplash.offsetWidth;
      this.playerCenterSplash.classList.add('animate');
      setTimeout(() => {
        if (this.playerCenterSplash) this.playerCenterSplash.classList.remove('animate');
      }, 400);
    }

    // ------------------------------------------------------------------------
    // DUAL SCRUB BAR & TOOLTIP WITH CHAPTERS
    // ------------------------------------------------------------------------
    initScrubBufferAndTooltip() {
      if (this.videoElement) {
        this.videoElement.addEventListener('progress', () => this.updateScrubBuffer());
      }
      if (this.scrubBar) {
        this.scrubBar.addEventListener('mousemove', (e) => this.handleScrubHover(e));
        this.scrubBar.addEventListener('mouseleave', () => {
          if (this.scrubTooltip) this.scrubTooltip.style.display = 'none';
        });
      }
    }

    updateScrubBuffer() {
      if (!this.scrubBuffer || !this.videoElement || !this.videoElement.duration) return;
      const b = this.videoElement.buffered;
      const dur = this.videoElement.duration;
      if (b && b.length > 0) {
        const cur = this.videoElement.currentTime;
        let bufEnd = 0;
        for (let i = 0; i < b.length; i++) {
          if (b.start(i) <= cur && cur <= b.end(i)) {
            bufEnd = b.end(i);
            break;
          }
        }
        if (bufEnd === 0) bufEnd = b.end(b.length - 1);
        const pct = Math.min(100, Math.max(0, (bufEnd / dur) * 100));
        this.scrubBuffer.style.width = `${pct}%`;
      }
    }

    handleScrubHover(e) {
      if (!this.scrubTooltip || !this.scrubBar || !this.videoElement || !this.videoElement.duration) return;
      const rect = this.scrubBar.getBoundingClientRect();
      const offsetX = Math.max(0, Math.min(e.clientX - rect.left, rect.width));
      const pct = offsetX / rect.width;
      const hoverTime = pct * this.videoElement.duration;

      if (this.tooltipTime) {
        this.tooltipTime.textContent = this.formatTime(hoverTime);
      }

      if (this.tooltipChapter && this.currentVideo) {
        const chapters = this.getVideoChapters(this.currentVideo);
        let matched = chapters[0] ? chapters[0].label : "Mundarija";
        for (let i = 0; i < chapters.length; i++) {
          if (hoverTime >= chapters[i].time) {
            matched = chapters[i].label;
          }
        }
        this.tooltipChapter.textContent = matched;
      }

      this.scrubTooltip.style.left = `${offsetX}px`;
      this.scrubTooltip.style.display = 'flex';
    }

    // ------------------------------------------------------------------------
    // VIDEO CHAPTERS (MUNDARIJA)
    // ------------------------------------------------------------------------
    getVideoChapters(video) {
      if (!video) return [];
      if (video.chapters && Array.isArray(video.chapters) && video.chapters.length > 0) {
        return video.chapters;
      }

      const desc = video.description || '';
      const regex = /(?:(\\d{1,2}):)?(\\d{2}):(\\d{2})\\s+([^\\n\\r]+)/g;
      let match;
      const parsed = [];
      while ((match = regex.exec(desc)) !== null) {
        const h = match[1] ? parseInt(match[1]) : 0;
        const m = parseInt(match[2]);
        const s = parseInt(match[3]);
        const sec = h * 3600 + m * 60 + s;
        parsed.push({ time: sec, label: match[0].trim() });
      }

      if (parsed.length >= 2) return parsed;

      const totalDur = (this.videoElement && this.videoElement.duration) || video.durationSec || 600;
      return [
        { time: 0, label: "00:00 Kirish va Maqsad" },
        { time: Math.floor(totalDur * 0.25), label: `${this.formatTime(totalDur * 0.25)} Arxitektura & Sxema` },
        { time: Math.floor(totalDur * 0.6), label: `${this.formatTime(totalDur * 0.6)} Jonli Amaliyot & MuzaffarZed Engine` },
        { time: Math.floor(totalDur * 0.85), label: `${this.formatTime(totalDur * 0.85)} Sinov, Xulosalar & Yakun` }
      ];
    }

    initChaptersEvents() {
      if (this.btnChapters) {
        this.btnChapters.addEventListener('click', () => this.openChaptersModal());
      }
      if (this.btnCloseChaptersModal) {
        this.btnCloseChaptersModal.addEventListener('click', () => {
          if (this.chaptersModal) this.chaptersModal.classList.remove('open');
        });
      }
      if (this.chaptersModal) {
        this.chaptersModal.addEventListener('click', (e) => {
          if (e.target === this.chaptersModal) this.chaptersModal.classList.remove('open');
        });
      }
    }

    openChaptersModal() {
      if (!this.chaptersModal || !this.chaptersListContainer || !this.currentVideo) return;
      const chapters = this.getVideoChapters(this.currentVideo);
      this.chaptersListContainer.innerHTML = '';

      chapters.forEach((ch) => {
        const row = document.createElement('div');
        row.className = 'yt-chapter-row';
        row.innerHTML = `
          <span class="yt-chapter-time-badge">${this.formatTime(ch.time)}</span>
          <span class="yt-chapter-title">${ch.label}</span>
          <i data-lucide="play-circle" style="width: 18px; height: 18px; color: var(--yt-blue); opacity: 0.8;"></i>
        `;
        row.addEventListener('click', () => {
          this.videoElement.currentTime = ch.time;
          if (this.videoElement.paused) this.videoElement.play();
          this.chaptersModal.classList.remove('open');
          this.showToast(`Mundarija: ${ch.label}`);
        });
        this.chaptersListContainer.appendChild(row);
      });

      this.refreshIcons();
      this.chaptersModal.classList.add('open');
    }

    // ------------------------------------------------------------------------
    // COMMENTS SORTING & TIMESTAMPS
    // ------------------------------------------------------------------------
    initCommentsSortingEvents() {
      if (this.btnSortComments) {
        this.btnSortComments.addEventListener('click', () => {
          this.commentsSortMode = this.commentsSortMode === 'top' ? 'newest' : 'top';
          if (this.sortCommentsLabel) {
            this.sortCommentsLabel.textContent = this.commentsSortMode === 'top' ? 'Eng saralar' : 'Yangilari avval';
          }
          if (this.currentVideo) {
            this.renderComments(this.currentVideo);
          }
          this.showToast(`Izohlar: ${this.commentsSortMode === 'top' ? 'Eng saralar' : 'Eng yangilari'} bo'yicha`);
        });
      }
    }

    formatTimestampsInText(text) {
      if (!text) return '';
      const regex = /(?:(\\d{1,2}):)?(\\d{2}):(\\d{2})/g;
      return text.replace(regex, (match, h, m, s) => {
        const hours = h ? parseInt(h) : 0;
        const totalSec = hours * 3600 + parseInt(m) * 60 + parseInt(s);
        return `<span class="yt-timestamp-link" data-sec="${totalSec}">${match}</span>`;
      });
    }

    // ------------------------------------------------------------------------
    // SHORTS COMMENTS DRAWER
    // ------------------------------------------------------------------------
    initShortsCommentsEvents() {
      if (this.btnCloseShortsComments) {
        this.btnCloseShortsComments.addEventListener('click', () => {
          if (this.shortsCommentsDrawer) this.shortsCommentsDrawer.style.display = 'none';
        });
      }

      if (this.btnSubmitShortsComment) {
        this.btnSubmitShortsComment.addEventListener('click', () => this.submitShortsComment());
      }

      if (this.shortsCommentInput) {
        this.shortsCommentInput.addEventListener('keydown', (e) => {
          if (e.key === 'Enter') this.submitShortsComment();
        });
      }
    }

    openShortsComments(shortData) {
      if (!this.shortsCommentsDrawer || !shortData) return;
      this.activeShortId = shortData.id;
      if (!this.shortsComments) this.shortsComments = {};
      if (!this.shortsComments[shortData.id]) {
        this.shortsComments[shortData.id] = [
          { author: "MuzaffarZed", text: "Ushbu short reel MuzaffarZed Ultra Engine asosida yaratildi!", time: "Hozirgina" },
          { author: "Sanjar Dev", text: "Zo'r effektlar va silliq montaj, davomini kutyapmiz!", time: "10 daqiqa oldin" },
          { author: "CyberPro", text: "Almashishi judayam tez va qotmasdan ishlayapti, ajoyib!", time: "1 soat oldin" }
        ];
      }

      this.renderShortsCommentsList();
      this.shortsCommentsDrawer.style.display = 'flex';
      if (this.shortsCommentInput) this.shortsCommentInput.focus();
    }

    renderShortsCommentsList() {
      if (!this.shortsCommentsList) return;
      const list = this.shortsComments[this.activeShortId] || [];
      if (this.shortsCommentsCount) {
        this.shortsCommentsCount.textContent = `(${list.length})`;
      }
      this.shortsCommentsList.innerHTML = list.map(c => `
        <div style="background: var(--yt-surface); border-radius: 8px; padding: 8px 12px; border: 1px solid var(--yt-border);">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
            <b style="font-size: 13px; color: var(--yt-blue);">${c.author}</b>
            <span style="font-size: 11px; color: var(--yt-text-secondary);">${c.time}</span>
          </div>
          <div style="font-size: 13px; color: var(--yt-text-primary);">${c.text}</div>
        </div>
      `).join('');
    }

    submitShortsComment() {
      if (!this.shortsCommentInput || !this.activeShortId) return;
      const val = this.shortsCommentInput.value.trim();
      if (!val) return;
      if (!this.shortsComments[this.activeShortId]) this.shortsComments[this.activeShortId] = [];
      this.shortsComments[this.activeShortId].unshift({
        author: "Muzaffar (Siz)",
        text: val,
        time: "Hozirgina"
      });
      this.shortsCommentInput.value = '';
      this.renderShortsCommentsList();
      this.showToast("Shorts izohingiz qo'shildi!");
    }

    // ------------------------------------------------------------------------
    // CUSTOM PLAYER CONTEXT MENU (RIGHT-CLICK)
    // ------------------------------------------------------------------------
    initVideoContextMenu() {
      if (!this.playerContainer || !this.playerContextMenu) return;

      this.playerContainer.addEventListener('contextmenu', (e) => {
        e.preventDefault();
        const menuWidth = 260;
        const menuHeight = 280;
        let x = e.clientX;
        let y = e.clientY;

        if (x + menuWidth > window.innerWidth) x = window.innerWidth - menuWidth - 10;
        if (y + menuHeight > window.innerHeight) y = window.innerHeight - menuHeight - 10;

        this.playerContextMenu.style.left = `${x}px`;
        this.playerContextMenu.style.top = `${y}px`;
        this.playerContextMenu.style.display = 'block';

        if (this.ctxLoopText) {
          this.ctxLoopText.textContent = this.videoElement.loop ? "Videoni takrorlash: Yoqilgan ✓" : "Videoni takrorlash (Loop)";
        }
        this.refreshIcons();
      });

      document.addEventListener('click', (e) => {
        if (this.playerContextMenu && !this.playerContextMenu.contains(e.target)) {
          this.playerContextMenu.style.display = 'none';
        }
      });

      if (this.ctxLoop) {
        this.ctxLoop.addEventListener('click', () => {
          this.btnLoopToggle.click();
          this.playerContextMenu.style.display = 'none';
        });
      }

      if (this.ctxCopyUrl) {
        this.ctxCopyUrl.addEventListener('click', () => {
          const url = window.location.href;
          navigator.clipboard.writeText(url);
          this.showToast("Video havolasi nusxalandi!");
          this.playerContextMenu.style.display = 'none';
        });
      }

      if (this.ctxCopyTime) {
        this.ctxCopyTime.addEventListener('click', () => {
          const t = Math.floor(this.videoElement.currentTime);
          const base = window.location.href.split('?')[0].split('#')[0];
          const timeUrl = `${base}?v=${this.currentVideo ? this.currentVideo.id : ''}&t=${t}`;
          navigator.clipboard.writeText(timeUrl);
          this.showToast(`Hozirgi vaqt (${this.formatTime(t)}) havolasi nusxalandi!`);
          this.playerContextMenu.style.display = 'none';
        });
      }

      if (this.ctxCopyEmbed) {
        this.ctxCopyEmbed.addEventListener('click', () => {
          const embed = `<iframe width="560" height="315" src="${this.videoElement.src}" title="YouTube video player" frameborder="0" allowfullscreen></iframe>`;
          navigator.clipboard.writeText(embed);
          this.showToast("Embed iframe kodi nusxalandi!");
          this.playerContextMenu.style.display = 'none';
        });
      }

      if (this.ctxStats) {
        this.ctxStats.addEventListener('click', () => {
          this.btnStatsNerds.click();
          this.playerContextMenu.style.display = 'none';
        });
      }

      if (this.ctxEq) {
        this.ctxEq.addEventListener('click', () => {
          this.btnAudioEq.click();
          this.playerContextMenu.style.display = 'none';
        });
      }

      if (this.ctxPip) {
        this.ctxPip.addEventListener('click', () => {
          this.btnPipNative.click();
          this.playerContextMenu.style.display = 'none';
        });
      }
    }

    // ------------------------------------------------------------------------
    // MOUSE WHEEL VOLUME CONTROL
    // ------------------------------------------------------------------------
    initPlayerWheelVolume() {
      if (!this.playerContainer || !this.videoElement) return;

      this.playerContainer.addEventListener('wheel', (e) => {
        e.preventDefault();
        const step = 0.05;
        let newVol = this.videoElement.volume + (e.deltaY < 0 ? step : -step);
        newVol = Math.max(0, Math.min(1, newVol));
        this.videoElement.volume = newVol;
        if (this.volumeSlider) this.volumeSlider.value = newVol;
        this.updateVolumeIcon();
        this.showVolumeHud(newVol);
      }, { passive: false });
    }
"""

# Insert new methods before closing of class YouTubeApp
format_num_anchor = """    formatNumber(num) {
      if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
      if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
      return num.toString();
    }"""

if format_num_anchor in code and "triggerCenterSplash" not in code:
    code = code.replace(format_num_anchor, format_num_anchor + "\n" + new_methods, 1)
    print("Injected all new methods successfully!")

with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("patch_methods.py complete!")
