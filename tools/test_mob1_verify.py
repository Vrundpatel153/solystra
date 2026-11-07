import asyncio
import json
import urllib.request
import websockets
import base64
import os

ARTIFACT_DIR = r"C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals"

async def test_mob1():
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(req.read().decode())
    target = [t for t in tabs if t.get('type') == 'page' and '8095' in t.get('url', '')][0]
    
    async with websockets.connect(target['webSocketDebuggerUrl'], max_size=50*1024*1024) as ws:
        async def send(method, params=None):
            mid = 100
            msg = {"id": mid, "method": method}
            if params: msg["params"] = params
            await ws.send(json.dumps(msg))
            while True:
                r = json.loads(await ws.recv())
                if r.get("id") == mid: return r.get("result", {})

        async def eval_js(expr):
            res = await send("Runtime.evaluate", {"expression": expr, "returnByValue": True})
            return res.get("result", {}).get("value")

        await send("Emulation.setDeviceMetricsOverride", {
            "width": 390,
            "height": 844,
            "deviceScaleFactor": 2,
            "mobile": True
        })
        await asyncio.sleep(0.3)
        # Ensure Combo 1 is active
        await eval_js("document.querySelectorAll('#curated-combo-dots button')[0].click()")
        await asyncio.sleep(0.6)
        
        # Click earring pin
        m = await eval_js("""
            (() => {
                const pin = document.querySelector('[data-hotspot-id="c1-item-2"]');
                if (pin) pin.click();
                const pop = document.querySelector('[data-popover="c1-item-2"]');
                const card = document.getElementById('combo-left-col');
                if (!pop || !card) return null;
                const pRect = pop.getBoundingClientRect();
                const cRect = card.getBoundingClientRect();
                return {
                    pinFound: true,
                    popVisible: !pop.classList.contains('invisible'),
                    overflowRight: pRect.right - cRect.right,
                    overflowLeft: cRect.left - pRect.left,
                    popBottom: pRect.bottom,
                    cardBottom: cRect.bottom
                };
            })()
        """)
        print("Mobile Combo 1 Earring Metrics:", m)
        await asyncio.sleep(0.4)
        
        # Screenshot
        res = await send("Page.captureScreenshot", {"format": "jpeg", "quality": 92})
        data = base64.b64decode(res["data"])
        p = os.path.join(ARTIFACT_DIR, "mobile_combo1_earring_hotspot_verified.jpg")
        with open(p, "wb") as f:
            f.write(data)
        print("Saved verified mobile combo 1 screenshot!")

        # Crop
        from PIL import Image
        im = Image.open(p)
        crop = im.crop((0, 0, 780, 1000))
        crop.save(os.path.join(ARTIFACT_DIR, "crop_mobile_curated_earring_verified.jpg"), quality=92)
        print("Saved verified crop!")

        # Reset Emulation
        await send("Emulation.setDeviceMetricsOverride", {
            "width": 1440,
            "height": 900,
            "deviceScaleFactor": 1,
            "mobile": False
        })

asyncio.run(test_mob1())
