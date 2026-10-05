import asyncio
from playwright.async_api import async_playwright
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    print("=== CAPTURANDO TEXTO COMPLETO DO STJ PARA JÚLIO PEREIRA MARCOS ===")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
        page = await browser.new_page()
        
        url = "https://processo.stj.jus.br/processo/pesquisa/?aplicacao=processos.ea&tipoPesquisa=tipoPesquisaNumeroRegistro&parametroNumeroRegistro=202603112107"
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=45000)
            await page.wait_for_timeout(4000)
            
            text_content = await page.evaluate("document.body.innerText")
            print("\n--- TEOR DA PÁGINA DO STJ ---")
            print(text_content[:3000])
        except Exception as e:
            print(f"Erro: {e}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
