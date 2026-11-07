import asyncio
import json
import urllib.request
import websockets

async def inspect():
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

        await asyncio.sleep(2.0)
        # Evaluate DOM items in Google Drive
        eval_res = await call('Runtime.evaluate', {
            'expression': """(() => {
                // Find all elements that look like file/folder rows or tiles
                const items = [];
                document.querySelectorAll('[data-id], [aria-label]').forEach(el => {
                    const label = el.getAttribute('aria-label');
                    const dataId = el.getAttribute('data-id');
                    if (label && (label.includes('.png') || label.includes('.jpg') || label.includes('.webp') || label.includes('Folder') || label.includes('folder') || label.includes('curated') || label.includes('combo') || label.includes('Curated'))) {
                        items.push({label, dataId, text: el.innerText ? el.innerText.trim() : ''});
                    }
                });
                
                // Also get all text in main content
                const allNames = Array.from(document.querySelectorAll('div[role="row"], div[role="gridcell"], div[role="listitem"], [data-target="doc"]')).map(e => e.innerText || e.getAttribute('aria-label'));
                
                return {
                    title: document.title,
                    url: window.location.href,
                    items: items.slice(0, 50),
                    allNames: allNames.filter(Boolean).slice(0, 50)
                };
            })()""",
            'returnByValue': True
        })
        val = eval_res.get('result', {}).get('value', {})
        print("Drive info:", json.dumps(val, indent=2))

asyncio.run(inspect())

