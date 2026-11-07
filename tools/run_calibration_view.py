import asyncio
import json
import urllib.request
import websockets
import base64

async def calibrate():
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
        await call('Page.navigate', {'url': 'http://127.0.0.1:8095/calibrate_hotspots.html'})
        await asyncio.sleep(2.0)

        shot = await call('Page.captureScreenshot', {'format': 'jpeg', 'quality': 85})
        with open("C:/Users/vrund/.gemini/antigravity/brain/68f27351-9b2c-41bf-b75f-ce5ad9262a98/audit_visuals/calibration_overview.jpg", "wb") as f:
            f.write(base64.b64decode(shot['data']))
        print("Captured calibration_overview.jpg")

asyncio.run(calibrate())

