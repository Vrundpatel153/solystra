import asyncio
import json
import urllib.request
import base64
import websockets
import os
import shutil

AUDIT_DIR_LOCAL = 'audit_visuals'
AUDIT_DIR_BRAIN = r'C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals'

async def send_cmd(ws, msg_id, method, params=None):
    payload = {'id': msg_id, 'method': method}
    if params:
        payload['params'] = params
    await ws.send(json.dumps(payload))
    while True:
        resp = json.loads(await ws.recv())
        if resp.get('id') == msg_id:
            return resp

async def capture_screenshot(ws, msg_id, filename):
    resp = await send_cmd(ws, msg_id, 'Page.captureScreenshot', {'format': 'jpeg', 'quality': 90})
    data = resp['result']['data']
    local_p = os.path.join(AUDIT_DIR_LOCAL, filename)
    brain_p = os.path.join(AUDIT_DIR_BRAIN, filename)
    with open(local_p, 'wb') as f:
        f.write(base64.b64decode(data))
    shutil.copy2(local_p, brain_p)
    print(f"✓ Saved screenshot: {filename}")

async def main():
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(req.read().decode('utf-8'))
    tab = next(t for t in tabs if t.get('type') == 'page' and 'products.html' in t.get('url', ''))
    
    ws_url = tab.get('webSocketDebuggerUrl')
    print("Connecting to:", tab.get('title'), f"({ws_url})")
    
    async with websockets.connect(ws_url, max_size=30*1024*1024) as ws:
        msg_id = 1
        await send_cmd(ws, msg_id, 'Page.enable')
        msg_id += 1
        
        # Reload fresh
        await send_cmd(ws, msg_id, 'Page.reload', {'ignoreCache': True})
        msg_id += 1
        await asyncio.sleep(1.5)
        
        # 1. Desktop 1440x900
        print("\n--- 1. Desktop 1440x900 ---")
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {'width': 1440, 'height': 900, 'deviceScaleFactor': 1, 'mobile': False})
        msg_id += 1
        await asyncio.sleep(0.4)
        
        # Open modal
        await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': 'window.openFilterModal();'})
        msg_id += 1
        await asyncio.sleep(0.5)
        
        resp = await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': '''(() => {
            const m = document.getElementById('mobile-filter-modal');
            const card = m ? m.firstElementChild : null;
            const h = card ? card.children[0] : null;
            const b = card ? card.children[1] : null;
            const f = card ? card.children[2] : null;
            return {
                windowH: window.innerHeight,
                cardTop: card.getBoundingClientRect().top,
                cardBottom: card.getBoundingClientRect().bottom,
                cardHeight: card.getBoundingClientRect().height,
                headerTop: h.getBoundingClientRect().top,
                headerHeight: h.getBoundingClientRect().height,
                bodyHeight: b.getBoundingClientRect().height,
                footerBottom: f.getBoundingClientRect().bottom,
                footerHeight: f.getBoundingClientRect().height,
                closeBtnRect: h.querySelector('button') ? h.querySelector('button').getBoundingClientRect() : null
            };
        })()''', 'returnByValue': True})
        msg_id += 1
        print("Desktop 1440x900 Rects:", json.dumps(resp['result']['result']['value'], indent=2))
        
        await capture_screenshot(ws, msg_id, 'solystra_modal_desktop_1440x900.jpg')
        msg_id += 1

        # 2. Short Laptop Viewport (1024x600)
        print("\n--- 2. Short Laptop Viewport 1024x600 ---")
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {'width': 1024, 'height': 600, 'deviceScaleFactor': 1, 'mobile': False})
        msg_id += 1
        await asyncio.sleep(0.5)
        
        resp = await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': '''(() => {
            const m = document.getElementById('mobile-filter-modal');
            const card = m ? m.firstElementChild : null;
            const h = card ? card.children[0] : null;
            const f = card ? card.children[2] : null;
            return {
                windowH: window.innerHeight,
                cardTop: card.getBoundingClientRect().top,
                cardBottom: card.getBoundingClientRect().bottom,
                cardHeight: card.getBoundingClientRect().height,
                headerTop: h.getBoundingClientRect().top,
                headerVisible: h.getBoundingClientRect().top >= 0,
                footerBottom: f.getBoundingClientRect().bottom,
                footerVisible: f.getBoundingClientRect().bottom <= window.innerHeight
            };
        })()''', 'returnByValue': True})
        msg_id += 1
        print("Short 1024x600 Rects:", json.dumps(resp['result']['result']['value'], indent=2))
        
        await capture_screenshot(ws, msg_id, 'solystra_modal_short_1024x600.jpg')
        msg_id += 1

        # 3. Mobile Viewport (390x844)
        print("\n--- 3. Mobile Viewport 390x844 ---")
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {'width': 390, 'height': 844, 'deviceScaleFactor': 2, 'mobile': True})
        msg_id += 1
        await asyncio.sleep(0.5)
        
        # Expand Accordion
        await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': 'window.toggleModalCuratedDropdown();'})
        msg_id += 1
        await asyncio.sleep(0.5)
        
        resp = await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': '''(() => {
            const m = document.getElementById('mobile-filter-modal');
            const card = m ? m.firstElementChild : null;
            const h = card ? card.children[0] : null;
            const f = card ? card.children[2] : null;
            return {
                windowH: window.innerHeight,
                cardTop: card.getBoundingClientRect().top,
                cardBottom: card.getBoundingClientRect().bottom,
                cardHeight: card.getBoundingClientRect().height,
                headerTop: h.getBoundingClientRect().top,
                headerVisible: h.getBoundingClientRect().top >= 0,
                footerBottom: f.getBoundingClientRect().bottom,
                footerVisible: f.getBoundingClientRect().bottom <= window.innerHeight
            };
        })()''', 'returnByValue': True})
        msg_id += 1
        print("Mobile 390x844 Rects:", json.dumps(resp['result']['result']['value'], indent=2))
        
        await capture_screenshot(ws, msg_id, 'solystra_modal_mobile_top.jpg')
        msg_id += 1

        # Scroll inside body
        print("\n--- 4. Scroll inside body ---")
        await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': '''(() => {
            const body = document.querySelector('#mobile-filter-modal .flex-1');
            if (body) body.scrollTo({ top: 350, behavior: 'smooth' });
        })()'''})
        msg_id += 1
        await asyncio.sleep(0.8)
        
        await capture_screenshot(ws, msg_id, 'solystra_modal_mobile_scrolled.jpg')
        msg_id += 1

        print("\n✓ All tests completed!")

if __name__ == '__main__':
    asyncio.run(main())
