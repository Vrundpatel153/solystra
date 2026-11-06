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
    tab = None
    for t in tabs:
        if t.get('type') == 'page' and 'products.html' in t.get('url', ''):
            tab = t
            break
    if not tab:
        for t in tabs:
            if t.get('type') == 'page':
                tab = t
                break

    ws_url = tab.get('webSocketDebuggerUrl')
    print("Connecting to tab:", tab.get('title'))
    
    async with websockets.connect(ws_url, max_size=30*1024*1024) as ws:
        msg_id = 1
        await send_cmd(ws, msg_id, 'Page.enable')
        msg_id += 1
        
        # Navigate to products.html
        await send_cmd(ws, msg_id, 'Page.navigate', {'url': 'http://127.0.0.1:8080/products.html'})
        msg_id += 1
        await asyncio.sleep(1.5)
        
        # TEST 1: Desktop 1440x900 - Open Filter Modal
        print("\n--- Test 1: Desktop (1440x900) ---")
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {'width': 1440, 'height': 900, 'deviceScaleFactor': 1, 'mobile': False})
        msg_id += 1
        await asyncio.sleep(0.5)
        
        await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': 'window.openFilterModal();'})
        msg_id += 1
        await asyncio.sleep(0.6)
        
        await capture_screenshot(ws, msg_id, 'modal_fixed_desktop_top.jpg')
        msg_id += 1

        # Expand Curated Collections Accordion and scroll down inside modal
        print("\n--- Test 2: Expand Accordion & Scroll Modal ---")
        await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': '''(() => {
            window.toggleModalCuratedDropdown();
            setTimeout(() => {
                const body = document.querySelector('#mobile-filter-modal .flex-1');
                if (body) body.scrollTo({ top: 350, behavior: 'smooth' });
            }, 300);
        })()'''})
        msg_id += 1
        await asyncio.sleep(1.0)
        
        await capture_screenshot(ws, msg_id, 'modal_fixed_desktop_scrolled.jpg')
        msg_id += 1

        # TEST 3: Short laptop viewport (1024x600) to prove Header & Footer NEVER get cut off!
        print("\n--- Test 3: Short Laptop Viewport (1024x600) ---")
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {'width': 1024, 'height': 600, 'deviceScaleFactor': 1, 'mobile': False})
        msg_id += 1
        await asyncio.sleep(0.5)
        await capture_screenshot(ws, msg_id, 'modal_fixed_short_viewport_1024x600.jpg')
        msg_id += 1

        # TEST 4: Mobile Viewport (390x844)
        print("\n--- Test 4: Mobile (390x844) ---")
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {'width': 390, 'height': 844, 'deviceScaleFactor': 2, 'mobile': True})
        msg_id += 1
        await asyncio.sleep(0.5)
        
        # Scroll back to top inside modal
        await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': '''(() => {
            const body = document.querySelector('#mobile-filter-modal .flex-1');
            if (body) body.scrollTo({ top: 0, behavior: 'instant' });
        })()'''})
        msg_id += 1
        await asyncio.sleep(0.4)
        await capture_screenshot(ws, msg_id, 'modal_fixed_mobile_top.jpg')
        msg_id += 1

        # Scroll inside mobile modal to bottom
        await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': '''(() => {
            const body = document.querySelector('#mobile-filter-modal .flex-1');
            if (body) body.scrollTo({ top: 380, behavior: 'smooth' });
        })()'''})
        msg_id += 1
        await asyncio.sleep(0.8)
        await capture_screenshot(ws, msg_id, 'modal_fixed_mobile_scrolled.jpg')
        msg_id += 1

        # TEST 5: Test Close Button
        print("\n--- Test 5: Close Modal via Close button ---")
        await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': 'window.closeMobileFilterModal();'})
        msg_id += 1
        await asyncio.sleep(0.5)
        await capture_screenshot(ws, msg_id, 'modal_fixed_mobile_closed.jpg')
        msg_id += 1

        print("\n✓ All modal tests completed successfully!")

if __name__ == '__main__':
    asyncio.run(main())
