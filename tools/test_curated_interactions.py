import asyncio
import json
import urllib.request
import websockets

async def test_interactions():
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

        # Switch to Desktop
        await call('Emulation.clearDeviceMetricsOverride')
        await call('Emulation.setDeviceMetricsOverride', {'width': 1440, 'height': 900, 'deviceScaleFactor': 1, 'mobile': False})
        
        # Test 1: Click first pin on Slide 1
        res1 = await call('Runtime.evaluate', {
            'expression': """(() => {
                const pin = document.querySelector('.combo-hotspot-pin[data-hotspot-id="c1-item-1"] button');
                if (pin) pin.click();
                const popover = document.querySelector('[data-popover="c1-item-1"]');
                return {
                    pinFound: !!pin,
                    popoverVisible: popover ? popover.classList.contains('visible') : false
                };
            })()""",
            'returnByValue': True
        })
        print("Test 1 (Click Necklace Pin):", res1['result']['value'])

        # Test 2: Click second pin on Slide 1
        res2 = await call('Runtime.evaluate', {
            'expression': """(() => {
                const pin = document.querySelector('.combo-hotspot-pin[data-hotspot-id="c1-item-2"] button');
                if (pin) pin.click();
                const popover = document.querySelector('[data-popover="c1-item-2"]');
                return {
                    pinFound: !!pin,
                    popoverVisible: popover ? popover.classList.contains('visible') : false
                };
            })()""",
            'returnByValue': True
        })
        print("Test 2 (Click Earring Pin):", res2['result']['value'])

        # Test 3: Switch to Slide 2 and click Golden Meadow Pin
        res3 = await call('Runtime.evaluate', {
            'expression': """(() => {
                const dot = document.querySelectorAll('#curated-combo-dots button')[1];
                if (dot) dot.click();
                const pin = document.querySelector('.combo-hotspot-pin[data-hotspot-id="c2-item-1"] button');
                if (pin) pin.click();
                const popover = document.querySelector('[data-popover="c2-item-1"]');
                return {
                    pinFound: !!pin,
                    popoverVisible: popover ? popover.classList.contains('visible') : false
                };
            })()""",
            'returnByValue': True
        })
        print("Test 3 (Click Golden Meadow Pin):", res3['result']['value'])

        # Test 4: Test Add to Bag Button
        res4 = await call('Runtime.evaluate', {
            'expression': """(() => {
                const btn = document.getElementById('btn-add-combo-to-bag');
                if (btn) btn.click();
                const drawer = document.getElementById('cart-drawer');
                return {
                    btnFound: !!btn,
                    drawerOpen: drawer ? drawer.classList.contains('translate-x-0') : false
                };
            })()""",
            'returnByValue': True
        })
        print("Test 4 (Click Add to Bag):", res4['result']['value'])

asyncio.run(test_interactions())

