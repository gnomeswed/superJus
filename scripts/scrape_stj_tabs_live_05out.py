# -*- coding: utf-8 -*-
import asyncio, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def consultar_processo(page, num_registro, nome_label):
    print(f"\n=======================================================")
    print(f"🏛️ CONSULTANDO AO VIVO NO STJ: {nome_label} ({num_registro})")
    print(f"=======================================================")
    url = "https://processo.stj.jus.br/processo/pesquisa/?aplicacao=processos.ea"
    await page.goto(url, wait_until="domcontentloaded", timeout=45000)
    await page.wait_for_timeout(2000)

    inp = await page.query_selector("input#num_registro, input[name='parametroNumeroRegistro'], input[name='num_registro']")
    if not inp:
        inp = await page.query_selector("input[type='text']")
        
    await inp.fill(num_registro)
    await page.wait_for_timeout(500)
    btn = await page.query_selector("input#btnPesquisar, button#btnPesquisar, input[type='submit']")
    if btn:
        await btn.click()
    else:
        await inp.press("Enter")
        
    await page.wait_for_timeout(5000)
    
    # 1. Detalhes
    detalhes_txt = await page.evaluate("document.body.innerText")
    with open(f"c:/Projetos/superJus/stj_detalhes_{num_registro}.txt", "w", encoding="utf-8") as f:
        f.write(detalhes_txt)
        
    # 2. Fases
    fases_btn = page.locator("a:has-text('Fases'), [id*='fases'], [href*='fases']")
    fases_txt = ""
    if await fases_btn.count() > 0:
        await fases_btn.first.click()
        await page.wait_for_timeout(3000)
        fases_txt = await page.evaluate("document.body.innerText")
        with open(f"c:/Projetos/superJus/stj_fases_{num_registro}.txt", "w", encoding="utf-8") as f:
            f.write(fases_txt)
            
    # 3. Decisões
    dec_btn = page.locator("a:has-text('Decisões'), [id*='decis'], [href*='decis']")
    dec_txt = ""
    if await dec_btn.count() > 0:
        await dec_btn.first.click()
        await page.wait_for_timeout(3000)
        dec_txt = await page.evaluate("document.body.innerText")
        with open(f"c:/Projetos/superJus/stj_decisoes_{num_registro}.txt", "w", encoding="utf-8") as f:
            f.write(dec_txt)

    # 4. Petições
    pet_btn = page.locator("a:has-text('Petições'), [id*='peti'], [href*='peti']")
    pet_txt = ""
    if await pet_btn.count() > 0:
        await pet_btn.first.click()
        await page.wait_for_timeout(3000)
        pet_txt = await page.evaluate("document.body.innerText")
        with open(f"c:/Projetos/superJus/stj_peticoes_{num_registro}.txt", "w", encoding="utf-8") as f:
            f.write(pet_txt)

    print(f"Salvo com sucesso: Detalhes ({len(detalhes_txt)}c), Fases ({len(fases_txt)}c), Decisões ({len(dec_txt)}c), Petições ({len(pet_txt)}c)")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
        )
        ctx = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            viewport={"width": 1366, "height": 850}
        )
        page = await ctx.new_page()
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # 1. RHC 244132 / RJ
        await consultar_processo(page, "202603180085", "RHC 244132 / RJ")
        # 2. HC 1.116.750 / RJ
        await consultar_processo(page, "202603112107", "HC 1.116.750 / RJ")
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
