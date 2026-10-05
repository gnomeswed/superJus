import asyncio
from playwright.async_api import async_playwright
import sys
sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
        ctx = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
        page = await ctx.new_page()
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        try:
            await page.goto("https://scon.stj.jus.br/SCON/pesquisar.jsp", wait_until="domcontentloaded", timeout=45000)
            await page.wait_for_timeout(6000)
            txt = await page.evaluate("document.body.innerText")
            print("--- SCON body ---")
            print(txt[:1500])
            forms = await page.evaluate("Array.from(document.querySelectorAll('form')).map(f=>f.name||f.id)")
            print("FORMS:", forms)
        except Exception as e:
            print(f"Erro: {e}")
        await browser.close()

asyncio.run(main())
