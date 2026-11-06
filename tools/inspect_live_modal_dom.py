import asyncio
import json
import urllib.request
import websockets

async def main():
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(req.read().decode('utf-8'))
    tab = [t for t in tabs if t.get('type') == 'page'][0]
    
    async with websockets.connect(tab.get('webSocketDebuggerUrl'), max_size=20*1024*1024) as ws:
        msg_id = 1
        await ws.send(json.dumps({'id': msg_id, 'method': 'Runtime.evaluate', 'params': {
            'expression': '''(() => {
                if (window.openFilterModal) window.openFilterModal();
                const m = document.getElementById('mobile-filter-modal');
                if (!m) return "NOT FOUND";
                return {
                    id: m.id,
                    className: m.className,
                    firstElementChildClass: m.firstElementChild ? m.firstElementChild.className : null,
                    cardChildren: Array.from(m.firstElementChild.children).map(c => ({
                        tag: c.tagName,
                        className: c.className,
                        textPreview: c.innerText.slice(0, 50)
                    }))
                };
            })()''',
            'returnByValue': True
        }}))
        resp = json.loads(await ws.recv())
        print(json.dumps(resp['result']['result']['value'], indent=2))

if __name__ == '__main__':
    asyncio.run(main())
