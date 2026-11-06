import asyncio
import json
import urllib.request
import websockets

async def check_header():
    req = urllib.request.urlopen('http://127.0.0.1:9222/json')
    tabs = json.loads(req.read())
    ws_url = [t['webSocketDebuggerUrl'] for t in tabs if t.get('type') == 'page'][0]
    async with websockets.connect(ws_url) as ws:
        msg_id = 1
        async def send(method, params=None):
            nonlocal msg_id
            m = {'id': msg_id, 'method': method}
            if params: m['params'] = params
            await ws.send(json.dumps(m))
            cur = msg_id
            msg_id += 1
            while True:
                r = json.loads(await ws.recv())
                if r.get('id') == cur:
                    return r.get('result', {}).get('result', {}).get('value')

        await send('Page.navigate', {'url': 'http://localhost:8080/index.html'})
        await asyncio.sleep(1.0)
        
        # Desktop
        await send('Emulation.setDeviceMetricsOverride', {'width': 1440, 'height': 900, 'deviceScaleFactor': 1, 'mobile': False})
        res_d = await send('Runtime.evaluate', {
            'expression': 'JSON.stringify({ headerBottom: document.querySelector("header").getBoundingClientRect().bottom, heroWrapH: document.querySelector(".solystra-hero-wrap").offsetHeight, winH: window.innerHeight })',
            'returnByValue': True
        })
        print('Desktop metrics:', res_d)

        # Mobile
        await send('Emulation.setDeviceMetricsOverride', {'width': 390, 'height': 844, 'deviceScaleFactor': 2, 'mobile': True})
        res_m = await send('Runtime.evaluate', {
            'expression': 'JSON.stringify({ headerBottom: document.querySelector("header").getBoundingClientRect().bottom, heroWrapH: document.querySelector(".solystra-hero-wrap").offsetHeight, winH: window.innerHeight })',
            'returnByValue': True
        })
        print('Mobile metrics:', res_m)

asyncio.run(check_header())
