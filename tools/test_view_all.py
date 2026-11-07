import urllib.request
import json
import asyncio
import websockets
import base64
import os
import shutil

ARTIFACT_DIR = r"C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals"

async def test_view_all():
    req = urllib.request.urlopen('http://127.0.0.1:9222/json')
    tabs = json.loads(req.read().decode())
    p = [t for t in tabs if t.get('type') == 'page'][0]
    async with websockets.connect(p['webSocketDebuggerUrl'], max_size=50*1024*1024) as ws:
        msg_id = 1
        async def send(method, params=None):
            nonlocal msg_id
            payload = {'id': msg_id, 'method': method}
            if params:
                payload['params'] = params
            msg_id += 1
            await ws.send(json.dumps(payload))
            while True:
                resp = json.loads(await ws.recv())
                if resp.get('id') == payload['id']:
                    return resp

        async def capture(filename):
            shot = await send('Page.captureScreenshot', {'format': 'jpeg', 'quality': 85})
            data = base64.b64decode(shot['result']['data'])
            local_p = os.path.join("audit_visuals", filename)
            with open(local_p, "wb") as f:
                f.write(data)
            shutil.copy(local_p, os.path.join(ARTIFACT_DIR, filename))
            print(f"Captured: {filename} ({len(data)} bytes)")

        # 1. Set mobile viewport 390x844
        await send('Emulation.setDeviceMetricsOverride', {
            'width': 390,
            'height': 844,
            'deviceScaleFactor': 2,
            'mobile': True
        })

        # Navigate to dist home
        await send('Page.navigate', {'url': 'http://127.0.0.1:8095/index.html?v=btnfix2026'})
        await asyncio.sleep(2.0)

        # Scroll to mobile category carousel
        await send('Runtime.evaluate', {'expression': 'window.scrollTo({ top: 580, behavior: "smooth" })'})
        await asyncio.sleep(1.0)

        # Scroll the horizontal carousel to the right to make "View All" fully visible
        await send('Runtime.evaluate', {'expression': '''(() => {
            const carousel = document.querySelector(".md\\\\:hidden.overflow-x-auto");
            if (carousel) carousel.scrollLeft = carousel.scrollWidth;
        })()'''})
        await asyncio.sleep(0.8)
        await capture("mobile_category_view_all_scrolled.jpg")

        # Click the "View All" button
        print("Clicking the View All button...")
        click_res = await send('Runtime.evaluate', {'expression': '''(() => {
            const items = document.querySelectorAll(".md\\\\:hidden.overflow-x-auto > div");
            const lastItem = items[items.length - 1];
            if (lastItem) {
                lastItem.click();
                return { clicked: true, text: lastItem.innerText.trim() };
            }
            return { clicked: false };
        })()''', 'returnByValue': True})
        print("Click result:", click_res.get('result', {}).get('result', {}).get('value'))

        # Wait for navigation to categories.html
        await asyncio.sleep(2.0)
        curr_url = await send('Runtime.evaluate', {'expression': 'window.location.href', 'returnByValue': True})
        print("Current URL after click:", curr_url.get('result', {}).get('result', {}).get('value'))

        # Capture categories page
        await capture("navigated_categories_page.jpg")

if __name__ == '__main__':
    asyncio.run(test_view_all())

