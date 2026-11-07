import asyncio
import json
import urllib.request
import websockets
import base64
from PIL import Image, ImageDraw

async def capture_gm():
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

        # Scroll to GM row
        await call('Runtime.evaluate', {
            'expression': "window.scrollTo(0, 600);"
        })
        await asyncio.sleep(0.5)

        shot = await call('Page.captureScreenshot', {'format': 'jpeg', 'quality': 85})
        with open("scratch/gm_page.jpg", "wb") as f:
            f.write(base64.b64decode(shot['data']))
        print("Captured gm_page.jpg")

asyncio.run(capture_gm())

# Crop GM mob and pc
im = Image.open("scratch/gm_page.jpg")
crop_gm_mob = im.crop((20, 150, 20 + 360, 150 + 382))
crop_gm_pc = im.crop((410, 150, 410 + 594, 150 + 432))

def add_grid(crop, filename):
    w, h = crop.size
    draw = ImageDraw.Draw(crop)
    for x_pct in range(0, 101, 10):
        x = int(w * x_pct / 100)
        draw.line([(x, 0), (x, h)], fill=(255, 255, 0, 120), width=1)
        draw.text((x + 2, 4), f"{x_pct}%", fill=(255, 255, 0))
    for y_pct in range(0, 101, 10):
        y = int(h * y_pct / 100)
        draw.line([(0, y), (w, y)], fill=(255, 255, 0, 120), width=1)
        draw.text((4, y + 2), f"{y_pct}%", fill=(255, 255, 0))
    crop.save(f"scratch/{filename}", quality=90)
    print(f"Saved scratch/{filename}")

add_grid(crop_gm_mob, "calib_gm_mob.jpg")
add_grid(crop_gm_pc, "calib_gm_pc.jpg")
