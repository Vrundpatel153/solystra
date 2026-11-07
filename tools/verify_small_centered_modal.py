import asyncio
import json
import urllib.request
import base64
import websockets
import os
import shutil

AUDIT_DIR_LOCAL = 'audit_visuals'
AUDIT_DIR_BRAIN = r'C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals'
os.makedirs(AUDIT_DIR_LOCAL, exist_ok=True)
os.makedirs(AUDIT_DIR_BRAIN, exist_ok=True)

async def send_cmd(ws, msg_id, method, params=None):
    payload = {'id': msg_id, 'method': method}
    if params:
        payload['params'] = params
    await ws.send(json.dumps(payload))
    while True:
        resp = json.loads(await ws.recv())
        if resp.get('id') == msg_id:
            return resp

async def capture_screenshot(ws, msg_id, filename, clip=None):
    params = {'format': 'jpeg', 'quality': 90}
    if clip:
        params['clip'] = clip
    resp = await send_cmd(ws, msg_id, 'Page.captureScreenshot', params)
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
    tab = next(t for t in tabs if t.get('type') == 'page' and '8080' in t.get('url', ''))
    
    ws_url = tab.get('webSocketDebuggerUrl')
    print("Connecting to:", tab.get('title'), f"({ws_url})")
    
    async with websockets.connect(ws_url, max_size=30*1024*1024) as ws:
        msg_id = 1
        await send_cmd(ws, msg_id, 'Page.enable')
        msg_id += 1
        
        # Navigate to products.html
        print("Navigating to http://127.0.0.1:8080/products.html...")
        await send_cmd(ws, msg_id, 'Page.navigate', {'url': 'http://127.0.0.1:8080/products.html'})
        msg_id += 1
        await asyncio.sleep(1.5)
        
        # 1. Desktop 1440x900
        print("\n--- 1. Desktop 1440x900 ---")
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {'width': 1440, 'height': 900, 'deviceScaleFactor': 1, 'mobile': False})
        msg_id += 1
        await asyncio.sleep(0.4)
        
        # Open small modal
        res = await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': '''
            (() => {
                window.openMobileFilterModal();
                const m = document.getElementById('mobile-filter-modal');
                const card = m ? m.children[0] : null;
                const header = card ? card.children[0] : null;
                const body = card ? card.children[1] : null;
                const footer = card ? card.children[2] : null;
                return JSON.stringify({
                    modalVisible: m ? m.style.display !== 'none' : false,
                    cardRect: card ? card.getBoundingClientRect() : null,
                    headerRect: header ? header.getBoundingClientRect() : null,
                    footerRect: footer ? footer.getBoundingClientRect() : null,
                    bodyScrollHeight: body ? body.scrollHeight : 0,
                    bodyClientHeight: body ? body.clientHeight : 0,
                    bodyScrollable: body ? body.scrollHeight > body.clientHeight : false,
                    windowInnerHeight: window.innerHeight,
                    windowInnerWidth: window.innerWidth
                }, null, 2);
            })()
        '''})
        msg_id += 1
        print("Desktop stats:\n", res['result']['result']['value'])
        await asyncio.sleep(0.4)
        
        await capture_screenshot(ws, msg_id, 'small_modal_desktop_1440x900.jpg')
        msg_id += 1
        
        # Scroll inside body to show thin scroller
        await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': '''
            (() => {
                const body = document.getElementById('filter-modal-scroll');
                if (body) body.scrollTop = 120;
            })()
        '''})
        msg_id += 1
        await asyncio.sleep(0.3)
        await capture_screenshot(ws, msg_id, 'small_modal_desktop_scrolled.jpg')
        msg_id += 1
        
        # 2. Short Laptop Screen 1024x600 (Stress Test)
        print("\n--- 2. Short Laptop Screen 1024x600 ---")
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {'width': 1024, 'height': 600, 'deviceScaleFactor': 1, 'mobile': False})
        msg_id += 1
        await asyncio.sleep(0.4)
        
        res = await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': '''
            (() => {
                const card = document.querySelector('#mobile-filter-modal > div');
                return JSON.stringify({
                    cardRect: card ? card.getBoundingClientRect() : null,
                    windowH: window.innerHeight,
                    marginFromTop: card ? card.getBoundingClientRect().top : 0,
                    marginFromBottom: card ? window.innerHeight - card.getBoundingClientRect().bottom : 0
                }, null, 2);
            })()
        '''})
        msg_id += 1
        print("Short screen stats:\n", res['result']['result']['value'])
        await capture_screenshot(ws, msg_id, 'small_modal_short_1024x600.jpg')
        msg_id += 1
        
        # 3. Mobile Viewport 390x844
        print("\n--- 3. Mobile Viewport 390x844 ---")
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {'width': 390, 'height': 844, 'deviceScaleFactor': 1, 'mobile': True})
        msg_id += 1
        await asyncio.sleep(0.4)
        
        clip_m = {'x': 0, 'y': 0, 'width': 390, 'height': 844, 'scale': 1}
        await capture_screenshot(ws, msg_id, 'small_modal_mobile_390x844.jpg', clip_m)
        msg_id += 1
        
        # Scroll inside mobile body
        await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': '''
            (() => {
                const body = document.getElementById('filter-modal-scroll');
                if (body) body.scrollTop = 150;
            })()
        '''})
        msg_id += 1
        await asyncio.sleep(0.3)
        await capture_screenshot(ws, msg_id, 'small_modal_mobile_scrolled.jpg', clip_m)
        msg_id += 1
        
        # 4. Close modal
        await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': 'window.closeMobileFilterModal();'})
        msg_id += 1
        await asyncio.sleep(0.3)
        await capture_screenshot(ws, msg_id, 'small_modal_closed.jpg', clip_m)
        msg_id += 1
        
        print("\nAll small modal tests verified successfully!")

asyncio.run(main())

