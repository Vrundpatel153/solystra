import asyncio
import json
import urllib.request
import websockets
import base64
import os

ARTIFACT_DIR = r"C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals"
os.makedirs(ARTIFACT_DIR, exist_ok=True)

async def capture_showcase():
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

        # Disable cache
        await call('Network.enable')
        await call('Network.setCacheDisabled', {'cacheDisabled': True})

        # -------------------------------------------------------------
        # 1. DESKTOP VIEWPORT (1440 x 950)
        # -------------------------------------------------------------
        await call('Emulation.clearDeviceMetricsOverride')
        await call('Emulation.setDeviceMetricsOverride', {
            'width': 1440,
            'height': 950,
            'deviceScaleFactor': 1,
            'mobile': False
        })
        await call('Page.navigate', {'url': 'http://127.0.0.1:8095/index.html?v=showcase_' + str(int(asyncio.get_event_loop().time()))})
        await asyncio.sleep(2.0)

        # Slide 1 Desktop
        await call('Runtime.evaluate', {
            'expression': """(() => {
                const sec = document.getElementById('curated-looks-section');
                if (sec) sec.scrollIntoView({ behavior: 'instant', block: 'start' });
                if (window.comboTimer) clearInterval(window.comboTimer);
                const dot = document.querySelectorAll('#curated-combo-dots button')[0];
                if (dot) dot.click();
            })()"""
        })
        await asyncio.sleep(0.8)

        # Get bounding box of curated section
        box_d1 = await call('Runtime.evaluate', {
            'expression': """(() => {
                const sec = document.getElementById('curated-looks-section');
                const r = sec.getBoundingClientRect();
                return { x: r.left, y: r.top, width: r.width, height: r.height };
            })()""",
            'returnByValue': True
        })
        b1 = box_d1['result']['value']
        shot1 = await call('Page.captureScreenshot', {
            'format': 'png',
            'clip': { 'x': max(0, b1['x']), 'y': max(0, b1['y']), 'width': b1['width'], 'height': b1['height'], 'scale': 1 }
        })
        with open(os.path.join(ARTIFACT_DIR, "showcase_desktop_slide1.png"), "wb") as f:
            f.write(base64.b64decode(shot1['data']))

        # Slide 2 Desktop
        await call('Runtime.evaluate', {
            'expression': """(() => {
                const dot = document.querySelectorAll('#curated-combo-dots button')[1];
                if (dot) dot.click();
            })()"""
        })
        await asyncio.sleep(0.8)

        box_d2 = await call('Runtime.evaluate', {
            'expression': """(() => {
                const sec = document.getElementById('curated-looks-section');
                const r = sec.getBoundingClientRect();
                return { x: r.left, y: r.top, width: r.width, height: r.height };
            })()""",
            'returnByValue': True
        })
        b2 = box_d2['result']['value']
        shot2 = await call('Page.captureScreenshot', {
            'format': 'png',
            'clip': { 'x': max(0, b2['x']), 'y': max(0, b2['y']), 'width': b2['width'], 'height': b2['height'], 'scale': 1 }
        })
        with open(os.path.join(ARTIFACT_DIR, "showcase_desktop_slide2.png"), "wb") as f:
            f.write(base64.b64decode(shot2['data']))

        # -------------------------------------------------------------
        # 2. MOBILE VIEWPORT (390 x 844, scale 2)
        # -------------------------------------------------------------
        await call('Emulation.clearDeviceMetricsOverride')
        await call('Emulation.setDeviceMetricsOverride', {
            'width': 390,
            'height': 844,
            'deviceScaleFactor': 2,
            'mobile': True
        })
        await call('Page.navigate', {'url': 'http://127.0.0.1:8095/index.html?v=mob_' + str(int(asyncio.get_event_loop().time()))})
        await asyncio.sleep(2.0)

        # Slide 1 Mobile
        await call('Runtime.evaluate', {
            'expression': """(() => {
                const sec = document.getElementById('curated-looks-section');
                if (sec) sec.scrollIntoView({ behavior: 'instant', block: 'start' });
                if (window.comboTimer) clearInterval(window.comboTimer);
                const dot = document.querySelectorAll('#curated-combo-dots button')[0];
                if (dot) dot.click();
            })()"""
        })
        await asyncio.sleep(0.8)

        box_m1 = await call('Runtime.evaluate', {
            'expression': """(() => {
                const sec = document.getElementById('curated-looks-section');
                const r = sec.getBoundingClientRect();
                return { x: r.left, y: r.top, width: r.width, height: r.height };
            })()""",
            'returnByValue': True
        })
        bm1 = box_m1['result']['value']
        shot_m1 = await call('Page.captureScreenshot', {
            'format': 'png',
            'clip': { 'x': max(0, bm1['x']), 'y': max(0, bm1['y']), 'width': bm1['width'], 'height': bm1['height'], 'scale': 2 }
        })
        with open(os.path.join(ARTIFACT_DIR, "showcase_mobile_slide1.png"), "wb") as f:
            f.write(base64.b64decode(shot_m1['data']))

        # Slide 2 Mobile
        await call('Runtime.evaluate', {
            'expression': """(() => {
                const dot = document.querySelectorAll('#curated-combo-dots button')[1];
                if (dot) dot.click();
            })()"""
        })
        await asyncio.sleep(0.8)

        box_m2 = await call('Runtime.evaluate', {
            'expression': """(() => {
                const sec = document.getElementById('curated-looks-section');
                const r = sec.getBoundingClientRect();
                return { x: r.left, y: r.top, width: r.width, height: r.height };
            })()""",
            'returnByValue': True
        })
        bm2 = box_m2['result']['value']
        shot_m2 = await call('Page.captureScreenshot', {
            'format': 'png',
            'clip': { 'x': max(0, bm2['x']), 'y': max(0, bm2['y']), 'width': bm2['width'], 'height': bm2['height'], 'scale': 2 }
        })
        with open(os.path.join(ARTIFACT_DIR, "showcase_mobile_slide2.png"), "wb") as f:
            f.write(base64.b64decode(shot_m2['data']))

        print("Showcase element screenshots saved successfully!")

asyncio.run(capture_showcase())

