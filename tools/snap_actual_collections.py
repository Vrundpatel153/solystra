import asyncio
import json
import base64
import urllib.request
import websockets

async def snap_actual_collections():
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
        
        # Find element with data-collection-card and scroll to it
        await send("Runtime.evaluate", {
            "expression": """
                const card = document.querySelector('[data-collection-card="true"]');
                if (card) {
                    card.scrollIntoView({block: 'center'});
                }
            """
        })
        await asyncio.sleep(0.8)
        
        shot_col = await send("Page.captureScreenshot", {"format": "jpeg", "quality": 88})
        out_col = "C:/Users/vrund/.gemini/antigravity/brain/68f27351-9b2c-41bf-b75f-ce5ad9262a98/audit_visuals/homepage_collections_actual_cards.jpg"
        with open(out_col, "wb") as f:
            f.write(base64.b64decode(shot_col["data"]))
        print(f"Collections screenshot saved: {out_col}")

asyncio.run(snap_actual_collections())
