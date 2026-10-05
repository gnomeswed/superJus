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
    ("0023013-51.2021.8.19.0078", False, "julio_tjrj_1A_Principal_Julio_22set.txt"),
    ("0001140-87.2024.8.19.0078", False, "julio_tjrj_1A_Apenso_RSE_22set.txt"),
    ("0022975-39.2021.8.19.0078", False, "julio_tjrj_1A_Original_Desmembrado_22set.txt"),
    ("0029845-67.2026.8.19.0000", True, "julio_tjrj_2A_HC_22set.txt")
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

                # Extrair os primeiros 5 movimentos
                lines = [l.strip() for l in body_text.split('\n') if l.strip()]
                parsed_movs = []
                for i, l in enumerate(lines):
                    if "Tipo do Movimento:" in l:
                        bloco = lines[i:min(len(lines), i + 8)]
                        parsed_movs.append(" | ".join(bloco))

                print(f"  • Localização: {loc_str[:120]}")
                print(f"  • Último Movimento: {mov_str[:120]}")

                results[proc_num] = {
                    "status": "sucesso",
                    "data_hora_consulta": time.strftime("%d/%m/%Y %H:%M:%S"),
                    "localizacao": loc_str,
                    "ultimo_movimento": mov_str,
                    "ultimos_movimentos": parsed_movs[:6],
                    "total_movimentos": body_text.count("Tipo do Movimento:"),
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

    # STJ Consulta Direta
    print("\n==========================================")
    print("Portal STJ (HC 1.116.750 / RJ)")
    print("==========================================")
    URL_STJ_RE = "https://processo.stj.jus.br/processo/pesquisa/?tipoPesquisa=tipoPesquisaNumeroRegistro&termo=202603112107"
    try:
        page.goto(URL_STJ_RE, wait_until="domcontentloaded", timeout=45000)
        time.sleep(5)

        page.evaluate("""() => {
            const links = Array.from(document.querySelectorAll('a'));
            const l = links.find(a => (a.textContent||'').includes('1116750') || (a.textContent||'').includes('2026/0311210-7') || (a.href||'').includes('num_registro=202603112107'));
            if(l) l.click();
        }""")
        time.sleep(6)

        stj_txt = page.evaluate("document.body.innerText")
        for d in target_dirs:
            try:
                stj_fpath = os.path.join(d, "julio_stj_live_direct_22set.txt")
                with open(stj_fpath, "w", encoding="utf-8") as f:
                    f.write(stj_txt)
                print(f"STJ Capturado ({len(stj_txt)} chars). Salvo em {stj_fpath}")
            except Exception as e:
                print(f"Erro STJ save {d}: {e}")

        relevant_stj = []
        for line in stj_txt.splitlines():
            if any(k in line.upper() for k in ["CONCLUSOS", "GABINETE", "FASE:", "ÚLTIMA FASE", "PARECER", "MINISTRO", "RELATOR"]):
                print(f"  • STJ Linha Relevante: {line.strip()}")
                relevant_stj.append(line.strip())

        results["STJ_HC_1116750"] = {
            "status": "sucesso",
            "data_hora_consulta": time.strftime("%d/%m/%Y %H:%M:%S"),
            "relevant_lines": relevant_stj[:10],
            "raw": stj_txt[:3000]
        }
    except Exception as e:
        print(f"Erro STJ Scraping: {e}")
        results["STJ_HC_1116750"] = {"status": "erro", "erro": str(e)}

    # DJERJ Consulta
    print("\n==========================================")
    print("DJERJ Consulta (01/09/2026 a 22/09/2026)")
    print("==========================================")
    djerj_results = {}
    for proc_num, _, _ in PROCS:
        url_djerj = f"https://www3.tjrj.jus.br/consultadje/Result.aspx?dtInicio=01%2F09%2F2026&dtFim=22%2F09%2F2026&txtPesq={proc_num}&tipoPesq=PROC"
        try:
            page.goto(url_djerj, wait_until="domcontentloaded", timeout=45000)
            time.sleep(4)
            djerj_body = page.evaluate("document.body.innerText")
            if "Não foram encontradas" in djerj_body or "Nenhum registro encontrado" in djerj_body:
                print(f"  • {proc_num}: Sem novas publicações no DJERJ.")
                djerj_results[proc_num] = "Sem publicações no período (01 a 22/09/2026)"
            else:
                print(f"  🚨 {proc_num}: PUBLICAÇÃO LOCALIZADA!\n{djerj_body[:1000]}")
                djerj_results[proc_num] = djerj_body[:2000]
        except Exception as e:
            print(f"Erro DJERJ {proc_num}: {e}")
            djerj_results[proc_num] = f"Erro: {e}"

    # DJERJ por nome
    try:
        url_nome = "https://www3.tjrj.jus.br/consultadje/Result.aspx?dtInicio=01%2F09%2F2026&dtFim=22%2F09%2F2026&txtPesq=Julio%20Pereira%20Marcos&tipoPesq=NOME"
        page.goto(url_nome, wait_until="domcontentloaded", timeout=45000)
        time.sleep(4)
        djerj_nome = page.evaluate("document.body.innerText")
        if "Não foram encontradas" in djerj_nome or "Nenhum registro encontrado" in djerj_nome:
            print("  • Julio Pereira Marcos: Sem publicações no DJERJ.")
            djerj_results["Julio Pereira Marcos"] = "Sem publicações no período (01 a 22/09/2026)"
        else:
            print(f"  🚨 Julio Pereira Marcos: PUBLICAÇÃO LOCALIZADA!\n{djerj_nome[:1000]}")
            djerj_results["Julio Pereira Marcos"] = djerj_nome[:2000]
    except Exception as e:
        print(f"Erro DJERJ Nome: {e}")
        djerj_results["Julio Pereira Marcos"] = f"Erro: {e}"

    results["djerj"] = djerj_results

    b.close()

# Salvar JSONs
json_data = {
    "data_consulta": "22/09/2026",
    "hora_consulta": time.strftime("%H:%M:%S"),
    "portal_tjrj": results
}

for json_path in [
    r"C:\Projetos\superJus\Clientes\Julio_Pereira_Marcos\Caso_Principal\consulta_ao_vivo_22_09_2026.json",
    r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\consulta_ao_vivo_22_09_2026.json",
    r"C:\Projetos\swedsystem\docs\consulta_ao_vivo_22_09_2026.json"
]:
    try:
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print("JSON salvo com sucesso:", json_path)
    except Exception as e:
        print("Erro ao salvar JSON:", json_path, e)

print("\n==========================================")
print("TODAS AS CONSULTAS TJRJ E STJ 22/09/2026 FINALIZADAS COM SUCESSO!")
print("==========================================")
