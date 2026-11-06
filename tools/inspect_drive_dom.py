import asyncio
import json
import urllib.request
import websockets

async def check_drive_objects():
    # Use existing drive tab
    req = urllib.request.Request("http://127.0.0.1:9222/json/list")
    with urllib.request.urlopen(req) as resp:
        tabs = json.loads(resp.read().decode())
    
    drive_tab = next((t for t in tabs if 'drive.google.com' in t.get('url', '')), None)
    if not drive_tab:
        print("No drive tab found")
        return
        
    async with websockets.connect(drive_tab['webSocketDebuggerUrl'], max_size=50*1024*1024) as ws:
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

        # Let's inspect the HTML of an item row
        res = await send("Runtime.evaluate", {
            "expression": """
                (() => {
                    const el = document.querySelector('[data-id]');
                    return el ? el.outerHTML : 'none';
                })()
            """,
            "returnByValue": True
        })
        print("Sample data-id element outerHTML:")
        print(res.get('result', {}).get('value')[:500])

asyncio.run(check_drive_objects())
