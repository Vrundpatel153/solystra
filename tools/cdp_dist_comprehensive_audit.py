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
    base_url = "http://127.0.0.1:8090"
    
    # 1. Connect to Chrome CDP
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(req.read().decode('utf-8'))
    
    target_tab = None
    for tab in tabs:
        if tab.get('type') == 'page' and ('8090' in tab.get('url', '') or '8089' in tab.get('url', '') or 'product.html' in tab.get('url', '')):
            target_tab = tab
            break
            
    if not target_tab:
        print("Opening new tab for dist verification...")
        new_req = urllib.request.Request(f"http://127.0.0.1:9222/json/new?{base_url}/product.html", method='PUT')
        with urllib.request.urlopen(new_req) as resp:
            target_tab = json.loads(resp.read().decode('utf-8'))

    ws_url = target_tab.get('webSocketDebuggerUrl')
    print("Connected to CDP:", ws_url)
    
    async with websockets.connect(ws_url, max_size=25*1024*1024) as ws:
        msg_id = 1
        await send_cmd(ws, msg_id, 'Page.enable'); msg_id += 1
        await send_cmd(ws, msg_id, 'DOM.enable'); msg_id += 1
        await send_cmd(ws, msg_id, 'Runtime.enable'); msg_id += 1

        results = {}

        # =========================================================================
        # PHASE 1: PC DESKTOP VIEWPORT VERIFICATION (1440x900)
        # =========================================================================
        print("\n--- PHASE 1: DESKTOP VIEWPORT (1440x900) ---")
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {
            'width': 1440,
            'height': 900,
            'deviceScaleFactor': 1,
            'mobile': False
        }); msg_id += 1

        pdp_url = f"{base_url}/product.html"
        print("Navigating to dist PDP:", pdp_url)
        await send_cmd(ws, msg_id, 'Page.navigate', {'url': pdp_url}); msg_id += 1
        await asyncio.sleep(2.0)

        # 1.1 Verify Left Clean & Sticky Gallery at scroll 0
        geo_0 = await run_eval(ws, msg_id, """(() => {
            window.scrollTo(0, 0);
            const gallery = document.querySelector('.pdp-fixed-gallery');
            const rightCol = document.querySelector('.lg\\\\:col-span-5');
            const gRect = gallery ? gallery.getBoundingClientRect() : null;
            const rRect = rightCol ? rightCol.getBoundingClientRect() : null;
            const hasUnwantedBadges = gallery ? (
                gallery.innerText.includes('Official BIS Hallmark') || 
                gallery.innerText.includes('Velvet Keepsake') ||
                gallery.innerText.includes('Lifetime Replating')
            ) : false;
            return {
                scrollY: window.scrollY,
                hasUnwantedBadges,
                galleryTop: gRect ? Math.round(gRect.top) : null,
                galleryHeight: gRect ? Math.round(gRect.height) : null,
                rightColHeight: rRect ? Math.round(rRect.height) : null
            };
        })()"""); msg_id += 1
        results['desktop_initial'] = geo_0
        print("Desktop PDP initial:", json.dumps(geo_0, indent=2))
        await save_screenshot(ws, msg_id, "dist_pc_pdp_initial_top.jpg"); msg_id += 1

        # 1.2 Verify Sticky behavior when scrolled 450px
        print("Smooth scrolling desktop to 450px...")
        for y in range(0, 460, 45):
            await run_eval(ws, msg_id, f"window.scrollTo(0, {y})"); msg_id += 1
            await asyncio.sleep(0.05)
        await asyncio.sleep(0.5)

        geo_450 = await run_eval(ws, msg_id, """(() => {
            const gallery = document.querySelector('.pdp-fixed-gallery');
            const gRect = gallery ? gallery.getBoundingClientRect() : null;
            return {
                scrollY: window.scrollY,
                galleryTop: gRect ? Math.round(gRect.top) : null,
                isSticky: gRect ? Math.abs(gRect.top - 98) < 15 : false
            };
        })()"""); msg_id += 1
        results['desktop_sticky_450'] = geo_450
        print("Desktop PDP sticky at 450px:", json.dumps(geo_450, indent=2))
        await save_screenshot(ws, msg_id, "dist_pc_pdp_sticky_scrolled.jpg"); msg_id += 1

        # Return to top for modal test
        await run_eval(ws, msg_id, "window.scrollTo(0, 0)"); msg_id += 1
        await asyncio.sleep(0.4)

        # 1.3 Trigger Enlarge Button
        print("Triggering Enlarge Image button...")
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

        # 1.4 Inspect Modal Centered Geometry in Normal Zoom
        modal_geo_normal = await run_eval(ws, msg_id, """(() => {
            const modal = document.getElementById('pdp-lightbox-modal');
            if (!modal) return { found: false };
            const dialog = modal.querySelector('div[role="dialog"]');
            const dRect = dialog ? dialog.getBoundingClientRect() : null;
            const img = document.getElementById('lightbox-main-img');
            const iRect = img ? img.getBoundingClientRect() : null;
            const counter = modal.querySelector('.font-mono.font-bold');
            return {
                display: modal.style.display,
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
                } : null,
                counterText: counter ? counter.innerText.trim() : null
            };
        })()"""); msg_id += 1
        results['desktop_modal_normal'] = modal_geo_normal
        print("Desktop Modal Geometry (Normal Zoom):", json.dumps(modal_geo_normal, indent=2))
        await save_screenshot(ws, msg_id, "dist_pc_pdp_modal_normal_zoom.jpg"); msg_id += 1

        # 1.5 Click Next Arrow (>)
        print("Clicking Next Angle (Right Arrow)...")
        await run_eval(ws, msg_id, """(() => {
            const nextBtn = document.querySelector('button[aria-label="Next Image"]');
            if (nextBtn) nextBtn.click();
        })()"""); msg_id += 1
        await asyncio.sleep(0.6)

        next_angle_info = await run_eval(ws, msg_id, """(() => {
            const img = document.getElementById('lightbox-main-img');
            const counter = document.querySelector('#pdp-lightbox-modal .font-mono.font-bold');
            return {
                src: img ? img.src : null,
                counterText: counter ? counter.innerText.trim() : null
            };
        })()"""); msg_id += 1
        results['desktop_modal_next_angle'] = next_angle_info
        print("Next angle info:", json.dumps(next_angle_info, indent=2))
        await save_screenshot(ws, msg_id, "dist_pc_pdp_modal_next_angle.jpg"); msg_id += 1

        # 1.6 Click Image to Toggle 1.8x Detail Zoom
        print("Clicking Image to Toggle 1.8x Detail Zoom...")
        await run_eval(ws, msg_id, """(() => {
            const img = document.getElementById('lightbox-main-img');
            if (img) img.click();
        })()"""); msg_id += 1
        await asyncio.sleep(0.5)
        await save_screenshot(ws, msg_id, "dist_pc_pdp_modal_zoomed_1_8x.jpg"); msg_id += 1

        # Reset zoom to 1x
        await run_eval(ws, msg_id, "window.toggleLightboxZoom()"); msg_id += 1
        await asyncio.sleep(0.3)

        # 1.7 Toggle Fullscreen / Theater Mode
        print("Toggling Fullscreen / Theater Mode...")
        await run_eval(ws, msg_id, "window.toggleLightboxFullscreen()"); msg_id += 1
        await asyncio.sleep(0.5)

        theater_geo = await run_eval(ws, msg_id, """(() => {
            const dialog = document.querySelector('#pdp-lightbox-modal div[role="dialog"]');
            const dRect = dialog ? dialog.getBoundingClientRect() : null;
            return dRect ? { width: Math.round(dRect.width), height: Math.round(dRect.height) } : null;
        })()"""); msg_id += 1
        results['desktop_theater_mode'] = theater_geo
        print("Desktop Theater Mode Geometry:", json.dumps(theater_geo, indent=2))
        await save_screenshot(ws, msg_id, "dist_pc_pdp_modal_theater_mode.jpg"); msg_id += 1

        # Toggle back to normal modal
        await run_eval(ws, msg_id, "window.toggleLightboxFullscreen()"); msg_id += 1
        await asyncio.sleep(0.3)

        # 1.8 Close Modal
        print("Closing Modal via Close button...")
        await run_eval(ws, msg_id, "window.closeImageLightbox()"); msg_id += 1
        await asyncio.sleep(0.5)

        post_close = await run_eval(ws, msg_id, """(() => {
            const modal = document.getElementById('pdp-lightbox-modal');
            return {
                modalDisplay: modal ? modal.style.display : null,
                bodyOverflow: document.body.style.overflow,
                scrollY: window.scrollY
            };
        })()"""); msg_id += 1
        results['desktop_post_close'] = post_close
        print("Desktop Post-close State:", json.dumps(post_close, indent=2))
        await save_screenshot(ws, msg_id, "dist_pc_pdp_modal_closed_intact.jpg"); msg_id += 1


        # =========================================================================
        # PHASE 2: MOBILE VIEWPORT VERIFICATION (390x844)
        # =========================================================================
        print("\n--- PHASE 2: MOBILE VIEWPORT (390x844) ---")
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {
            'width': 390,
            'height': 844,
            'deviceScaleFactor': 2,
            'mobile': True
        }); msg_id += 1
        await asyncio.sleep(0.5)

        # 2.1 Mobile PDP Initial Top View
        await run_eval(ws, msg_id, "window.scrollTo(0, 0)"); msg_id += 1
        await asyncio.sleep(0.5)
        await save_screenshot(ws, msg_id, "dist_mobile_pdp_top_view.jpg"); msg_id += 1

        # 2.2 Open Modal on Mobile
        print("Opening modal on mobile...")
        await run_eval(ws, msg_id, """(() => {
            const btn = document.querySelector('button[aria-label="Enlarge Image"]');
            if (btn) btn.click();
            else window.openImageLightbox();
        })()"""); msg_id += 1
        await asyncio.sleep(0.8)

        mobile_modal_geo = await run_eval(ws, msg_id, """(() => {
            const modal = document.getElementById('pdp-lightbox-modal');
            if (!modal) return { found: false };
            const dialog = modal.querySelector('div[role="dialog"]');
            const dRect = dialog ? dialog.getBoundingClientRect() : null;
            const counter = modal.querySelector('.font-mono.font-bold');
            return {
                display: modal.style.display,
                bodyOverflow: document.body.style.overflow,
                dialog: dRect ? {
                    width: Math.round(dRect.width),
                    height: Math.round(dRect.height),
                    top: Math.round(dRect.top),
                    left: Math.round(dRect.left)
                } : null,
                counterText: counter ? counter.innerText.trim() : null
            };
        })()"""); msg_id += 1
        results['mobile_modal_open'] = mobile_modal_geo
        print("Mobile Modal Geometry:", json.dumps(mobile_modal_geo, indent=2))
        await save_screenshot(ws, msg_id, "dist_mobile_pdp_modal_open.jpg"); msg_id += 1

        # 2.3 Mobile Navigation (Next button)
        print("Tapping Next button on mobile...")
        await run_eval(ws, msg_id, """(() => {
            const nextBtn = document.querySelector('button[aria-label="Next Image"]');
            if (nextBtn) nextBtn.click();
        })()"""); msg_id += 1
        await asyncio.sleep(0.6)
        await save_screenshot(ws, msg_id, "dist_mobile_pdp_modal_next.jpg"); msg_id += 1

        # 2.4 Mobile Navigation (Previous button)
        print("Tapping Previous button on mobile...")
        await run_eval(ws, msg_id, """(() => {
            const prevBtn = document.querySelector('button[aria-label="Previous Image"]');
            if (prevBtn) prevBtn.click();
        })()"""); msg_id += 1
        await asyncio.sleep(0.6)
        await save_screenshot(ws, msg_id, "dist_mobile_pdp_modal_prev.jpg"); msg_id += 1

        # 2.5 Close Mobile Modal
        print("Closing Mobile Modal...")
        await run_eval(ws, msg_id, "window.closeImageLightbox()"); msg_id += 1
        await asyncio.sleep(0.5)
        await save_screenshot(ws, msg_id, "dist_mobile_pdp_modal_closed.jpg"); msg_id += 1


        # =========================================================================
        # PHASE 3: HOMEPAGE & CATALOG VERIFICATION IN DIST
        # =========================================================================
        print("\n--- PHASE 3: HOMEPAGE & CATALOG VERIFICATION IN DIST ---")
        
        # 3.1 Homepage Desktop
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {
            'width': 1440,
            'height': 900,
            'deviceScaleFactor': 1,
            'mobile': False
        }); msg_id += 1
        home_url = f"{base_url}/index.html"
        print("Navigating to dist Home:", home_url)
        await send_cmd(ws, msg_id, 'Page.navigate', {'url': home_url}); msg_id += 1
        await asyncio.sleep(2.0)
        await save_screenshot(ws, msg_id, "dist_pc_home_hero_desktop.jpg"); msg_id += 1

        # 3.2 Homepage Mobile
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {
            'width': 390,
            'height': 844,
            'deviceScaleFactor': 2,
            'mobile': True
        }); msg_id += 1
        await run_eval(ws, msg_id, "window.scrollTo(0, 0)"); msg_id += 1
        await asyncio.sleep(0.6)
        await save_screenshot(ws, msg_id, "dist_mobile_home_hero_mobile.jpg"); msg_id += 1

        # 3.3 Catalog Desktop
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {
            'width': 1440,
            'height': 900,
            'deviceScaleFactor': 1,
            'mobile': False
        }); msg_id += 1
        catalog_url = f"{base_url}/products.html"
        print("Navigating to dist Catalog:", catalog_url)
        await send_cmd(ws, msg_id, 'Page.navigate', {'url': catalog_url}); msg_id += 1
        await asyncio.sleep(2.0)
        await save_screenshot(ws, msg_id, "dist_pc_catalog_grid_desktop.jpg"); msg_id += 1

        # 3.4 Catalog Mobile
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {
            'width': 390,
            'height': 844,
            'deviceScaleFactor': 2,
            'mobile': True
        }); msg_id += 1
        await run_eval(ws, msg_id, "window.scrollTo(0, 0)"); msg_id += 1
        await asyncio.sleep(0.6)
        await save_screenshot(ws, msg_id, "dist_mobile_catalog_grid_mobile.jpg"); msg_id += 1

        # Restore interactive desktop viewport
        await send_cmd(ws, msg_id, 'Emulation.setDeviceMetricsOverride', {
            'width': 1440,
            'height': 900,
            'deviceScaleFactor': 1,
            'mobile': False
        }); msg_id += 1
        await send_cmd(ws, msg_id, 'Page.navigate', {'url': f"{base_url}/product.html"}); msg_id += 1
        await asyncio.sleep(1.0)
        await run_eval(ws, msg_id, "window.openImageLightbox()"); msg_id += 1

        with open("dist_audit_report.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print("\nAll PC and Mobile verification audits on dist completed successfully!")

if __name__ == '__main__':
    asyncio.run(main())

