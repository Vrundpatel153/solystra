import asyncio
import json
import urllib.request
import websockets
import base64
import os

ARTIFACT_DIR = r"C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals"
os.makedirs(ARTIFACT_DIR, exist_ok=True)

async def verify_compact():
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
        # 1. DESKTOP VERIFICATION (1440 x 900)
        # ==========================================
        await call('Emulation.clearDeviceMetricsOverride')
        await call('Emulation.setDeviceMetricsOverride', {
            'width': 1440,
            'height': 900,
            'deviceScaleFactor': 1,
            'mobile': False
        })
        await call('Page.navigate', {'url': 'http://127.0.0.1:8095/index.html?v=compact_' + str(int(asyncio.get_event_loop().time()))})
        await asyncio.sleep(2.0)

        # Slide 1 Desktop
        await call('Runtime.evaluate', {
            'expression': """(() => {
                const sec = document.getElementById('curated-looks-section');
                const dot = document.querySelectorAll('#curated-combo-dots button')[0];
                if (dot) dot.click();
                if (window.comboTimer) clearInterval(window.comboTimer);
                window.scrollTo(0, sec.offsetTop);
            })()"""
        })
        await asyncio.sleep(0.8)

        stats1_pc = await call('Runtime.evaluate', {
            'expression': """(() => {
                const sec = document.getElementById('curated-looks-section');
                const left = document.getElementById('combo-left-col');
                const right = document.getElementById('combo-right-col');
                const pins = Array.from(document.querySelectorAll('.combo-hotspot-pin')).map(pin => {
                    const r = pin.getBoundingClientRect();
                    const lr = left.getBoundingClientRect();
                    return {
                        id: pin.getAttribute('data-hotspot-id'),
                        pctX: ((r.left + r.width/2 - lr.left) / lr.width * 100).toFixed(1) + '%',
                        pctY: ((r.top + r.height/2 - lr.top) / lr.height * 100).toFixed(1) + '%'
                    };
                });
                return {
                    sectionH: sec.offsetHeight,
                    leftW: left.offsetWidth,
                    leftH: left.offsetHeight,
                    leftRatio: (left.offsetWidth / left.offsetHeight).toFixed(3),
                    rightW: right.offsetWidth,
                    rightH: right.offsetHeight,
                    pins: pins
                };
            })()""",
            'returnByValue': True
        })
        print("Desktop Slide 1 stats:", json.dumps(stats1_pc['result']['value'], indent=2))

        # Capture Desktop Slide 1
        sec_box = await call('Runtime.evaluate', {
            'expression': """(() => {
                const sec = document.getElementById('curated-looks-section');
                const r = sec.getBoundingClientRect();
                return { top: r.top, height: r.height, width: r.width };
            })()""",
            'returnByValue': True
        })
        b1 = sec_box['result']['value']
        shot1 = await call('Page.captureScreenshot', {
            'format': 'png',
            'clip': { 'x': 0, 'y': max(0, b1['top']), 'width': 1440, 'height': b1['height'], 'scale': 1 }
        })
        with open(os.path.join(ARTIFACT_DIR, "compact_desktop_slide1.png"), "wb") as f:
            f.write(base64.b64decode(shot1['data']))

        # Switch to Slide 2 Desktop
        await call('Runtime.evaluate', {
            'expression': """(() => {
                const dot = document.querySelectorAll('#curated-combo-dots button')[1];
                if (dot) dot.click();
            })()"""
        })
        await asyncio.sleep(0.8)

        stats2_pc = await call('Runtime.evaluate', {
            'expression': """(() => {
                const left = document.getElementById('combo-left-col');
                const right = document.getElementById('combo-right-col');
                const pins = Array.from(document.querySelectorAll('.combo-hotspot-pin')).map(pin => {
                    const r = pin.getBoundingClientRect();
                    const lr = left.getBoundingClientRect();
                    return {
                        id: pin.getAttribute('data-hotspot-id'),
                        pctX: ((r.left + r.width/2 - lr.left) / lr.width * 100).toFixed(1) + '%',
                        pctY: ((r.top + r.height/2 - lr.top) / lr.height * 100).toFixed(1) + '%'
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
        print("Desktop Slide 2 stats:", json.dumps(stats2_pc['result']['value'], indent=2))

        shot2 = await call('Page.captureScreenshot', {
            'format': 'png',
            'clip': { 'x': 0, 'y': max(0, b1['top']), 'width': 1440, 'height': b1['height'], 'scale': 1 }
        })
        with open(os.path.join(ARTIFACT_DIR, "compact_desktop_slide2.png"), "wb") as f:
            f.write(base64.b64decode(shot2['data']))

        # ==========================================
        # 2. MOBILE VERIFICATION (390 x 844)
        # ==========================================
        await call('Emulation.clearDeviceMetricsOverride')
        await call('Emulation.setDeviceMetricsOverride', {
            'width': 390,
            'height': 844,
            'deviceScaleFactor': 2,
            'mobile': True
        })
        await call('Page.navigate', {'url': 'http://127.0.0.1:8095/index.html?v=compact_mob_' + str(int(asyncio.get_event_loop().time()))})
        await asyncio.sleep(2.0)

        # Slide 1 Mobile
        await call('Runtime.evaluate', {
            'expression': """(() => {
                const sec = document.getElementById('curated-looks-section');
                const dot = document.querySelectorAll('#curated-combo-dots button')[0];
                if (dot) dot.click();
                if (window.comboTimer) clearInterval(window.comboTimer);
                window.scrollTo(0, sec.offsetTop);
            })()"""
        })
        await asyncio.sleep(0.8)

        stats1_mob = await call('Runtime.evaluate', {
            'expression': """(() => {
                const left = document.getElementById('combo-left-col');
                const right = document.getElementById('combo-right-col');
                const pins = Array.from(document.querySelectorAll('.combo-hotspot-pin')).map(pin => {
                    const r = pin.getBoundingClientRect();
                    const lr = left.getBoundingClientRect();
                    return {
                        id: pin.getAttribute('data-hotspot-id'),
                        pctX: ((r.left + r.width/2 - lr.left) / lr.width * 100).toFixed(1) + '%',
                        pctY: ((r.top + r.height/2 - lr.top) / lr.height * 100).toFixed(1) + '%'
                    };
                });
                return {
                    leftW: left.offsetWidth,
                    leftH: left.offsetHeight,
                    leftRatio: (left.offsetWidth / left.offsetHeight).toFixed(3),
                    rightH: right.offsetHeight,
                    pins: pins
                };
            })()""",
            'returnByValue': True
        })
        print("Mobile Slide 1 stats:", json.dumps(stats1_mob['result']['value'], indent=2))

        shot_mob1 = await call('Page.captureScreenshot', {
            'format': 'png',
            'clip': { 'x': 0, 'y': 0, 'width': 390, 'height': 844, 'scale': 2 }
        })
        with open(os.path.join(ARTIFACT_DIR, "compact_mobile_slide1.png"), "wb") as f:
            f.write(base64.b64decode(shot_mob1['data']))

        # Slide 2 Mobile
        await call('Runtime.evaluate', {
            'expression': """(() => {
                const dot = document.querySelectorAll('#curated-combo-dots button')[1];
                if (dot) dot.click();
            })()"""
        })
        await asyncio.sleep(0.8)

        stats2_mob = await call('Runtime.evaluate', {
            'expression': """(() => {
                const left = document.getElementById('combo-left-col');
                const pins = Array.from(document.querySelectorAll('.combo-hotspot-pin')).map(pin => {
                    const r = pin.getBoundingClientRect();
                    const lr = left.getBoundingClientRect();
                    return {
                        id: pin.getAttribute('data-hotspot-id'),
                        pctX: ((r.left + r.width/2 - lr.left) / lr.width * 100).toFixed(1) + '%',
                        pctY: ((r.top + r.height/2 - lr.top) / lr.height * 100).toFixed(1) + '%'
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
        print("Mobile Slide 2 stats:", json.dumps(stats2_mob['result']['value'], indent=2))

        shot_mob2 = await call('Page.captureScreenshot', {
            'format': 'png',
            'clip': { 'x': 0, 'y': 0, 'width': 390, 'height': 844, 'scale': 2 }
        })
        with open(os.path.join(ARTIFACT_DIR, "compact_mobile_slide2.png"), "wb") as f:
            f.write(base64.b64decode(shot_mob2['data']))

        print("\nAll compact verification screenshots captured!")

asyncio.run(verify_compact())

