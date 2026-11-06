import asyncio
import json
import urllib.request
import websockets

async def main():
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(req.read().decode('utf-8'))
    tab = None
    for t in tabs:
        if t.get('type') == 'page' and ('products.html' in t.get('url', '') or '8080' in t.get('url', '')):
            tab = t
            break
    if not tab:
        tab = tabs[0]
        
    async with websockets.connect(tab.get('webSocketDebuggerUrl'), max_size=20*1024*1024) as ws:
        msg_id = 1
        # Set desktop 1440x900
        await ws.send(json.dumps({'id': msg_id, 'method': 'Emulation.setDeviceMetricsOverride', 'params': {
            'width': 1440, 'height': 900, 'deviceScaleFactor': 1, 'mobile': False
        }}))
        await ws.recv()
        msg_id += 1
        
        await ws.send(json.dumps({'id': msg_id, 'method': 'Runtime.evaluate', 'params': {
            'expression': '''(() => {
                if (window.openFilterModal) window.openFilterModal();
                const m = document.getElementById('mobile-filter-modal');
                if (!m) return "modal still not found";
                const card = m.firstElementChild;
                const rM = m.getBoundingClientRect();
                const rCard = card.getBoundingClientRect();
                const header = card.firstElementChild;
                const rHeader = header ? header.getBoundingClientRect() : null;
                const body = card.children[1];
                const rBody = body ? body.getBoundingClientRect() : null;
                const footer = card.lastElementChild;
                const rFooter = footer ? footer.getBoundingClientRect() : null;
                
                return {
                    windowHeight: window.innerHeight,
                    mRect: { top: rM.top, bottom: rM.bottom, height: rM.height },
                    cardRect: { top: rCard.top, bottom: rCard.bottom, height: rCard.height },
                    headerRect: rHeader ? { top: rHeader.top, bottom: rHeader.bottom, height: rHeader.height } : null,
                    bodyRect: rBody ? { top: rBody.top, bottom: rBody.bottom, height: rBody.height, scrollHeight: rBody.scrollHeight } : null,
                    footerRect: rFooter ? { top: rFooter.top, bottom: rFooter.bottom, height: rFooter.height } : null,
                    cardClasses: card.className,
                    cardInlineStyle: card.getAttribute('style')
                };
            })()''',
            'returnByValue': True
        }}))
        resp = json.loads(await ws.recv())
        print(json.dumps(resp.get('result', {}).get('result', {}).get('value'), indent=2))

if __name__ == '__main__':
    asyncio.run(main())
