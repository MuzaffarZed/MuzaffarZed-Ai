with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Constructor additions
constructor_anchor = "this.miniplayerActive = false;"
constructor_additions = """this.miniplayerActive = false;
      this.commentsSortMode = 'top';
      this.shortsComments = {};
      this.activeShortId = null;"""

if constructor_anchor in code and "this.commentsSortMode" not in code:
    code = code.replace(constructor_anchor, constructor_additions, 1)
    print("Added constructor state properties!")

# 2. cacheDom additions
cache_dom_anchor = """      this.btnToggleTheme = document.getElementById('btn-toggle-theme');
      this.themeIcon = document.getElementById('theme-icon');
    }"""

cache_dom_additions = """      this.btnToggleTheme = document.getElementById('btn-toggle-theme');
      this.themeIcon = document.getElementById('theme-icon');

      // Pro Polish DOM elements
      this.scrubBuffer = document.getElementById('scrub-buffer');
      this.scrubTooltip = document.getElementById('scrub-tooltip');
      this.tooltipChapter = document.getElementById('tooltip-chapter');
      this.tooltipTime = document.getElementById('tooltip-time');

      this.playerCenterSplash = document.getElementById('player-center-splash');
      this.centerSplashIcon = document.getElementById('center-splash-icon');

      this.btnChapters = document.getElementById('btn-chapters');
      this.chaptersModal = document.getElementById('chapters-modal');
      this.btnCloseChaptersModal = document.getElementById('btn-close-chapters-modal');
      this.chaptersListContainer = document.getElementById('chapters-list-container');

      this.btnSortComments = document.getElementById('btn-sort-comments');
      this.sortCommentsLabel = document.getElementById('sort-comments-label');

      this.shortsCommentsDrawer = document.getElementById('shorts-comments-drawer');
      this.btnCloseShortsComments = document.getElementById('btn-close-shorts-comments');
      this.shortsCommentsList = document.getElementById('shorts-comments-list');
      this.shortsCommentInput = document.getElementById('shorts-comment-input');
      this.btnSubmitShortsComment = document.getElementById('btn-submit-shorts-comment');
      this.shortsCommentsCount = document.getElementById('shorts-comments-count');

      this.playerContextMenu = document.getElementById('player-context-menu');
      this.ctxLoop = document.getElementById('ctx-loop');
      this.ctxLoopText = document.getElementById('ctx-loop-text');
      this.ctxCopyUrl = document.getElementById('ctx-copy-url');
      this.ctxCopyTime = document.getElementById('ctx-copy-time');
      this.ctxCopyEmbed = document.getElementById('ctx-copy-embed');
      this.ctxStats = document.getElementById('ctx-stats');
      this.ctxEq = document.getElementById('ctx-eq');
      this.ctxPip = document.getElementById('ctx-pip');
    }"""

if cache_dom_anchor in code and "this.scrubBuffer" not in code:
    code = code.replace(cache_dom_anchor, cache_dom_additions, 1)
    print("Added cacheDom elements!")

# 3. bindEvents calls before end of bindEvents
bind_end_anchor = """        } else if (this.currentView === 'shorts') {
          if (e.key === 'ArrowDown') {
            this.shortsContainer.scrollBy({ top: 640, behavior: 'smooth' });
          } else if (e.key === 'ArrowUp') {
            this.shortsContainer.scrollBy({ top: -640, behavior: 'smooth' });
          }
        }
      });
    }"""

bind_end_additions = """        } else if (this.currentView === 'shorts') {
          if (e.key === 'ArrowDown') {
            this.shortsContainer.scrollBy({ top: 640, behavior: 'smooth' });
          } else if (e.key === 'ArrowUp') {
            this.shortsContainer.scrollBy({ top: -640, behavior: 'smooth' });
          }
        }
      });

      // Advanced Pro Polish Modules
      this.initScrubBufferAndTooltip();
      this.initChaptersEvents();
      this.initCommentsSortingEvents();
      this.initShortsCommentsEvents();
      this.initVideoContextMenu();
      this.initPlayerWheelVolume();
    }"""

if bind_end_anchor in code and "this.initScrubBufferAndTooltip()" not in code:
    code = code.replace(bind_end_anchor, bind_end_additions, 1)
    print("Added bindEvents initialization calls!")

# 4. Center splash trigger in togglePlayPause
toggle_anchor = """    togglePlayPause() {
      if (this.videoElement.paused) {
        this.videoElement.play();
        this.updatePlayPauseIcon(true);
      } else {
        this.videoElement.pause();
        this.updatePlayPauseIcon(false);
      }
    }"""

toggle_new = """    togglePlayPause() {
      if (this.videoElement.paused) {
        this.videoElement.play();
        this.updatePlayPauseIcon(true);
        this.triggerCenterSplash(true);
      } else {
        this.videoElement.pause();
        this.updatePlayPauseIcon(false);
        this.triggerCenterSplash(false);
      }
    }"""

if toggle_anchor in code:
    code = code.replace(toggle_anchor, toggle_new, 1)
    print("Added center splash trigger to togglePlayPause!")

# 5. Scrub buffer update inside onTimeUpdate
on_time_anchor = """    onTimeUpdate() {
      const cur = this.videoElement.currentTime;
      const dur = this.videoElement.duration || 1;
      const pct = (cur / dur) * 100;
      this.scrubFill.style.width = `${pct}%`;
      this.timeDisplay.textContent = `${this.formatTime(cur)} / ${this.formatTime(dur)}`;"""

on_time_new = """    onTimeUpdate() {
      const cur = this.videoElement.currentTime;
      const dur = this.videoElement.duration || 1;
      const pct = (cur / dur) * 100;
      this.scrubFill.style.width = `${pct}%`;
      this.timeDisplay.textContent = `${this.formatTime(cur)} / ${this.formatTime(dur)}`;
      this.updateScrubBuffer();"""

if on_time_anchor in code:
    code = code.replace(on_time_anchor, on_time_new, 1)
    print("Added updateScrubBuffer to onTimeUpdate!")

# 6. Append new methods before the closing of class YouTubeApp
class_close_anchor = "    // Helper for PWA check\n    initPwa() {"
# Let's find where initPwa or the end of class is
if "initPwa() {" in code:
    pwa_idx = code.find("initPwa() {")
    end_class_idx = code.rfind("  }\n\n  // Initialize Application")
    if end_class_idx == -1:
        end_class_idx = code.rfind("  }\n\n  window.addEventListener('DOMContentLoaded'")
    if end_class_idx == -1:
        end_class_idx = code.rfind("  }\n})();")
    print(f"End of class found at {end_class_idx}")

with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Pre-patch 1 applied!")
