import asyncio
import json
import urllib.request
import base64
import websockets
import os
import shutil

async def send_cmd(ws, msg_id, method, params=None):
    payload = {'id': msg_id, 'method': method}
    if params:
        payload['params'] = params
    await ws.send(json.dumps(payload))
    while True:
        resp = json.loads(await ws.recv())
        if resp.get('id') == msg_id:
            return resp

async def capture_pagination():
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(req.read().decode('utf-8'))
    
    target_tab = None
    for t in tabs:
        if t.get('type') == 'page' and 'products.html' in t.get('url', ''):
            target_tab = t
            break
            
    if not target_tab:
        print("Tab for products.html not found, will navigate first available tab")
        target_tab = tabs[0]
        
    ws_url = target_tab.get('webSocketDebuggerUrl')
    print(f"Connecting to: {target_tab.get('title')}")
    
    async with websockets.connect(ws_url, max_size=25*1024*1024) as ws:
        msg_id = 1
        await send_cmd(ws, msg_id, 'Page.enable')
        msg_id += 1
        
        # Ensure we are on products.html
        await send_cmd(ws, msg_id, 'Page.navigate', {'url': 'http://127.0.0.1:8080/products.html'})
        msg_id += 1
        await asyncio.sleep(1.5)
        
        # 1. Desktop pagination
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {'width': 1440, 'height': 900, 'deviceScaleFactor': 1, 'mobile': False})
        msg_id += 1
        await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': 'if (window.closeMobileFilterModal) window.closeMobileFilterModal(); window.scrollTo({top: 1400, behavior: "instant"});'})
        msg_id += 1
        await asyncio.sleep(0.6)
        
        resp = await send_cmd(ws, msg_id, 'Page.captureScreenshot', {'format': 'jpeg', 'quality': 90})
        msg_id += 1
        data = resp['result']['data']
        with open('audit_visuals/audit_2_catalog_pagination_desktop.jpg', 'wb') as f:
            f.write(base64.b64decode(data))
        shutil.copy2('audit_visuals/audit_2_catalog_pagination_desktop.jpg', r'C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals\audit_2_catalog_pagination_desktop.jpg')
        print("✓ Desktop pagination screenshot updated!")

        # 2. Mobile pagination
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {'width': 390, 'height': 844, 'deviceScaleFactor': 2, 'mobile': True})
        msg_id += 1
        await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': 'if (window.closeMobileFilterModal) window.closeMobileFilterModal(); window.scrollTo({top: 3400, behavior: "instant"});'})
        msg_id += 1
        await asyncio.sleep(0.6)
        
        resp = await send_cmd(ws, msg_id, 'Page.captureScreenshot', {'format': 'jpeg', 'quality': 90})
        msg_id += 1
        data = resp['result']['data']
        with open('audit_visuals/audit_2_catalog_mobile_pagination.jpg', 'wb') as f:
            f.write(base64.b64decode(data))
        shutil.copy2('audit_visuals/audit_2_catalog_mobile_pagination.jpg', r'C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals\audit_2_catalog_mobile_pagination.jpg')
        print("✓ Mobile pagination screenshot updated!")

if __name__ == '__main__':
    asyncio.run(capture_pagination())
