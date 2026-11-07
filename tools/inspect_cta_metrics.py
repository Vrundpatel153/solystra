import urllib.request
import json
import asyncio
import websockets

async def inspect():
    req = urllib.request.urlopen('http://127.0.0.1:9222/json')
    tabs = json.loads(req.read().decode())
    p = [t for t in tabs if t.get('type') == 'page'][0]
    async with websockets.connect(p['webSocketDebuggerUrl'], max_size=50*1024*1024) as ws:
        msg_id = 1
        async def send(method, params=None):
            nonlocal msg_id
            payload = {'id': msg_id, 'method': method}
            if params:
                payload['params'] = params
            msg_id += 1
            await ws.send(json.dumps(payload))
            while True:
                resp = json.loads(await ws.recv())
                if resp.get('id') == payload['id']:
                    return resp

        # Check mobile (390x844)
        await send('Emulation.setDeviceMetricsOverride', {
            'width': 390,
            'height': 844,
            'deviceScaleFactor': 2,
            'mobile': True
        })
        await send('Page.navigate', {'url': 'http://127.0.0.1:8095/index.html'})
        await asyncio.sleep(1.5)

        res = await send('Runtime.evaluate', {'expression': '''(() => {
            function rect(el) {
                if (!el) return null;
                const r = el.getBoundingClientRect();
                return { top: Math.round(r.top), bottom: Math.round(r.bottom), left: Math.round(r.left), right: Math.round(r.right), width: Math.round(r.width), height: Math.round(r.height) };
            }
            const dots = document.querySelector('.absolute.bottom-4.inset-x-0');
            const data = {
                dots: rect(dots),
                slides: []
            };
            
            for (let i = 0; i < 4; i++) {
                const slide = document.querySelector(`#hero-slide-${i}`);
                if (!slide) continue;
                const h2 = slide.querySelector('h2');
                const p = slide.querySelector('p');
                const btn = slide.querySelector('button');
                const span = slide.querySelector('span');
                const txtWrap = slide.querySelector('.max-w-xl');
                
                data.slides.push({
                    slide: i,
                    tag: rect(span),
                    h2: rect(h2),
                    p: rect(p),
                    btn: rect(btn),
                    txtWrap: rect(txtWrap)
                });
            }
            return data;
        })()''', 'returnByValue': True})
        
        print("Mobile Metrics:")
        print(json.dumps(res.get('result', {}).get('result', {}).get('value'), indent=2))

if __name__ == '__main__':
    asyncio.run(inspect())
