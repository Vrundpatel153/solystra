import asyncio
import json
import base64
import urllib.request
import websockets

async def audit():
    # 1. Desktop Audit (1440x900)
    print("Connecting to Chrome CDP for Desktop...")
    req = urllib.request.Request("http://127.0.0.1:9222/json/new?http://127.0.0.1:8080/index.html", method="PUT")
    with urllib.request.urlopen(req) as resp:
        tab = json.loads(resp.read().decode())
    
    ws_url = tab['webSocketDebuggerUrl']
    tab_id = tab['id']
    
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
        await send("DOM.enable")
        await send("Emulation.setDeviceMetricsOverride", {
            "width": 1440,
            "height": 900,
            "deviceScaleFactor": 1,
            "mobile": False
        })
        
        # wait 1.5s for page load
        await asyncio.sleep(1.5)
        
        # open collections menu
        print("Opening collections menu on desktop...")
        await send("Runtime.evaluate", {
            "expression": "window.toggleCollectionsMenu();"
        })
        await asyncio.sleep(0.8)
        
        # take screenshot of desktop menu
        shot = await send("Page.captureScreenshot", {"format": "jpeg", "quality": 88})
        out_path = "C:/Users/vrund/.gemini/antigravity/brain/68f27351-9b2c-41bf-b75f-ce5ad9262a98/audit_visuals/collections_menu_all_products_desktop.jpg"
        with open(out_path, "wb") as f:
            f.write(base64.b64decode(shot["data"]))
        print(f"Desktop screenshot saved: {out_path}")
        
        # Now test clicking the Explore All Products button to verify redirection!
        print("Testing click on Explore All Products button...")
        click_res = await send("Runtime.evaluate", {
            "expression": """
                const btns = Array.from(document.querySelectorAll('button'));
                const btn = btns.find(b => b.textContent.includes('Explore All Products'));
                if (btn) {
                    btn.click();
                    'CLICKED';
                } else {
                    'NOT_FOUND';
                }
            """
        })
        print("Click result:", click_res)
        await asyncio.sleep(1.5)
        
        # Check current URL
        url_res = await send("Runtime.evaluate", {"expression": "window.location.href"})
        print("Redirection target URL:", url_res.get('result', {}).get('value'))
        
        # Now test product.html breadcrumb
        await send("Page.navigate", {"url": "http://127.0.0.1:8080/product.html?id=accent-circle-925-silver-necklace"})
        await asyncio.sleep(1.5)
        
        shot_pdp = await send("Page.captureScreenshot", {"format": "jpeg", "quality": 88})
        out_pdp = "C:/Users/vrund/.gemini/antigravity/brain/68f27351-9b2c-41bf-b75f-ce5ad9262a98/audit_visuals/pdp_breadcrumb_all_products.jpg"
        with open(out_pdp, "wb") as f:
            f.write(base64.b64decode(shot_pdp["data"]))
        print(f"PDP breadcrumb screenshot saved: {out_pdp}")

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
        
        # open mobile menu
        print("Opening collections menu on mobile...")
        await send2("Runtime.evaluate", {
            "expression": "window.toggleCollectionsMenu();"
        })
        await asyncio.sleep(0.8)
        
        shot_mob = await send2("Page.captureScreenshot", {"format": "jpeg", "quality": 88})
        out_mob = "C:/Users/vrund/.gemini/antigravity/brain/68f27351-9b2c-41bf-b75f-ce5ad9262a98/audit_visuals/collections_menu_all_products_mobile.jpg"
        with open(out_mob, "wb") as f:
            f.write(base64.b64decode(shot_mob["data"]))
        print(f"Mobile screenshot saved: {out_mob}")

asyncio.run(audit())
