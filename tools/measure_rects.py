import asyncio
import json
import urllib.request
import websockets

async def main():
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(req.read().decode('utf-8'))
    tab = tabs[0]
    for t in tabs:
        if t.get('type') == 'page' and ('products.html' in t.get('url', '') or '8080' in t.get('url', '')):
            tab = t
            break
            
    async with websockets.connect(tab.get('webSocketDebuggerUrl'), max_size=20*1024*1024) as ws:
        msg_id = 1
        await ws.send(json.dumps({'id': msg_id, 'method': 'Emulation.setDeviceMetricsOverride', 'params': {
            'width': 1024, 'height': 650, 'deviceScaleFactor': 1, 'mobile': False
        }}))
        await ws.recv()
        msg_id += 1
        
        await ws.send(json.dumps({'id': msg_id, 'method': 'Runtime.evaluate', 'params': {
            'expression': '''(() => {
                if (window.openFilterModal) window.openFilterModal();
                const m = document.getElementById('mobile-filter-modal');
                if (!m) return "modal not found";
                const card = m.firstElementChild;
                const h = card ? card.children[0] : null;
                const b = card ? card.children[1] : null;
                const f = card ? card.children[2] : null;
                
                return {
                    windowH: window.innerHeight,
                    mRect: m.getBoundingClientRect(),
                    cardRect: card.getBoundingClientRect(),
                    headerRect: h ? h.getBoundingClientRect() : null,
                    bodyRect: b ? b.getBoundingClientRect() : null,
                    footerRect: f ? f.getBoundingClientRect() : null,
                    cardChildrenCount: card.children.length,
                    headerHtml: h ? h.outerHTML.slice(0, 100) : null
                };
            })()''',
            'returnByValue': True
        }}))
        resp = json.loads(await ws.recv())
        print(json.dumps(resp['result']['result']['value'], indent=2))

if __name__ == '__main__':
    asyncio.run(main())
