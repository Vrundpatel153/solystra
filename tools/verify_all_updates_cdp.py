import asyncio
import json
import urllib.request
import websockets
import base64
import os

ARTIFACT_DIR = r"C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals"
os.makedirs(ARTIFACT_DIR, exist_ok=True)

class CDPClient:
    def __init__(self, ws):
        self.ws = ws
        self.msg_id = 1

    async def send(self, method, params=None):
        mid = self.msg_id
        self.msg_id += 1
        msg = {"id": mid, "method": method}
        if params:
            msg["params"] = params
        await self.ws.send(json.dumps(msg))
        while True:
            resp_raw = await self.ws.recv()
            resp = json.loads(resp_raw)
            if resp.get("id") == mid:
                return resp.get("result", {})

    async def eval(self, expr):
        res = await self.send("Runtime.evaluate", {"expression": expr, "returnByValue": True})
        return res.get("result", {}).get("value")

    async def screenshot(self, path):
        res = await self.send("Page.captureScreenshot", {"format": "jpeg", "quality": 90})
        data = base64.b64decode(res["data"])
        with open(path, "wb") as f:
            f.write(data)
        print(f"Captured: {path}")

async def main():
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(req.read().decode())
    pages = [t for t in tabs if t.get('type') == 'page']
    
    # Prefer tab with 8095 or first page
    target = None
    for p in pages:
        if '8095' in p.get('url', ''):
            target = p
            break
    if not target and pages:
        target = pages[0]
        
    print(f"Connecting to tab: {target['title']} ({target['url']})")
    
    async with websockets.connect(target['webSocketDebuggerUrl'], max_size=50*1024*1024) as ws:
        cdp = CDPClient(ws)
        await cdp.send("Page.enable")
        await cdp.send("DOM.enable")
        await cdp.send("CSS.enable")

        # ----------------------------------------------------
        # 1. Desktop Verification (1440x900)
        # ----------------------------------------------------
        print("\n--- Verifying Desktop (1440x900) ---")
        await cdp.send("Emulation.setDeviceMetricsOverride", {
            "width": 1440,
            "height": 900,
            "deviceScaleFactor": 1,
            "mobile": False
        })
        await cdp.send("Page.navigate", {"url": "http://127.0.0.1:8095/index.html?v=" + str(os.urandom(4).hex())})
        await asyncio.sleep(2.0)

        # Slide 0
        await cdp.eval("window.setHeroSlide(0)")
        await asyncio.sleep(0.8)
        await cdp.screenshot(os.path.join(ARTIFACT_DIR, "desktop_hero_slide0.jpg"))

        # Slide 1
        await cdp.eval("window.setHeroSlide(1)")
        await asyncio.sleep(0.8)
        await cdp.screenshot(os.path.join(ARTIFACT_DIR, "desktop_hero_slide1.jpg"))

        # Slide 2 (Banner 3)
        await cdp.eval("window.setHeroSlide(2)")
        await asyncio.sleep(0.8)
        await cdp.screenshot(os.path.join(ARTIFACT_DIR, "desktop_hero_slide2_banner3.jpg"))

        # Slide 3 (Banner 4)
        await cdp.eval("window.setHeroSlide(3)")
        await asyncio.sleep(0.8)
        await cdp.screenshot(os.path.join(ARTIFACT_DIR, "desktop_hero_slide3_banner4.jpg"))

        # Scroll to Collections Section
        await cdp.eval("""
            const sec = document.querySelector('#shop-by-collection') || document.querySelector('section:has(.collection-card)') || document.querySelector('h2:contains("Curated"), h2');
            const headings = Array.from(document.querySelectorAll('h2, span')).filter(e => e.textContent.includes('Collections') || e.textContent.includes('Curated Collections') || e.textContent.includes('Signature Collections'));
            if (headings.length > 0) {
                headings[0].scrollIntoView({behavior: 'smooth', block: 'center'});
            } else {
                window.scrollTo({top: 700, behavior: 'smooth'});
            }
        """)
        await asyncio.sleep(1.0)
        await cdp.screenshot(os.path.join(ARTIFACT_DIR, "desktop_collections_view.jpg"))

        # ----------------------------------------------------
        # 2. Mobile Verification (390x844 - iPhone 14 / modern phone)
        # ----------------------------------------------------
        print("\n--- Verifying Mobile (390x844) ---")
        await cdp.send("Emulation.setDeviceMetricsOverride", {
            "width": 390,
            "height": 844,
            "deviceScaleFactor": 2,
            "mobile": True
        })
        await cdp.eval("window.scrollTo(0, 0)")
        await asyncio.sleep(0.5)

        # Mobile Slide 0
        await cdp.eval("window.setHeroSlide(0)")
        await asyncio.sleep(0.8)
        await cdp.screenshot(os.path.join(ARTIFACT_DIR, "mobile_hero_slide0.jpg"))

        # Mobile Slide 1
        await cdp.eval("window.setHeroSlide(1)")
        await asyncio.sleep(0.8)
        await cdp.screenshot(os.path.join(ARTIFACT_DIR, "mobile_hero_slide1.jpg"))

        # Mobile Slide 2 (Banner 3 Mobile)
        await cdp.eval("window.setHeroSlide(2)")
        await asyncio.sleep(0.8)
        await cdp.screenshot(os.path.join(ARTIFACT_DIR, "mobile_hero_slide2_banner3.jpg"))

        # Mobile Slide 3 (Banner 4 Mobile)
        await cdp.eval("window.setHeroSlide(3)")
        await asyncio.sleep(0.8)
        await cdp.screenshot(os.path.join(ARTIFACT_DIR, "mobile_hero_slide3_banner4.jpg"))

        # Scroll to Collections on Mobile
        await cdp.eval("""
            const el = Array.from(document.querySelectorAll('h2, span, p')).find(e => e.textContent.includes('Signature Collections') || e.textContent.includes('Collections'));
            if (el) el.scrollIntoView({behavior: 'smooth', block: 'start'});
            else window.scrollTo({top: 600, behavior: 'smooth'});
        """)
        await asyncio.sleep(1.0)
        await cdp.screenshot(os.path.join(ARTIFACT_DIR, "mobile_collections_view.jpg"))

        # Reset Emulation back to desktop interactive
        await cdp.send("Emulation.setDeviceMetricsOverride", {
            "width": 1440,
            "height": 900,
            "deviceScaleFactor": 1,
            "mobile": False
        })
        await cdp.eval("window.scrollTo(0, 0)")

    print("\nVerification complete! All screenshots saved in artifact directory.")

if __name__ == "__main__":
    asyncio.run(main())

