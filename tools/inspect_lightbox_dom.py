import asyncio
import json
import urllib.request
import websockets

async def main():
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(req.read().decode('utf-8'))
    for tab in tabs:
        if '8089' in tab.get('url', '') or 'product.html' in tab.get('url', ''):
            async with websockets.connect(tab.get('webSocketDebuggerUrl')) as ws:
                payload = {
                    'id': 1,
                    'method': 'Runtime.evaluate',
                    'params': {
                        'expression': 'document.getElementById("pdp-lightbox-modal") ? document.getElementById("pdp-lightbox-modal").outerHTML : "None"',
                        'returnByValue': True
                    }
                }
                await ws.send(json.dumps(payload))
                res = json.loads(await ws.recv())
                html = res.get('result', {}).get('result', {}).get('value')
                print("HTML length:", len(html))
                print(html[:1500])
                break

if __name__ == '__main__':
    asyncio.run(main())

