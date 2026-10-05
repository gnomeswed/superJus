# -*- coding: utf-8 -*-
import os, sys, time
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

CNJ_2A = "0029845-67.2026.8.19.0000"
OUT_DIR = r"C:\Projetos\superJus\Clientes\Julio_Pereira_Marcos\Caso_Principal\documentos_processo\_varredura_18_08_2026"
os.makedirs(OUT_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
    page = browser.new_page(viewport={"width": 1366, "height": 900})

    print(f"\n==========================================", flush=True)
    print(f"Consultando TJRJ 2ª Instância ({CNJ_2A})", flush=True)
    print(f"==========================================", flush=True)

    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=35000, wait_until="domcontentloaded")
    time.sleep(3)
    iframe = page.wait_for_selector("iframe#mainframe", timeout=20000).content_frame()

    iframe.evaluate(f"""() => {{
        const inp = Array.from(document.querySelectorAll('input')).find(i => i.name==='numeroProcesso' || i.id==='numeroProcesso');
        if(inp){{ inp.value='{CNJ_2A}'; inp.dispatchEvent(new Event('input',{{bubbles:true}})); inp.dispatchEvent(new Event('change',{{bubbles:true}})); }}
    }}""")
    time.sleep(1)
    iframe.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.offsetWidth>0 && (b.textContent||'').toLowerCase().includes('pesquisar'));
        if(btn) btn.click();
    }""")
    time.sleep(6)

    # Captura tabela inicial com todos os links
    table_text = iframe.inner_text("body")
    with open(os.path.join(OUT_DIR, "2A_tabela_inicial.txt"), "w", encoding="utf-8") as f:
        f.write(table_text)

    # Identifica links disponíveis
    links_info = iframe.evaluate("""() => {
        return Array.from(document.querySelectorAll('table a, .table a')).map(a => ({
            text: (a.textContent || '').trim(),
            href: a.href
        })).filter(x => x.text.length > 0);
    }""")
    print(f"Links encontrados na tabela de 2ª instância: {links_info}", flush=True)

    # Para cada link encontrado, clica e extrai o teor
    for idx, item in enumerate(links_info):
        print(f"\n--- Abrindo processo de 2ª inst: {item['text']} ---", flush=True)
        try:
            # Re-pesquisa se necessário
            if idx > 0:
                page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=35000, wait_until="domcontentloaded")
                time.sleep(3)
                iframe = page.wait_for_selector("iframe#mainframe", timeout=20000).content_frame()
                iframe.evaluate(f"""() => {{
                    const inp = Array.from(document.querySelectorAll('input')).find(i => i.name==='numeroProcesso' || i.id==='numeroProcesso');
                    if(inp){{ inp.value='{CNJ_2A}'; inp.dispatchEvent(new Event('input',{{bubbles:true}})); inp.dispatchEvent(new Event('change',{{bubbles:true}})); }}
                }}""")
                time.sleep(1)
                iframe.evaluate("""() => {
                    const btn = Array.from(document.querySelectorAll('button')).find(b => b.offsetWidth>0 && (b.textContent||'').toLowerCase().includes('pesquisar'));
                    if(btn) btn.click();
                }""")
                time.sleep(6)

            # Clica no link específico
            iframe.evaluate(f"""(targetText) => {{
                const links = Array.from(document.querySelectorAll('table a, .table a'));
                const l = links.find(a => (a.textContent||'').trim() === targetText);
                if(l) l.click();
            }}""", item['text'])
            time.sleep(6)

            # Tenta expandir Todos os Movimentos
            iframe.evaluate("""() => {
                const btn = Array.from(document.querySelectorAll('button, a')).find(b => (b.textContent||'').toLowerCase().includes('todos os movimentos'));
                if(btn) btn.click();
            }""")
            time.sleep(4)

            proc_txt = iframe.inner_text("body")
            safe_name = item['text'].replace('/', '_').replace('.', '_').replace(' ', '_')
            with open(os.path.join(OUT_DIR, f"2A_detalhe_{safe_name}.txt"), "w", encoding="utf-8") as f:
                f.write(proc_txt)

            lines = [l.strip() for l in proc_txt.split('\n') if l.strip()]
            print(f"Total de linhas capturadas: {len(lines)}", flush=True)
            for l in lines[:20]:
                print(f"  > {l[:120]}", flush=True)

        except Exception as e:
            print(f"Erro ao processar item {item['text']}: {e}", flush=True)

    browser.close()
