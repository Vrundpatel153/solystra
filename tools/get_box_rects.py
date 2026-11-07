import asyncio
import json
import urllib.request
import websockets

async def get_box_rects():
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(req.read().decode())
    p = [t for t in tabs if t.get('type') == 'page' and '8095' in t.get('url', '')][0]
    
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
                    return res.get('result', {})

        res = await call('Runtime.evaluate', {
            'expression': """(() => {
                function r(id) {
                    const el = document.getElementById(id);
                    if (!el) return null;
                    const b = el.getBoundingClientRect();
                    return { x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height) };
                }
                return {
                    c2_mob: r('box-c2-mob'),
                    c2_pc: r('box-c2-pc'),
                    gm_mob: r('box-gm-mob'),
                    gm_pc: r('box-gm-pc')
                };
            })()""",
            'returnByValue': True
        })
        print(json.dumps(res.get('result', {}).get('value', {}), indent=2))

asyncio.run(get_box_rects())

