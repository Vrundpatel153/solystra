import asyncio
import json
import urllib.request
import base64
import websockets
import shutil

async def main():
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(req.read().decode('utf-8'))
    tab = next(t for t in tabs if t.get('type') == 'page' and 'products.html' in t.get('url', ''))
    
    ws_url = tab.get('webSocketDebuggerUrl')
    print("Connecting to:", tab.get('title'))
    
    async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
        msg_id = 1
        
        # Enable
        await ws.send(json.dumps({'id': msg_id, 'method': 'Page.enable'}))
        await ws.recv()
        msg_id += 1
        
        # Close any modal and scroll to pagination
        expr = "if (window.closeMobileFilterModal) window.closeMobileFilterModal(); window.scrollTo({top: 1500, behavior: 'instant'});"
        await ws.send(json.dumps({'id': msg_id, 'method': 'Runtime.evaluate', 'params': {'expression': expr}}))
        await ws.recv()
        msg_id += 1
        await asyncio.sleep(0.5)
        
        # Set desktop viewport
        await ws.send(json.dumps({
            'id': msg_id,
            'method': 'Emulation.setDeviceMetricsOverride',
            'params': {'width': 1440, 'height': 900, 'deviceScaleFactor': 1, 'mobile': False}
        }))
        await ws.recv()
        msg_id += 1
        await asyncio.sleep(0.4)
        
        # Capture screenshot
        await ws.send(json.dumps({
            'id': msg_id,
            'method': 'Page.captureScreenshot',
            'params': {'format': 'jpeg', 'quality': 90}
        }))
        
        while True:
            resp = json.loads(await ws.recv())
            if resp.get('id') == msg_id:
                data = resp['result']['data']
                out_path = 'audit_visuals/audit_2_catalog_pagination_desktop.jpg'
                brain_path = r'C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals\audit_2_catalog_pagination_desktop.jpg'
                with open(out_path, 'wb') as f:
                    f.write(base64.b64decode(data))
                shutil.copy2(out_path, brain_path)
                print("✓ Saved clean desktop pagination!")
                break

if __name__ == '__main__':
    asyncio.run(main())

