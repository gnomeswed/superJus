import time
import os
from playwright.sync_api import sync_playwright

OUT_DIR = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"
os.makedirs(OUT_DIR, exist_ok=True)

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

    def search_tjrj(proc_number, is_second_instance=False, save_name="test.txt"):
        print(f"\n==========================================")
        print(f"Buscando: {proc_number} (2ª Instância: {is_second_instance})")
        page.goto('https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica', wait_until='domcontentloaded', timeout=40000)
        time.sleep(3)

        if is_second_instance:
            # Click radio for 2a instancia
            page.click('label[for="radioOrigem2"]')
            time.sleep(1)
        else:
            page.click('label[for="radioOrigem1"]')
            time.sleep(1)

        inp = page.wait_for_selector('input[placeholder*="número do processo"]', timeout=15000)
        inp.fill(proc_number)
        time.sleep(1)

        page.click('button:has-text("Pesquisar")')
        print("Pesquisar clicado, aguardando iframe...")

        # Aguarda o iframe surgir
        page.wait_for_selector('iframe#mainframe', timeout=30000)
        time.sleep(3)

        frame = page.frame(name="") # or query_selector
        frame_el = page.query_selector('iframe#mainframe')
        frame = frame_el.content_frame()
        time.sleep(3)

        # Clica em Todos Os Movimentos se existir no frame
        try:
            todos_btn = frame.query_selector('a:has-text("Todos Os Movimentos"), a:has-text("Todos")')
            if todos_btn:
                print("Clicando em 'Todos Os Movimentos'...")
                todos_btn.click()
                time.sleep(3)
        except Exception as e:
            print("Não foi possível clicar em todos os movimentos:", e)

        # Se for 2ª instância, pode listar uma tabela de processos. Se houver link do HC, clica nele!
        if is_second_instance:
            try:
                hc_link = frame.query_selector('a:has-text("2026.059.10770"), a:has-text("10770"), table a')
                if hc_link:
                    print(f"Clicando no link do HC: {hc_link.inner_text()}")
                    hc_link.click()
                    time.sleep(4)
            except Exception as e:
                print("Aviso 2ª instância link:", e)

        body_text = frame.inner_text("body")
        print(f"Sucesso! Caracteres: {len(body_text)}")
        out_path = os.path.join(OUT_DIR, save_name)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(body_text)
        print(f"Salvo em: {out_path}")
        print("Primeiros 300 chars:", body_text[:300].replace('\n', ' '))
        return body_text

    # Test 1: Principal
    search_tjrj("0023013-51.2021.8.19.0078", False, "test_principal_21set.txt")
    # Test 2: 2a Instancia
    search_tjrj("0029845-67.2026.8.19.0000", True, "test_2instancia_21set.txt")

    b.close()
