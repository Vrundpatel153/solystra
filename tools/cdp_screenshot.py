import asyncio
import json
import urllib.request
import base64
import sys
import websockets

async def capture_cdp_screenshot(url_filter, out_path, width=1440, height=900, is_mobile=False, slide_idx=None):
    # 1. Get tabs
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(req.read().decode('utf-8'))
    
    target_tab = None
    for tab in tabs:
        if tab.get('type') == 'page' and url_filter in tab.get('url', ''):
            target_tab = tab
            break
            
    if not target_tab:
        print(f"Tab matching '{url_filter}' not found among {[t.get('url') for t in tabs]}")
        return False
        
    ws_url = target_tab.get('webSocketDebuggerUrl')
    print(f"Connecting to tab: {target_tab.get('title')} ({ws_url})")
    
    async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
        msg_id = 1
        
        # Enable Page and Emulation
        await ws.send(json.dumps({'id': msg_id, 'method': 'Page.enable'}))
        await ws.recv()
        msg_id += 1
        
        # Set viewport
        device_metrics = {
            'width': width,
            'height': height,
            'deviceScaleFactor': 2 if is_mobile else 1,
            'mobile': is_mobile,
        }
        await ws.send(json.dumps({'id': msg_id, 'method': 'Emulation.setDeviceMetricsOverride', 'params': device_metrics}))
        await ws.recv()
        msg_id += 1
        
        # If slide specified, set hero slide
        if slide_idx is not None:
            expr = f"window.setHeroSlide({slide_idx});"
            await ws.send(json.dumps({'id': msg_id, 'method': 'Runtime.evaluate', 'params': {'expression': expr}}))
            await ws.recv()
            msg_id += 1
            await asyncio.sleep(0.3)
            
        # Capture screenshot
        await ws.send(json.dumps({
            'id': msg_id,
            'method': 'Page.captureScreenshot',
            'params': {'format': 'jpeg', 'quality': 85}
        }))
        
        while True:
            resp = json.loads(await ws.recv())
            if resp.get('id') == msg_id:
                data = resp['result']['data']
                with open(out_path, 'wb') as f:
                    f.write(base64.b64decode(data))
                print(f"✓ Screenshot successfully saved to {out_path} ({len(data)//1024} KB)")
                return True

if __name__ == '__main__':
    url_filter = sys.argv[1] if len(sys.argv) > 1 else '8080'
    out_path = sys.argv[2] if len(sys.argv) > 2 else 'scratch/cdp_test.jpg'
    w = int(sys.argv[3]) if len(sys.argv) > 3 else 1440
    h = int(sys.argv[4]) if len(sys.argv) > 4 else 900
    is_mob = (sys.argv[5].lower() == 'true') if len(sys.argv) > 5 else False
    slide = int(sys.argv[6]) if len(sys.argv) > 6 else None
    
    asyncio.run(capture_cdp_screenshot(url_filter, out_path, w, h, is_mob, slide))

