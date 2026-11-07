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

async def main():
    target_url = "http://127.0.0.1:8089/product.html"
    
    # Check if a tab with product.html or 8089 already exists
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(req.read().decode('utf-8'))
    
    target_tab = None
    for tab in tabs:
        if tab.get('type') == 'page' and ('8089' in tab.get('url', '') or 'product.html' in tab.get('url', '')):
            target_tab = tab
            break
            
    if not target_tab:
        print("Creating new tab for Solystra product page...")
        new_req = urllib.request.Request(
            f"http://127.0.0.1:9222/json/new?{target_url}",
            method='PUT'
        )
        with urllib.request.urlopen(new_req) as resp:
            target_tab = json.loads(resp.read().decode('utf-8'))
            print("Opened new tab:", target_tab.get('id'))
    else:
        print("Reusing tab:", target_tab.get('id'), target_tab.get('url'))

    ws_url = target_tab.get('webSocketDebuggerUrl')
    print("Connecting to ws:", ws_url)
    
    async with websockets.connect(ws_url, max_size=25*1024*1024) as ws:
        msg_id = 1
        await send_cmd(ws, msg_id, 'Page.enable'); msg_id += 1
        await send_cmd(ws, msg_id, 'DOM.enable'); msg_id += 1
        await send_cmd(ws, msg_id, 'Runtime.enable'); msg_id += 1

        # Navigate to 8089
        await send_cmd(ws, msg_id, 'Page.navigate', {'url': target_url}); msg_id += 1
        await asyncio.sleep(2.0)

        # 1. Desktop Viewport (1440x900)
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {
            'width': 1440,
            'height': 900,
            'deviceScaleFactor': 1,
            'mobile': False
        }); msg_id += 1
        await asyncio.sleep(0.5)

        # Scroll to 0
        await run_eval(ws, msg_id, "window.scrollTo(0, 0)"); msg_id += 1
        await asyncio.sleep(0.5)

        # Check badges existence
        has_badges = await run_eval(ws, msg_id, """(() => {
            const gallery = document.querySelector('.pdp-fixed-gallery');
            if (!gallery) return 'gallery-not-found';
            return gallery.innerText.includes('Official BIS Hallmark') || 
                   gallery.innerText.includes('Velvet Keepsake') ||
                   gallery.innerText.includes('Lifetime Replating');
        })()"""); msg_id += 1
        print("Left gallery contains unwanted badges:", has_badges)

        # Initial geometry
        geo_0 = await run_eval(ws, msg_id, """(() => {
            const gallery = document.querySelector('.pdp-fixed-gallery');
            const mainImg = document.querySelector('#pdp-main-img');
            const rightCol = document.querySelector('.lg\\\\:col-span-5');
            const gRect = gallery ? gallery.getBoundingClientRect() : null;
            const rRect = rightCol ? rightCol.getBoundingClientRect() : null;
            return {
                scrollY: window.scrollY,
                galleryTop: gRect ? Math.round(gRect.top) : null,
                galleryHeight: gRect ? Math.round(gRect.height) : null,
                rightColTop: rRect ? Math.round(rRect.top) : null,
                rightColHeight: rRect ? Math.round(rRect.height) : null
            };
        })()"""); msg_id += 1
        print("Geometry at scroll 0:", json.dumps(geo_0, indent=2))

        # Take Top screenshot
        shot_0 = await send_cmd(ws, msg_id, 'Page.captureScreenshot', {'format': 'jpeg', 'quality': 85}); msg_id += 1
        img_data_0 = base64.b64decode(shot_0['result']['data'])
        with open("audit_visuals/pdp_desktop_top_clean.jpg", "wb") as f:
            f.write(img_data_0)
        shutil.copy("audit_visuals/pdp_desktop_top_clean.jpg", os.path.join(ARTIFACT_DIR, "pdp_desktop_top_clean.jpg"))
        print("Captured audit_visuals/pdp_desktop_top_clean.jpg")

        # Smooth scroll to 450px
        print("Smoothly scrolling down to 450px...")
        for y in range(0, 460, 45):
            await run_eval(ws, msg_id, f"window.scrollTo(0, {y})"); msg_id += 1
            await asyncio.sleep(0.06)

        await asyncio.sleep(0.5)

        # Scrolled geometry at 450px
        geo_450 = await run_eval(ws, msg_id, """(() => {
            const gallery = document.querySelector('.pdp-fixed-gallery');
            const rightCol = document.querySelector('.lg\\\\:col-span-5');
            const gRect = gallery ? gallery.getBoundingClientRect() : null;
            const rRect = rightCol ? rightCol.getBoundingClientRect() : null;
            return {
                scrollY: window.scrollY,
                galleryTop: gRect ? Math.round(gRect.top) : null,
                galleryHeight: gRect ? Math.round(gRect.height) : null,
                rightColTop: rRect ? Math.round(rRect.top) : null,
                isSticky: gRect ? Math.abs(gRect.top - 98) < 15 : false
            };
        })()"""); msg_id += 1
        print("Geometry at scroll 450:", json.dumps(geo_450, indent=2))

        # Take Scrolled screenshot
        shot_450 = await send_cmd(ws, msg_id, 'Page.captureScreenshot', {'format': 'jpeg', 'quality': 85}); msg_id += 1
        img_data_450 = base64.b64decode(shot_450['result']['data'])
        with open("audit_visuals/pdp_desktop_sticky_scrolled.jpg", "wb") as f:
            f.write(img_data_450)
        shutil.copy("audit_visuals/pdp_desktop_sticky_scrolled.jpg", os.path.join(ARTIFACT_DIR, "pdp_desktop_sticky_scrolled.jpg"))
        print("Captured audit_visuals/pdp_desktop_sticky_scrolled.jpg")

        # Smooth scroll to 750px
        print("Smoothly scrolling down to 750px...")
        for y in range(450, 760, 50):
            await run_eval(ws, msg_id, f"window.scrollTo(0, {y})"); msg_id += 1
            await asyncio.sleep(0.06)

        await asyncio.sleep(0.5)

        geo_750 = await run_eval(ws, msg_id, """(() => {
            const gallery = document.querySelector('.pdp-fixed-gallery');
            const rightCol = document.querySelector('.lg\\\\:col-span-5');
            const gRect = gallery ? gallery.getBoundingClientRect() : null;
            const rRect = rightCol ? rightCol.getBoundingClientRect() : null;
            return {
                scrollY: window.scrollY,
                galleryTop: gRect ? Math.round(gRect.top) : null,
                rightColTop: rRect ? Math.round(rRect.top) : null,
                isSticky: gRect ? Math.abs(gRect.top - 98) < 15 : false
            };
        })()"""); msg_id += 1
        print("Geometry at scroll 750:", json.dumps(geo_750, indent=2))

        shot_750 = await send_cmd(ws, msg_id, 'Page.captureScreenshot', {'format': 'jpeg', 'quality': 85}); msg_id += 1
        img_data_750 = base64.b64decode(shot_750['result']['data'])
        with open("audit_visuals/pdp_desktop_sticky_deep_scroll.jpg", "wb") as f:
            f.write(img_data_750)
        shutil.copy("audit_visuals/pdp_desktop_sticky_deep_scroll.jpg", os.path.join(ARTIFACT_DIR, "pdp_desktop_sticky_deep_scroll.jpg"))
        print("Captured audit_visuals/pdp_desktop_sticky_deep_scroll.jpg")

        # Mobile Viewport (390x844)
        print("Emulating Mobile Viewport (390x844)...")
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {
            'width': 390,
            'height': 844,
            'deviceScaleFactor': 2,
            'mobile': True
        }); msg_id += 1
        await run_eval(ws, msg_id, "window.scrollTo(0, 0)"); msg_id += 1
        await asyncio.sleep(0.5)

        shot_mob = await send_cmd(ws, msg_id, 'Page.captureScreenshot', {'format': 'jpeg', 'quality': 85}); msg_id += 1
        img_data_mob = base64.b64decode(shot_mob['result']['data'])
        with open("audit_visuals/pdp_mobile_top_clean.jpg", "wb") as f:
            f.write(img_data_mob)
        shutil.copy("audit_visuals/pdp_mobile_top_clean.jpg", os.path.join(ARTIFACT_DIR, "pdp_mobile_top_clean.jpg"))
        print("Captured audit_visuals/pdp_mobile_top_clean.jpg")

        # Restore Desktop Viewport for interactive viewing
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {
            'width': 1440,
            'height': 900,
            'deviceScaleFactor': 1,
            'mobile': False
        }); msg_id += 1
        await run_eval(ws, msg_id, "window.scrollTo(0, 420)"); msg_id += 1
        print("Restored interactive desktop viewport on WinSta0\\Default!")

if __name__ == '__main__':
    asyncio.run(main())
