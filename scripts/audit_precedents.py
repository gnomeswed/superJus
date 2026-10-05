import asyncio
import urllib.parse
import json
from patchright.async_api import async_playwright

async def check_stf(q):
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
            'queryString': q,
        })
        
        await page.goto(url, wait_until='networkidle', timeout=30000)
        locs = await page.locator('div[id^=result-index-]').all()
        print(f"\n==========================================")
        print(f"STF Busca: '{q}' -> {len(locs)} resultados")
        print(f"==========================================")
        
        for i, loc in enumerate(locs[:3]):
            btn = loc.locator('app-clipboard').first
            if await btn.count() > 0:
                await btn.click()
                handle = await page.evaluate_handle('() => navigator.clipboard.readText()')
                summary = await handle.json_value()
                print(f"\n[Resultado #{i+1}]:")
                print(summary[:500] + "...\n")
        await browser.close()

async def main():
    queries = [
        "129170",
        "187672",
        "101442",
        "114208"
    ]
    for q in queries:
        try:
            await check_stf(q)
        except Exception as e:
            print(f"Erro em {q}: {e}")

if __name__ == "__main__":
    asyncio.run(main())
