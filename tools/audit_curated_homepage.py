import asyncio
import json
import base64
import urllib.request
import websockets

async def audit_home():
    # 1. Desktop Audit (1440x900)
    print("Connecting to Chrome CDP for Desktop...")
    req = urllib.request.Request("http://127.0.0.1:9222/json/new?http://127.0.0.1:8080/index.html", method="PUT")
    with urllib.request.urlopen(req) as resp:
        tab = json.loads(resp.read().decode())
    
    ws_url = tab['webSocketDebuggerUrl']
    
    async with websockets.connect(ws_url, max_size=50*1024*1024) as ws:
        msg_id = 1
        async def send(method, params=None):
            nonlocal msg_id
            m = {"id": msg_id, "method": method, "params": params or {}}
            msg_id += 1
            await ws.send(json.dumps(m))
            while True:
                res = json.loads(await ws.recv())
                if res.get("id") == m["id"]:
                    return res.get("result", {})

        await send("Page.enable")
        await send("Emulation.setDeviceMetricsOverride", {
            "width": 1440,
            "height": 900,
            "deviceScaleFactor": 1,
            "mobile": False
        })
        await asyncio.sleep(1.5)
        
        # Scroll to Category carousel (approx y=550)
        await send("Runtime.evaluate", {
            "expression": """
                const catSec = document.querySelector('section:has(.grid, [class*="category"])') || document.querySelector('h2');
                window.scrollTo(0, 520);
            """
        })
        await asyncio.sleep(0.8)
        
        shot_cat = await send("Page.captureScreenshot", {"format": "jpeg", "quality": 88})
        out_cat = "C:/Users/vrund/.gemini/antigravity/brain/68f27351-9b2c-41bf-b75f-ce5ad9262a98/audit_visuals/homepage_categories_drive_curated.jpg"
        with open(out_cat, "wb") as f:
            f.write(base64.b64decode(shot_cat["data"]))
        print(f"Categories screenshot saved: {out_cat}")
        
        # Scroll to Curated Collections carousel (approx y=1200)
        await send("Runtime.evaluate", {
            "expression": "window.scrollTo(0, 1150);"
        })
        await asyncio.sleep(0.8)
        
        shot_col = await send("Page.captureScreenshot", {"format": "jpeg", "quality": 88})
        out_col = "C:/Users/vrund/.gemini/antigravity/brain/68f27351-9b2c-41bf-b75f-ce5ad9262a98/audit_visuals/homepage_collections_drive_curated.jpg"
        with open(out_col, "wb") as f:
            f.write(base64.b64decode(shot_col["data"]))
        print(f"Collections screenshot saved: {out_col}")

    # 2. Mobile Audit (390x844)
    print("\nConnecting to Chrome CDP for Mobile...")
    req2 = urllib.request.Request("http://127.0.0.1:9222/json/new?http://127.0.0.1:8080/index.html", method="PUT")
    with urllib.request.urlopen(req2) as resp:
        tab2 = json.loads(resp.read().decode())
    
    ws_url2 = tab2['webSocketDebuggerUrl']
    
    async with websockets.connect(ws_url2, max_size=50*1024*1024) as ws2:
        msg_id2 = 1
        async def send2(method, params=None):
            nonlocal msg_id2
            m = {"id": msg_id2, "method": method, "params": params or {}}
            msg_id2 += 1
            await ws2.send(json.dumps(m))
            while True:
                res = json.loads(await ws2.recv())
                if res.get("id") == m["id"]:
                    return res.get("result", {})

        await send2("Page.enable")
        await send2("Emulation.setDeviceMetricsOverride", {
            "width": 390,
            "height": 844,
            "deviceScaleFactor": 2,
            "mobile": True
        })
        await asyncio.sleep(1.5)
        
        # Scroll down to categories on mobile
        await send2("Runtime.evaluate", {
            "expression": "window.scrollTo(0, 480);"
        })
        await asyncio.sleep(0.8)
        
        shot_mob = await send2("Page.captureScreenshot", {"format": "jpeg", "quality": 88})
        out_mob = "C:/Users/vrund/.gemini/antigravity/brain/68f27351-9b2c-41bf-b75f-ce5ad9262a98/audit_visuals/mobile_categories_drive_curated.jpg"
        with open(out_mob, "wb") as f:
            f.write(base64.b64decode(shot_mob["data"]))
        print(f"Mobile categories screenshot saved: {out_mob}")

asyncio.run(audit_home())
