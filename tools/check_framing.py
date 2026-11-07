import asyncio
import json
import urllib.request
import websockets
import base64

async def check_image_framing():
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(req.read().decode())
    p = [t for t in tabs if t.get('type') == 'page' and '8095' in t.get('url', '')][0]
    
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
                    return res.get('result', {})

        await call('Page.navigate', {'url': 'http://127.0.0.1:8095/calibrate_hotspots.html?t=2'})
        await asyncio.sleep(2.0)

        res = await call('Runtime.evaluate', {
            'expression': """(() => {
                function info(id) {
                    const img = document.getElementById(id);
                    if (!img) return null;
                    const r = img.getBoundingClientRect();
                    return {
                        id,
                        renderedWidth: r.width,
                        renderedHeight: r.height,
                        naturalWidth: img.naturalWidth,
                        naturalHeight: img.naturalHeight
                    };
                }
                return {
                    c2_mob: info('img-c2-mob'),
                    c2_pc: info('img-c2-pc'),
                    gm_mob: info('img-gm-mob'),
                    gm_pc: info('img-gm-pc')
                };
            })()""",
            'returnByValue': True
        })
        print(json.dumps(res.get('result', {}).get('value', {}), indent=2))

        shot = await call('Page.captureScreenshot', {'format': 'jpeg', 'quality': 85})
        with open("C:/Users/vrund/.gemini/antigravity/brain/68f27351-9b2c-41bf-b75f-ce5ad9262a98/audit_visuals/calibration_loaded.jpg", "wb") as f:
            f.write(base64.b64decode(shot['data']))
        print("Captured calibration_loaded.jpg")

asyncio.run(check_image_framing())
