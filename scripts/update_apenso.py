import time
import os
import json
from playwright.sync_api import sync_playwright

OUT_DIR = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"

with sync_playwright() as p:
    b = p.chromium.launch(
        headless=True,
        args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
    )
    ctx = b.new_context(
        viewport={"width": 1366, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        locale="pt-BR"
    )
    page = ctx.new_page()
    page.goto('https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica', wait_until='domcontentloaded', timeout=40000)
    time.sleep(3)

    page.click("label[for='radioOrigem1']")
    time.sleep(1)

    inp = page.wait_for_selector("input[placeholder*='número do processo']", timeout=15000)
    inp.click()
    inp.type('0001140-87.2024.8.19.0078', delay=40)
    time.sleep(1)

    page.click("button:has-text('Pesquisar')")
    page.wait_for_selector('iframe#mainframe', timeout=30000)
    time.sleep(3)

    frame = page.query_selector('iframe#mainframe').content_frame()
    time.sleep(3)

    todos = frame.query_selector("a:has-text('Todos Os Movimentos'), a:has-text('Todos')")
    if todos:
        todos.click()
        time.sleep(3)

    txt = frame.inner_text('body')
    fpath = os.path.join(OUT_DIR, 'julio_tjrj_1A_Apenso_RSE_21set.txt')
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(txt)
    print('Salvo Apenso RSE:', len(txt), 'chars')

    for json_path in [
        r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\consulta_ao_vivo_21_09_2026.json",
        r"C:\Projetos\swedsystem\docs\consulta_ao_vivo_21_09_2026.json"
    ]:
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            loc_str = 'N/A'
            if 'Localização na Serventia' in txt:
                idx = txt.index('Localização na Serventia')
                loc_str = txt[idx:idx+300].replace('\n', ' | ')

            mov_str = 'N/A'
            if 'Tipo do Movimento:' in txt:
                idx = txt.index('Tipo do Movimento:')
                mov_str = txt[idx:idx+300].replace('\n', ' | ')

            data['portal_tjrj']['0001140-87.2024.8.19.0078'] = {
                'status': 'sucesso',
                'data_hora_consulta': time.strftime('%d/%m/%Y %H:%M:%S'),
                'localizacao': loc_str,
                'ultimo_movimento': mov_str,
                'fpath': fpath,
                'raw': txt
            }
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print('JSON atualizado:', json_path)

    b.close()
