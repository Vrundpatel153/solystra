import asyncio
import json
import urllib.request
import websockets
import time

async def main():
    drive_url = "https://drive.google.com/drive/folders/1tHGJa96A4F7xCrTY2tayF9X-IQD2ieLw"
    print("Navigating to new Google Drive folder:", drive_url)
    
    # Check open tabs
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(req.read().decode())
    
    tab = None
    for t in tabs:
        if t.get('type') == 'page':
            tab = t
            break
            
    if not tab:
        req_new = urllib.request.Request(f"http://127.0.0.1:9222/json/new?{drive_url}", method="PUT")
        with urllib.request.urlopen(req_new) as resp:
            tab = json.loads(resp.read().decode())
    else:
        # Navigate existing tab
        pass

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
        await send("Page.navigate", {"url": drive_url})
        print("Waiting 6 seconds for Google Drive folder to load...")
        await asyncio.sleep(6)

        # Get page title and inspect DOM
        title_res = await send("Runtime.evaluate", {"expression": "document.title"})
        print("Drive Page Title:", title_res.get('result', {}).get('value'))

        # Inspect items (folders and files)
        items_res = await send("Runtime.evaluate", {
            "expression": """(() => {
                const results = [];
                // Look for elements with data-id or role="row" or [aria-label]
                const els = document.querySelectorAll('[data-id], [role="row"], [data-target="item"]');
                for (const el of els) {
                    const id = el.getAttribute('data-id') || el.dataset.id;
                    const label = el.getAttribute('aria-label') || el.innerText || '';
                    if (id || label) {
                        results.push({
                            id: id,
                            text: el.innerText.trim().split('\\n').slice(0, 3).join(' | '),
                            aria: el.getAttribute('aria-label')
                        });
                    }
                }
                return results;
            })()""",
            "returnByValue": True
        })
        items = items_res.get('result', {}).get('value')
        print(f"Found {len(items)} items on screen:")
        for it in items[:30]:
            print(" -", it)

if __name__ == '__main__':
    asyncio.run(main())

