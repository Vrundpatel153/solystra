import asyncio
import json
import urllib.request
import websockets
import time

FOLDERS = {
    "collections": "https://drive.google.com/drive/folders/1raauaBKHZO2B_4bhQhaZwP3GYXTZd5ht",
    "hero-banner": "https://drive.google.com/drive/folders/1g8Z-yT3VIm8VD9eXm0uXMtCEtT-sDm3y"
}

async def inspect_subfolders():
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(req.read().decode())
    
    # Pick a page tab
    page_tabs = [t for t in tabs if t.get('type') == 'page']
    tab = page_tabs[0]
    ws_url = tab['webSocketDebuggerUrl']

    results = {}

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

        for name, url in FOLDERS.items():
            print(f"\n--- Navigating to {name} ({url}) ---")
            await call("Page.navigate", {"url": url})
            await asyncio.sleep(6)

            res = await call("Runtime.evaluate", {
                "expression": """(() => {
                    const items = [];
                    // Look for elements with data-id
                    document.querySelectorAll('[data-id]').forEach(el => {
                        const id = el.getAttribute('data-id');
                        const text = el.innerText || el.getAttribute('aria-label') || '';
                        if (id && text && !id.startsWith('_') && id.length > 15) {
                            items.push({ id, text: text.trim().replace(/\\n+/g, ' | ') });
                        }
                    });
                    return items;
                })()""",
                "returnByValue": True
            })
            val = res.get("result", {}).get("value", [])
            print(f"Found {len(val)} items in {name}:")
            for item in val:
                print(f"  ID: {item['id']} -> {item['text']}")
            results[name] = val

    with open("scratch/drive_collections_and_banners.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("\nSaved scratch/drive_collections_and_banners.json")

asyncio.run(inspect_subfolders())

