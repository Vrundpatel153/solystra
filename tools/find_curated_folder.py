import asyncio
import json
import urllib.request
import websockets

async def inspect_folder():
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

        # Find the folder link / id or double click it
        res = await call('Runtime.evaluate', {
            'expression': """(() => {
                const els = Array.from(document.querySelectorAll('*'));
                for (const el of els) {
                    if (el.innerText && el.innerText.includes('curated-look photo') && (el.getAttribute('data-id') || el.closest('[data-id]'))) {
                        const target = el.closest('[data-id]') || el;
                        return {
                            dataId: target.getAttribute('data-id'),
                            innerHTML: target.outerHTML.slice(0, 500)
                        };
                    }
                }
                // Try searching in page HTML for 'curated-look photo'
                return {
                    bodySnippet: document.body.innerHTML.slice(document.body.innerHTML.indexOf('curated-look photo') - 100, document.body.innerHTML.indexOf('curated-look photo') + 200)
                };
            })()""",
            'returnByValue': True
        })
        print("Folder element info:", json.dumps(res.get('result', {}).get('value', {}), indent=2))

asyncio.run(inspect_folder())

