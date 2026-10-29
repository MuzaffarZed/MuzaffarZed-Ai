import urllib.request
import json
import websocket

raw = urllib.request.urlopen('http://127.0.0.1:9228/json').read().decode()
tabs = json.loads(raw)
ws_url = tabs[0]['webSocketDebuggerUrl']
ws = websocket.create_connection(ws_url, suppress_origin=True)

# Enable Runtime
ws.send(json.dumps({'id': 1, 'method': 'Runtime.enable'}))

def eval_expr(expr, req_id):
    ws.send(json.dumps({'id': req_id, 'method': 'Runtime.evaluate', 'params': {'expression': expr}}))
    while True:
        msg = json.loads(ws.recv())
        if msg.get('id') == req_id:
            return msg.get('result', {}).get('result', {}).get('value')

print('Live URL:', eval_expr('window.location.href', 10))
print('document.title:', eval_expr('document.title', 11))
print('Body innerText:\n', eval_expr('document.body.innerText', 12))
print('Root innerHTML preview:\n', eval_expr('document.getElementById("root") ? document.getElementById("root").innerHTML.substring(0, 400) : "NO ROOT"', 13))

# Check for console errors or pending promises
print('LocalStorage keys:', eval_expr('Object.keys(localStorage)', 14))
print('Scripts in DOM count:', eval_expr('document.querySelectorAll("script").length', 15))

ws.close()
