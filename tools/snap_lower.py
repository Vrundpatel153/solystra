import asyncio
import json
import base64
import urllib.request
import websockets

async def snap_lower():
    req = urllib.request.Request("http://127.0.0.1:9222/json/new?http://127.0.0.1:8080/category_curation_candidates.html", method="PUT")
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
        await asyncio.sleep(1)
        
        # Scroll down to section 4
        await send("Runtime.evaluate", {
            "expression": "window.scrollTo(0, 1000);"
        })
        await asyncio.sleep(0.8)
        
        shot = await send("Page.captureScreenshot", {"format": "jpeg", "quality": 85})
        out_path = "C:/Users/vrund/.gemini/antigravity/brain/68f27351-9b2c-41bf-b75f-ce5ad9262a98/audit_visuals/drive_candidates_lower.jpg"
        with open(out_path, "wb") as f:
            f.write(base64.b64decode(shot["data"]))
        print("Saved:", out_path)

asyncio.run(snap_lower())
