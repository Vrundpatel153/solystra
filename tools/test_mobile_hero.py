import urllib.request
import json
import asyncio
import websockets
import base64
import os
import shutil

ARTIFACT_DIR = r"C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals"

async def test_mobile_hero():
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

        # Set mobile viewport 390x844
        await send('Emulation.setDeviceMetricsOverride', {
            'width': 390,
            'height': 844,
            'deviceScaleFactor': 2,
            'mobile': True
        })

        await send('Page.navigate', {'url': 'http://127.0.0.1:8095/index.html'})
        await asyncio.sleep(2.0)

        # First, capture current mobile slide 0 and slide 1
        await capture("hero_mobile_current_slide0.jpg")
        await send('Runtime.evaluate', {'expression': 'window.setHeroSlide(1)'})
        await asyncio.sleep(0.8)
        await capture("hero_mobile_current_slide1.jpg")

        # Now test rearranging text to bottom with elegant bottom gradient:
        # We can dynamically apply styling to all slides to see the visual comparison
        js_apply_rearrange = """
        document.querySelectorAll('[data-hero-slide]').forEach(slide => {
            // Find text container
            const textOverlay = slide.querySelector('.absolute.inset-0.z-10');
            if (textOverlay) {
                textOverlay.className = "absolute inset-0 z-10 flex items-end pb-12 sm:pb-0 sm:items-center";
            }
            // Find mobile gradient
            const mobGrad = slide.querySelector('.sm\\\\:hidden');
            if (mobGrad) {
                mobGrad.className = "absolute inset-0 bg-gradient-to-t from-black/90 via-black/45 via-45% to-transparent sm:hidden pointer-events-none";
            }
            // Adjust margin top of button
            const btnGroup = slide.querySelector('.mt-9');
            if (btnGroup) {
                btnGroup.className = "mt-3 sm:mt-7 flex items-center gap-3";
            }
            // Make title and subtitle compact and crisp on mobile
            const title = slide.querySelector('h2');
            if (title) {
                title.className = "font-serif text-[22px] xs:text-[24px] sm:text-4xl md:text-5xl lg:text-6xl text-white font-normal leading-tight tracking-tight drop-shadow-[0_2px_10px_rgba(0,0,0,0.85)] max-w-full";
            }
            const desc = slide.querySelector('p');
            if (desc) {
                desc.className = "text-[11.5px] xs:text-xs sm:text-base lg:text-lg text-stone-200 mt-1 sm:mt-3 leading-snug sm:leading-relaxed font-light drop-shadow-[0_2px_8px_rgba(0,0,0,0.85)] max-w-[280px] xs:max-w-sm sm:max-w-lg line-clamp-2 sm:line-clamp-none";
            }
        });
        """
        await send('Runtime.evaluate', {'expression': js_apply_rearrange})
        await asyncio.sleep(0.5)

        # Capture rearranged Slide 1
        await capture("hero_mobile_rearranged_slide1.jpg")

        # Switch to rearranged Slide 0
        await send('Runtime.evaluate', {'expression': 'window.setHeroSlide(0)'})
        await asyncio.sleep(0.8)
        await capture("hero_mobile_rearranged_slide0.jpg")

        # Switch to rearranged Slide 2
        await send('Runtime.evaluate', {'expression': 'window.setHeroSlide(2)'})
        await asyncio.sleep(0.8)
        await capture("hero_mobile_rearranged_slide2.jpg")

        # Switch to rearranged Slide 3
        await send('Runtime.evaluate', {'expression': 'window.setHeroSlide(3)'})
        await asyncio.sleep(0.8)
        await capture("hero_mobile_rearranged_slide3.jpg")

if __name__ == '__main__':
    asyncio.run(test_mobile_hero())
