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
        
        # 1. Desktop 1440x900
        print("\n--- 1. Desktop 1440x900 Initial Load ---")
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {'width': 1440, 'height': 900, 'deviceScaleFactor': 1, 'mobile': False})
        msg_id += 1
        
        # Navigate to index.html with cache disabled
        await send_cmd(ws, msg_id, 'Page.navigate', {'url': 'http://127.0.0.1:8080/index.html'})
        msg_id += 1
        await asyncio.sleep(0.8) # initial render
        
        # Check computed styles of all 4 slides
        res = await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': '''
            (() => {
                const results = [];
                for (let i = 0; i < 4; i++) {
                    const el = document.getElementById('hero-slide-' + i);
                    if (el) {
                        const style = window.getComputedStyle(el);
                        results.push({
                            slide: i,
                            className: el.className,
                            opacity: style.opacity,
                            zIndex: style.zIndex,
                            pointerEvents: style.pointerEvents,
                            title: el.querySelector('h2') ? el.querySelector('h2').innerText : ''
                        });
                    }
                }
                return JSON.stringify(results, null, 2);
            })()
        '''})
        msg_id += 1
        print("Slide states immediately after load:\n", res['result']['result']['value'])
        
        # Capture desktop hero banner
        clip_hero_desktop = {'x': 0, 'y': 0, 'width': 1440, 'height': 720, 'scale': 1}
        await capture_screenshot(ws, msg_id, 'hero_fixed_initial_desktop.jpg', clip_hero_desktop)
        msg_id += 1
        
        # 2. Test Slide Transition to Slide 1
        print("\n--- 2. Transitioning to Slide 1 (Blush Tones) ---")
        await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': 'window.setHeroSlide(1)'})
        msg_id += 1
        await asyncio.sleep(0.8) # wait for 700ms transition
        await capture_screenshot(ws, msg_id, 'hero_fixed_slide1_desktop.jpg', clip_hero_desktop)
        msg_id += 1
        
        # 3. Test Slide Transition to Slide 2 (Modern Classics)
        print("\n--- 3. Transitioning to Slide 2 (Modern Classics) ---")
        await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': 'window.setHeroSlide(2)'})
        msg_id += 1
        await asyncio.sleep(0.8)
        await capture_screenshot(ws, msg_id, 'hero_fixed_slide2_desktop.jpg', clip_hero_desktop)
        msg_id += 1
        
        # Reset back to Slide 0
        await send_cmd(ws, msg_id, 'Runtime.evaluate', {'expression': 'window.setHeroSlide(0)'})
        msg_id += 1
        await asyncio.sleep(0.8)
        
        # 4. Mobile 390x844 Initial Load
        print("\n--- 4. Mobile 390x844 Initial Load ---")
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {'width': 390, 'height': 844, 'deviceScaleFactor': 1, 'mobile': True})
        msg_id += 1
        
        # Hard reload on mobile
        await send_cmd(ws, msg_id, 'Page.reload', {'ignoreCache': True})
        msg_id += 1
        await asyncio.sleep(0.8)
        
        clip_hero_mobile = {'x': 0, 'y': 0, 'width': 390, 'height': 640, 'scale': 1}
        await capture_screenshot(ws, msg_id, 'hero_fixed_initial_mobile.jpg', clip_hero_mobile)
        msg_id += 1
        
        print("\nAll hero banner glitch verification tests completed!")

asyncio.run(main())

