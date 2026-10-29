with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'r', encoding='utf-8') as f:
    c = f.read().replace('\r\n', '\n')

# 1. Optimize startAmbientLoop
old_ambient = """    startAmbientLoop() {
      if (!this.ambientCanvas || !this.ambientCtx) return;
      const renderAmbient = () => {
        if (this.ambientActive && !this.videoElement.paused && !this.videoElement.ended && this.videoElement.videoWidth) {
          try {
            this.ambientCanvas.width = 64;
            this.ambientCanvas.height = 36;
            this.ambientCtx.drawImage(this.videoElement, 0, 0, 64, 36);
          } catch (e) {}
        }
        if (this.currentView === 'watch') {
          this.ambientAnimFrame = requestAnimationFrame(renderAmbient);
        }
      };
      cancelAnimationFrame(this.ambientAnimFrame);
      this.ambientAnimFrame = requestAnimationFrame(renderAmbient);
    }"""

new_ambient = """    startAmbientLoop() {
      if (!this.ambientCanvas || !this.ambientCtx) return;
      if (this.ambientCanvas.width !== 64) this.ambientCanvas.width = 64;
      if (this.ambientCanvas.height !== 36) this.ambientCanvas.height = 36;
      const renderAmbient = () => {
        if (this.ambientActive && !this.videoElement.paused && !this.videoElement.ended && this.videoElement.videoWidth) {
          try {
            this.ambientCtx.drawImage(this.videoElement, 0, 0, 64, 36);
          } catch (e) {}
        }
        if (this.currentView === 'watch') {
          this.ambientAnimFrame = requestAnimationFrame(renderAmbient);
        }
      };
      cancelAnimationFrame(this.ambientAnimFrame);
      this.ambientAnimFrame = requestAnimationFrame(renderAmbient);
    }"""

if old_ambient in c:
    c = c.replace(old_ambient, new_ambient)
    print("SUCCESS: startAmbientLoop optimized!")
else:
    print("WARNING: old_ambient not found")

# 2. Add btnChannelPageSub in bindEvents()
target_sub_hook = "      this.initNetworkStatusWatcher();"
replacement_sub_hook = """      this.initNetworkStatusWatcher();

      if (this.btnChannelPageSub) {
        this.btnChannelPageSub.addEventListener('click', () => {
          this.isSubscribed = !this.isSubscribed;
          this.btnChannelPageSub.textContent = this.isSubscribed ? "Obuna bo'lindi" : "Obuna bo'lish";
          this.btnChannelPageSub.className = `yt-subscribe-btn ${this.isSubscribed ? 'subscribed' : ''}`;
          const chName = this.channelPageTitle ? this.channelPageTitle.textContent : "Kanal";
          this.showToast(this.isSubscribed ? `"${chName}" kanaliga obuna bo'lindi!` : `"${chName}" obunasi bekor qilindi`);
        });
      }"""

if target_sub_hook in c:
    c = c.replace(target_sub_hook, replacement_sub_hook)
    print("SUCCESS: btnChannelPageSub listener hooked!")
else:
    print("WARNING: target_sub_hook not found")

# 3. Remove duplicate btnQuality and btnSpeed cycling listeners
old_dup_quality = """      // Quality Toggle
      this.btnQuality.addEventListener('click', () => {
        this.currentQualityIdx = (this.currentQualityIdx + 1) % this.qualities.length;
        const q = this.qualities[this.currentQualityIdx];
        this.btnQuality.textContent = q;
        this.showToast(`Sifat sozlandi: ${q}`);
      });"""

if old_dup_quality in c:
    c = c.replace(old_dup_quality, "// Quality Dropdown managed via qualityDropdown")
    print("SUCCESS: Duplicate btnQuality listener removed!")
else:
    print("WARNING: old_dup_quality not found")

old_dup_speed = """      // Speed Selector
      const speeds = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 4.0];
      this.btnSpeed.addEventListener('click', () => {
        let cur = this.videoElement.playbackRate;
        let idx = speeds.indexOf(cur);
        let nextIdx = (idx + 1) % speeds.length;
        let nextSpeed = speeds[nextIdx];
        this.videoElement.playbackRate = nextSpeed;
        this.btnSpeed.textContent = `${nextSpeed}x`;
        this.showToast(`Tezlik: ${nextSpeed}x`);
      });"""

if old_dup_speed in c:
    c = c.replace(old_dup_speed, "// Speed Dropdown managed via speedDropdown")
    print("SUCCESS: Duplicate btnSpeed listener removed!")
else:
    print("WARNING: old_dup_speed not found")

# 4. Enhance renderShorts() with fully interactive subBtn, likeBtn, dislikeBtn, shareBtn
old_shorts_render = """        reel.innerHTML = `
          ${mediaHtml}
          <div class="yt-short-progress"><div class="yt-short-progress-fill"></div></div>
          <div class="yt-short-overlay">
            <div class="yt-short-channel">
              <img src="${s.avatar}" style="width: 32px; height: 32px; border-radius: 50%; object-fit: cover;" alt="${s.channel}">
              <span style="font-weight: 600; font-size: 14px;">@${s.channel}</span>
              <button class="yt-btn-primary" style="padding: 4px 12px; font-size: 12px; background: white; color: black;">Obuna</button>
            </div>
            <p style="font-size: 14px; margin-bottom: 8px;">${s.title}</p>
            <div class="yt-short-sound-tag" style="display: flex; align-items: center; gap: 6px; font-size: 12px; color: #ccc; cursor: pointer;">
              <i data-lucide="music" style="width: 14px; height: 14px; color: var(--yt-blue);"></i>
              <span>${s.sound || 'Original Audio'}</span>
            </div>
          </div>

          <div class="yt-short-actions-sidebar">
            <button class="yt-short-action-btn btn-short-like">
              <i data-lucide="thumbs-up" style="width: 22px; height: 22px;"></i>
              <span class="yt-short-action-label">${s.likes || '100K'}</span>
            </button>
            <button class="yt-short-action-btn">
              <i data-lucide="thumbs-down" style="width: 22px; height: 22px;"></i>
              <span class="yt-short-action-label">Yoqmadi</span>
            </button>
            <button class="yt-short-action-btn btn-short-comment" title="Izohlar">
              <i data-lucide="message-square" style="width: 22px; height: 22px;"></i>
              <span class="yt-short-action-label">${s.comments || '1.2K'}</span>
            </button>
            <button class="yt-short-action-btn">
              <i data-lucide="share-2" style="width: 22px; height: 22px;"></i>
              <span class="yt-short-action-label">Ulashish</span>
            </button>
            <button class="yt-short-action-btn btn-short-sound">
              <i data-lucide="volume-2" style="width: 22px; height: 22px;"></i>
            </button>
          </div>
        `;"""

new_shorts_render = """        reel.innerHTML = `
          ${mediaHtml}
          <div class="yt-short-progress"><div class="yt-short-progress-fill"></div></div>
          <div class="yt-short-overlay">
            <div class="yt-short-channel">
              <img src="${s.avatar}" style="width: 32px; height: 32px; border-radius: 50%; object-fit: cover;" alt="${s.channel}">
              <span style="font-weight: 600; font-size: 14px;">@${s.channel}</span>
              <button class="yt-btn-primary btn-short-sub" style="padding: 4px 12px; font-size: 12px; background: white; color: black; border-radius: 16px; cursor: pointer; transition: all 0.2s ease;">Obuna</button>
            </div>
            <p style="font-size: 14px; margin-bottom: 8px;">${s.title}</p>
            <div class="yt-short-sound-tag" style="display: flex; align-items: center; gap: 6px; font-size: 12px; color: #ccc; cursor: pointer;">
              <i data-lucide="music" style="width: 14px; height: 14px; color: var(--yt-blue);"></i>
              <span>${s.sound || 'Original Audio'}</span>
            </div>
          </div>

          <div class="yt-short-actions-sidebar">
            <button class="yt-short-action-btn btn-short-like" title="Yoqdi">
              <i data-lucide="thumbs-up" style="width: 22px; height: 22px;"></i>
              <span class="yt-short-action-label">${s.likes || '100K'}</span>
            </button>
            <button class="yt-short-action-btn btn-short-dislike" title="Yoqmadi">
              <i data-lucide="thumbs-down" style="width: 22px; height: 22px;"></i>
              <span class="yt-short-action-label">Yoqmadi</span>
            </button>
            <button class="yt-short-action-btn btn-short-comment" title="Izohlar">
              <i data-lucide="message-square" style="width: 22px; height: 22px;"></i>
              <span class="yt-short-action-label">${s.comments || '1.2K'}</span>
            </button>
            <button class="yt-short-action-btn btn-short-share" title="Ulashish">
              <i data-lucide="share-2" style="width: 22px; height: 22px;"></i>
              <span class="yt-short-action-label">Ulashish</span>
            </button>
            <button class="yt-short-action-btn btn-short-sound" title="Ovoz">
              <i data-lucide="volume-2" style="width: 22px; height: 22px;"></i>
            </button>
          </div>
        `;"""

if old_shorts_render in c:
    c = c.replace(old_shorts_render, new_shorts_render)
    print("SUCCESS: Shorts markup upgraded!")
else:
    print("WARNING: old_shorts_render not found")

# 5. Update Shorts button click listeners
old_shorts_listeners = """        const likeBtn = reel.querySelector('.btn-short-like');
        likeBtn.addEventListener('click', () => {
          likeBtn.style.color = 'var(--yt-red)';
          this.showToast("Shorts videoga like bosildi!");
        });

        // Double-click heart pop animation
        reel.addEventListener('dblclick', (e) => {
          const heart = document.createElement('div');
          heart.className = 'yt-heart-pop';
          heart.innerHTML = '<svg viewBox="0 0 24 24" width="80" height="80" fill="#ff0000"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>';
          reel.appendChild(heart);
          setTimeout(() => heart.remove(), 750);
          likeBtn.style.color = 'var(--yt-red)';
          this.showToast("Shorts yoqtirildi! ❤️");
        });"""

new_shorts_listeners = """        // Channel subscribe in shorts
        const subBtn = reel.querySelector('.btn-short-sub');
        let isShortSub = false;
        if (subBtn) {
          subBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            isShortSub = !isShortSub;
            subBtn.textContent = isShortSub ? "Obunadasiz" : "Obuna";
            subBtn.style.background = isShortSub ? "rgba(255,255,255,0.2)" : "white";
            subBtn.style.color = isShortSub ? "white" : "black";
            this.showToast(isShortSub ? `"${s.channel}" kanaliga obuna bo'lindi!` : `"${s.channel}" obunasi bekor qilindi`);
          });
        }

        // Like / Dislike / Share in shorts
        const likeBtn = reel.querySelector('.btn-short-like');
        const dislikeBtn = reel.querySelector('.btn-short-dislike');
        let isLiked = false;
        let isDisliked = false;

        const triggerShortLike = (fromDblClick = false) => {
          isLiked = !isLiked;
          if (isLiked) {
            likeBtn.style.color = 'var(--yt-red)';
            if (isDisliked && dislikeBtn) {
              isDisliked = false;
              dislikeBtn.style.color = 'inherit';
            }
            if (fromDblClick) {
              const heart = document.createElement('div');
              heart.className = 'yt-heart-pop';
              heart.innerHTML = '<svg viewBox="0 0 24 24" width="80" height="80" fill="#ff0000"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>';
              reel.appendChild(heart);
              setTimeout(() => heart.remove(), 750);
            }
            this.showToast("Shorts yoqtirildi! ❤️");
          } else {
            likeBtn.style.color = 'inherit';
            this.showToast("Like qaytarib olindi");
          }
        };

        if (likeBtn) {
          likeBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            triggerShortLike(false);
          });
        }

        if (dislikeBtn) {
          dislikeBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            isDisliked = !isDisliked;
            dislikeBtn.style.color = isDisliked ? 'var(--yt-blue)' : 'inherit';
            if (isDisliked && isLiked && likeBtn) {
              isLiked = false;
              likeBtn.style.color = 'inherit';
            }
            this.showToast(isDisliked ? "Fikr bildirildi (Yoqmadi)" : "Fikr bekor qilindi");
          });
        }

        const shareBtn = reel.querySelector('.btn-short-share');
        if (shareBtn) {
          shareBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            const url = `${window.location.origin}/?v=${s.id || 'shorts'}`;
            navigator.clipboard.writeText(url).then(() => {
              this.showToast("Shorts havolasi nusxalandi! 📋");
            }).catch(() => {
              this.showToast("Havola nusxalandi!");
            });
          });
        }

        reel.addEventListener('dblclick', (e) => {
          if (e.target.closest('.yt-short-actions-sidebar') || e.target.closest('.yt-short-channel')) return;
          triggerShortLike(true);
        });"""

if old_shorts_listeners in c:
    c = c.replace(old_shorts_listeners, new_shorts_listeners)
    print("SUCCESS: Shorts button listeners upgraded!")
else:
    print("WARNING: old_shorts_listeners not found")

with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'w', encoding='utf-8') as f:
    f.write(c)
