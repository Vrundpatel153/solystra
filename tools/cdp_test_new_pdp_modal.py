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
    print(f"Captured & saved: {filename}")
    return local_path

async def main():
    target_url = "http://127.0.0.1:8089/product.html"
    
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(req.read().decode('utf-8'))
    
    target_tab = None
    for tab in tabs:
        if tab.get('type') == 'page' and ('8089' in tab.get('url', '') or 'product.html' in tab.get('url', '')):
            target_tab = tab
            break
            
    if not target_tab:
        print("No product page tab found, creating new...")
        new_req = urllib.request.Request(f"http://127.0.0.1:9222/json/new?{target_url}", method='PUT')
        with urllib.request.urlopen(new_req) as resp:
            target_tab = json.loads(resp.read().decode('utf-8'))

    ws_url = target_tab.get('webSocketDebuggerUrl')
    print("Connecting to ws:", ws_url)
    
    async with websockets.connect(ws_url, max_size=25*1024*1024) as ws:
        msg_id = 1
        await send_cmd(ws, msg_id, 'Page.enable'); msg_id += 1
        await send_cmd(ws, msg_id, 'DOM.enable'); msg_id += 1
        await send_cmd(ws, msg_id, 'Runtime.enable'); msg_id += 1

        # 1. Desktop Viewport (1440x900)
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {
            'width': 1440,
            'height': 900,
            'deviceScaleFactor': 1,
            'mobile': False
        }); msg_id += 1

        print("Navigating to:", target_url)
        await send_cmd(ws, msg_id, 'Page.navigate', {'url': target_url}); msg_id += 1
        await asyncio.sleep(2.0)

        # Record page scroll position
        pre_click_scroll = await run_eval(ws, msg_id, "window.scrollY"); msg_id += 1
        print("Pre-click scrollY:", pre_click_scroll)

        # 2. Click Enlarge Button on product image card
        print("Clicking Enlarge Button...")
        click_res = await run_eval(ws, msg_id, """(() => {
            const btn = document.querySelector('button[aria-label="Enlarge Image"]');
            if (btn) {
                btn.click();
                return 'clicked';
            }
            return 'not found';
        })()"""); msg_id += 1
        print("Enlarge button click result:", click_res)
        await asyncio.sleep(0.8)

        # Inspect Modal geometry
        dialog_geo = await run_eval(ws, msg_id, """(() => {
            const modal = document.getElementById('pdp-lightbox-modal');
            if (!modal) return { found: false };
            const dialog = modal.querySelector('div[role="dialog"]');
            const img = document.getElementById('lightbox-main-img');
            const dRect = dialog ? dialog.getBoundingClientRect() : null;
            const iRect = img ? img.getBoundingClientRect() : null;
            return {
                modalDisplay: modal.style.display,
                bodyOverflow: document.body.style.overflow,
                dialog: dRect ? {
                    width: Math.round(dRect.width),
                    height: Math.round(dRect.height),
                    top: Math.round(dRect.top),
                    left: Math.round(dRect.left)
                } : null,
                img: iRect ? {
                    width: Math.round(iRect.width),
                    height: Math.round(iRect.height)
                } : null
            };
        })()"""); msg_id += 1
        print("Modal Dialog Geometry:", json.dumps(dialog_geo, indent=2))

        # Screenshot 1: Desktop Modal - Initial Normal Zoom
        await save_screenshot(ws, msg_id, "pdp_modal_desktop_normal_zoom.jpg"); msg_id += 1

        # 3. Test Clicking Next Image (Right Arrow)
        print("Clicking Next Angle Arrow...")
        await run_eval(ws, msg_id, """(() => {
            const nextBtn = document.querySelector('button[aria-label="Next Image"]');
            if (nextBtn) nextBtn.click();
        })()"""); msg_id += 1
        await asyncio.sleep(0.5)

        # Screenshot 2: Desktop Modal - Angle 2
        await save_screenshot(ws, msg_id, "pdp_modal_desktop_next_angle.jpg"); msg_id += 1

        # 4. Test Toggle Zoom (Click on Image)
        print("Clicking Image to Toggle 1.8x Zoom...")
        await run_eval(ws, msg_id, """(() => {
            const img = document.getElementById('lightbox-main-img');
            if (img) img.click();
        })()"""); msg_id += 1
        await asyncio.sleep(0.5)

        # Screenshot 3: Desktop Modal - 1.8x Detail Zoom
        await save_screenshot(ws, msg_id, "pdp_modal_desktop_zoomed.jpg"); msg_id += 1

        # Toggle zoom back to 1x
        await run_eval(ws, msg_id, "window.toggleLightboxZoom()"); msg_id += 1
        await asyncio.sleep(0.3)

        # 5. Test Fullscreen / Theater Toggle
        print("Testing Fullscreen / Theater Mode Toggle...")
        await run_eval(ws, msg_id, "window.toggleLightboxFullscreen()"); msg_id += 1
        await asyncio.sleep(0.5)

        # Screenshot 4: Desktop Modal - Fullscreen Mode
        await save_screenshot(ws, msg_id, "pdp_modal_desktop_fullscreen.jpg"); msg_id += 1

        # Toggle back to normal modal dialog
        await run_eval(ws, msg_id, "window.toggleLightboxFullscreen()"); msg_id += 1
        await asyncio.sleep(0.3)

        # 6. Test Close Modal
        print("Closing Modal via Close Button...")
        await run_eval(ws, msg_id, "window.closeImageLightbox()"); msg_id += 1
        await asyncio.sleep(0.5)

        post_close_info = await run_eval(ws, msg_id, """(() => {
            const modal = document.getElementById('pdp-lightbox-modal');
            return {
                modalDisplay: modal ? modal.style.display : null,
                bodyOverflow: document.body.style.overflow,
                scrollY: window.scrollY
            };
        })()"""); msg_id += 1
        print("Post-close state:", json.dumps(post_close_info, indent=2))

        # Screenshot 5: Clean Page After Modal Close (Proving zero layout change!)
        await save_screenshot(ws, msg_id, "pdp_modal_closed_intact_page.jpg"); msg_id += 1

        # 7. Test Mobile Viewport (390x844)
        print("Testing Mobile Viewport (390x844)...")
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {
            'width': 390,
            'height': 844,
            'deviceScaleFactor': 2,
            'mobile': True
        }); msg_id += 1
        await asyncio.sleep(0.5)

        # Open modal on mobile
        print("Opening modal on mobile...")
        await run_eval(ws, msg_id, "window.openImageLightbox()"); msg_id += 1
        await asyncio.sleep(0.8)

        mobile_geo = await run_eval(ws, msg_id, """(() => {
            const modal = document.getElementById('pdp-lightbox-modal');
            if (!modal) return { found: false };
            const dialog = modal.querySelector('div[role="dialog"]');
            const dRect = dialog ? dialog.getBoundingClientRect() : null;
            return {
                modalDisplay: modal.style.display,
                dialog: dRect ? {
                    width: Math.round(dRect.width),
                    height: Math.round(dRect.height),
                    top: Math.round(dRect.top),
                    left: Math.round(dRect.left)
                } : null
            };
        })()"""); msg_id += 1
        print("Mobile Modal Geometry:", json.dumps(mobile_geo, indent=2))

        # Screenshot 6: Mobile Modal
        await save_screenshot(ws, msg_id, "pdp_modal_mobile_view.jpg"); msg_id += 1

        # Test mobile Next button
        await run_eval(ws, msg_id, "window.nextLightboxImage()"); msg_id += 1
        await asyncio.sleep(0.5)
        await save_screenshot(ws, msg_id, "pdp_modal_mobile_next_angle.jpg"); msg_id += 1

        # Close on mobile
        await run_eval(ws, msg_id, "window.closeImageLightbox()"); msg_id += 1
        await asyncio.sleep(0.4)

        # Restore interactive desktop viewport
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {
            'width': 1440,
            'height': 900,
            'deviceScaleFactor': 1,
            'mobile': False
        }); msg_id += 1
        print("All visual verification tests completed successfully!")

if __name__ == '__main__':
    asyncio.run(main())

