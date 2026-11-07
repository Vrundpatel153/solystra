import urllib.request
import json
import asyncio
import websockets

async def check():
    req = urllib.request.urlopen('http://127.0.0.1:9222/json')
    tabs = json.loads(req.read().decode())
    p = [t for t in tabs if t.get('type') == 'page'][0]
    
    async with websockets.connect(p['webSocketDebuggerUrl'], max_size=50*1024*1024) as ws:
        msg_id = 1
        async def call(method, params=None):
            nonlocal msg_id
            msg_id += 1
            payload = {"id": msg_id, "method": method, "params": params or {}}
            await ws.send(json.dumps(payload))
            while True:
                res = json.loads(await ws.recv())
                if res.get('id') == msg_id:
                    return res

        res = await call('Runtime.evaluate', {
            'expression': """(() => {
                const btn = document.querySelector('#hero-slide-1 button');
                const rect = btn.getBoundingClientRect();
                return {
                    text: btn.innerText.trim(),
                    padding: getComputedStyle(btn).padding,
                    rect: {x: Math.round(rect.x), y: Math.round(rect.y), width: Math.round(rect.width), height: Math.round(rect.height)}
                };
            })()""",
            'returnByValue': True
        })
        print(json.dumps(res, indent=2))

asyncio.run(check())

