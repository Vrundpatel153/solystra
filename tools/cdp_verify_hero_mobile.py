import urllib.request
import json
import asyncio
import websockets
import base64
import os
import shutil

ARTIFACT_DIR = r"C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals"

async def verify():
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

        # 1. MOBILE AUDIT (390x844)
        print("=== MOBILE VIEWPORT AUDIT (390x844) ===")
        await send('Emulation.setDeviceMetricsOverride', {
            'width': 390,
            'height': 844,
            'deviceScaleFactor': 2,
            'mobile': True
        })
        await send('Page.navigate', {'url': 'http://127.0.0.1:8095/index.html?v=herofix2026'})
        await asyncio.sleep(2.5)

        # Slide 0: The 18K Gold Suite
        await capture("dist_mobile_hero_slide0_final.jpg")

        # Slide 1: Blush Tones Collection
        await send('Runtime.evaluate', {'expression': 'window.setHeroSlide(1)'})
        await asyncio.sleep(0.8)
        await capture("dist_mobile_hero_slide1_final.jpg")

        # Slide 2: Modern Classics
        await send('Runtime.evaluate', {'expression': 'window.setHeroSlide(2)'})
        await asyncio.sleep(0.8)
        await capture("dist_mobile_hero_slide2_final.jpg")

        # Slide 3: Signature Gift Sets
        await send('Runtime.evaluate', {'expression': 'window.setHeroSlide(3)'})
        await asyncio.sleep(0.8)
        await capture("dist_mobile_hero_slide3_final.jpg")

        # 2. DESKTOP AUDIT (1440x900)
        print("=== DESKTOP VIEWPORT AUDIT (1440x900) ===")
        await send('Emulation.setDeviceMetricsOverride', {
            'width': 1440,
            'height': 900,
            'deviceScaleFactor': 1,
            'mobile': False
        })
        await send('Page.navigate', {'url': 'http://127.0.0.1:8095/index.html?v=herofix2026'})
        await asyncio.sleep(2.0)
        await capture("dist_desktop_hero_slide0_final.jpg")
        await send('Runtime.evaluate', {'expression': 'window.setHeroSlide(1)'})
        await asyncio.sleep(0.8)
        await capture("dist_desktop_hero_slide1_final.jpg")

        print("Verification complete!")

if __name__ == '__main__':
    asyncio.run(verify())
