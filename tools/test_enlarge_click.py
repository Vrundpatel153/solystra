import asyncio
import json
import urllib.request
import base64
import websockets
import os

async def send_cmd(ws, msg_id, method, params=None):
    payload = {'id': msg_id, 'method': method}
    if params:
        payload['params'] = params
    await ws.send(json.dumps(payload))
    while True:
        resp = json.loads(await ws.recv())
        if resp.get('id') == msg_id:
            return resp

async def run_eval(ws, msg_id, expr):
    resp = await send_cmd(ws, msg_id, 'Runtime.evaluate', {
        'expression': expr,
        'returnByValue': True,
        'awaitPromise': True
    })
    return resp.get('result', {}).get('result', {}).get('value')

async def main():
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(req.read().decode('utf-8'))
    
    target_tab = None
    for tab in tabs:
        if tab.get('type') == 'page' and ('8089' in tab.get('url', '') or 'product.html' in tab.get('url', '')):
            target_tab = tab
            break
            
    if not target_tab:
        print("No product page tab found!")
        return

    ws_url = target_tab.get('webSocketDebuggerUrl')
    async with websockets.connect(ws_url, max_size=25*1024*1024) as ws:
        msg_id = 1
        
        # Check what onclick or listeners are on the enlarge button
        btn_info = await run_eval(ws, msg_id, """(() => {
            const btn = document.querySelector('button[aria-label="Enlarge Image"]');
            if (!btn) return 'not found';
            return {
                onclick: btn.onclick ? btn.onclick.toString() : null,
                hasAttributeOnclick: btn.getAttribute('onclick'),
                html: btn.outerHTML
            };
        })()"""); msg_id += 1
        print("Button info:", json.dumps(btn_info, indent=2))

        # Check if window.openImageLightbox exists
        has_lightbox_fn = await run_eval(ws, msg_id, "typeof window.openImageLightbox"); msg_id += 1
        print("typeof window.openImageLightbox:", has_lightbox_fn)

        # Click the button
        click_res = await run_eval(ws, msg_id, """(() => {
            const btn = document.querySelector('button[aria-label="Enlarge Image"]');
            if (btn) {
                btn.click();
                return 'clicked';
            }
            return 'not found';
        })()"""); msg_id += 1
        print("Click result:", click_res)

        await asyncio.sleep(1.0)

        # Check what DOM elements were created or modified
        modal_info = await run_eval(ws, msg_id, """(() => {
            const lb = document.getElementById('pdp-lightbox-modal');
            if (!lb) return { found: false };
            const rect = lb.getBoundingClientRect();
            return {
                found: true,
                display: lb.style.display,
                position: lb.style.position,
                rect: { top: rect.top, left: rect.left, width: rect.width, height: rect.height },
                innerHTML_len: lb.innerHTML.length,
                classes: lb.className
            };
        })()"""); msg_id += 1
        print("Modal info after click:", json.dumps(modal_info, indent=2))

        # Capture a screenshot of the page after clicking
        shot = await send_cmd(ws, msg_id, 'Page.captureScreenshot', {'format': 'jpeg', 'quality': 85}); msg_id += 1
        img_data = base64.b64decode(shot['result']['data'])
        with open("audit_visuals/current_enlarge_modal_screen.jpg", "wb") as f:
            f.write(img_data)
        print("Saved screenshot to audit_visuals/current_enlarge_modal_screen.jpg")

if __name__ == '__main__':
    asyncio.run(main())

