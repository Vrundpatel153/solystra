import urllib.request
import json
import asyncio
import websockets
import base64
import os

ARTIFACT_DIR = r"C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals"
os.makedirs(ARTIFACT_DIR, exist_ok=True)

async def inspect():
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

        # Disable cache
        await call('Network.enable')
        await call('Network.setCacheDisabled', {'cacheDisabled': True})

        # Set mobile viewport
        await call('Emulation.setDeviceMetricsOverride', {
            'width': 390,
            'height': 844,
            'deviceScaleFactor': 2,
            'mobile': True
        })
        await asyncio.sleep(0.2)

        # Navigate with cache disabled and timestamp
        await call('Page.navigate', {'url': 'http://127.0.0.1:8095/index.html?t=hero_v2'})
        await asyncio.sleep(1.5)

        for s_id in range(4):
            # activate slide
            await call('Runtime.evaluate', {
                'expression': f"""
                    for (let i = 0; i < 4; i++) {{
                        const s = document.getElementById('hero-slide-' + i);
                        if (s) {{
                            s.classList.remove('opacity-100', 'z-10', 'pointer-events-auto');
                            s.classList.add('opacity-0', 'z-0', 'pointer-events-none');
                        }}
                    }}
                    const target = document.getElementById('hero-slide-{s_id}');
                    if (target) {{
                        target.classList.remove('opacity-0', 'z-0', 'pointer-events-none');
                        target.classList.add('opacity-100', 'z-10', 'pointer-events-auto');
                    }}
                """
            })
            await asyncio.sleep(0.3)

            eval_res = await call('Runtime.evaluate', {
                'expression': f"""
                    (() => {{
                        function r(el) {{
                            if (!el) return null;
                            const rect = el.getBoundingClientRect();
                            return {{ x: Math.round(rect.x), y: Math.round(rect.y), width: Math.round(rect.width), height: Math.round(rect.height), bottom: Math.round(rect.bottom) }};
                        }}
                        const s = document.getElementById('hero-slide-{s_id}');
                        const btn = s ? s.querySelector('button') : null;
                        const span = btn ? btn.querySelector('span') : null;
                        const svg = btn ? btn.querySelector('svg') : null;
                        const h2 = s ? s.querySelector('h2') : null;
                        const p = s ? s.querySelector('p') : null;
                        const dots = document.getElementById('hero-dots') || document.querySelector('.absolute.bottom-4');

                        return {{
                            slide: {s_id},
                            btn: btn ? {{
                                text: btn.innerText.trim(),
                                rect: r(btn),
                                padding: getComputedStyle(btn).padding,
                                display: getComputedStyle(btn).display,
                                alignItems: getComputedStyle(btn).alignItems,
                                justifyContent: getComputedStyle(btn).justifyContent,
                            }} : null,
                            spanRect: r(span),
                            svgRect: r(svg),
                            h2Rect: r(h2),
                            pRect: r(p),
                            dotsRect: r(dots),
                            h2Styles: h2 ? {{
                                fontSize: getComputedStyle(h2).fontSize,
                                textShadow: getComputedStyle(h2).textShadow,
                            }} : null,
                            pStyles: p ? {{
                                fontSize: getComputedStyle(p).fontSize,
                                textShadow: getComputedStyle(p).textShadow,
                            }} : null
                        }};
                    }})()
                """,
                'returnByValue': True
            })
            val = eval_res.get('result', {}).get('result', {}).get('value', {})
            print(f"Slide {s_id}:", json.dumps(val, indent=2))

            # Take screenshot
            shot = await call('Page.captureScreenshot', {'format': 'jpeg', 'quality': 85})
            with open(os.path.join(ARTIFACT_DIR, f"mobile_slide_{s_id}_fixed.jpg"), "wb") as f:
                f.write(base64.b64decode(shot['result']['data']))

        print("Done capturing 4 mobile slides with cache disabled.")

asyncio.run(inspect())
