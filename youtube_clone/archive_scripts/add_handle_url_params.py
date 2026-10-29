with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'r', encoding='utf-8') as f:
    code = f.read()

handle_url_method = """
    handleUrlParams() {
      try {
        const urlParams = new URLSearchParams(window.location.search);
        const videoId = urlParams.get('v');
        const timeParam = urlParams.get('t');
        if (videoId) {
          const found = this.videos.find(v => v.id === videoId);
          if (found) {
            this.openWatch(found);
            if (timeParam && this.videoElement) {
              const sec = parseInt(timeParam);
              if (!isNaN(sec)) {
                setTimeout(() => {
                  if (this.videoElement) this.videoElement.currentTime = sec;
                }, 300);
              }
            }
          }
        }
      } catch (e) {}
    }
"""

if "handleUrlParams() {" not in code:
    anchor = "initPwa() {"
    pos = code.find(anchor)
    if pos != -1:
        code = code[:pos] + handle_url_method + "\n    " + code[pos:]
        print("Inserted handleUrlParams method before initPwa!")

with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'w', encoding='utf-8') as f:
    f.write(code)

# Fix twitter icon in index.html to message-circle or share
with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('data-lucide="twitter"', 'data-lucide="share"')
with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Patch complete!")
