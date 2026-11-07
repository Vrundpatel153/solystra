import asyncio
import json
import urllib.request
import base64
import websockets
import os
import shutil

ARTIFACT_DIR = r"C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals"
os.makedirs(ARTIFACT_DIR, exist_ok=True)
os.makedirs("audit_visuals", exist_ok=True)

async def send_cmd(ws, msg_id, method, params=None):
    payload = {'id': msg_id, 'method': method}
    if params:
        payload['params'] = params
    await ws.send(json.dumps(payload))
    while True:
        resp = json.loads(await ws.recv())
        if resp.get('id') == msg_id:
            return resp

async def run_eval(ws, msg_id, expr):
    resp = await send_cmd(ws, msg_id, 'Runtime.evaluate', {
        'expression': expr,
        'returnByValue': True,
        'awaitPromise': True
    })
    return resp.get('result', {}).get('result', {}).get('value')

async def save_screenshot(ws, msg_id, filename):
    shot = await send_cmd(ws, msg_id, 'Page.captureScreenshot', {'format': 'jpeg', 'quality': 85})
    img_data = base64.b64decode(shot['result']['data'])
    local_path = os.path.join("audit_visuals", filename)
    with open(local_path, "wb") as f:
        f.write(img_data)
    art_path = os.path.join(ARTIFACT_DIR, filename)
    shutil.copy(local_path, art_path)
    print(f"Captured & saved: {filename} ({len(img_data)} bytes)")
    return local_path

async def main():
    base_url = "http://127.0.0.1:8095"
    
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(req.read().decode())
    
    tab = None
    for t in tabs:
        if t.get('type') == 'page':
            tab = t
            break
            
    if not tab:
        new_req = urllib.request.Request(f"http://127.0.0.1:9222/json/new?{base_url}/index.html", method='PUT')
        with urllib.request.urlopen(new_req) as resp:
            tab = json.loads(resp.read().decode())

    ws_url = tab['webSocketDebuggerUrl']
    print("Connected to CDP:", ws_url)
    
    async with websockets.connect(ws_url, max_size=50*1024*1024) as ws:
        msg_id = 1
        await send_cmd(ws, msg_id, 'Page.enable'); msg_id += 1
        await send_cmd(ws, msg_id, 'DOM.enable'); msg_id += 1
        await send_cmd(ws, msg_id, 'Runtime.enable'); msg_id += 1

        # =========================================================================
        # PHASE 1: PC DESKTOP VIEW (1440x900)
        # =========================================================================
        print("\n--- PHASE 1: DESKTOP VIEWPORT (1440x900) ---")
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {
            'width': 1440,
            'height': 900,
            'deviceScaleFactor': 1,
            'mobile': False
        }); msg_id += 1

        home_url = f"{base_url}/index.html?v=drive2026"
        print("Navigating to dist Home on port 8095:", home_url)
        await send_cmd(ws, msg_id, 'Page.navigate', {'url': home_url}); msg_id += 1
        await asyncio.sleep(2.5)

        # 1.1 Desktop Hero Slide 0 (banner-1-pc)
        slide_0_img = await run_eval(ws, msg_id, """(() => {
            const img = document.querySelector('#hero-slide-0 img');
            return img ? (img.currentSrc || img.src) : null;
        })()"""); msg_id += 1
        print("Desktop Slide 0 Loaded Image:", slide_0_img)
        await save_screenshot(ws, msg_id, "dist_verified_pc_hero_slide0.jpg"); msg_id += 1

        # 1.2 Desktop Hero Slide 1 (banner-2-pc)
        print("Advancing to Hero Slide 1...")
        await run_eval(ws, msg_id, "window.setHeroSlide && window.setHeroSlide(1)"); msg_id += 1
        await asyncio.sleep(1.2)
        slide_1_img = await run_eval(ws, msg_id, """(() => {
            const img = document.querySelector('#hero-slide-1 img');
            return img ? (img.currentSrc || img.src) : null;
        })()"""); msg_id += 1
        print("Desktop Slide 1 Loaded Image:", slide_1_img)
        await save_screenshot(ws, msg_id, "dist_verified_pc_hero_slide1.jpg"); msg_id += 1

        # 1.3 Desktop Category Cards Section
        print("Scrolling to Explore by Category...")
        await run_eval(ws, msg_id, "window.scrollTo({ top: 580, behavior: 'smooth' })"); msg_id += 1
        await asyncio.sleep(1.2)
        cat_srcs = await run_eval(ws, msg_id, """(() => {
            const imgs = Array.from(document.querySelectorAll('section:has(h2) img, .aspect-square img'));
            return imgs.slice(0, 6).map(i => i.currentSrc || i.src);
        })()"""); msg_id += 1
        print("Desktop Category images loaded:", cat_srcs)
        await save_screenshot(ws, msg_id, "dist_verified_pc_categories.jpg"); msg_id += 1

        # 1.4 Desktop Curated Collections Section
        print("Scrolling to Curated Collections...")
        await run_eval(ws, msg_id, "window.scrollTo({ top: 1250, behavior: 'smooth' })"); msg_id += 1
        await asyncio.sleep(1.2)
        col_srcs = await run_eval(ws, msg_id, """(() => {
            const cards = Array.from(document.querySelectorAll('[data-collection-card="true"] img'));
            return cards.slice(0, 5).map(i => i.currentSrc || i.src);
        })()"""); msg_id += 1
        print("Desktop Collection images loaded:", col_srcs)
        await save_screenshot(ws, msg_id, "dist_verified_pc_collections.jpg"); msg_id += 1

        # =========================================================================
        # PHASE 2: MOBILE VIEW (390x844)
        # =========================================================================
        print("\n--- PHASE 2: MOBILE VIEWPORT (390x844) ---")
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {
            'width': 390,
            'height': 844,
            'deviceScaleFactor': 2,
            'mobile': True
        }); msg_id += 1
        await run_eval(ws, msg_id, "window.scrollTo(0, 0)"); msg_id += 1
        await asyncio.sleep(1.2)

        # 2.1 Mobile Hero Slide 0 (banner-1-mobile)
        mob_slide_0_img = await run_eval(ws, msg_id, """(() => {
            const img = document.querySelector('#hero-slide-0 img');
            return img ? (img.currentSrc || img.src) : null;
        })()"""); msg_id += 1
        print("Mobile Slide 0 Loaded Image:", mob_slide_0_img)
        await save_screenshot(ws, msg_id, "dist_verified_mobile_hero_slide0.jpg"); msg_id += 1

        # 2.2 Mobile Hero Slide 1 (banner2-mobile)
        print("Advancing to Mobile Hero Slide 1...")
        await run_eval(ws, msg_id, "window.setHeroSlide && window.setHeroSlide(1)"); msg_id += 1
        await asyncio.sleep(1.2)
        mob_slide_1_img = await run_eval(ws, msg_id, """(() => {
            const img = document.querySelector('#hero-slide-1 img');
            return img ? (img.currentSrc || img.src) : null;
        })()"""); msg_id += 1
        print("Mobile Slide 1 Loaded Image:", mob_slide_1_img)
        await save_screenshot(ws, msg_id, "dist_verified_mobile_hero_slide1.jpg"); msg_id += 1

        # 2.3 Mobile Category Cards Section
        print("Scrolling to Mobile Categories...")
        await run_eval(ws, msg_id, "window.scrollTo({ top: 580, behavior: 'smooth' })"); msg_id += 1
        await asyncio.sleep(1.2)
        await save_screenshot(ws, msg_id, "dist_verified_mobile_categories.jpg"); msg_id += 1

        # 2.4 Mobile Curated Collections Section
        print("Scrolling to Mobile Collections...")
        await run_eval(ws, msg_id, "window.scrollTo({ top: 1200, behavior: 'smooth' })"); msg_id += 1
        await asyncio.sleep(1.2)
        await save_screenshot(ws, msg_id, "dist_verified_mobile_collections.jpg"); msg_id += 1

        # Restore desktop viewport for interactive view
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {
            'width': 1440,
            'height': 900,
            'deviceScaleFactor': 1,
            'mobile': False
        }); msg_id += 1
        await run_eval(ws, msg_id, "window.scrollTo({ top: 0, behavior: 'smooth' })"); msg_id += 1
        print("\nAll live browser verification audits completed successfully!")

if __name__ == '__main__':
    asyncio.run(main())
