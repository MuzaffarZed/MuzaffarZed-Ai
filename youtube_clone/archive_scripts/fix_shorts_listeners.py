with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'r', encoding='utf-8') as f:
    c = f.read()

target = """        const video = reel.querySelector('video');
        if (video) {
          video.muted = true;
          const progFill = reel.querySelector('.yt-short-progress-fill');
          video.addEventListener('timeupdate', () => {
            if (video.duration && progFill) {
              progFill.style.width = ((video.currentTime / video.duration) * 100) + '%';
            }
          });
          video.addEventListener('click', () => {
            if (video.paused) video.play();
            else video.pause();
          });

          const soundTag = reel.querySelector('.yt-short-sound-tag');
        if (soundTag) {
          soundTag.addEventListener('click', (e) => {
            e.stopPropagation();
            this.openShortsSoundModal(s.sound, s.channel);
          });
        }
        const soundBtn = reel.querySelector('.btn-short-sound');
          soundBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            video.muted = !video.muted;
            soundBtn.querySelector('i').setAttribute('data-lucide', video.muted ? 'volume-x' : 'volume-2');
            this.refreshIcons();
          });
        }"""

replacement = """        const video = reel.querySelector('video');
        if (video) {
          video.muted = true;
          const progFill = reel.querySelector('.yt-short-progress-fill');
          video.addEventListener('timeupdate', () => {
            if (video.duration && progFill) {
              progFill.style.width = ((video.currentTime / video.duration) * 100) + '%';
            }
          });
          video.addEventListener('click', () => {
            if (video.paused) video.play();
            else video.pause();
          });
        }

        const soundTag = reel.querySelector('.yt-short-sound-tag');
        if (soundTag) {
          soundTag.addEventListener('click', (e) => {
            e.stopPropagation();
            this.openShortsSoundModal(s.sound, s.channel);
          });
        }

        const soundBtn = reel.querySelector('.btn-short-sound');
        if (soundBtn) {
          soundBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            if (video) {
              video.muted = !video.muted;
              const icon = soundBtn.querySelector('i');
              if (icon) icon.setAttribute('data-lucide', video.muted ? 'volume-x' : 'volume-2');
              this.refreshIcons();
            } else {
              this.showToast("Audio holati o'zgartirildi");
            }
          });
        }"""

c_norm = c.replace('\r\n', '\n')
if target in c_norm:
    c_norm = c_norm.replace(target, replacement)
    with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'w', encoding='utf-8') as f:
        f.write(c_norm)
    print("SUCCESS: listeners attached outside if(video)")
else:
    print("FAILED: Target string not found")
