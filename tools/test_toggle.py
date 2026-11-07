import urllib.request
import json
import asyncio
import websockets
import base64
import os
import shutil

ARTIFACT_DIR = r"C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals"

async def test():
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

        # Set desktop viewport
        await send('Emulation.setDeviceMetricsOverride', {
            'width': 1440,
            'height': 900,
            'deviceScaleFactor': 1,
            'mobile': False
        })

        # Navigate to dist
        await send('Page.navigate', {'url': 'http://127.0.0.1:8095/index.html?v=navfix2026'})
        await asyncio.sleep(2.5)

        # 1. Open Collections dropdown
        print("Opening Collections dropdown...")
        await send('Runtime.evaluate', {'expression': 'window.toggleCollectionsMenu()'})
        await asyncio.sleep(0.8)
        await capture("nav_dropdown_opened.jpg")

        # 2. Click 925 Silver accordion
        print("Clicking 925 Silver accordion...")
        await send('Runtime.evaluate', {'expression': 'window.toggleCategoryDropdown("desktop-silver")'})
        await asyncio.sleep(0.8)
        await capture("nav_silver_accordion_expanded.jpg")

        # 3. Click 18K Gold accordion (should close Silver and open Gold)
        print("Clicking 18K Gold accordion...")
        await send('Runtime.evaluate', {'expression': 'window.toggleCategoryDropdown("desktop-gold")'})
        await asyncio.sleep(0.8)
        await capture("nav_gold_accordion_expanded.jpg")

        # 4. Mobile Viewport test
        print("Testing Mobile Viewport (390x844)...")
        await send('Emulation.setDeviceMetricsOverride', {
            'width': 390,
            'height': 844,
            'deviceScaleFactor': 2,
            'mobile': True
        })
        await asyncio.sleep(0.8)

        # In mobile, open mobile collections menu
        await send('Runtime.evaluate', {'expression': 'window.toggleCategoryDropdown("mob-silver")'})
        await asyncio.sleep(0.8)
        await capture("nav_mobile_silver_accordion.jpg")

        await send('Runtime.evaluate', {'expression': 'window.toggleCategoryDropdown("mob-gold")'})
        await asyncio.sleep(0.8)
        await capture("nav_mobile_gold_accordion.jpg")

        # Restore
        await send('Emulation.setDeviceMetricsOverride', {
            'width': 1440,
            'height': 900,
            'deviceScaleFactor': 1,
            'mobile': False
        })
        print("Nav test complete!")

if __name__ == '__main__':
    asyncio.run(test())
