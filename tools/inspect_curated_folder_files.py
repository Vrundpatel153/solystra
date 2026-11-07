import asyncio
import json
import urllib.request
import websockets
import re

async def open_curated_folder():
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(req.read().decode())
    drive_tab = [t for t in tabs if t.get('type') == 'page' and 'drive.google.com' in t.get('url', '')][0]
    
    async with websockets.connect(drive_tab['webSocketDebuggerUrl'], max_size=50*1024*1024) as ws:
        msg_id = 1
        async def call(method, params=None):
            nonlocal msg_id
            msg_id += 1
            payload = {"id": msg_id, "method": method, "params": params or {}}
            await ws.send(json.dumps(payload))
            while True:
                res = json.loads(await ws.recv())
                if res.get('id') == msg_id:
                    return res.get('result', {})

        folder_url = "https://drive.google.com/drive/folders/1YJZnPbsbsOWMJBSSNhEUtY6wowOgmL5h"
        await call('Page.navigate', {'url': folder_url})
        await asyncio.sleep(3.5)

        # Inspect items
        eval_res = await call('Runtime.evaluate', {
            'expression': """(() => {
                const items = [];
                document.querySelectorAll('[data-id]').forEach(el => {
                    const dataId = el.getAttribute('data-id');
                    const text = el.innerText ? el.innerText.trim() : '';
                    const label = el.getAttribute('aria-label') || '';
                    items.push({dataId, label, text});
                });
                
                // Get all script data
                const scripts = Array.from(document.querySelectorAll('script')).map(s => s.innerText).join('\\n');
                
                return {
                    url: window.location.href,
                    title: document.title,
                    items: items,
                    bodyText: document.body.innerText
                };
            })()""",
            'returnByValue': True
        })
        val = eval_res.get('result', {}).get('value', {})
        print("Folder Title:", val.get('title'))
        print("Body text:\n", val.get('bodyText'))
        print("Items found:", json.dumps(val.get('items', []), indent=2))

asyncio.run(open_curated_folder())

