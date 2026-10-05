# -*- coding: utf-8 -*-
import asyncio
import sys
from playwright.async_api import async_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
        )
        ctx = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36"
        )
        page = await ctx.new_page()
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        url = "https://processo.stj.jus.br/processo/pesquisa/?aplicacao=processos.ea&tipoPesquisa=tipoPesquisaNumeroRegistro&parametroNumeroRegistro=202603112107"
        try:
            print("Navegando para o STJ...")
            await page.goto(url, wait_until="domcontentloaded", timeout=45000)
            print("Aguardando verificação do Cloudflare...")
            passed = False
            for i in range(20):
                await page.wait_for_timeout(1000)
                txt = await page.evaluate("document.body.innerText")
                if "Verificação automática" not in txt and "Habeas Corpus" in txt:
                    print(f"Passou do Cloudflare em {i+1}s!")
                    passed = True
                    break
            
            if not passed:
                print("Cloudflare ainda bloqueando...")
                await page.screenshot(path="c:/Projetos/superJus/stj_cloudflare_state.png")
                return

            print("Clicando na aba Petições...")
            pet_tabs = page.locator("a:has-text('Petições'), [id*='peticao'], [href*='peticao']")
            if await pet_tabs.count() > 0:
                await pet_tabs.first.click()
                await page.wait_for_timeout(4000)
                body = await page.evaluate("document.body.innerText")
                print("=== TEXTO DA ABA PETIÇÕES ===")
                print(body[:3000])
                
                links = await page.eval_on_selector_all("a", "els => els.map(e => ({t: e.innerText, h: e.href, oc: e.getAttribute('onclick')}))")
                for l in links:
                    s = str(l)
                    if any(k in s.lower() for k in ["1025001", "peticao", "petição", "download", "pdf", "visualizar"]):
                        print("LINK ENCONTRADO:", l)
            else:
                print("Aba Petições não encontrada diretamente.")
        except Exception as e:
            print(f"Erro: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
