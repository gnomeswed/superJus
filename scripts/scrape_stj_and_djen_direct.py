# -*- coding: utf-8 -*-
import asyncio, sys, os
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    print("=== CONSULTA STJ AO VIVO COM PLAYWRIGHT STEALTH (25/08/2026) ===")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )
        ctx = await browser.new_context(
            viewport={"width": 1366, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            locale="pt-BR"
        )
        page = await ctx.new_page()
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        url = "https://processo.stj.jus.br/processo/pesquisa/?aplicacao=processos.ea&tipoPesquisa=tipoPesquisaNumeroRegistro&parametroNumeroRegistro=202603112107"
        print(f">> Acessando: {url}")
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=45000)
            print(">> Aguardando resolução do desafio Cloudflare / CSID...")
            for i in range(12):
                await page.wait_for_timeout(1000)
                cur_url = page.url
                if "cf_chl" not in cur_url:
                    break
            
            await page.wait_for_timeout(3000)
            print(f">> URL atual: {page.url}")
            
            body_txt = await page.evaluate("document.body.innerText")
            print(f"\n--- CONTEÚDO DO PORTAL STJ ({len(body_txt)} chars) ---")
            print(body_txt[:4000])
            
            # Verificar se há link ou tab de fases
            fases_btn = page.locator("a:has-text('Fases'), [id*='fases'], [href*='fases']")
            if await fases_btn.count() > 0:
                print(">> Clicando na aba Fases...")
                await fases_btn.first.click()
                await page.wait_for_timeout(4000)
                fases_txt = await page.evaluate("document.body.innerText")
                print("\n--- FASES DO PROCESSO NO STJ ---")
                print(fases_txt[:4000])
                
        except Exception as e:
            print(f"Erro na consulta STJ: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
