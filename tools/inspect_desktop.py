import urllib.request
import json
import asyncio
import websockets

async def inspect_desktop():
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

        # Clear override (desktop)
        await call('Emulation.clearDeviceMetricsOverride')
        await asyncio.sleep(0.5)

        for s_id in range(4):
            eval_res = await call('Runtime.evaluate', {
                'expression': f"""
                    (() => {{
                        const s = document.getElementById('hero-slide-{s_id}');
                        const btn = s ? s.querySelector('button') : null;
                        const h2 = s ? s.querySelector('h2') : null;
                        const p = s ? s.querySelector('p') : null;

                        return {{
                            slide: {s_id},
                            btn: btn ? {{
                                text: btn.innerText.trim(),
                                padding: getComputedStyle(btn).padding,
                                height: getComputedStyle(btn).height,
                            }} : null,
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
            print(f"Desktop Slide {s_id}:", json.dumps(val, indent=2))

asyncio.run(inspect_desktop())
