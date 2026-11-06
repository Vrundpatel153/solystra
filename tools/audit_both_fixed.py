import asyncio, json, urllib.request, websockets, base64, os

OUT_DIR = r"C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals"
os.makedirs(OUT_DIR, exist_ok=True)

async def audit():
    req = urllib.request.urlopen('http://127.0.0.1:9222/json')
    tabs = json.loads(req.read().decode('utf-8'))
    target_tab = None
    for t in tabs:
        if t.get('type') == 'page' and '8080' in t.get('url', ''):
            target_tab = t
            break
    if not target_tab:
        for t in tabs:
            if t.get('type') == 'page':
                target_tab = t
                break

    ws_url = target_tab['webSocketDebuggerUrl']
    print("Connecting to tab:", target_tab.get('title'))

    async with websockets.connect(ws_url, max_size=25*1024*1024) as ws:
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

        # -------------------------------------------------------------
        # 1. DESKTOP HERO BANNER (1440 x 900)
        # -------------------------------------------------------------
        print("\n--- Auditing Recovered Desktop Hero Banner ---")
        await send('Emulation.setDeviceMetricsOverride', {'width': 1440, 'height': 900, 'deviceScaleFactor': 1, 'mobile': False})
        await send('Page.navigate', {'url': 'http://localhost:8080/index.html'})
        await asyncio.sleep(2.0)

        # Stop carousel auto-rotation for deterministic audit capture
        await send('Runtime.evaluate', {'expression': '''
            if (window.heroCarouselInterval) clearInterval(window.heroCarouselInterval);
            window.setHeroSlide(0);
        '''})
        await asyncio.sleep(0.5)

        res = await send('Page.captureScreenshot', {'format': 'jpeg', 'quality': 88})
        p1 = os.path.join(OUT_DIR, 'recovered_hero_desktop.jpg')
        with open(p1, 'wb') as f:
            f.write(base64.b64decode(res['data']))
        print("✓ Saved", p1)

        # -------------------------------------------------------------
        # 2. MOBILE HERO BANNER (390 x 844 iPhone)
        # -------------------------------------------------------------
        print("\n--- Auditing Recovered Mobile Hero Banner ---")
        await send('Emulation.setDeviceMetricsOverride', {'width': 390, 'height': 844, 'deviceScaleFactor': 2, 'mobile': True})
        await send('Page.navigate', {'url': 'http://localhost:8080/index.html'})
        await asyncio.sleep(2.0)

        await send('Runtime.evaluate', {'expression': '''
            if (window.heroCarouselInterval) clearInterval(window.heroCarouselInterval);
            window.setHeroSlide(0);
        '''})
        await asyncio.sleep(0.5)

        res = await send('Page.captureScreenshot', {'format': 'jpeg', 'quality': 88})
        p2 = os.path.join(OUT_DIR, 'recovered_hero_mobile.jpg')
        with open(p2, 'wb') as f:
            f.write(base64.b64decode(res['data']))
        print("✓ Saved", p2)

        # -------------------------------------------------------------
        # 3. DESKTOP PRODUCTS PAGE WITH LEFT & RIGHT PADDING
        # -------------------------------------------------------------
        print("\n--- Auditing Desktop Products Page Padding ---")
        await send('Emulation.setDeviceMetricsOverride', {'width': 1440, 'height': 900, 'deviceScaleFactor': 1, 'mobile': False})
        await send('Page.navigate', {'url': 'http://localhost:8080/products.html'})
        await asyncio.sleep(1.8)

        await send('Runtime.evaluate', {'expression': '''
            const el = document.getElementById('catalog-products-count') || document.getElementById('products-catalog-grid');
            if (el) el.scrollIntoView({ behavior: 'instant', block: 'start' });
            window.scrollBy(0, -90);
        '''})
        await asyncio.sleep(0.8)

        res = await send('Page.captureScreenshot', {'format': 'jpeg', 'quality': 88})
        p3 = os.path.join(OUT_DIR, 'recovered_products_desktop_padding.jpg')
        with open(p3, 'wb') as f:
            f.write(base64.b64decode(res['data']))
        print("✓ Saved", p3)

        # -------------------------------------------------------------
        # 4. MOBILE PRODUCTS PAGE WITH LEFT & RIGHT PADDING
        # -------------------------------------------------------------
        print("\n--- Auditing Mobile Products Page Padding ---")
        await send('Emulation.setDeviceMetricsOverride', {'width': 390, 'height': 844, 'deviceScaleFactor': 2, 'mobile': True})
        await send('Page.navigate', {'url': 'http://localhost:8080/products.html'})
        await asyncio.sleep(1.8)

        await send('Runtime.evaluate', {'expression': '''
            const el = document.getElementById('mobile-catalog-products-count') || document.querySelector('.lg\\\\:hidden');
            if (el) el.scrollIntoView({ behavior: 'instant', block: 'start' });
            window.scrollBy(0, -70);
        '''})
        await asyncio.sleep(0.8)

        res = await send('Page.captureScreenshot', {'format': 'jpeg', 'quality': 88})
        p4 = os.path.join(OUT_DIR, 'recovered_products_mobile_padding.jpg')
        with open(p4, 'wb') as f:
            f.write(base64.b64decode(res['data']))
        print("✓ Saved", p4)

        # Reset device override to normal desktop
        await send('Emulation.setDeviceMetricsOverride', {'width': 1440, 'height': 900, 'deviceScaleFactor': 1, 'mobile': False})
        print("\nAudit of both fixes completed successfully!")

if __name__ == '__main__':
    asyncio.run(audit())
