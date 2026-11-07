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
        res = await self.send("Page.captureScreenshot", {"format": "jpeg", "quality": 92})
        data = base64.b64decode(res["data"])
        with open(path, "wb") as f:
            f.write(data)
        print(f"Captured: {path}")

async def main():
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(req.read().decode())
    pages = [t for t in tabs if t.get('type') == 'page']
    
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

        # ----------------------------------------------------
        # 1. Desktop Verification (1440x900)
        # ----------------------------------------------------
        print("\n--- Testing Desktop (1440x900) ---")
        await cdp.send("Emulation.setDeviceMetricsOverride", {
            "width": 1440,
            "height": 900,
            "deviceScaleFactor": 1,
            "mobile": False
        })
        await cdp.send("Page.navigate", {"url": "http://127.0.0.1:8095/index.html?v=" + str(os.urandom(4).hex())})
        await asyncio.sleep(2.0)

        # Scroll to Curated Looks section
        await cdp.eval("""
            const sec = document.getElementById('curated-looks-section');
            if (sec) sec.scrollIntoView({behavior: 'smooth', block: 'center'});
        """)
        await asyncio.sleep(1.0)

        # Combo 1: Activate Earring Hotspot
        metrics1 = await cdp.eval("""
            (() => {
                const pin = document.querySelector('[data-hotspot-id="c1-item-2"]');
                if (pin) pin.dispatchEvent(new MouseEvent('mouseenter', {bubbles: true}));
                const pop = document.querySelector('[data-popover="c1-item-2"]');
                const card = document.getElementById('combo-left-col');
                if (!pop || !card) return null;
                const pRect = pop.getBoundingClientRect();
                const cRect = card.getBoundingClientRect();
                return {
                    pinFound: true,
                    popVisible: !pop.classList.contains('invisible'),
                    popRight: pRect.right,
                    cardRight: cRect.right,
                    overflowRight: pRect.right - cRect.right,
                    popLeft: pRect.left,
                    cardLeft: cRect.left,
                    overflowLeft: cRect.left - pRect.left
                };
            })()
        """)
        print("Combo 1 Earring Desktop Metrics:", metrics1)
        await asyncio.sleep(0.5)
        await cdp.screenshot(os.path.join(ARTIFACT_DIR, "desktop_combo1_earring_hotspot.jpg"))

        # Combo 1: Activate Necklace Hotspot
        metrics2 = await cdp.eval("""
            (() => {
                const pin = document.querySelector('[data-hotspot-id="c1-item-1"]');
                if (pin) pin.dispatchEvent(new MouseEvent('mouseenter', {bubbles: true}));
                const pop = document.querySelector('[data-popover="c1-item-1"]');
                const card = document.getElementById('combo-left-col');
                if (!pop || !card) return null;
                const pRect = pop.getBoundingClientRect();
                const cRect = card.getBoundingClientRect();
                return {
                    pinFound: true,
                    popVisible: !pop.classList.contains('invisible'),
                    overflowRight: pRect.right - cRect.right,
                    overflowLeft: cRect.left - pRect.left
                };
            })()
        """)
        print("Combo 1 Necklace Desktop Metrics:", metrics2)
        await asyncio.sleep(0.5)
        await cdp.screenshot(os.path.join(ARTIFACT_DIR, "desktop_combo1_necklace_hotspot.jpg"))

        # Switch to Combo 2
        await cdp.eval("""
            const dot2 = document.querySelector('#curated-combo-dots button[data-combo-dot="1"]') || document.querySelectorAll('#curated-combo-dots button')[1];
            if (dot2) dot2.click();
        """)
        await asyncio.sleep(1.0)

        # Combo 2: Activate Golden Meadow Hotspot
        metrics3 = await cdp.eval("""
            (() => {
                const pin = document.querySelector('[data-hotspot-id="c2-item-1"]');
                if (pin) pin.dispatchEvent(new MouseEvent('mouseenter', {bubbles: true}));
                const pop = document.querySelector('[data-popover="c2-item-1"]');
                const card = document.getElementById('combo-left-col');
                if (!pop || !card) return null;
                const pRect = pop.getBoundingClientRect();
                const cRect = card.getBoundingClientRect();
                return {
                    pinFound: true,
                    popVisible: !pop.classList.contains('invisible'),
                    overflowRight: pRect.right - cRect.right,
                    overflowLeft: cRect.left - pRect.left
                };
            })()
        """)
        print("Combo 2 Golden Meadow Desktop Metrics:", metrics3)
        await asyncio.sleep(0.5)
        await cdp.screenshot(os.path.join(ARTIFACT_DIR, "desktop_combo2_golden_meadow_hotspot.jpg"))

        # ----------------------------------------------------
        # 2. Mobile Verification (390x844)
        # ----------------------------------------------------
        print("\n--- Testing Mobile (390x844) ---")
        await cdp.send("Emulation.setDeviceMetricsOverride", {
            "width": 390,
            "height": 844,
            "deviceScaleFactor": 2,
            "mobile": True
        })
        await asyncio.sleep(0.5)
        await cdp.eval("""
            const sec = document.getElementById('curated-looks-section');
            if (sec) sec.scrollIntoView({behavior: 'smooth', block: 'start'});
        """)
        await asyncio.sleep(0.8)

        # Combo 2 on Mobile: Click Golden Meadow pin
        mobMetrics1 = await cdp.eval("""
            (() => {
                const pin = document.querySelector('[data-hotspot-id="c2-item-1"]');
                if (pin) pin.click();
                const pop = document.querySelector('[data-popover="c2-item-1"]');
                const card = document.getElementById('combo-left-col');
                if (!pop || !card) return null;
                const pRect = pop.getBoundingClientRect();
                const cRect = card.getBoundingClientRect();
                return {
                    pinFound: true,
                    popVisible: !pop.classList.contains('invisible'),
                    overflowRight: pRect.right - cRect.right,
                    overflowLeft: cRect.left - pRect.left,
                    popBottom: pRect.bottom,
                    cardBottom: cRect.bottom
                };
            })()
        """)
        print("Combo 2 Golden Meadow Mobile Metrics:", mobMetrics1)
        await asyncio.sleep(0.5)
        await cdp.screenshot(os.path.join(ARTIFACT_DIR, "mobile_combo2_golden_meadow_hotspot.jpg"))

        # Switch back to Combo 1 on Mobile
        await cdp.eval("""
            const dot1 = document.querySelectorAll('#curated-combo-dots button')[0];
            if (dot1) dot1.click();
        """)
        await asyncio.sleep(0.8)

        # Combo 1 on Mobile: Click Earring pin
        mobMetrics2 = await cdp.eval("""
            (() => {
                const pin = document.querySelector('[data-hotspot-id="c1-item-2"]');
                if (pin) pin.click();
                const pop = document.querySelector('[data-popover="c1-item-2"]');
                const card = document.getElementById('combo-left-col');
                if (!pop || !card) return null;
                const pRect = pop.getBoundingClientRect();
                const cRect = card.getBoundingClientRect();
                return {
                    pinFound: true,
                    popVisible: !pop.classList.contains('invisible'),
                    overflowRight: pRect.right - cRect.right,
                    overflowLeft: cRect.left - pRect.left
                };
            })()
        """)
        print("Combo 1 Earring Mobile Metrics:", mobMetrics2)
        await asyncio.sleep(0.5)
        await cdp.screenshot(os.path.join(ARTIFACT_DIR, "mobile_combo1_earring_hotspot.jpg"))

        # Reset Emulation
        await cdp.send("Emulation.setDeviceMetricsOverride", {
            "width": 1440,
            "height": 900,
            "deviceScaleFactor": 1,
            "mobile": False
        })
        await cdp.eval("window.scrollTo(0, 0)")

    print("\nVisual verification finished successfully!")

if __name__ == "__main__":
    asyncio.run(main())
