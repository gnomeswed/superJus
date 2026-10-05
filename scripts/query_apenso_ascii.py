import sys
import time
import os
import json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

p1 = r"C:\Projetos\superJus\Clientes\Julio_Pereira_Marcos\Caso_Principal\documentos_processo\julio_tjrj_1A_Apenso_RSE_21set.txt"
p2 = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo\julio_tjrj_1A_Apenso_RSE_21set.txt"

print("Iniciando Playwright...", flush=True)
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
    print("Navegando ao portal TJRJ...", flush=True)
    page.goto('https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica', wait_until='commit', timeout=45000)
    
    print("Aguardando input[type='search']...", flush=True)
    inp = page.wait_for_selector("input[type='search']", timeout=30000)
    time.sleep(2)
    inp.click()
    inp.fill('0001140-87.2024.8.19.0078')
    time.sleep(1)

    print("Clicando Pesquisar...", flush=True)
    page.click("button[type='submit']")
    page.wait_for_selector('iframe#mainframe', timeout=30000)
    time.sleep(3)

    frame = page.query_selector('iframe#mainframe').content_frame()
    time.sleep(3)

    try:
        todos = frame.wait_for_selector("a:has-text('Todos')", timeout=8000)
        if todos:
            print("Clicando em Todos Os Movimentos...", flush=True)
            todos.click()
            time.sleep(3)
    except Exception as e:
        print("Aviso Todos:", e, flush=True)

    txt = frame.inner_text('body')
    print(f"Texto capturado: {len(txt)} chars", flush=True)

    for target in [p1, p2]:
        try:
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, 'w', encoding='utf-8') as f:
                f.write(txt)
            print("Salvo em:", target, "Tamanho:", os.path.getsize(target), flush=True)
        except Exception as e:
            print("Erro ao salvar em", target, e, flush=True)

    # Atualizar JSONs
    for jpath in [
        r"C:\Projetos\superJus\Clientes\Julio_Pereira_Marcos\Caso_Principal\consulta_ao_vivo_21_09_2026.json",
        r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\consulta_ao_vivo_21_09_2026.json",
        r"C:\Projetos\swedsystem\docs\consulta_ao_vivo_21_09_2026.json"
    ]:
        if os.path.exists(jpath):
            with open(jpath, 'r', encoding='utf-8') as f:
                d = json.load(f)

            loc_str = 'N/A'
            if 'Localização na Serventia' in txt:
                idx = txt.index('Localização na Serventia')
                loc_str = txt[idx:idx+300].replace('\n', ' | ')

            mov_str = 'N/A'
            if 'Tipo do Movimento:' in txt:
                idx = txt.index('Tipo do Movimento:')
                mov_str = txt[idx:idx+300].replace('\n', ' | ')

            d['portal_tjrj']['0001140-87.2024.8.19.0078'] = {
                'status': 'sucesso',
                'data_hora_consulta': time.strftime('%d/%m/%Y %H:%M:%S'),
                'localizacao': loc_str,
                'ultimo_movimento': mov_str,
                'fpath': p1,
                'raw': txt
            }
            with open(jpath, 'w', encoding='utf-8') as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
            print("JSON atualizado:", jpath, flush=True)

    b.close()
print("FINALIZADO COM SUCESSO!", flush=True)
