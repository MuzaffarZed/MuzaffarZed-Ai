import urllib.request, json, time

port = open(r'C:\Users\MuzaffarZed\AppData\Local\UzbekMusiqaMarkaziPro\running_port.txt').read().strip()

def eval_js(code):
    data = {'action': 'evalJs', 'code': code}
    req = urllib.request.Request(f'http://127.0.0.1:{port}/api/native/action', data=json.dumps(data).encode(), headers={'Content-Type': 'application/json'})
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read().decode())

# Find MP4 and play
print("Triggering playback of MP4...")
res = eval_js("""
(function() {
    const item = (state.libraryItems || []).find(x => x.mediaType === 'mp4');
    if (item) {
        playFileImmediately(item.path, item.title, item.artist);
        return 'Started: ' + item.title + ' | path=' + item.path;
    }
    return 'No mp4 found';
})()
""")
print("Play result:", res)

time.sleep(2.0)

# Check video element state
res2 = eval_js("""
JSON.stringify({
    src: videoEl.src,
    currentSrc: videoEl.currentSrc,
    error: videoEl.error ? {code: videoEl.error.code, message: videoEl.error.message} : null,
    networkState: videoEl.networkState,
    readyState: videoEl.readyState,
    paused: videoEl.paused,
    currentTime: videoEl.currentTime,
    duration: videoEl.duration,
    videoWidth: videoEl.videoWidth,
    videoHeight: videoEl.videoHeight,
    activeTab: state.activeTab
})
""")
print("Video state after 2s:", res2)
