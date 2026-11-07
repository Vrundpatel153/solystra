import asyncio
import json
import urllib.request
import websockets

async def main():
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(req.read().decode())
    
    tab = None
    for t in tabs:
        if t.get('type') == 'page' and 'drive.google.com' in t.get('url', ''):
            tab = t
            break
            
    if not tab:
        print("Drive tab not found")
        return

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

        # Extract all script tags with class starting with ds:
        scripts_res = await send("Runtime.evaluate", {
            "expression": """(() => {
                const results = [];
                for (const s of document.querySelectorAll('script')) {
                    if (s.className && s.className.startsWith('ds:')) {
                        results.push({ cls: s.className, content: s.textContent });
                    }
                }
                return results;
            })()""",
            "returnByValue": True
        })
        scripts = scripts_res.get('result', {}).get('value', [])
        print(f"Found {len(scripts)} ds scripts:")
        for idx, s in enumerate(scripts):
            print(f" - Script {idx}: class={s['cls']}, length={len(s['content'])}")
            with open(f"scratch/drive_ds_{idx}.txt", "w", encoding="utf-8") as f:
                f.write(s['content'])

if __name__ == '__main__':
    asyncio.run(main())

