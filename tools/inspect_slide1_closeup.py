import urllib.request
import json
import asyncio
import websockets
import base64
import os
import shutil

ARTIFACT_DIR = r"C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals"

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

        async def capture(filename):
            shot = await send('Page.captureScreenshot', {'format': 'jpeg', 'quality': 85})
            data = base64.b64decode(shot['result']['data'])
            local_p = os.path.join("audit_visuals", filename)
            with open(local_p, "wb") as f:
                f.write(data)
            shutil.copy(local_p, os.path.join(ARTIFACT_DIR, filename))
            print(f"Captured: {filename} ({len(data)} bytes)")

        # Mobile 390x844
        await send('Emulation.setDeviceMetricsOverride', {
            'width': 390,
            'height': 844,
            'deviceScaleFactor': 2,
            'mobile': True
        })
        await send('Page.navigate', {'url': 'http://127.0.0.1:8095/index.html'})
        await asyncio.sleep(1.5)

        # Switch to slide 1
        await send('Runtime.evaluate', {'expression': 'window.setHeroSlide(1)'})
        await asyncio.sleep(0.8)

        # Get computed styles of slide 1 text & button
        info = await send('Runtime.evaluate', {'expression': '''(() => {
            const s1 = document.querySelector('#hero-slide-1');
            const h2 = s1.querySelector('h2');
            const p = s1.querySelector('p');
            const btn = s1.querySelector('button');
            const span = btn ? btn.querySelector('span') : null;
            const svg = btn ? btn.querySelector('svg') : null;
            const btnWrap = s1.querySelector('.mt-3\\\\.5, .mt-3, .mt-9');
            
            return {
                h2Style: {
                    color: getComputedStyle(h2).color,
                    fontSize: getComputedStyle(h2).fontSize,
                    textShadow: getComputedStyle(h2).textShadow,
                    filter: getComputedStyle(h2).filter
                },
                pStyle: {
                    color: getComputedStyle(p).color,
                    fontSize: getComputedStyle(p).fontSize,
                    textShadow: getComputedStyle(p).textShadow,
                    filter: getComputedStyle(p).filter
                },
                btnStyle: {
                    display: getComputedStyle(btn).display,
                    alignItems: getComputedStyle(btn).alignItems,
                    padding: getComputedStyle(btn).padding,
                    height: getComputedStyle(btn).height,
                    lineHeight: getComputedStyle(btn).lineHeight
                },
                spanRect: span ? span.getBoundingClientRect() : null,
                svgRect: svg ? svg.getBoundingClientRect() : null,
                btnRect: btn ? btn.getBoundingClientRect() : null
            };
        })()''', 'returnByValue': True})
        print("Slide 1 Styles & Rects:", json.dumps(info.get('result', {}).get('result', {}).get('value'), indent=2))

        await capture("slide1_current_closeup.jpg")

if __name__ == '__main__':
    asyncio.run(inspect())

