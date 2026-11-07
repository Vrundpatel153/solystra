import asyncio
import json
import urllib.request
import websockets
import time

DRIVE_URL = "https://drive.google.com/drive/folders/1tHGJa96A4F7xCrTY2tayF9X-IQD2ieLw"

async def scan_drive():
    print("Opening Google Drive URL:", DRIVE_URL)
    # Open new tab
    req = urllib.request.Request(f"http://127.0.0.1:9222/json/new?{DRIVE_URL}", method="PUT")
    with urllib.request.urlopen(req) as resp:
        tab = json.loads(resp.read().decode())
    
    ws_url = tab['webSocketDebuggerUrl']
    tab_id = tab['id']
    print(f"Opened tab {tab_id}, connecting websocket...")

    async with websockets.connect(ws_url, max_size=50*1024*1024) as ws:
        msg_id = 1
        async def call(method, params=None):
            nonlocal msg_id
            msg_id += 1
            payload = {"id": msg_id, "method": method, "params": params or {}}
            await ws.send(json.dumps(payload))
            while True:
                res = json.loads(await ws.recv())
                if res.get("id") == msg_id:
                    return res.get("result", {})

        print("Waiting 6 seconds for Drive folder to load...")
        await asyncio.sleep(6)

        # Inspect subfolders
        eval_folders = await call("Runtime.evaluate", {
            "expression": """(() => {
                // Find all items in the folder view
                const items = [];
                document.querySelectorAll('[data-id]').forEach(el => {
                    const id = el.getAttribute('data-id');
                    const text = el.innerText || el.getAttribute('aria-label') || '';
                    items.push({ id, text: text.trim().replace(/\\n+/g, ' | ') });
                });
                return items;
            })()""",
            "returnByValue": True
        })
        print("Root folder items:", json.dumps(eval_folders.get("result", {}).get("value", []), indent=2))

asyncio.run(scan_drive())

