import asyncio
import os
from playwright.async_api import async_playwright

os.makedirs('audit_visuals', exist_ok=True)
os.makedirs(r'C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals', exist_ok=True)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0] if browser.contexts else await browser.new_context()
        page = context.pages[0] if context.pages else await context.new_page()

        # 1. Desktop 1440x900
        await page.set_viewport_size({"width": 1440, "height": 900})
        await page.goto('http://127.0.0.1:8080/index.html', wait_until='networkidle')
        await asyncio.sleep(1)

        # Scroll so bottom of hero and trust badges are centered
        await page.evaluate("""() => {
            const el = document.querySelector('section:has(#hero-dot-0)') || document.querySelector('section.relative');
            window.scrollTo({ top: 380, behavior: 'smooth' });
        }""")
        await asyncio.sleep(1)

        local_path = 'audit_visuals/homepage_trust_badges_fixed_desktop.jpg'
        brain_path = r'C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals\homepage_trust_badges_fixed_desktop.jpg'
        await page.screenshot(path=local_path, quality=90, type='jpeg')
        await page.screenshot(path=brain_path, quality=90, type='jpeg')
        print(f"Desktop screenshot saved to {local_path}")

        # 2. Mobile 390x844
        await page.set_viewport_size({"width": 390, "height": 844})
        await asyncio.sleep(0.5)
        await page.evaluate("window.scrollTo({ top: 320, behavior: 'smooth' });")
        await asyncio.sleep(1)

        local_path_mob = 'audit_visuals/homepage_trust_badges_fixed_mobile.jpg'
        brain_path_mob = r'C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals\homepage_trust_badges_fixed_mobile.jpg'
        await page.screenshot(path=local_path_mob, quality=90, type='jpeg')
        await page.screenshot(path=brain_path_mob, quality=90, type='jpeg')
        print(f"Mobile screenshot saved to {local_path_mob}")

        # 3. Product detail page PDP trust badges
        await page.set_viewport_size({"width": 1440, "height": 900})
        await page.goto('http://127.0.0.1:8080/product.html', wait_until='networkidle')
        await asyncio.sleep(1)
        await page.evaluate("window.scrollTo({ top: 450, behavior: 'smooth' });")
        await asyncio.sleep(0.8)

        pdp_desk = 'audit_visuals/pdp_trust_badges_desktop.jpg'
        pdp_desk_brain = r'C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals\pdp_trust_badges_desktop.jpg'
        await page.screenshot(path=pdp_desk, quality=90, type='jpeg')
        await page.screenshot(path=pdp_desk_brain, quality=90, type='jpeg')
        print(f"PDP desktop screenshot saved to {pdp_desk}")

if __name__ == '__main__':
    asyncio.run(main())

