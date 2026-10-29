import urllib.request
import json
import websocket

raw = urllib.request.urlopen('http://127.0.0.1:9228/json').read().decode()
tabs = json.loads(raw)
ws_url = tabs[0]['webSocketDebuggerUrl']
ws = websocket.create_connection(ws_url, suppress_origin=True)

ws.send(json.dumps({'id': 1, 'method': 'Runtime.enable'}))

def eval_expr(expr, req_id):
    ws.send(json.dumps({'id': req_id, 'method': 'Runtime.evaluate', 'params': {'expression': expr}}))
    while True:
        msg = json.loads(ws.recv())
        if msg.get('id') == req_id:
            return msg.get('result', {}).get('result', {}).get('value')

body_html = eval_expr('document.body.innerHTML', 10)
with open(r'C:\Users\MuzaffarZed\.gemini\antigravity\brain\776c4a96-8eb4-4dda-9f36-a6e771149a78\phone_body.html', 'w', encoding='utf-8') as f:
    f.write(body_html or '')

print('Saved phone_body.html, length:', len(body_html or ''))

# Check console exceptions
ws.send(json.dumps({'id': 20, 'method': 'Runtime.evaluate', 'params': {'expression': 'window.__ERRORS__ || []'}}))
res20 = json.loads(ws.recv())
while res20.get('id') != 20:
    res20 = json.loads(ws.recv())
print('Window errors:', res20)

ws.close()
