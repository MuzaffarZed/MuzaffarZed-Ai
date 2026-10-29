# 1. Update styles.css with .yt-thumb-progress
css_path = r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\styles.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read().replace('\r\n', '\n')

css_thumb_prog = """
/* Video Thumbnail Watch Progress Bar */
.yt-thumb-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: rgba(255, 255, 255, 0.25);
  overflow: hidden;
  z-index: 4;
}

.yt-thumb-progress-fill {
  height: 100%;
  background: var(--yt-red);
  transition: width 0.2s ease;
}
"""

if '.yt-thumb-progress {' not in css:
    css += '\n' + css_thumb_prog
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css)
    print("SUCCESS: styles.css updated with .yt-thumb-progress")
else:
    print("styles.css already contains .yt-thumb-progress")

# 2. Update app.js
app_path = r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    c = f.read().replace('\r\n', '\n')

# Constructor videoProgress
old_cons = "      this.currentLang = localStorage.getItem('yt_lang') || 'UZ';"
new_cons = """      this.currentLang = localStorage.getItem('yt_lang') || 'UZ';
      this.videoProgress = JSON.parse(localStorage.getItem('yt_video_progress') || '{}');"""

if old_cons in c:
    c = c.replace(old_cons, new_cons, 1)
    print("SUCCESS: videoProgress added to constructor")
else:
    print("WARNING: old_cons not found")

# Volume restore in cacheDom()
old_cache = "      this.btnNextVideo = document.getElementById('btn-next-video');"
new_cache = """      this.btnNextVideo = document.getElementById('btn-next-video');

      // Volume & Mute Persistence
      const savedVol = localStorage.getItem('yt_volume');
      if (savedVol !== null && this.videoElement) {
        const parsedVol = parseFloat(savedVol);
        this.videoElement.volume = parsedVol;
        if (this.volumeSlider) this.volumeSlider.value = parsedVol;
      }
      const savedMuted = localStorage.getItem('yt_muted');
      if (savedMuted === 'true' && this.videoElement) {
        this.videoElement.muted = true;
        this.updateVolumeIcon();
      }"""

if old_cache in c:
    c = c.replace(old_cache, new_cache, 1)
    print("SUCCESS: Volume restore added to cacheDom()")
else:
    print("WARNING: old_cache not found")

# Volume save on volumeSlider input
old_vol_slider = """      this.volumeSlider.addEventListener('input', (e) => {
        const val = parseFloat(e.target.value);
        this.videoElement.volume = val;
        this.videoElement.muted = (val === 0);
        this.updateVolumeIcon();
      });"""

new_vol_slider = """      this.volumeSlider.addEventListener('input', (e) => {
        const val = parseFloat(e.target.value);
        this.videoElement.volume = val;
        this.videoElement.muted = (val === 0);
        localStorage.setItem('yt_volume', val);
        localStorage.setItem('yt_muted', val === 0);
        this.updateVolumeIcon();
      });"""

if old_vol_slider in c:
    c = c.replace(old_vol_slider, new_vol_slider, 1)
    print("SUCCESS: Volume save added to volumeSlider")
else:
    print("WARNING: old_vol_slider not found")

# Volume save in toggleMute
old_toggle_mute = """    toggleMute() {
      this.videoElement.muted = !this.videoElement.muted;
      this.volumeSlider.value = this.videoElement.muted ? 0 : this.videoElement.volume;
      this.updateVolumeIcon();
    }"""

new_toggle_mute = """    toggleMute() {
      this.videoElement.muted = !this.videoElement.muted;
      this.volumeSlider.value = this.videoElement.muted ? 0 : this.videoElement.volume;
      localStorage.setItem('yt_muted', this.videoElement.muted);
      this.updateVolumeIcon();
    }"""

if old_toggle_mute in c:
    c = c.replace(old_toggle_mute, new_toggle_mute, 1)
    print("SUCCESS: Mute save added to toggleMute")
else:
    print("WARNING: old_toggle_mute not found")

# Progress tracking in onTimeUpdate
old_timeupdate = """      this.scrubFill.style.width = `${pct}%`;
      this.timeDisplay.textContent = `${this.formatTime(cur)} / ${this.formatTime(dur)}`;
      this.updateScrubBuffer();"""

new_timeupdate = """      this.scrubFill.style.width = `${pct}%`;
      this.timeDisplay.textContent = `${this.formatTime(cur)} / ${this.formatTime(dur)}`;
      this.updateScrubBuffer();

      // Track playback progress for thumbnails and resume
      if (this.currentVideo && dur > 0) {
        this.videoProgress[this.currentVideo.id] = {
          time: cur,
          duration: dur,
          percent: Math.min(100, Math.round(pct))
        };
        localStorage.setItem('yt_video_progress', JSON.stringify(this.videoProgress));
      }"""

if old_timeupdate in c:
    c = c.replace(old_timeupdate, new_timeupdate, 1)
    print("SUCCESS: Progress tracking added to onTimeUpdate")
else:
    print("WARNING: old_timeupdate not found")

# Progress resumption in openWatch
old_open_watch_play = """        this.videoElement.src = streamUrl;
        this.videoElement.load();
        this.videoElement.play().catch(() => {});"""

new_open_watch_play = """        this.videoElement.src = streamUrl;
        this.videoElement.load();
        const savedProg = this.videoProgress && this.videoProgress[video.id];
        if (savedProg && savedProg.time > 5 && savedProg.duration && savedProg.time < savedProg.duration - 10) {
          const onCanPlay = () => {
            this.videoElement.currentTime = savedProg.time;
            this.showToast(`Qolgan joyidan davom ettirilmoqda (${this.formatTime(savedProg.time)})`);
            this.videoElement.removeEventListener('canplay', onCanPlay);
          };
          this.videoElement.addEventListener('canplay', onCanPlay);
        }
        this.videoElement.play().catch(() => {});"""

if old_open_watch_play in c:
    c = c.replace(old_open_watch_play, new_open_watch_play, 1)
    print("SUCCESS: Progress resume added to openWatch")
else:
    print("WARNING: old_open_watch_play not found")

# Render progress bar on thumbnails in renderCustomGrid
old_grid_card = """      videos.forEach(video => {
        const card = document.createElement('div');
        card.className = 'yt-card';
        card.innerHTML = `
          <div class="yt-thumbnail-wrapper">
            <img src="${video.thumbnail}" class="yt-thumbnail-img" alt="${video.title}">
            <span class="yt-duration-badge">${video.duration}</span>
            <div class="yt-thumb-quick-actions">"""

new_grid_card = """      videos.forEach(video => {
        const card = document.createElement('div');
        card.className = 'yt-card';
        const prog = this.videoProgress && this.videoProgress[video.id];
        const progressHtml = (prog && prog.percent > 2)
          ? `<div class="yt-thumb-progress"><div class="yt-thumb-progress-fill" style="width: ${prog.percent}%;"></div></div>`
          : '';
        card.innerHTML = `
          <div class="yt-thumbnail-wrapper">
            <img src="${video.thumbnail}" class="yt-thumbnail-img" alt="${video.title}">
            <span class="yt-duration-badge">${video.duration}</span>
            ${progressHtml}
            <div class="yt-thumb-quick-actions">"""

if old_grid_card in c:
    c = c.replace(old_grid_card, new_grid_card, 1)
    print("SUCCESS: Progress bar added to renderCustomGrid")
else:
    print("WARNING: old_grid_card not found")

# Global Escape key handler
old_esc = """    initKeyboardShortcutsGlobal() {
      document.addEventListener('keydown', (e) => {
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
        if (e.key === '?' || (e.shiftKey && e.key === '/')) {
          e.preventDefault();
          if (this.shortcutsModal) {
            this.shortcutsModal.classList.toggle('open');
          }
        }
      });
    }"""

new_esc = """    initKeyboardShortcutsGlobal() {
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
          if (this.cardContextMenu) this.hideCardContextMenu();
          if (this.playerContextMenu) this.playerContextMenu.style.display = 'none';
          if (this.speedDropdown) this.speedDropdown.style.display = 'none';
          if (this.qualityDropdown) this.qualityDropdown.style.display = 'none';
          if (this.sleepTimerDropdown) this.sleepTimerDropdown.style.display = 'none';
          if (this.subtitlesLangMenu) this.subtitlesLangMenu.style.display = 'none';
          if (this.notificationsDropdown) this.notificationsDropdown.style.display = 'none';
          if (this.userProfileDropdown) this.userProfileDropdown.style.display = 'none';
          if (this.recentSearchesContainer) this.recentSearchesContainer.style.display = 'none';
          if (this.shortcutsModal) this.shortcutsModal.classList.remove('open');
          if (this.chaptersModal) this.chaptersModal.classList.remove('open');
          if (this.shortsSoundModal) this.shortsSoundModal.classList.remove('open');
          if (this.playlistModal) this.playlistModal.classList.remove('open');
          if (this.voiceSearchModal) this.voiceSearchModal.classList.remove('open');
          return;
        }
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
        if (e.key === '?' || (e.shiftKey && e.key === '/')) {
          e.preventDefault();
          if (this.shortcutsModal) {
            this.shortcutsModal.classList.toggle('open');
          }
        }
      });
    }"""

if old_esc in c:
    c = c.replace(old_esc, new_esc, 1)
    print("SUCCESS: Global Escape key handler added")
else:
    print("WARNING: old_esc not found")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(c)
