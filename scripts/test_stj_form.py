# -*- coding: utf-8 -*-
import asyncio, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def buscar_no_stj(page, num_registro, nome_label):
    print(f"\n=======================================================")
    print(f"🏛️ BUSCA INTERATIVA STJ: {nome_label} ({num_registro})")
    print(f"=======================================================")
    url = "https://processo.stj.jus.br/processo/pesquisa/?aplicacao=processos.ea"
    await page.goto(url, wait_until="domcontentloaded", timeout=45000)
    await page.wait_for_timeout(4000)

    inp = await page.query_selector("input#num_registro, input[name='parametroNumeroRegistro'], input[name='num_registro']")
    if not inp:
        inp = await page.query_selector("input[type='text']")
        
    if not inp:
        print(f"ERRO: Campo de texto de busca não encontrado para {num_registro}")
        return

    await inp.fill(num_registro)
    await page.wait_for_timeout(800)
    btn = await page.query_selector("input#btnPesquisar, button#btnPesquisar, input[type='submit']")
    if btn:
        await btn.click()
    else:
        await inp.press("Enter")
        
    print("Aguardando carregamento da página de detalhes...")
    await page.wait_for_timeout(6000)

    body_txt = await page.evaluate("document.body.innerText")
    lines = [l.strip() for l in body_txt.splitlines() if l.strip()]
    print(f">> Total de linhas capturadas: {len(lines)}")
    for l in lines[20:45]:
        print(f"   • {l}")
        
    with open(f"c:/Projetos/superJus/stj_detalhes_{num_registro}.txt", "w", encoding="utf-8") as f:
        f.write(body_txt)
        
    # Clicar na aba Fases
    fases_btn = page.locator("a:has-text('Fases'), [id*='fases'], [href*='fases']")
    if await fases_btn.count() > 0:
        print("\n>> Clicando na aba FASES...")
        await fases_btn.first.click()
        await page.wait_for_timeout(3500)
        fases_txt = await page.evaluate("document.body.innerText")
        fases_lines = [l.strip() for l in fases_txt.splitlines() if l.strip()]
        print(">> ÚLTIMAS FASES REGISTRADAS:")
        for l in fases_lines[20:50]:
            print(f"     {l}")
        with open(f"c:/Projetos/superJus/stj_fases_{num_registro}.txt", "w", encoding="utf-8") as f:
            f.write(fases_txt)

    # Clicar na aba Decisões
    dec_btn = page.locator("a:has-text('Decisões'), [id*='decis'], [href*='decis']")
    if await dec_btn.count() > 0:
        print("\n>> Clicando na aba DECISÕES...")
        await dec_btn.first.click()
        await page.wait_for_timeout(3500)
        dec_txt = await page.evaluate("document.body.innerText")
        dec_lines = [l.strip() for l in dec_txt.splitlines() if l.strip()]
        print(">> DECISÕES REGISTRADAS:")
        for l in dec_lines[20:50]:
            print(f"     {l}")
        with open(f"c:/Projetos/superJus/stj_decisoes_{num_registro}.txt", "w", encoding="utf-8") as f:
            f.write(dec_txt)

    # Clicar na aba Petições
    pet_btn = page.locator("a:has-text('Petições'), [id*='peti'], [href*='peti']")
    if await pet_btn.count() > 0:
        print("\n>> Clicando na aba PETIÇÕES...")
        await pet_btn.first.click()
        await page.wait_for_timeout(3500)
        pet_txt = await page.evaluate("document.body.innerText")
        pet_lines = [l.strip() for l in pet_txt.splitlines() if l.strip()]
        print(">> PETIÇÕES REGISTRADAS:")
        for l in pet_lines[20:50]:
            print(f"     {l}")
        with open(f"c:/Projetos/superJus/stj_peticoes_{num_registro}.txt", "w", encoding="utf-8") as f:
            f.write(pet_txt)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
        )
        ctx = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            viewport={"width": 1366, "height": 850}
        )
        page = await ctx.new_page()
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        # 1. HC 1.116.750 / RJ (Processo principal no STJ onde está a Manifestação de 28/09)
        await buscar_no_stj(page, "202603112107", "HC 1.116.750 / RJ")
        
        # 2. RHC 244.132 / RJ (Recurso originário onde saiu a monocrática)
        await buscar_no_stj(page, "202603180085", "RHC 244.132 / RJ")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
