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
    tab = next(t for t in tabs if t.get('type') == 'page' and '8080' in t.get('url', ''))
    
    ws_url = tab.get('webSocketDebuggerUrl')
    print("Connecting to:", tab.get('title'), f"({ws_url})")
    
    async with websockets.connect(ws_url, max_size=30*1024*1024) as ws:
        msg_id = 1
        await send_cmd(ws, msg_id, 'Page.enable')
        msg_id += 1
        
        # Hard reload fresh
        await send_cmd(ws, msg_id, 'Page.reload', {'ignoreCache': True})
        msg_id += 1
        await asyncio.sleep(2.0)
        
        # 1. Desktop 1440x900
        print("\n--- 1. Desktop 1440x900 ---")
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {'width': 1440, 'height': 900, 'deviceScaleFactor': 1, 'mobile': False})
        msg_id += 1
        await asyncio.sleep(0.5)
        
        # Open modal
        res = await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': '''
            (() => {
                window.openMobileFilterModal();
                const m = document.getElementById('mobile-filter-modal');
                const card = m ? m.children[0] : null;
                const header = card ? card.children[0] : null;
                const body = card ? card.children[1] : null;
                const footer = card ? card.children[2] : null;
                return JSON.stringify({
                    modalVisible: !m.classList.contains('hidden'),
                    cardRect: card ? card.getBoundingClientRect() : null,
                    headerRect: header ? header.getBoundingClientRect() : null,
                    footerRect: footer ? footer.getBoundingClientRect() : null,
                    bodyScrollHeight: body ? body.scrollHeight : 0,
                    bodyClientHeight: body ? body.clientHeight : 0,
                    bodyScrollable: body ? body.scrollHeight > body.clientHeight : false
                }, null, 2);
            })()
        ''', 'returnByValue': True})
        msg_id += 1
        print("Desktop 1440x900 stats:\n", res['result']['result']['value'])
        await asyncio.sleep(0.4)
        await capture_screenshot(ws, msg_id, 'solystra_modal_desktop_1440x900.jpg')
        msg_id += 1
        
        # 2. Short Laptop Screen 1024x600 (Stress test)
        print("\n--- 2. Short Laptop Screen 1024x600 ---")
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {'width': 1024, 'height': 600, 'deviceScaleFactor': 1, 'mobile': False})
        msg_id += 1
        await asyncio.sleep(0.5)
        res = await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': '''
            (() => {
                const m = document.getElementById('mobile-filter-modal');
                const card = m ? m.children[0] : null;
                const header = card ? card.children[0] : null;
                const footer = card ? card.children[2] : null;
                return JSON.stringify({
                    cardTop: card ? card.getBoundingClientRect().top : null,
                    cardBottom: card ? card.getBoundingClientRect().bottom : null,
                    cardHeight: card ? card.getBoundingClientRect().height : null,
                    headerTop: header ? header.getBoundingClientRect().top : null,
                    footerBottom: footer ? footer.getBoundingClientRect().bottom : null,
                    windowHeight: window.innerHeight
                }, null, 2);
            })()
        ''', 'returnByValue': True})
        msg_id += 1
        print("Short Screen 1024x600 stats:\n", res['result']['result']['value'])
        await capture_screenshot(ws, msg_id, 'solystra_modal_short_1024x600.jpg')
        msg_id += 1
        
        # 3. Mobile Viewport 390x844
        print("\n--- 3. Mobile Viewport 390x844 ---")
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {'width': 390, 'height': 844, 'deviceScaleFactor': 2, 'mobile': True})
        msg_id += 1
        await asyncio.sleep(0.5)
        
        res = await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': '''
            (() => {
                const m = document.getElementById('mobile-filter-modal');
                const card = m ? m.children[0] : null;
                const header = card ? card.children[0] : null;
                const closeBtn = header ? header.querySelector('button') : null;
                return JSON.stringify({
                    windowInnerWidth: window.innerWidth,
                    cardRect: card ? card.getBoundingClientRect() : null,
                    headerRect: header ? header.getBoundingClientRect() : null,
                    closeBtnRect: closeBtn ? closeBtn.getBoundingClientRect() : null
                }, null, 2);
            })()
        ''', 'returnByValue': True})
        msg_id += 1
        print("Mobile 390x844 stats:\n", res['result']['result']['value'])
        
        await capture_screenshot(ws, msg_id, 'solystra_modal_mobile_top.jpg')
        msg_id += 1
        
        # Scroll down inside modal body
        await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': '''
            (() => {
                const m = document.getElementById('mobile-filter-modal');
                const body = m.children[0].children[1];
                body.scrollTop = 250;
            })()
        '''})
        msg_id += 1
        await asyncio.sleep(0.4)
        await capture_screenshot(ws, msg_id, 'solystra_modal_mobile_scrolled.jpg')
        msg_id += 1
        
        print("\nAll Solystra modal verification captures finished!")

asyncio.run(main())
