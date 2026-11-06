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

class CDPAuditor:
    def __init__(self, ws_url):
        self.ws_url = ws_url
        self.msg_id = 1
        self.ws = None

    async def connect(self):
        self.ws = await websockets.connect(self.ws_url, max_size=35*1024*1024)
        await self.send('Page.enable')
        await self.send('Runtime.enable')

    async def send(self, method, params=None):
        self.msg_id += 1
        curr_id = self.msg_id
        payload = {'id': curr_id, 'method': method}
        if params:
            payload['params'] = params
        await self.ws.send(json.dumps(payload))
        while True:
            raw = await self.ws.recv()
            resp = json.loads(raw)
            if resp.get('id') == curr_id:
                return resp

    async def evaluate(self, expr):
        resp = await self.send('Runtime.evaluate', {'expression': expr, 'returnByValue': True})
        result = resp.get('result', {}).get('result', {})
        return result.get('value')

    async def set_viewport(self, width, height, is_mobile=False):
        device_metrics = {
            'width': width,
            'height': height,
            'deviceScaleFactor': 2 if is_mobile else 1,
            'mobile': is_mobile,
        }
        await self.send('Emulation.setDeviceMetricsOverride', device_metrics)
        await asyncio.sleep(0.4)

    async def navigate(self, url):
        await self.send('Page.navigate', {'url': url})
        # Wait for load
        await asyncio.sleep(1.8)

    async def smooth_scroll(self, top_px):
        code = f"window.scrollTo({{ top: {top_px}, behavior: 'smooth' }});"
        await self.evaluate(code)
        await asyncio.sleep(0.6)

    async def capture_screenshot(self, filename):
        resp = await self.send('Page.captureScreenshot', {'format': 'jpeg', 'quality': 90})
        data = resp['result']['data']
        local_p = os.path.join(AUDIT_DIR_LOCAL, filename)
        brain_p = os.path.join(AUDIT_DIR_BRAIN, filename)
        with open(local_p, 'wb') as f:
            f.write(base64.b64decode(data))
        shutil.copy2(local_p, brain_p)
        print(f"✓ Screenshot captured: {filename}")
        return local_p

    async def run_diagnostics(self):
        diag_code = """(() => {
            const overflow = {
                hasHorizontalScroll: document.body.scrollWidth > window.innerWidth,
                scrollWidth: document.body.scrollWidth,
                innerWidth: window.innerWidth,
                overflowingElements: []
            };

            const allEls = document.querySelectorAll('*');
            for (let el of allEls) {
                const rect = el.getBoundingClientRect();
                if (rect.right > window.innerWidth + 2 && rect.width > 0 && !['HTML','BODY','svg','path'].includes(el.tagName)) {
                    overflow.overflowingElements.push({
                        tag: el.tagName,
                        id: el.id || '',
                        class: (el.className || '').toString().slice(0, 60),
                        right: Math.round(rect.right),
                        width: Math.round(rect.width)
                    });
                    if (overflow.overflowingElements.length >= 5) break;
                }
            }

            const images = [...document.querySelectorAll('img')];
            const brokenImages = images.filter(img => !img.complete || img.naturalWidth === 0).map(img => img.src || img.getAttribute('src'));
            const missingAlts = images.filter(img => !img.alt || img.alt.trim() === '').length;

            return {
                title: document.title,
                overflow,
                totalImages: images.length,
                brokenImages,
                missingAlts
            };
        })()"""
        return await self.evaluate(diag_code)

    async def close(self):
        if self.ws:
            await self.ws.close()

def get_tab_ws(url_pattern):
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(req.read().decode('utf-8'))
    for tab in tabs:
        if tab.get('type') == 'page' and url_pattern in tab.get('url', ''):
            return tab.get('webSocketDebuggerUrl'), tab.get('url')
    # If not found, return first page tab
    for tab in tabs:
        if tab.get('type') == 'page':
            return tab.get('webSocketDebuggerUrl'), tab.get('url')
    return None, None

async def main():
    ws_url, _ = get_tab_ws('8080')
    if not ws_url:
        print("No active Chrome page tab found on port 9222!")
        return

    auditor = CDPAuditor(ws_url)
    await auditor.connect()
    audit_results = {}

    try:
        # ==========================================
        # 1. HOMEPAGE AUDIT (index.html)
        # ==========================================
        print("\n--- Auditing Homepage Desktop (1440px) ---")
        await auditor.set_viewport(1440, 900, is_mobile=False)
        await auditor.navigate('http://127.0.0.1:8080/index.html')
        await auditor.smooth_scroll(0)
        await auditor.capture_screenshot('audit_1_home_hero_desktop.jpg')

        # Hero Banner slide check
        await auditor.evaluate("if (window.setHeroSlide) window.setHeroSlide(1);")
        await asyncio.sleep(0.4)
        await auditor.capture_screenshot('audit_1_home_hero_slide1_desktop.jpg')

        # Scroll to Trust Badges & Categories
        await auditor.smooth_scroll(450)
        await auditor.capture_screenshot('audit_1_home_trust_and_categories_desktop.jpg')

        # Scroll to Curated Collections
        await auditor.smooth_scroll(1100)
        await auditor.capture_screenshot('audit_1_home_collections_desktop.jpg')

        # Check Collections Dropdown Menu
        await auditor.smooth_scroll(0)
        await auditor.evaluate("""(() => {
            const btn = document.querySelector('button:has(#collections-chevron)') || [...document.querySelectorAll('button')].find(b => b.innerText.includes('Collections'));
            if (btn) btn.click();
        })()""")
        await asyncio.sleep(0.5)
        await auditor.capture_screenshot('audit_1_home_collections_dropdown_desktop.jpg')
        # Close dropdown
        await auditor.evaluate("""(() => {
            const btn = document.querySelector('button:has(#collections-chevron)') || [...document.querySelectorAll('button')].find(b => b.innerText.includes('Collections'));
            if (btn) btn.click();
        })()""")
        await asyncio.sleep(0.3)

        diag_home_desktop = await auditor.run_diagnostics()
        audit_results['home_desktop'] = diag_home_desktop

        # Mobile Viewport (390px)
        print("\n--- Auditing Homepage Mobile (390px) ---")
        await auditor.set_viewport(390, 844, is_mobile=True)
        await auditor.smooth_scroll(0)
        await auditor.capture_screenshot('audit_1_home_hero_mobile.jpg')

        await auditor.smooth_scroll(320)
        await auditor.capture_screenshot('audit_1_home_trust_and_categories_mobile.jpg')

        await auditor.smooth_scroll(900)
        await auditor.capture_screenshot('audit_1_home_collections_mobile.jpg')

        diag_home_mobile = await auditor.run_diagnostics()
        audit_results['home_mobile'] = diag_home_mobile

        # ==========================================
        # 2. PRODUCTS CATALOG AUDIT (products.html)
        # ==========================================
        print("\n--- Auditing Products Catalog Desktop (1440px) ---")
        await auditor.set_viewport(1440, 900, is_mobile=False)
        await auditor.navigate('http://127.0.0.1:8080/products.html')
        await auditor.smooth_scroll(0)
        await auditor.capture_screenshot('audit_2_catalog_header_desktop.jpg')

        # Verify 5-card row grid
        await auditor.smooth_scroll(250)
        await auditor.capture_screenshot('audit_2_catalog_5cards_grid_desktop.jpg')

        # Open Filter Modal Popup
        await auditor.evaluate("""(() => {
            const filterBtn = [...document.querySelectorAll('button')].find(b => b.innerText.includes('Filter') || b.id === 'filter-toggle-btn');
            if (filterBtn) filterBtn.click();
        })()""")
        await asyncio.sleep(0.5)
        await auditor.capture_screenshot('audit_2_catalog_filter_modal_open_desktop.jpg')

        # Close Filter Modal
        await auditor.evaluate("""(() => {
            const closeBtn = document.querySelector('#filter-modal-close') || document.querySelector('[onclick*=\"closeFilter\"]') || document.querySelector('#filter-drawer button');
            if (closeBtn) closeBtn.click();
        })()""")
        await asyncio.sleep(0.3)

        # Scroll to Pagination
        await auditor.smooth_scroll(1400)
        await auditor.capture_screenshot('audit_2_catalog_pagination_desktop.jpg')

        diag_cat_desktop = await auditor.run_diagnostics()
        audit_results['catalog_desktop'] = diag_cat_desktop

        # Mobile Viewport (390px)
        print("\n--- Auditing Products Catalog Mobile (390px) ---")
        await auditor.set_viewport(390, 844, is_mobile=True)
        await auditor.smooth_scroll(0)
        await auditor.capture_screenshot('audit_2_catalog_mobile_top.jpg')

        await auditor.smooth_scroll(250)
        await auditor.capture_screenshot('audit_2_catalog_mobile_cards.jpg')

        # Open mobile filter drawer
        await auditor.evaluate("""(() => {
            const filterBtn = [...document.querySelectorAll('button')].find(b => b.innerText.includes('Filter') || b.id === 'filter-toggle-btn');
            if (filterBtn) filterBtn.click();
        })()""")
        await asyncio.sleep(0.5)
        await auditor.capture_screenshot('audit_2_catalog_mobile_filter_drawer.jpg')

        # Close filter
        await auditor.evaluate("""(() => {
            const closeBtn = document.querySelector('#filter-modal-close') || document.querySelector('[onclick*=\"closeFilter\"]') || document.querySelector('#filter-drawer button');
            if (closeBtn) closeBtn.click();
        })()""")
        await asyncio.sleep(0.3)

        # Scroll to Mobile Pagination
        await auditor.smooth_scroll(1600)
        await auditor.capture_screenshot('audit_2_catalog_mobile_pagination.jpg')

        diag_cat_mobile = await auditor.run_diagnostics()
        audit_results['catalog_mobile'] = diag_cat_mobile

        # ==========================================
        # 3. PRODUCT DETAIL PAGE AUDIT (product.html)
        # ==========================================
        print("\n--- Auditing Product Detail Page Desktop (1440px) ---")
        await auditor.set_viewport(1440, 900, is_mobile=False)
        await auditor.navigate('http://127.0.0.1:8080/product.html?id=accent-circle-925-silver-necklace')
        await auditor.smooth_scroll(0)
        await auditor.capture_screenshot('audit_3_pdp_desktop_top_gallery.jpg')

        await auditor.smooth_scroll(380)
        await auditor.capture_screenshot('audit_3_pdp_desktop_trust_badges.jpg')

        diag_pdp_desktop = await auditor.run_diagnostics()
        audit_results['pdp_desktop'] = diag_pdp_desktop

        # Mobile Viewport (390px)
        print("\n--- Auditing Product Detail Page Mobile (390px) ---")
        await auditor.set_viewport(390, 844, is_mobile=True)
        await auditor.smooth_scroll(0)
        await auditor.capture_screenshot('audit_3_pdp_mobile_top.jpg')

        await auditor.smooth_scroll(520)
        await auditor.capture_screenshot('audit_3_pdp_mobile_trust_badges.jpg')

        diag_pdp_mobile = await auditor.run_diagnostics()
        audit_results['pdp_mobile'] = diag_pdp_mobile

        # Save diagnostic report
        with open('audit_results.json', 'w', encoding='utf-8') as f:
            json.dump(audit_results, f, indent=2)
        print("\n✓ Full Visual Audit Completed! Diagnostics saved to audit_results.json")

    finally:
        await auditor.close()

if __name__ == '__main__':
    asyncio.run(main())

