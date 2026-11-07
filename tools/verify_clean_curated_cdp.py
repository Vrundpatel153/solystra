import asyncio
import json
import urllib.request
import websockets
import base64
import os

ARTIFACT_DIR = r"C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals"
os.makedirs(ARTIFACT_DIR, exist_ok=True)

async def verify_clean():
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
        # 1. DESKTOP (1440 x 900)
        # -------------------------------------------------------------
        await call('Emulation.clearDeviceMetricsOverride')
        await call('Emulation.setDeviceMetricsOverride', {
            'width': 1440,
            'height': 900,
            'deviceScaleFactor': 1,
            'mobile': False
        })
        await call('Page.navigate', {'url': 'http://127.0.0.1:8095/index.html?v=clean_luxury_' + str(int(asyncio.get_event_loop().time()))})
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

        stats_d1 = await call('Runtime.evaluate', {
            'expression': """(() => {
                const left = document.getElementById('combo-left-col');
                const right = document.getElementById('combo-right-col');
                const pins = Array.from(document.querySelectorAll('.combo-hotspot-pin')).map(p => {
                    const r = p.getBoundingClientRect();
                    const lr = left.getBoundingClientRect();
                    return {
                        id: p.getAttribute('data-hotspot-id'),
                        pctX: ((r.left + r.width/2 - lr.left)/lr.width*100).toFixed(1) + '%',
                        pctY: ((r.top + r.height/2 - lr.top)/lr.height*100).toFixed(1) + '%'
                    };
                });
                return {
                    leftW: left.offsetWidth,
                    leftH: left.offsetHeight,
                    rightW: right.offsetWidth,
                    rightH: right.offsetHeight,
                    pins: pins
                };
            })()""",
            'returnByValue': True
        })
        print("Desktop Slide 1 stats:", json.dumps(stats_d1['result']['value'], indent=2))

        shot_d1 = await call('Page.captureScreenshot', {'format': 'jpeg', 'quality': 95})
        with open(os.path.join(ARTIFACT_DIR, "clean_desktop_slide1.jpg"), "wb") as f:
            f.write(base64.b64decode(shot_d1['data']))

        # Switch to Slide 2 Desktop (Golden Meadow)
        await call('Runtime.evaluate', {
            'expression': """(() => {
                const dot = document.querySelectorAll('#curated-combo-dots button')[1];
                if (dot) dot.click();
            })()"""
        })
        await asyncio.sleep(0.8)

        stats_d2 = await call('Runtime.evaluate', {
            'expression': """(() => {
                const left = document.getElementById('combo-left-col');
                const right = document.getElementById('combo-right-col');
                const pins = Array.from(document.querySelectorAll('.combo-hotspot-pin')).map(p => {
                    const r = p.getBoundingClientRect();
                    const lr = left.getBoundingClientRect();
                    return {
                        id: p.getAttribute('data-hotspot-id'),
                        pctX: ((r.left + r.width/2 - lr.left)/lr.width*100).toFixed(1) + '%',
                        pctY: ((r.top + r.height/2 - lr.top)/lr.height*100).toFixed(1) + '%'
                    };
                });
                return {
                    leftW: left.offsetWidth,
                    leftH: left.offsetHeight,
                    rightW: right.offsetWidth,
                    rightH: right.offsetHeight,
                    pins: pins
                };
            })()""",
            'returnByValue': True
        })
        print("Desktop Slide 2 stats:", json.dumps(stats_d2['result']['value'], indent=2))

        shot_d2 = await call('Page.captureScreenshot', {'format': 'jpeg', 'quality': 95})
        with open(os.path.join(ARTIFACT_DIR, "clean_desktop_slide2.jpg"), "wb") as f:
            f.write(base64.b64decode(shot_d2['data']))

        # -------------------------------------------------------------
        # 2. MOBILE (390 x 844)
        # -------------------------------------------------------------
        await call('Emulation.clearDeviceMetricsOverride')
        await call('Emulation.setDeviceMetricsOverride', {
            'width': 390,
            'height': 844,
            'deviceScaleFactor': 2,
            'mobile': True
        })
        await call('Page.navigate', {'url': 'http://127.0.0.1:8095/index.html?v=clean_mob_' + str(int(asyncio.get_event_loop().time()))})
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

        stats_m1 = await call('Runtime.evaluate', {
            'expression': """(() => {
                const left = document.getElementById('combo-left-col');
                const pins = Array.from(document.querySelectorAll('.combo-hotspot-pin')).map(p => {
                    const r = p.getBoundingClientRect();
                    const lr = left.getBoundingClientRect();
                    return {
                        id: p.getAttribute('data-hotspot-id'),
                        pctX: ((r.left + r.width/2 - lr.left)/lr.width*100).toFixed(1) + '%',
                        pctY: ((r.top + r.height/2 - lr.top)/lr.height*100).toFixed(1) + '%'
                    };
                });
                return {
                    leftW: left.offsetWidth,
                    leftH: left.offsetHeight,
                    pins: pins
                };
            })()""",
            'returnByValue': True
        })
        print("Mobile Slide 1 stats:", json.dumps(stats_m1['result']['value'], indent=2))

        shot_m1 = await call('Page.captureScreenshot', {'format': 'jpeg', 'quality': 90})
        with open(os.path.join(ARTIFACT_DIR, "clean_mobile_slide1.jpg"), "wb") as f:
            f.write(base64.b64decode(shot_m1['data']))

        # Slide 2 Mobile
        await call('Runtime.evaluate', {
            'expression': """(() => {
                const dot = document.querySelectorAll('#curated-combo-dots button')[1];
                if (dot) dot.click();
            })()"""
        })
        await asyncio.sleep(0.8)

        stats_m2 = await call('Runtime.evaluate', {
            'expression': """(() => {
                const left = document.getElementById('combo-left-col');
                const pins = Array.from(document.querySelectorAll('.combo-hotspot-pin')).map(p => {
                    const r = p.getBoundingClientRect();
                    const lr = left.getBoundingClientRect();
                    return {
                        id: p.getAttribute('data-hotspot-id'),
                        pctX: ((r.left + r.width/2 - lr.left)/lr.width*100).toFixed(1) + '%',
                        pctY: ((r.top + r.height/2 - lr.top)/lr.height*100).toFixed(1) + '%'
                    };
                });
                return {
                    leftW: left.offsetWidth,
                    leftH: left.offsetHeight,
                    pins: pins
                };
            })()""",
            'returnByValue': True
        })
        print("Mobile Slide 2 stats:", json.dumps(stats_m2['result']['value'], indent=2))

        shot_m2 = await call('Page.captureScreenshot', {'format': 'jpeg', 'quality': 90})
        with open(os.path.join(ARTIFACT_DIR, "clean_mobile_slide2.jpg"), "wb") as f:
            f.write(base64.b64decode(shot_m2['data']))

        print("\nAll clean verification screenshots captured successfully!")

asyncio.run(verify_clean())

