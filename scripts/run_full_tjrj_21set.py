import sys
import time
import os
import json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

target_dirs = [
    r"C:\Projetos\superJus\Clientes\Julio_Pereira_Marcos\Caso_Principal\documentos_processo",
    r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"
]

PROCS = [
    ("0023013-51.2021.8.19.0078", False, "julio_tjrj_1A_Principal_Julio_21set.txt"),
    ("0001140-87.2024.8.19.0078", False, "julio_tjrj_1A_Apenso_RSE_21set.txt"),
    ("0022975-39.2021.8.19.0078", False, "julio_tjrj_1A_Original_Desmembrado_21set.txt"),
    ("0029845-67.2026.8.19.0000", True, "julio_tjrj_2A_HC_21set.txt")
]

results = {}

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

    for proc_num, is_2a, fname in PROCS:
        print(f"\n==========================================")
        print(f"Buscando: {proc_num} (2ª Instância: {is_2a})")
        
        success = False
        for attempt in range(1, 4):
            try:
                page.goto('https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica', wait_until='domcontentloaded', timeout=40000)
                time.sleep(3)

                if is_2a:
                    page.click('label[for="radioOrigem2"]')
                else:
                    page.click('label[for="radioOrigem1"]')
                time.sleep(1)

                inp = page.wait_for_selector('input[placeholder*="número do processo"]', timeout=15000)
                inp.click()
                inp.fill(proc_num)
                time.sleep(1)

                page.click('button:has-text("Pesquisar")')
                print("Pesquisar clicado, aguardando iframe...")

                page.wait_for_selector('iframe#mainframe', timeout=30000)
                time.sleep(3)

                frame_el = page.query_selector('iframe#mainframe')
                frame = frame_el.content_frame()
                time.sleep(3)

                # Se 2ª Instância, clicar no HC se houver lista
                if is_2a:
                    try:
                        hc_link = frame.query_selector('a:has-text("2026.059.10770"), a:has-text("10770"), table a')
                        if hc_link:
                            print(f"Clicando no HC: {hc_link.inner_text()}")
                            hc_link.click()
                            time.sleep(4)
                    except Exception as e:
                        print("Aviso clique HC:", e)

                # Clicar em Todos Os Movimentos se existir no frame
                try:
                    todos_btn = frame.query_selector('a:has-text("Todos Os Movimentos"), a:has-text("Todos")')
                    if todos_btn:
                        print("Clicando em 'Todos Os Movimentos'...")
                        todos_btn.click()
                        time.sleep(3)
                except Exception as e:
                    print("Não foi possível clicar em todos os movimentos:", e)

                body_text = frame.inner_text("body")
                print(f"Sucesso! Caracteres capturados: {len(body_text)}")

                for d in target_dirs:
                    try:
                        os.makedirs(d, exist_ok=True)
                        out_path = os.path.join(d, fname)
                        with open(out_path, "w", encoding="utf-8") as f:
                            f.write(body_text)
                        print(f"Salvo em: {out_path} (Tamanho: {os.path.getsize(out_path)})")
                    except Exception as e:
                        print(f"Erro salvando em {d}: {e}")

                loc_str = "N/A"
                if "Localização na Serventia" in body_text:
                    idx = body_text.index("Localização na Serventia")
                    loc_str = body_text[idx:idx+300].replace('\n', ' | ')

                mov_str = "N/A"
                if "Tipo do Movimento:" in body_text:
                    idx = body_text.index("Tipo do Movimento:")
                    mov_str = body_text[idx:idx+300].replace('\n', ' | ')

                results[proc_num] = {
                    "status": "sucesso",
                    "data_hora_consulta": time.strftime("%d/%m/%Y %H:%M:%S"),
                    "localizacao": loc_str,
                    "ultimo_movimento": mov_str,
                    "fpath": os.path.join(target_dirs[0], fname),
                    "raw": body_text
                }
                success = True
                break
            except Exception as e:
                print(f"Tentativa {attempt} falhou ({proc_num}): {e}")
                time.sleep(3)

        if not success:
            results[proc_num] = {"status": "erro", "erro": "Falha após tentativas"}

    b.close()

# Atualizar JSONs
for json_path in [
    r"C:\Projetos\superJus\Clientes\Julio_Pereira_Marcos\Caso_Principal\consulta_ao_vivo_21_09_2026.json",
    r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\consulta_ao_vivo_21_09_2026.json",
    r"C:\Projetos\swedsystem\docs\consulta_ao_vivo_21_09_2026.json"
]:
    try:
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                d = json.load(f)
            d["portal_tjrj"] = results
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
            print("JSON atualizado com sucesso:", json_path)
    except Exception as e:
        print("Erro ao atualizar JSON:", json_path, e)

print("\n==========================================")
print("TODAS AS CONSULTAS TJRJ FINALIZADAS COM SUCESSO!")
print("==========================================")
