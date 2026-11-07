import asyncio
import json
import urllib.request
import websockets
import base64
import os

ARTIFACT_DIR = r"C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals"
os.makedirs(ARTIFACT_DIR, exist_ok=True)

async def verify():
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

        # ==========================================
        # 1. MOBILE VERIFICATION (390 x 844)
        # ==========================================
        await call('Emulation.clearDeviceMetricsOverride')
        await call('Emulation.setDeviceMetricsOverride', {
            'width': 390,
            'height': 844,
            'deviceScaleFactor': 2,
            'mobile': True
        })
        await call('Page.navigate', {'url': 'http://127.0.0.1:8095/index.html?v=' + str(int(asyncio.get_event_loop().time()))})
        await asyncio.sleep(2.0)

        # Scroll to curated section and pause timer
        await call('Runtime.evaluate', {
            'expression': """(() => {
                const sec = document.getElementById('curated-looks-section');
                if (sec) sec.scrollIntoView({ behavior: 'instant', block: 'center' });
                // stop auto timer for deterministic audit
                if (window.comboTimer) clearInterval(window.comboTimer);
            })()"""
        })
        await asyncio.sleep(0.8)

        # Slide 1 (Combo 0): Classic Solitaire Set
        slide1_mob = await call('Runtime.evaluate', {
            'expression': """(() => {
                const dots = document.querySelectorAll('.combo-hotspot-pin');
                const counter = document.getElementById('curated-combo-counter');
                const title = document.querySelector('#combo-left-col h3');
                return {
                    counter: counter ? counter.innerText : '',
                    title: title ? title.innerText : '',
                    dotCount: dots.length,
                    dots: Array.from(dots).map(d => ({
                        id: d.getAttribute('data-hotspot-id'),
                        style: d.getAttribute('style')
                    }))
                };
            })()""",
            'returnByValue': True
        })
        print("Mobile Slide 1 info:", json.dumps(slide1_mob.get('result', {}).get('value', {}), indent=2))

        # Screenshot Slide 1 Mobile
        shot = await call('Page.captureScreenshot', {'format': 'jpeg', 'quality': 85})
        with open(os.path.join(ARTIFACT_DIR, "curated_slide1_mobile.jpg"), "wb") as f:
            f.write(base64.b64decode(shot['data']))

        # Switch to Slide 2 (Combo 1): Golden Meadow Set
        await call('Runtime.evaluate', {
            'expression': """(() => {
                const dotBtn = document.querySelectorAll('#curated-combo-dots button')[1];
                if (dotBtn) dotBtn.click();
            })()"""
        })
        await asyncio.sleep(0.8)

        slide2_mob = await call('Runtime.evaluate', {
            'expression': """(() => {
                const dots = document.querySelectorAll('.combo-hotspot-pin');
                const counter = document.getElementById('curated-combo-counter');
                const title = document.querySelector('#combo-left-col h3');
                return {
                    counter: counter ? counter.innerText : '',
                    title: title ? title.innerText : '',
                    dotCount: dots.length,
                    dots: Array.from(dots).map(d => ({
                        id: d.getAttribute('data-hotspot-id'),
                        style: d.getAttribute('style')
                    }))
                };
            })()""",
            'returnByValue': True
        })
        print("Mobile Slide 2 info:", json.dumps(slide2_mob.get('result', {}).get('value', {}), indent=2))

        # Screenshot Slide 2 Mobile
        shot = await call('Page.captureScreenshot', {'format': 'jpeg', 'quality': 85})
        with open(os.path.join(ARTIFACT_DIR, "curated_slide2_mobile.jpg"), "wb") as f:
            f.write(base64.b64decode(shot['data']))

        # ==========================================
        # 2. DESKTOP VERIFICATION (1440 x 900)
        # ==========================================
        await call('Emulation.clearDeviceMetricsOverride')
        await call('Emulation.setDeviceMetricsOverride', {
            'width': 1440,
            'height': 900,
            'deviceScaleFactor': 1,
            'mobile': False
        })
        await call('Page.navigate', {'url': 'http://127.0.0.1:8095/index.html?v=pc_' + str(int(asyncio.get_event_loop().time()))})
        await asyncio.sleep(2.0)

        # Scroll to curated section and pause timer
        await call('Runtime.evaluate', {
            'expression': """(() => {
                const sec = document.getElementById('curated-looks-section');
                if (sec) sec.scrollIntoView({ behavior: 'instant', block: 'center' });
                if (window.comboTimer) clearInterval(window.comboTimer);
            })()"""
        })
        await asyncio.sleep(0.8)

        # Slide 1 Desktop
        slide1_pc = await call('Runtime.evaluate', {
            'expression': """(() => {
                const dots = document.querySelectorAll('.combo-hotspot-pin');
                const counter = document.getElementById('curated-combo-counter');
                const title = document.querySelector('#combo-left-col h3');
                return {
                    counter: counter ? counter.innerText : '',
                    title: title ? title.innerText : '',
                    dotCount: dots.length,
                    dots: Array.from(dots).map(d => ({
                        id: d.getAttribute('data-hotspot-id'),
                        style: d.getAttribute('style')
                    }))
                };
            })()""",
            'returnByValue': True
        })
        print("Desktop Slide 1 info:", json.dumps(slide1_pc.get('result', {}).get('value', {}), indent=2))

        # Screenshot Slide 1 Desktop
        shot = await call('Page.captureScreenshot', {'format': 'jpeg', 'quality': 85})
        with open(os.path.join(ARTIFACT_DIR, "curated_slide1_desktop.jpg"), "wb") as f:
            f.write(base64.b64decode(shot['data']))

        # Switch to Slide 2 Desktop
        await call('Runtime.evaluate', {
            'expression': """(() => {
                const dotBtn = document.querySelectorAll('#curated-combo-dots button')[1];
                if (dotBtn) dotBtn.click();
            })()"""
        })
        await asyncio.sleep(0.8)

        slide2_pc = await call('Runtime.evaluate', {
            'expression': """(() => {
                const dots = document.querySelectorAll('.combo-hotspot-pin');
                const counter = document.getElementById('curated-combo-counter');
                const title = document.querySelector('#combo-left-col h3');
                return {
                    counter: counter ? counter.innerText : '',
                    title: title ? title.innerText : '',
                    dotCount: dots.length,
                    dots: Array.from(dots).map(d => ({
                        id: d.getAttribute('data-hotspot-id'),
                        style: d.getAttribute('style')
                    }))
                };
            })()""",
            'returnByValue': True
        })
        print("Desktop Slide 2 info:", json.dumps(slide2_pc.get('result', {}).get('value', {}), indent=2))

        # Screenshot Slide 2 Desktop
        shot = await call('Page.captureScreenshot', {'format': 'jpeg', 'quality': 85})
        with open(os.path.join(ARTIFACT_DIR, "curated_slide2_desktop.jpg"), "wb") as f:
            f.write(base64.b64decode(shot['data']))

        print("\nAll 4 live verification screenshots captured successfully!")

asyncio.run(verify())

