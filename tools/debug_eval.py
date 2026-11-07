import asyncio
import json
import urllib.request
import websockets

async def check_dom():
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(req.read().decode())
    target = [t for t in tabs if t.get('type') == 'page' and '8095' in t.get('url', '')][0]
    
    async with websockets.connect(target['webSocketDebuggerUrl']) as ws:
        async def eval_js(expr):
            mid = 101
            await ws.send(json.dumps({"id": mid, "method": "Runtime.evaluate", "params": {"expression": expr, "returnByValue": True}}))
            while True:
                r = json.loads(await ws.recv())
                if r.get("id") == mid:
                    print("CDP Result:", r)
                    return r.get("result", {}).get("value")

        info = await eval_js("document.title")
        print("Page Title:", info)

asyncio.run(check_dom())
