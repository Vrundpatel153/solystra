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

async def capture_target(tab_url_match, filename, width, height, is_mobile=False, scroll_y=0):
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(req.read().decode('utf-8'))
    
    target_tab = None
    for tab in tabs:
        if tab.get('type') == 'page' and tab_url_match in tab.get('url', ''):
            target_tab = tab
            break
            
    if not target_tab:
        print(f"Tab matching '{tab_url_match}' not found")
        return False
        
    ws_url = target_tab.get('webSocketDebuggerUrl')
    print(f"Connecting to: {target_tab.get('title')} ({ws_url})")
    
    async with websockets.connect(ws_url, max_size=25*1024*1024) as ws:
        msg_id = 1
        
        await send_cmd(ws, msg_id, 'Page.enable')
        msg_id += 1
        
        # Reload page
        await send_cmd(ws, msg_id, 'Page.reload')
        msg_id += 1
        await asyncio.sleep(1.2)
        
        # Emulation viewport
        device_metrics = {
            'width': width,
            'height': height,
            'deviceScaleFactor': 2 if is_mobile else 1,
            'mobile': is_mobile,
        }
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', device_metrics)
        msg_id += 1
        await asyncio.sleep(0.5)
        
        # Scroll to target position
        scroll_code = f"window.scrollTo({{ top: {scroll_y}, behavior: 'instant' }});"
        await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': scroll_code})
        msg_id += 1
        await asyncio.sleep(0.6)
        
        # Capture screenshot
        resp = await send_cmd(ws, msg_id, 'Page.captureScreenshot', {'format': 'jpeg', 'quality': 90})
        msg_id += 1
        
        data = resp['result']['data']
        os.makedirs('audit_visuals', exist_ok=True)
        brain_dir = r'C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals'
        os.makedirs(brain_dir, exist_ok=True)
        local_path = os.path.join('audit_visuals', filename)
        brain_path = os.path.join(brain_dir, filename)
        
        with open(local_path, 'wb') as f:
            f.write(base64.b64decode(data))
        shutil.copy2(local_path, brain_path)
        print(f"Saved: {local_path} and {brain_path}")
        return True

async def main():
    # 1. Homepage desktop trust badges (scroll 420px to see hero bottom + badges + category heading)
    await capture_target('index.html', 'homepage_trust_badges_fixed_desktop.jpg', 1440, 900, is_mobile=False, scroll_y=420)
    
    # 2. Homepage mobile trust badges (scroll 280px)
    await capture_target('index.html', 'homepage_trust_badges_fixed_mobile.jpg', 390, 844, is_mobile=True, scroll_y=280)
    
    # 3. Product page desktop trust badges
    await capture_target('product.html', 'pdp_trust_badges_desktop.jpg', 1440, 900, is_mobile=False, scroll_y=550)

if __name__ == '__main__':
    asyncio.run(main())
