import asyncio
import urllib.parse
from patchright.async_api import async_playwright

async def check_stf_case(proc):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        await context.grant_permissions(['clipboard-read'])
        page = await context.new_page()
        
        url = 'https://jurisprudencia.stf.jus.br/pages/search?' + urllib.parse.urlencode({
            'base': 'acordaos',
            'pesquisa_inteiro_teor': 'false',
            'sinonimo': 'true',
            'plural': 'true',
            'radicais': 'false',
            'buscaExata': 'false',
            'page': '1',
            'pageSize': '5',
            'queryString': proc,
        })
        await page.goto(url, wait_until='networkidle', timeout=30000)
        locs = await page.locator('div[id^=result-index-]').all()
        print(f"=== STF Busca '{proc}': {len(locs)} resultados ===")
        for i, loc in enumerate(locs[:2]):
            btn = loc.locator('app-clipboard').first
            if await btn.count() > 0:
                await btn.click()
                handle = await page.evaluate_handle('() => navigator.clipboard.readText()')
                summary = await handle.json_value()
                print(f"--- [Resultado #{i+1}] ---")
                print(summary[:400] + "...")
        await browser.close()

asyncio.run(check_stf_case('233.825'))
