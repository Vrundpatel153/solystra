import asyncio
import json
import urllib.request
import websockets
import base64

async def test_calib_v2():
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

        await call('Emulation.clearDeviceMetricsOverride')
        await call('Emulation.setDeviceMetricsOverride', {
            'width': 1440,
            'height': 900,
            'deviceScaleFactor': 1,
            'mobile': False
        })
        await call('Network.enable')
        await call('Network.setCacheDisabled', {'cacheDisabled': True})
        await call('Page.navigate', {'url': 'http://127.0.0.1:8095/calibrate_hotspots.html?v=3'})
        await asyncio.sleep(2.0)

        # Capture top section
        shot1 = await call('Page.captureScreenshot', {'format': 'jpeg', 'quality': 85})
        with open("scratch/calib_v2_top.jpg", "wb") as f:
            f.write(base64.b64decode(shot1['data']))

        # Scroll down to GM section
        await call('Runtime.evaluate', {'expression': 'window.scrollTo(0, 600);'})
        await asyncio.sleep(0.5)

        shot2 = await call('Page.captureScreenshot', {'format': 'jpeg', 'quality': 85})
        with open("scratch/calib_v2_bottom.jpg", "wb") as f:
            f.write(base64.b64decode(shot2['data']))

        print("Captured calib_v2_top.jpg and calib_v2_bottom.jpg")

asyncio.run(test_calib_v2())

