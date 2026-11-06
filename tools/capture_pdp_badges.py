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

async def capture_pdp():
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(req.read().decode('utf-8'))
    
    target_tab = None
    for tab in tabs:
        if tab.get('type') == 'page' and 'product.html' in tab.get('url', ''):
            target_tab = tab
            break
            
    if not target_tab:
        print("PDP tab not found")
        return False
        
    ws_url = target_tab.get('webSocketDebuggerUrl')
    print(f"Connecting to: {target_tab.get('title')}")
    
    async with websockets.connect(ws_url, max_size=25*1024*1024) as ws:
        msg_id = 1
        await send_cmd(ws, msg_id, 'Page.enable')
        msg_id += 1
        
        # Navigate directly
        await send_cmd(ws, msg_id, 'Page.navigate', {'url': 'http://127.0.0.1:8080/product.html?id=accent-circle-925-silver-necklace'})
        msg_id += 1
        await asyncio.sleep(1.5)
        
        # Emulation viewport
        device_metrics = {
            'width': 1440,
            'height': 900,
            'deviceScaleFactor': 1,
            'mobile': False,
        }
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', device_metrics)
        msg_id += 1
        
        # Scroll to trust badges in PDP
        scroll_code = "window.scrollTo({ top: 400, behavior: 'instant' });"
        await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': scroll_code})
        msg_id += 1
        await asyncio.sleep(0.5)
        
        # Capture screenshot
        resp = await send_cmd(ws, msg_id, 'Page.captureScreenshot', {'format': 'jpeg', 'quality': 90})
        msg_id += 1
        
        data = resp['result']['data']
        local_path = os.path.join('audit_visuals', 'pdp_trust_badges_desktop.jpg')
        brain_path = os.path.join(r'C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals', 'pdp_trust_badges_desktop.jpg')
        
        with open(local_path, 'wb') as f:
            f.write(base64.b64decode(data))
        shutil.copy2(local_path, brain_path)
        print(f"Saved: {local_path} and {brain_path}")

if __name__ == '__main__':
    asyncio.run(capture_pdp())

