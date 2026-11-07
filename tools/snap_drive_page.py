import asyncio
import json
import urllib.request
import base64
import websockets
import os

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

        shot = await send("Page.captureScreenshot", {"format": "jpeg", "quality": 80})
        with open("audit_visuals/drive_folder_view.jpg", "wb") as f:
            f.write(base64.b64decode(shot['data']))
        print("Captured audit_visuals/drive_folder_view.jpg")

        # Let's inspect all text or elements with role or testid
        dom_info = await send("Runtime.evaluate", {
            "expression": """(() => {
                const textNodes = [];
                const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
                let node;
                while (node = walker.nextNode()) {
                    if (node.children.length === 0 && node.innerText && node.innerText.trim()) {
                        textNodes.push({
                            tag: node.tagName,
                            text: node.innerText.trim(),
                            className: node.className,
                            parentTag: node.parentElement ? node.parentElement.tagName : null,
                            parentRole: node.parentElement ? node.parentElement.getAttribute('role') : null,
                            dataId: node.closest('[data-id]') ? node.closest('[data-id]').getAttribute('data-id') : null
                        });
                    }
                }
                return textNodes;
            })()""",
            "returnByValue": True
        })
        texts = dom_info.get('result', {}).get('value', [])
        print(f"Extracted {len(texts)} text elements:")
        for t in texts:
            if any(k in t['text'].lower() for k in ['category', 'collection', 'banner', 'folder', 'image', 'dsc', 'png', 'jpg', 'jpeg', 'webp', 'pc', 'mobile']):
                print(" ->", t)

if __name__ == '__main__':
    asyncio.run(main())
