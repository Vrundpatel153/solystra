import asyncio, json, urllib.request, websockets, base64

async def snap():
    req = urllib.request.urlopen('http://127.0.0.1:9222/json')
    tabs = json.loads(req.read().decode('utf-8'))
    target_tab = [t for t in tabs if t.get('type') == 'page' and '8080' in t.get('url', '')][0]
    ws_url = target_tab['webSocketDebuggerUrl']
    
    async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
        msg_id = 1
        async def send(method, params=None):
            nonlocal msg_id
            m = {'id': msg_id, 'method': method}
            if params: m['params'] = params
            await ws.send(json.dumps(m))
            cur = msg_id
            msg_id += 1
            while True:
                r = json.loads(await ws.recv())
                if r.get('id') == cur: return r.get('result')

        await send('Page.enable')
        await send('Emulation.setDeviceMetricsOverride', {'width': 390, 'height': 844, 'deviceScaleFactor': 2, 'mobile': True})
        await send('Page.navigate', {'url': 'http://localhost:8080/products.html'})
        await asyncio.sleep(1.5)
        
        # Scroll to mobile controls
        await send('Runtime.evaluate', {'expression': '''
            const el = document.getElementById('mobile-catalog-products-count') || document.querySelector('.lg\\\\:hidden');
            if (el) el.scrollIntoView({ behavior: 'instant', block: 'start' });
            window.scrollBy(0, -70);
        '''})
        await asyncio.sleep(0.8)

        res = await send('Page.captureScreenshot', {'format': 'jpeg', 'quality': 88})
        with open(r'C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals\catalog_mobile_padding_fixed.jpg', 'wb') as f:
            f.write(base64.b64decode(res['data']))
        print('Captured catalog_mobile_padding_fixed.jpg')

asyncio.run(snap())
