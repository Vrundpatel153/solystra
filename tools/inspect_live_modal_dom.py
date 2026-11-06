import asyncio
import json
import urllib.request
import websockets

async def send_cmd(ws, msg_id, method, params=None):
    payload = {'id': msg_id, 'method': method}
    if params:
        payload['params'] = params
    await ws.send(json.dumps(payload))
    while True:
        resp = json.loads(await ws.recv())
        if resp.get('id') == msg_id:
            return resp

async def main():
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(req.read().decode('utf-8'))
    tab = next(t for t in tabs if t.get('type') == 'page' and '8080' in t.get('url', ''))
    
    async with websockets.connect(tab.get('webSocketDebuggerUrl'), max_size=30*1024*1024) as ws:
        msg_id = 1
        res = await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': '''
            (() => {
                const m = document.getElementById('mobile-filter-modal');
                if (!m) return "NO MODAL ELEMENT IN DOM";
                return m.outerHTML;
            })()
        '''})
        html = res['result']['result']['value']
        print("Modal outerHTML length:", len(html))
        # Print first 1500 chars
        print(html[:1500])

asyncio.run(main())
