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
    tab = [t for t in tabs if t.get('type') == 'page'][0]
    
    async with websockets.connect(tab.get('webSocketDebuggerUrl'), max_size=30*1024*1024) as ws:
        msg_id = 1
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {'width': 390, 'height': 844, 'deviceScaleFactor': 1, 'mobile': True})
        msg_id += 1
        await asyncio.sleep(0.5)
        
        res = await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': '''
            (() => {
                window.openMobileFilterModal();
                const m = document.getElementById('mobile-filter-modal');
                const card = m ? m.children[0] : null;
                const header = card ? card.children[0] : null;
                const closeBtn = header ? header.querySelector('button') : null;
                return JSON.stringify({
                    windowInnerWidth: window.innerWidth,
                    documentClientWidth: document.documentElement.clientWidth,
                    modalRect: m ? m.getBoundingClientRect() : null,
                    cardRect: card ? card.getBoundingClientRect() : null,
                    headerRect: header ? header.getBoundingClientRect() : null,
                    closeBtnRect: closeBtn ? closeBtn.getBoundingClientRect() : null
                }, null, 2);
            })()
        '''})
        print("Mobile measurements:\n", res['result']['result']['value'])

asyncio.run(main())
