import asyncio
import json
import os
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        
        # Open or reuse a page for Solystra
        page = None
        for p_page in context.pages:
            if "8089" in p_page.url or "product.html" in p_page.url:
                page = p_page
                break
        if not page:
            page = await context.new_page()

        # Set desktop viewport 1440x900
        await page.set_viewport_size({"width": 1440, "height": 900})
        
        url = "http://127.0.0.1:8089/product.html"
        print(f"Navigating to {url}...")
        await page.goto(url, wait_until="networkidle")
        await asyncio.sleep(1)

        # Check for unrequested badges on left
        left_has_badges = await page.evaluate("""() => {
            const gallery = document.querySelector('.pdp-fixed-gallery');
            if (!gallery) return false;
            return gallery.innerText.includes('Official BIS Hallmark') || 
                   gallery.innerText.includes('Velvet Keepsake') ||
                   gallery.innerText.includes('Lifetime Replating');
        }""")
        print(f"Left gallery has unwanted badges: {left_has_badges}")

        # Measure initial geometry at scrollY = 0
        initial_geo = await page.evaluate("""() => {
            window.scrollTo(0, 0);
            const gallery = document.querySelector('.pdp-fixed-gallery');
            const mainImg = document.querySelector('#pdp-main-img');
            const rightCol = document.querySelector('.lg\\\\:col-span-5');
            const gRect = gallery ? gallery.getBoundingClientRect() : null;
            const rRect = rightCol ? rightCol.getBoundingClientRect() : null;
            return {
                scrollY: window.scrollY,
                galleryTop: gRect ? gRect.top : null,
                galleryHeight: gRect ? gRect.height : null,
                rightColTop: rRect ? rRect.top : null,
                rightColHeight: rRect ? rRect.height : null
            };
        }""")
        print(f"Initial geometry at scroll 0: {json.dumps(initial_geo, indent=2)}")

        # Capture top screenshot
        os.makedirs("audit_visuals", exist_ok=True)
        top_shot_path = os.path.abspath("audit_visuals/pdp_clean_gallery_top_desktop.jpg")
        await page.screenshot(path=top_shot_path, quality=85, type="jpeg")
        print(f"Saved top screenshot: {top_shot_path}")

        # Now smooth scroll down to 450px with delays
        print("Smoothly scrolling down to 450px...")
        for y in range(0, 460, 50):
            await page.evaluate(f"window.scrollTo(0, {y})")
            await asyncio.sleep(0.08)

        await asyncio.sleep(0.5)

        # Measure scrolled geometry
        scrolled_geo = await page.evaluate("""() => {
            const gallery = document.querySelector('.pdp-fixed-gallery');
            const rightCol = document.querySelector('.lg\\\\:col-span-5');
            const gRect = gallery ? gallery.getBoundingClientRect() : null;
            const rRect = rightCol ? rightCol.getBoundingClientRect() : null;
            return {
                scrollY: window.scrollY,
                galleryTop: gRect ? gRect.top : null,
                galleryHeight: gRect ? gRect.height : null,
                rightColTop: rRect ? rRect.top : null,
                rightColHeight: rRect ? rRect.height : null,
                isSticky: gRect ? Math.abs(gRect.top - 98) < 15 : false
            };
        }""")
        print(f"Scrolled geometry at scroll 450: {json.dumps(scrolled_geo, indent=2)}")

        # Capture scrolled screenshot
        scrolled_shot_path = os.path.abspath("audit_visuals/pdp_sticky_gallery_scrolled_desktop.jpg")
        await page.screenshot(path=scrolled_shot_path, quality=85, type="jpeg")
        print(f"Saved scrolled screenshot: {scrolled_shot_path}")

        # Also scroll to 700px
        print("Smoothly scrolling further down to 750px...")
        for y in range(450, 760, 50):
            await page.evaluate(f"window.scrollTo(0, {y})")
            await asyncio.sleep(0.08)

        await asyncio.sleep(0.5)
        deep_geo = await page.evaluate("""() => {
            const gallery = document.querySelector('.pdp-fixed-gallery');
            const rightCol = document.querySelector('.lg\\\\:col-span-5');
            const gRect = gallery ? gallery.getBoundingClientRect() : null;
            const rRect = rightCol ? rightCol.getBoundingClientRect() : null;
            return {
                scrollY: window.scrollY,
                galleryTop: gRect ? gRect.top : null,
                rightColTop: rRect ? rRect.top : null,
                isSticky: gRect ? Math.abs(gRect.top - 98) < 15 : false
            };
        }""")
        print(f"Deep scroll geometry at 750px: {json.dumps(deep_geo, indent=2)}")

        deep_shot_path = os.path.abspath("audit_visuals/pdp_sticky_gallery_deep_scroll_desktop.jpg")
        await page.screenshot(path=deep_shot_path, quality=85, type="jpeg")
        print(f"Saved deep scroll screenshot: {deep_shot_path}")

        # Also verify mobile viewport (390x844)
        print("Testing mobile viewport 390x844...")
        await page.set_viewport_size({"width": 390, "height": 844})
        await page.evaluate("window.scrollTo(0, 0)")
        await asyncio.sleep(0.5)
        mobile_shot_path = os.path.abspath("audit_visuals/pdp_mobile_clean_top.jpg")
        await page.screenshot(path=mobile_shot_path, quality=85, type="jpeg")
        print(f"Saved mobile screenshot: {mobile_shot_path}")

        # Return to desktop size so user can inspect directly
        await page.set_viewport_size({"width": 1440, "height": 900})
        await page.evaluate("window.scrollTo(0, 400)")

if __name__ == "__main__":
    asyncio.run(main())
