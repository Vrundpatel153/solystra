import asyncio
import json
import urllib.request
import base64
import os
import websockets

OUT_DIR = r"C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals"
os.makedirs(OUT_DIR, exist_ok=True)

async def audit_catalog():
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(req.read().decode('utf-8'))
    
    target_tab = None
    for tab in tabs:
        if tab.get('type') == 'page' and '8080' in tab.get('url', ''):
            target_tab = tab
            break
            
    if not target_tab:
        for tab in tabs:
            if tab.get('type') == 'page':
                target_tab = tab
                break
                
    if not target_tab:
        print("No page tab found on port 9222!")
        return

    ws_url = target_tab.get('webSocketDebuggerUrl')
    print(f"Connecting to tab: {target_tab.get('title')}")
    
    async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
        msg_id = 1
        
        async def send_cmd(method, params=None):
            nonlocal msg_id
            m = {'id': msg_id, 'method': method}
            if params: m['params'] = params
            await ws.send(json.dumps(m))
            cur_id = msg_id
            msg_id += 1
            while True:
                resp = json.loads(await ws.recv())
                if resp.get('id') == cur_id:
                    return resp.get('result')

        await send_cmd('Page.enable')

        # =============================================================
        # 1. DESKTOP VIEW AUDIT (1440 x 900)
        # =============================================================
        print("\n--- AUDITING DESKTOP (1440x900) ---")
        await send_cmd('Emulation.setDeviceMetricsOverride', {
            'width': 1440, 'height': 900, 'deviceScaleFactor': 1, 'mobile': False
        })
        await asyncio.sleep(0.3)
        await send_cmd('Page.navigate', {'url': 'http://localhost:8080/products.html'})
        await asyncio.sleep(2.0)

        # Scroll to top of catalog controls
        await send_cmd('Runtime.evaluate', {'expression': '''
            const el = document.getElementById('catalog-products-count') || document.getElementById('products-catalog-grid');
            if (el) el.scrollIntoView({ behavior: 'instant', block: 'start' });
            window.scrollBy(0, -90);
        '''})
        await asyncio.sleep(0.8)

        # Capture Screenshot 1: Desktop Single-Line Controls + 5-Col Grid
        res = await send_cmd('Page.captureScreenshot', {'format': 'jpeg', 'quality': 88})
        path1 = os.path.join(OUT_DIR, "catalog_desktop_single_row_5col.jpg")
        with open(path1, 'wb') as f:
            f.write(base64.b64decode(res['data']))
        print(f"✓ Saved {path1}")

        # Check DOM metrics in desktop
        eval_res = await send_cmd('Runtime.evaluate', {'expression': '''
            (() => {
                const aside = document.querySelector('aside');
                const grid = document.getElementById('products-catalog-grid');
                const cards = grid ? Array.from(grid.children).filter(c => c.style.display !== 'none') : [];
                const countText = document.getElementById('catalog-products-count')?.textContent;
                const pagination = document.getElementById('catalog-pagination-container');
                return {
                    asideExists: !!aside,
                    visibleCardsOnPage1: cards.length,
                    countText: countText,
                    paginationVisible: pagination && pagination.style.display !== 'none'
                };
            })()
        ''', 'returnByValue': True})
        print("Desktop DOM state:", eval_res.get('value'))

        # Open Filter Modal on Desktop
        await send_cmd('Runtime.evaluate', {'expression': 'window.openFilterModal();'})
        await asyncio.sleep(0.8)
        res = await send_cmd('Page.captureScreenshot', {'format': 'jpeg', 'quality': 88})
        path2 = os.path.join(OUT_DIR, "catalog_desktop_filter_modal.jpg")
        with open(path2, 'wb') as f:
            f.write(base64.b64decode(res['data']))
        print(f"✓ Saved {path2}")

        # Close Modal
        await send_cmd('Runtime.evaluate', {'expression': 'window.closeFilterModal();'})
        await asyncio.sleep(0.5)

        # Scroll down to pagination bar
        await send_cmd('Runtime.evaluate', {'expression': '''
            const pag = document.getElementById('catalog-pagination-container');
            if (pag) pag.scrollIntoView({ behavior: 'instant', block: 'center' });
        '''})
        await asyncio.sleep(0.8)
        res = await send_cmd('Page.captureScreenshot', {'format': 'jpeg', 'quality': 88})
        path3 = os.path.join(OUT_DIR, "catalog_desktop_pagination_p1.jpg")
        with open(path3, 'wb') as f:
            f.write(base64.b64decode(res['data']))
        print(f"✓ Saved {path3}")

        # Click Page 2
        await send_cmd('Runtime.evaluate', {'expression': 'window.changeCatalogPage(2);'})
        await asyncio.sleep(1.0)
        res = await send_cmd('Page.captureScreenshot', {'format': 'jpeg', 'quality': 88})
        path4 = os.path.join(OUT_DIR, "catalog_desktop_page_2.jpg")
        with open(path4, 'wb') as f:
            f.write(base64.b64decode(res['data']))
        print(f"✓ Saved {path4}")

        eval_p2 = await send_cmd('Runtime.evaluate', {'expression': '''
            (() => {
                const curPage = window.getCurrentCatalogPage();
                const summary = document.getElementById('catalog-pagination-summary')?.textContent.trim();
                const grid = document.getElementById('products-catalog-grid');
                const cards = grid ? Array.from(grid.children).filter(c => c.style.display !== 'none') : [];
                return {
                    currentPage: curPage,
                    summary: summary,
                    visibleCardsOnPage2: cards.length
                };
            })()
        ''', 'returnByValue': True})
        print("Page 2 DOM state:", eval_p2.get('value'))

        # Reset back to Page 1
        await send_cmd('Runtime.evaluate', {'expression': 'window.changeCatalogPage(1);'})
        await asyncio.sleep(0.5)

        # =============================================================
        # 2. MOBILE VIEW AUDIT (390 x 844 iPhone)
        # =============================================================
        print("\n--- AUDITING MOBILE (390x844) ---")
        await send_cmd('Emulation.setDeviceMetricsOverride', {
            'width': 390, 'height': 844, 'deviceScaleFactor': 2, 'mobile': True
        })
        await asyncio.sleep(0.3)
        await send_cmd('Page.navigate', {'url': 'http://localhost:8080/products.html'})
        await asyncio.sleep(2.0)

        # Scroll to mobile controls
        await send_cmd('Runtime.evaluate', {'expression': '''
            const el = document.getElementById('mobile-catalog-products-count') || document.querySelector('.lg\\\\:hidden');
            if (el) el.scrollIntoView({ behavior: 'instant', block: 'start' });
            window.scrollBy(0, -70);
        '''})
        await asyncio.sleep(0.8)

        # Capture Mobile Screenshot 1: Mobile Header, Scrollable Pills, 50/50 Filter/Sort & 2-Col Cards
        res = await send_cmd('Page.captureScreenshot', {'format': 'jpeg', 'quality': 88})
        path5 = os.path.join(OUT_DIR, "catalog_mobile_top_and_cards.jpg")
        with open(path5, 'wb') as f:
            f.write(base64.b64decode(res['data']))
        print(f"✓ Saved {path5}")

        # Open Filter Modal on Mobile
        await send_cmd('Runtime.evaluate', {'expression': 'window.openFilterModal();'})
        await asyncio.sleep(0.8)
        res = await send_cmd('Page.captureScreenshot', {'format': 'jpeg', 'quality': 88})
        path6 = os.path.join(OUT_DIR, "catalog_mobile_filter_modal.jpg")
        with open(path6, 'wb') as f:
            f.write(base64.b64decode(res['data']))
        print(f"✓ Saved {path6}")

        # Close Modal
        await send_cmd('Runtime.evaluate', {'expression': 'window.closeFilterModal();'})
        await asyncio.sleep(0.5)

        # Scroll to mobile pagination
        await send_cmd('Runtime.evaluate', {'expression': '''
            const pag = document.getElementById('catalog-pagination-container');
            if (pag) pag.scrollIntoView({ behavior: 'instant', block: 'center' });
        '''})
        await asyncio.sleep(0.8)
        res = await send_cmd('Page.captureScreenshot', {'format': 'jpeg', 'quality': 88})
        path7 = os.path.join(OUT_DIR, "catalog_mobile_pagination.jpg")
        with open(path7, 'wb') as f:
            f.write(base64.b64decode(res['data']))
        print(f"✓ Saved {path7}")

        # Reset device metrics override back to standard desktop for normal viewing
        await send_cmd('Emulation.setDeviceMetricsOverride', {
            'width': 1440, 'height': 900, 'deviceScaleFactor': 1, 'mobile': False
        })
        print("\nAll catalog redesign audit captures completed successfully!")

if __name__ == '__main__':
    asyncio.run(audit_catalog())

