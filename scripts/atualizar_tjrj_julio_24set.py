# -*- coding: utf-8 -*-
"""
Atualização Oficial ao Vivo Direto do TJRJ e STJ — Júlio Pereira Marcos (24/09/2026)
Executa via Playwright:
1. Portal TJRJ (1ª Instância - Principal Búzios, Apenso RSE, Originário Co-réus)
2. Portal TJRJ (2ª Instância - HC 7ª Câmara Criminal e ROC 2ª Vice)
3. DJERJ (Varredura de 01/09/2026 a 24/09/2026)
4. Portal STJ (HC 1.116.750 / RJ - Gabinete Min. Og Fernandes)
5. Gera relatórios técnico e amigável + JSON estruturado
"""
import sys
import time
import os
import json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

target_dirs = [
    r"C:\Projetos\superJus\Clientes\Julio_Pereira_Marcos\Caso_Principal\documentos_processo",
    r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo",
    r"C:\Projetos\superJus\Clientes\Julio_Pereira_Marcos\Caso_Principal",
    r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal",
    r"C:\Projetos\superJus"
]

for d in target_dirs:
    os.makedirs(d, exist_ok=True)

PROCS = [
    ("0023013-51.2021.8.19.0078", False, "julio_tjrj_1A_Principal_Julio_24set.txt", "Ação Penal Principal - 2ª Vara de Búzios"),
    ("0001140-87.2024.8.19.0078", False, "julio_tjrj_1A_Apenso_RSE_24set.txt", "Recurso em Sentido Estrito / Apenso - Búzios"),
    ("0022975-39.2021.8.19.0078", False, "julio_tjrj_1A_Original_Desmembrado_24set.txt", "Processo Originário / Co-réus - Búzios"),
    ("0029845-67.2026.8.19.0000", True, "julio_tjrj_2A_HC_24set.txt", "2ª Instância TJRJ (HC e ROC)")
]

results = {
    "data_consulta": "24/09/2026",
    "hora_consulta": time.strftime("%H:%M:%S"),
    "tjrj": {},
    "stj": {},
    "djerj": {}
}

print("==================================================================", flush=True)
print(f"=== INICIANDO CONSULTA ONLINE DIRETO DO TJRJ E STJ (24/09/2026) ===", flush=True)
print("==================================================================", flush=True)

with sync_playwright() as p:
    b = p.chromium.launch(
        headless=True,
        args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
    )
    ctx = b.new_context(
        viewport={"width": 1366, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        locale="pt-BR"
    )
    page = ctx.new_page()

    # 1. PROCESSOS TJRJ
    for proc_num, is_2a, fname, desc in PROCS:
        print(f"\n[+] Consultando TJRJ: {proc_num} ({desc}) | 2ª Instância: {is_2a}", flush=True)
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
                print("    Pesquisar clicado, aguardando resultado/iframe...", flush=True)

                page.wait_for_selector('iframe#mainframe', timeout=30000)
                time.sleep(3)

                frame_el = page.query_selector('iframe#mainframe')
                frame = frame_el.content_frame()
                time.sleep(3)

                # Se 2ª Instância, selecionar o HC 10770
                if is_2a:
                    try:
                        hc_link = frame.query_selector('a:has-text("2026.059.10770"), a:has-text("10770"), table a')
                        if hc_link:
                            print(f"    Clicando no link do HC: {hc_link.inner_text()}", flush=True)
                            hc_link.click()
                            time.sleep(4)
                    except Exception as e:
                        print(f"    Aviso clique 2ª instância: {e}", flush=True)

                # Clicar em "Todos Os Movimentos" para expandir histórico completo
                try:
                    todos_btn = frame.query_selector('a:has-text("Todos Os Movimentos"), a:has-text("Todos")')
                    if todos_btn:
                        todos_btn.click()
                        time.sleep(3)
                except Exception as e:
                    pass

                body_text = frame.inner_text("body")
                print(f"    ✓ Sucesso! Texto capturado: {len(body_text)} caracteres.", flush=True)

                # Salvar arquivos de texto nas pastas de destino
                for d in target_dirs[:2]:
                    try:
                        out_path = os.path.join(d, fname)
                        with open(out_path, "w", encoding="utf-8") as f:
                            f.write(body_text)
                    except Exception as e:
                        print(f"    Erro ao salvar em {d}: {e}", flush=True)

                loc_str = "N/A"
                if "Localização na Serventia" in body_text:
                    idx = body_text.index("Localização na Serventia")
                    loc_str = body_text[idx:idx+250].replace('\n', ' | ')

                mov_str = "N/A"
                if "Tipo do Movimento:" in body_text:
                    idx = body_text.index("Tipo do Movimento:")
                    mov_str = body_text[idx:idx+250].replace('\n', ' | ')

                lines = [l.strip() for l in body_text.split('\n') if l.strip()]
                parsed_movs = []
                for i, l in enumerate(lines):
                    if "Tipo do Movimento:" in l:
                        bloco = lines[i:min(len(lines), i + 8)]
                        parsed_movs.append(" | ".join(bloco))

                print(f"    • Localização: {loc_str[:100]}", flush=True)
                print(f"    • Último Movimento: {mov_str[:120]}", flush=True)

                results["tjrj"][proc_num] = {
                    "status": "sucesso",
                    "descricao": desc,
                    "data_hora_consulta": time.strftime("%d/%m/%Y %H:%M:%S"),
                    "localizacao": loc_str,
                    "ultimo_movimento": mov_str,
                    "ultimos_movimentos": parsed_movs[:6],
                    "total_movimentos": body_text.count("Tipo do Movimento:"),
                    "raw": body_text
                }
                success = True
                break
            except Exception as e:
                print(f"    Tentativa {attempt} falhou ({proc_num}): {e}", flush=True)
                time.sleep(3)

        if not success:
            results["tjrj"][proc_num] = {"status": "erro", "erro": "Falha após 3 tentativas"}

    # 2. STJ - HC 1.116.750 / RJ (Registro 2026/0311210-7)
    print("\n[+] Consultando STJ ao Vivo (HC 1.116.750 / RJ)...", flush=True)
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
        for d in target_dirs[:2]:
            stj_fpath = os.path.join(d, "julio_stj_live_direct_24set.txt")
            with open(stj_fpath, "w", encoding="utf-8") as f:
                f.write(stj_txt)

        relevant_stj = []
        for line in stj_txt.splitlines():
            if any(k in line.upper() for k in ["CONCLUSOS", "GABINETE", "FASE:", "ÚLTIMA FASE", "PARECER", "MINISTRO", "RELATOR"]):
                print(f"    • STJ: {line.strip()}", flush=True)
                relevant_stj.append(line.strip())

        results["stj"] = {
            "status": "sucesso",
            "data_hora_consulta": time.strftime("%d/%m/%Y %H:%M:%S"),
            "relevant_lines": relevant_stj[:10],
            "raw": stj_txt[:4000]
        }
        print("    ✓ STJ capturado com sucesso.", flush=True)
    except Exception as e:
        print(f"    Erro STJ Scraping: {e}", flush=True)
        results["stj"] = {"status": "erro", "erro": str(e)}

    # 3. DJERJ (01/09/2026 a 24/09/2026)
    print("\n[+] Consultando DJERJ (01/09/2026 a 24/09/2026)...", flush=True)
    djerj_queries = ["0023013-51.2021.8.19.0078", "0001140-87.2024.8.19.0078", "0022975-39.2021.8.19.0078", "0029845-67.2026.8.19.0000", "Julio Pereira Marcos"]
    for q in djerj_queries:
        is_name = (q == "Julio Pereira Marcos")
        safe_type = "NOME" if is_name else "PROC"
        safe_param = "Julio%20Pereira%20Marcos" if is_name else q
        url_djerj = f"https://www3.tjrj.jus.br/consultadje/Result.aspx?dtInicio=01%2F09%2F2026&dtFim=24%2F09%2F2026&txtPesq={safe_param}&tipoPesq={safe_type}"
        try:
            page.goto(url_djerj, wait_until="domcontentloaded", timeout=45000)
            time.sleep(4)
            djerj_body = page.evaluate("document.body.innerText")
            if "Não foram encontradas" in djerj_body or "Nenhum registro encontrado" in djerj_body:
                print(f"    • DJERJ [{q}]: Sem publicações no período (01 a 24/09/2026).", flush=True)
                results["djerj"][q] = "Sem publicações no período (01 a 24/09/2026)"
            else:
                print(f"    🚨 DJERJ [{q}]: PUBLICAÇÃO ENCONTRADA!\n{djerj_body[:500]}", flush=True)
                results["djerj"][q] = djerj_body[:2000]
        except Exception as e:
            print(f"    Erro DJERJ {q}: {e}", flush=True)
            results["djerj"][q] = f"Erro: {e}"

    b.close()

# Salvar snapshot JSON completo
snapshot_path = r"C:\Projetos\superJus\consulta_ao_vivo_24_09_2026.json"
with open(snapshot_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"\n[✓] Snapshot JSON salvo em: {snapshot_path}", flush=True)

for d in target_dirs[:2]:
    with open(os.path.join(d, "consulta_ao_vivo_24_09_2026.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

print("\n=== CONSULTA FINALIZADA COM SUCESSO! ===", flush=True)
