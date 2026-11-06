import asyncio
import json
import urllib.request
import base64
import os
import websockets

os.makedirs('scratch/ui_audit_shots', exist_ok=True)

async def audit_all():
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
        print("No page tab found!")
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

        # 1. Navigate to index.html with fresh reload
        await send_cmd('Page.enable')
        await send_cmd('Page.navigate', {'url': 'http://localhost:8080/index.html'})
        await asyncio.sleep(2.0)
        
        # Stop auto-rotate interval definitively
        await send_cmd('Runtime.evaluate', {'expression': '''
            if (window.heroCarouselInterval) clearInterval(window.heroCarouselInterval);
            let id = window.setInterval(function() {}, 0);
            while (id--) window.clearInterval(id);
        '''})

        # -------------------------------------------------------------
        # DESKTOP AUDIT (1440 x 900)
        # -------------------------------------------------------------
        await send_cmd('Emulation.setDeviceMetricsOverride', {
            'width': 1440, 'height': 900, 'deviceScaleFactor': 1, 'mobile': False
        })
        await asyncio.sleep(0.5)
        
        for slide_idx in range(4):
            await send_cmd('Runtime.evaluate', {'expression': f'window.setHeroSlide({slide_idx});'})
            await asyncio.sleep(1.0)
            res = await send_cmd('Page.captureScreenshot', {'format': 'jpeg', 'quality': 85})
            shot_path = f'scratch/ui_audit_shots/desktop_slide_{slide_idx}.jpg'
            with open(shot_path, 'wb') as f:
                f.write(base64.b64decode(res['data']))
            print(f"✓ Saved {shot_path}")

        # -------------------------------------------------------------
        # MOBILE AUDIT (390 x 844 iPhone 14/15)
        # -------------------------------------------------------------
        await send_cmd('Emulation.setDeviceMetricsOverride', {
            'width': 390, 'height': 844, 'deviceScaleFactor': 2, 'mobile': True
        })
        await asyncio.sleep(0.5)
        
        for slide_idx in range(4):
            await send_cmd('Runtime.evaluate', {'expression': f'window.setHeroSlide({slide_idx});'})
            await asyncio.sleep(1.0)
            res = await send_cmd('Page.captureScreenshot', {'format': 'jpeg', 'quality': 85})
            shot_path = f'scratch/ui_audit_shots/mobile_slide_{slide_idx}.jpg'
            with open(shot_path, 'wb') as f:
                f.write(base64.b64decode(res['data']))
            print(f"✓ Saved {shot_path}")

        # -------------------------------------------------------------
        # CATEGORIES PAGE AUDIT (categories.html)
        # -------------------------------------------------------------
        await send_cmd('Page.navigate', {'url': 'http://localhost:8080/categories.html'})
        await asyncio.sleep(1.0)
        res = await send_cmd('Page.captureScreenshot', {'format': 'jpeg', 'quality': 85})
        with open('scratch/ui_audit_shots/categories_mobile_grid.jpg', 'wb') as f:
            f.write(base64.b64decode(res['data']))
        print("✓ Saved scratch/ui_audit_shots/categories_mobile_grid.jpg")
        
        # -------------------------------------------------------------
        # PRODUCTS FILTER MODAL AUDIT (products.html)
        # -------------------------------------------------------------
        await send_cmd('Page.navigate', {'url': 'http://localhost:8080/products.html'})
        await asyncio.sleep(1.0)
        await send_cmd('Runtime.evaluate', {'expression': 'if(window.openMobileFilterModal) window.openMobileFilterModal();'})
        await asyncio.sleep(0.5)
        res = await send_cmd('Page.captureScreenshot', {'format': 'jpeg', 'quality': 85})
        with open('scratch/ui_audit_shots/products_mobile_filter_modal.jpg', 'wb') as f:
            f.write(base64.b64decode(res['data']))
        print("✓ Saved scratch/ui_audit_shots/products_mobile_filter_modal.jpg")

asyncio.run(audit_all())
