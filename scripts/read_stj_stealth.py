import asyncio
from playwright.async_api import async_playwright
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    print("=== CONSULTA STJ AO VIVO COM PLAYWRIGHT STEALTH ===")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
        )
        ctx = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
        )
        page = await ctx.new_page()
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        url = "https://processo.stj.jus.br/processo/pesquisa/?aplicacao=processos.ea&tipoPesquisa=tipoPesquisaNumeroRegistro&parametroNumeroRegistro=202603112107"
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=45000)
            await page.wait_for_timeout(8000) # Wait for Cloudflare turnstile auto-redirect
            
            text_content = await page.evaluate("document.body.innerText")
            print("\n--- TEOR RETORNADO DO STJ ---")
            print(text_content[:3500])
        except Exception as e:
            print(f"Erro: {e}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
