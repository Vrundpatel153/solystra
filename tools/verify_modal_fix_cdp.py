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
    tab = tabs[0]
    for t in tabs:
        if t.get('type') == 'page' and ('products.html' in t.get('url', '') or '8080' in t.get('url', '')):
            tab = t
            break

    ws_url = tab.get('webSocketDebuggerUrl')
    print("Connecting to tab:", tab.get('title'))
    
    async with websockets.connect(ws_url, max_size=30*1024*1024) as ws:
        msg_id = 1
        await send_cmd(ws, msg_id, 'Page.enable')
        msg_id += 1
        
        # Navigate directly to fresh URL to bypass cache
        await send_cmd(ws, msg_id, 'Page.navigate', {'url': 'http://127.0.0.1:8080/products.html?ts=20261107_v13'})
        msg_id += 1
        await asyncio.sleep(1.8)
        
        # 1. Desktop 1440x900
        print("\n--- Testing Desktop 1440x900 ---")
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {'width': 1440, 'height': 900, 'deviceScaleFactor': 1, 'mobile': False})
        msg_id += 1
        await asyncio.sleep(0.4)
        
        # Open modal
        await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': 'window.openFilterModal();'})
        msg_id += 1
        await asyncio.sleep(0.6)
        
        # Check bounding rects
        rect_resp = await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': '''(() => {
            const m = document.getElementById('mobile-filter-modal');
            const card = m ? m.firstElementChild : null;
            const h = card ? card.firstElementChild : null;
            const f = card ? card.lastElementChild : null;
            return {
                windowHeight: window.innerHeight,
                cardTop: card ? card.getBoundingClientRect().top : 0,
                cardBottom: card ? card.getBoundingClientRect().bottom : 0,
                headerVisible: h ? h.getBoundingClientRect().top >= 0 : false,
                footerVisible: f ? f.getBoundingClientRect().bottom <= window.innerHeight : false
            };
        })()''', 'returnByValue': True})
        msg_id += 1
        print("DOM Check (1440x900):", json.dumps(rect_resp['result']['result']['value']))
        
        await capture_screenshot(ws, msg_id, 'modal_verified_desktop_1440x900.jpg')
        msg_id += 1

        # 2. Short Laptop Viewport (1024x650)
        print("\n--- Testing Short Laptop Viewport 1024x650 ---")
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {'width': 1024, 'height': 650, 'deviceScaleFactor': 1, 'mobile': False})
        msg_id += 1
        await asyncio.sleep(0.5)
        
        rect_resp = await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': '''(() => {
            const m = document.getElementById('mobile-filter-modal');
            const card = m ? m.firstElementChild : null;
            const h = card ? card.firstElementChild : null;
            const f = card ? card.lastElementChild : null;
            return {
                windowHeight: window.innerHeight,
                cardTop: card ? card.getBoundingClientRect().top : 0,
                cardBottom: card ? card.getBoundingClientRect().bottom : 0,
                headerVisible: h ? h.getBoundingClientRect().top >= 0 : false,
                footerVisible: f ? f.getBoundingClientRect().bottom <= window.innerHeight : false
            };
        })()''', 'returnByValue': True})
        msg_id += 1
        print("DOM Check (1024x650):", json.dumps(rect_resp['result']['result']['value']))
        
        await capture_screenshot(ws, msg_id, 'modal_verified_short_1024x650.jpg')
        msg_id += 1

        # 3. Mobile Viewport (390x844)
        print("\n--- Testing Mobile 390x844 ---")
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {'width': 390, 'height': 844, 'deviceScaleFactor': 2, 'mobile': True})
        msg_id += 1
        await asyncio.sleep(0.5)
        
        # Expand Accordion on mobile
        await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': 'window.toggleModalCuratedDropdown();'})
        msg_id += 1
        await asyncio.sleep(0.5)
        
        rect_resp = await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': '''(() => {
            const m = document.getElementById('mobile-filter-modal');
            const card = m ? m.firstElementChild : null;
            const h = card ? card.firstElementChild : null;
            const f = card ? card.lastElementChild : null;
            return {
                windowHeight: window.innerHeight,
                cardTop: card ? card.getBoundingClientRect().top : 0,
                cardBottom: card ? card.getBoundingClientRect().bottom : 0,
                headerVisible: h ? h.getBoundingClientRect().top >= 0 : false,
                footerVisible: f ? f.getBoundingClientRect().bottom <= window.innerHeight : false
            };
        })()''', 'returnByValue': True})
        msg_id += 1
        print("DOM Check (Mobile 390x844):", json.dumps(rect_resp['result']['result']['value']))
        
        await capture_screenshot(ws, msg_id, 'modal_verified_mobile_accordion_open.jpg')
        msg_id += 1

        # Scroll inside mobile body
        await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': '''(() => {
            const body = document.querySelector('#mobile-filter-modal .flex-1');
            if (body) body.scrollTo({ top: 300, behavior: 'instant' });
        })()'''})
        msg_id += 1
        await asyncio.sleep(0.4)
        await capture_screenshot(ws, msg_id, 'modal_verified_mobile_scrolled.jpg')
        msg_id += 1

        print("\n✓ Verification finished!")

if __name__ == '__main__':
    asyncio.run(main())
