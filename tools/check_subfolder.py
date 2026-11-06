import asyncio
import json
import urllib.request
import websockets

async def check_subfolder():
    sub_url = "https://drive.google.com/drive/folders/1IzLhq3kwsNxt8HgckZP65nVgne4dRPZF"
    print("Navigating to subfolder 'Heart product raw' in Chrome...")
    req = urllib.request.Request(f"http://127.0.0.1:9222/json/new?{sub_url}", method="PUT")
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
        await asyncio.sleep(4)
        
        title_res = await send("Runtime.evaluate", {"expression": "document.title"})
        print("Page title:", title_res.get('result', {}).get('value'))
        
        # Extract items in Heart product raw
        res = await send("Runtime.evaluate", {
            "expression": """
                (() => {
                    const map = {};
                    document.querySelectorAll('div[data-id]').forEach(d => {
                        const id = d.getAttribute('data-id');
                        const label = d.getAttribute('aria-label') || d.innerText || '';
                        if (id && id.length > 20 && id !== '1IzLhq3kwsNxt8HgckZP65nVgne4dRPZF') {
                            if (!map[id] || (label && label.length > map[id].length)) {
                                map[id] = label.trim();
                            }
                        }
                    });
                    return map;
                })()
            """,
            "returnByValue": True
        })
        
        items = res.get('result', {}).get('value', {})
        print(f"Items in 'Heart product raw': {len(items)}")
        for fid, name in list(items.items())[:15]:
            print(f"  {name} -> {fid}")

asyncio.run(check_subfolder())
