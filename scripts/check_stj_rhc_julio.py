import asyncio
from playwright.async_api import async_playwright
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    print("=== CONSULTA AO VIVO - STJ: HC 1.116.750/RJ (2026/0311210-7) ===")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
        page = await browser.new_page()
        
        url = "https://processo.stj.jus.br/processo/pesquisa/?aplicacao=processos.ea&tipoPesquisa=tipoPesquisaNumeroRegistro&parametroNumeroRegistro=202603112107"
        print(f"Acessando portal do STJ: {url}")
        
        try:
            # Increase timeout and use domcontentloaded
            await page.goto(url, wait_until="domcontentloaded", timeout=45000)
            await page.wait_for_timeout(3000) # Give it 3 extra seconds for JS to render
            
            text_content = await page.evaluate("document.body.innerText")
            
            lines = [line.strip() for line in text_content.split('\n') if line.strip()]
            
            print("\n--- ANDAMENTOS ENCONTRADOS ---")
            found = False
            for i, line in enumerate(lines):
                if "2026" in line and ("/" in line or "-" in line):
                    print(f"  {line}")
                    if i + 1 < len(lines):
                        print(f"  {lines[i+1]}")
                        print("-" * 40)
                    found = True
            
            if not found:
                print("Não foram encontrados andamentos explícitos na página retornada.")
                print("Início do conteúdo da página:")
                print("\n".join(lines[:20]))
                
        except Exception as e:
            print(f"Erro ao acessar STJ: {e}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
