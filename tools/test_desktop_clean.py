import urllib.request
import json
import asyncio
import websockets
import base64
import os

ARTIFACT_DIR = r"C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals"
os.makedirs(ARTIFACT_DIR, exist_ok=True)

async def test_desktop():
    req = urllib.request.urlopen('http://127.0.0.1:9222/json')
    tabs = json.loads(req.read().decode())
    p = [t for t in tabs if t.get('type') == 'page'][0]
    
    async with websockets.connect(p['webSocketDebuggerUrl'], max_size=50*1024*1024) as ws:
        msg_id = 1
        async def call(method, params=None):
            nonlocal msg_id
            msg_id += 1
            payload = {"id": msg_id, "method": method, "params": params or {}}
            await ws.send(json.dumps(payload))
            while True:
                res = json.loads(await ws.recv())
                if res.get('id') == msg_id:
                    return res

        # Clear override and set desktop 1440x900
        await call('Emulation.clearDeviceMetricsOverride')
        await call('Emulation.setDeviceMetricsOverride', {
            'width': 1440,
            'height': 900,
            'deviceScaleFactor': 1,
            'mobile': False
        })
        await call('Network.enable')
        await call('Network.setCacheDisabled', {'cacheDisabled': True})
        await call('Page.navigate', {'url': 'http://127.0.0.1:8095/index.html?t=' + str(int(asyncio.get_event_loop().time()))})
        await asyncio.sleep(1.5)

        # Stop auto-slide
        await call('Runtime.evaluate', {
            'expression': """
                if (window.heroSliderInterval) clearInterval(window.heroSliderInterval);
                if (window.heroTimer) clearInterval(window.heroTimer);
                for (let i = 0; i < 4; i++) {
                    const s = document.getElementById('hero-slide-' + i);
                    if (s) s.style.transition = 'none';
                }
            """
        })

        for s_id in range(4):
            await call('Runtime.evaluate', {
                'expression': f"""
                    window.setHeroSlide({s_id});
                    for (let i = 0; i < 4; i++) {{
                        const s = document.getElementById('hero-slide-' + i);
                        if (s) {{
                            s.style.transition = 'none';
                            if (i === {s_id}) {{
                                s.style.opacity = '1';
                                s.style.zIndex = '10';
                                s.style.pointerEvents = 'auto';
                            }} else {{
                                s.style.opacity = '0';
                                s.style.zIndex = '0';
                                s.style.pointerEvents = 'none';
                            }}
                        }}
                    }}
                """
            })
            await asyncio.sleep(0.4)

            shot = await call('Page.captureScreenshot', {'format': 'jpeg', 'quality': 85})
            with open(os.path.join(ARTIFACT_DIR, f"desktop_slide_{s_id}_clean.jpg"), "wb") as f:
                f.write(base64.b64decode(shot['result']['data']))

        print("Desktop slides 0-3 captured cleanly!")

asyncio.run(test_desktop())

