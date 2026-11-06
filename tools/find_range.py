import asyncio
import json
import urllib.request
import websockets
import re

async def find_range():
    req = urllib.request.Request("http://127.0.0.1:9222/json/list")
    with urllib.request.urlopen(req) as resp:
        tabs = json.loads(resp.read().decode())
    
    drive_tab = next((t for t in tabs if 'drive.google.com' in t.get('url', '') and 'soly' in t.get('title', '').lower()), None)
    if not drive_tab:
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

        # Let's get the entire page HTML text
        res = await send("Runtime.evaluate", {
            "expression": "document.body.innerText"
        })
        text = res.get('result', {}).get('value', '')
        dscs = re.findall(r'DSC\d{5}', text)
        print("DSC occurrences in innerText:", len(dscs))
        if dscs:
            s = sorted(set(dscs))
            print("Lowest in view:", s[0], "Highest in view:", s[-1], "Total unique in view:", len(s))

asyncio.run(find_range())

