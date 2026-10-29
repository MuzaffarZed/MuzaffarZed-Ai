import urllib.request, json, time, os

def get_port():
    p = os.path.expandvars(r'%LOCALAPPDATA%\UzbekMusiqaMarkaziPro\running_port.txt')
    return open(p).read().strip()

def eval_js(code):
    port = get_port()
    data = {'action': 'evalJs', 'code': code}
    req = urllib.request.Request(f'http://127.0.0.1:{port}/api/native/action', data=json.dumps(data).encode(), headers={'Content-Type': 'application/json'})
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read().decode())

print("Using port:", get_port())
res = eval_js("""
(function() {
    switchTab('aimp');
    setLibraryViewMode('details');
    if (!state.showInspectorPane) toggleInspectorPane('details');
    if (state.playlist && state.playlist.length > 0) {
        selectLibraryTrackItem(0);
    }
    return 'Done tab-aimp';
})()
""")
print("Library state prepared:", res)
