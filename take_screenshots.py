import asyncio
from playwright.async_api import async_playwright
import os

URL = "http://localhost:5000"
OUT = "picture"
os.makedirs(OUT, exist_ok=True)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1400, "height": 900})

        print("Loading dashboard...")
        await page.goto(URL, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(3000)

        # 1. Full-page overview (tall viewport)
        await page.set_viewport_size({"width": 1400, "height": 900})
        await page.screenshot(path=f"{OUT}/01_header_kpi.jpg", clip={"x":0,"y":0,"width":1400,"height":900})
        print("✓ 01_header_kpi.jpg")

        # 2. Scroll to charts row 1
        await page.evaluate("window.scrollTo(0, 650)")
        await page.wait_for_timeout(1000)
        await page.screenshot(path=f"{OUT}/02_failure_distribution_bar.jpg", clip={"x":310,"y":0,"width":1090,"height":900})
        print("✓ 02_failure_distribution_bar.jpg")

        # 3. Monthly trend chart
        await page.evaluate("window.scrollTo(0, 700)")
        await page.wait_for_timeout(800)
        await page.screenshot(path=f"{OUT}/03_monthly_trend_line.jpg", clip={"x":310,"y":0,"width":1090,"height":900})
        print("✓ 03_monthly_trend_line.jpg")

        # 4. Scroll to row 2 charts
        await page.evaluate("window.scrollTo(0, 1300)")
        await page.wait_for_timeout(1000)
        await page.screenshot(path=f"{OUT}/04_machine_condition_scatter.jpg", clip={"x":310,"y":0,"width":1090,"height":900})
        print("✓ 04_machine_condition_scatter.jpg")

        # 5. Product quality bar chart
        await page.evaluate("window.scrollTo(0, 1400)")
        await page.wait_for_timeout(800)
        await page.screenshot(path=f"{OUT}/05_product_quality_bar.jpg", clip={"x":310,"y":0,"width":1090,"height":900})
        print("✓ 05_product_quality_bar.jpg")

        # 6. Data tables section
        await page.evaluate("window.scrollTo(0, 2100)")
        await page.wait_for_timeout(1000)
        await page.screenshot(path=f"{OUT}/06_data_tables.jpg", clip={"x":310,"y":0,"width":1090,"height":900})
        print("✓ 06_data_tables.jpg")

        # 7. Sidebar filters full view
        await page.evaluate("window.scrollTo(0, 0)")
        await page.wait_for_timeout(800)
        await page.screenshot(path=f"{OUT}/07_sidebar_filters.jpg", clip={"x":0,"y":0,"width":310,"height":900})
        print("✓ 07_sidebar_filters.jpg")

        # 8. Full page composite
        total_height = await page.evaluate("document.body.scrollHeight")
        await page.set_viewport_size({"width": 1400, "height": total_height})
        await page.wait_for_timeout(1500)
        await page.screenshot(path=f"{OUT}/08_full_dashboard.jpg", full_page=True)
        print("✓ 08_full_dashboard.jpg")

        await browser.close()
        print("\nAll screenshots saved to:", OUT)

asyncio.run(main())
