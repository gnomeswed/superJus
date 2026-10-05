# -*- coding: utf-8 -*-
"""
Consulta e Atualização Oficial ao Vivo Direto do TJRJ — Júlio Pereira Marcos (25/09/2026)
Executa via Playwright:
1. TJRJ 1ª Instância:
   - 0023013-51.2021.8.19.0078 (Ação Penal Principal Desmembrada - 2ª Vara de Búzios)
   - 0001140-87.2024.8.19.0078 (Recurso em Sentido Estrito / Apenso Búzios)
   - 0022975-39.2021.8.19.0078 (Processo Originário / Co-réus Búzios)
2. TJRJ 2ª Instância:
   - 0029845-67.2026.8.19.0000 (HC 2026.059.10770 e ROC 2026.141.00580 - 7ª Câmara Criminal / 2ª VP)
3. DJERJ (Diário da Justiça RJ):
   - Pesquisa de 01/09/2026 a 25/09/2026 para todos os processos e nome Júlio Pereira Marcos
4. Salva snapshots e arquivos TXT/JSON em todas as pastas oficiais do caso.
"""
import sys
import os
import time
import json
import re
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TARGET_DIRS = [
    r"C:\Projetos\superJus\Clientes\Julio_Pereira_Marcos\Caso_Principal\documentos_processo",
    r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo",
    r"C:\Projetos\superJus",
    r"C:\Projetos\swedsystem\docs"
]

for d in TARGET_DIRS:
    os.makedirs(d, exist_ok=True)

PROCS_1A = [
    ("0023013-51.2021.8.19.0078", "julio_tjrj_1A_Principal_Julio_25set.txt", "Ação Penal Principal Desmembrada - 2ª Vara de Búzios"),
    ("0001140-87.2024.8.19.0078", "julio_tjrj_1A_Apenso_RSE_25set.txt", "Recurso em Sentido Estrito / Apenso Búzios"),
    ("0022975-39.2021.8.19.0078", "julio_tjrj_1A_Original_Desmembrado_25set.txt", "Processo Originário / Co-réus Búzios")
]

PROC_2A = ("0029845-67.2026.8.19.0000", "julio_tjrj_2A_HC_25set.txt", "2ª Instância TJRJ (HC e ROC - 7ª Câmara Criminal)")

results = {
    "data_consulta": "25/09/2026",
    "hora_consulta": time.strftime("%H:%M:%S"),
    "tjrj": {},
    "djerj": {}
}

print("="*80, flush=True)
print("=== ATUALIZAÇÃO AO VIVO DIRETO DO TJRJ — JÚLIO PEREIRA MARCOS (25/09/2026) ===", flush=True)
print("="*80, flush=True)

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--disable-blink-features=AutomationControlled", "--no-sandbox", "--disable-dev-shm-usage"]
    )
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        viewport={"width": 1366, "height": 900},
        locale="pt-BR"
    )
    page = ctx.new_page()

    # 1. PROCESSOS DE 1ª INSTÂNCIA
    for cnj, fname, desc in PROCS_1A:
        print(f"\n[+] Consultando 1ª Instância: {cnj} ({desc})...", flush=True)
        success = False
        for attempt in range(1, 4):
            try:
                page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000, wait_until="domcontentloaded")
                time.sleep(3)
                iframe_el = page.wait_for_selector("iframe#mainframe", timeout=30000)
                frame = iframe_el.content_frame()
                time.sleep(2)

                frame.evaluate(f"""() => {{
                    const inp = Array.from(document.querySelectorAll('input')).find(i => i.name==='numeroProcesso' || i.id==='numeroProcesso');
                    if(inp) {{
                        inp.value = '{cnj}';
                        inp.dispatchEvent(new Event('input', {{bubbles:true}}));
                        inp.dispatchEvent(new Event('change', {{bubbles:true}}));
                    }}
                }}""")
                time.sleep(1)

                frame.evaluate("""() => {
                    const btn = Array.from(document.querySelectorAll('button')).find(b => b.offsetWidth>0 && (b.textContent||'').toLowerCase().includes('pesquisar'));
                    if(btn) btn.click();
                }""")
                time.sleep(8)

                # Tentar expandir todos os movimentos
                try:
                    frame.evaluate("""() => {
                        const links = Array.from(document.querySelectorAll('a, button'));
                        const btnAll = links.find(el => (el.textContent||'').toLowerCase().includes('todos os movimentos'));
                        if(btnAll) btnAll.click();
                    }""")
                    time.sleep(4)
                except Exception:
                    pass

                body_text = frame.inner_text("body")
                if len(body_text.strip()) > 100:
                    print(f"    ✓ Sucesso! Dados capturados ({len(body_text)} caracteres).", flush=True)
                    
                    # Extrair localização e movimentos
                    lines = [l.strip() for l in body_text.split('\n') if l.strip()]
                    loc = "N/A"
                    for idx, l in enumerate(lines):
                        if "Localização na Serventia" in l and idx+1 < len(lines):
                            loc = lines[idx+1]
                            break

                    parsed_movs = []
                    for idx, l in enumerate(lines):
                        if "Tipo do Movimento:" in l:
                            chunk = lines[idx:min(len(lines), idx+8)]
                            parsed_movs.append(" | ".join(chunk))

                    print(f"    • Localização: {loc}", flush=True)
                    print(f"    • Total Movimentos Encontrados: {len(parsed_movs)}", flush=True)
                    if parsed_movs:
                        print(f"    • Último Movimento: {parsed_movs[0][:150]}", flush=True)

                    # Salvar nas pastas
                    for d in TARGET_DIRS:
                        out_p = os.path.join(d, fname)
                        with open(out_p, "w", encoding="utf-8") as f:
                            f.write(body_text)

                    results["tjrj"][cnj] = {
                        "status": "sucesso",
                        "descricao": desc,
                        "localizacao": loc,
                        "total_movimentos": len(parsed_movs),
                        "ultimos_movimentos": parsed_movs[:6],
                        "raw": body_text[:3000]
                    }
                    success = True
                    break
            except Exception as e:
                print(f"    Tentativa {attempt} falhou ({cnj}): {e}", flush=True)
                time.sleep(3)

        if not success:
            results["tjrj"][cnj] = {"status": "erro", "erro": "Falha após 3 tentativas"}

    # 2. PROCESSO DE 2ª INSTÂNCIA
    cnj_2a, fname_2a, desc_2a = PROC_2A
    print(f"\n[+] Consultando 2ª Instância: {cnj_2a} ({desc_2a})...", flush=True)
    success_2a = False
    for attempt in range(1, 4):
        try:
            page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000, wait_until="domcontentloaded")
            time.sleep(3)
            iframe_el = page.wait_for_selector("iframe#mainframe", timeout=30000)
            frame = iframe_el.content_frame()
            time.sleep(2)

            frame.evaluate(f"""() => {{
                const inp = Array.from(document.querySelectorAll('input')).find(i => i.name==='numeroProcesso' || i.id==='numeroProcesso');
                if(inp) {{
                    inp.value = '{cnj_2a}';
                    inp.dispatchEvent(new Event('input', {{bubbles:true}}));
                    inp.dispatchEvent(new Event('change', {{bubbles:true}}));
                }}
            }}""")
            time.sleep(1)

            frame.evaluate("""() => {
                const btn = Array.from(document.querySelectorAll('button')).find(b => b.offsetWidth>0 && (b.textContent||'').toLowerCase().includes('pesquisar'));
                if(btn) btn.click();
            }""")
            time.sleep(8)

            # Clicar no link de 2ª instância do HC se houver tabela
            try:
                frame.evaluate("""() => {
                    const links = Array.from(document.querySelectorAll('table a, .table a, a'));
                    const l = links.find(a => (a.textContent||'').includes('2026.059.10770') || (a.textContent||'').includes('10770'));
                    if(l) l.click();
                }""")
                time.sleep(6)
            except Exception:
                pass

            # Expandir movimentos
            try:
                frame.evaluate("""() => {
                    const links = Array.from(document.querySelectorAll('a, button'));
                    const btnAll = links.find(el => (el.textContent||'').toLowerCase().includes('todos os movimentos'));
                    if(btnAll) btnAll.click();
                }""")
                time.sleep(4)
            except Exception:
                pass

            body_2a = frame.inner_text("body")
            if len(body_2a.strip()) > 100:
                print(f"    ✓ Sucesso 2ª Instância! Dados capturados ({len(body_2a)} caracteres).", flush=True)
                lines_2a = [l.strip() for l in body_2a.split('\n') if l.strip()]
                loc_2a = "N/A"
                for idx, l in enumerate(lines_2a):
                    if "Localização na Serventia" in l and idx+1 < len(lines_2a):
                        loc_2a = lines_2a[idx+1]
                        break

                parsed_movs_2a = []
                for idx, l in enumerate(lines_2a):
                    if "Tipo do Movimento:" in l:
                        chunk = lines_2a[idx:min(len(lines_2a), idx+8)]
                        parsed_movs_2a.append(" | ".join(chunk))

                print(f"    • Localização 2ª Instância: {loc_2a}", flush=True)
                print(f"    • Total Movimentos: {len(parsed_movs_2a)}", flush=True)
                if parsed_movs_2a:
                    print(f"    • Último Movimento: {parsed_movs_2a[0][:150]}", flush=True)

                for d in TARGET_DIRS:
                    out_p = os.path.join(d, fname_2a)
                    with open(out_p, "w", encoding="utf-8") as f:
                        f.write(body_2a)

                results["tjrj"][cnj_2a] = {
                    "status": "sucesso",
                    "descricao": desc_2a,
                    "localizacao": loc_2a,
                    "total_movimentos": len(parsed_movs_2a),
                    "ultimos_movimentos": parsed_movs_2a[:6],
                    "raw": body_2a[:3000]
                }
                success_2a = True
                break
        except Exception as e:
            print(f"    Tentativa {attempt} falhou ({cnj_2a}): {e}", flush=True)
            time.sleep(3)

    if not success_2a:
        results["tjrj"][cnj_2a] = {"status": "erro", "erro": "Falha após 3 tentativas"}

    # 3. DIÁRIO DA JUSTIÇA (DJERJ) - VARREDURA SETEMBRO 2026
    print("\n[+] Consultando Diário da Justiça (DJERJ) de 01/09/2026 a 25/09/2026...", flush=True)
    djerj_queries = [
        "0023013-51.2021.8.19.0078",
        "0001140-87.2024.8.19.0078",
        "0022975-39.2021.8.19.0078",
        "0029845-67.2026.8.19.0000",
        "Julio Pereira Marcos"
    ]
    for q in djerj_queries:
        is_name = (q == "Julio Pereira Marcos")
        safe_type = "NOME" if is_name else "PROC"
        safe_param = "Julio%20Pereira%20Marcos" if is_name else q
        url_djerj = f"https://www3.tjrj.jus.br/consultadje/Result.aspx?dtInicio=01%2F09%2F2026&dtFim=25%2F09%2F2026&txtPesq={safe_param}&tipoPesq={safe_type}"
        try:
            page.goto(url_djerj, wait_until="domcontentloaded", timeout=40000)
            time.sleep(4)
            djerj_body = page.evaluate("document.body.innerText")
            if "Não foram encontradas" in djerj_body or "Nenhum registro encontrado" in djerj_body or "0 registros" in djerj_body.lower():
                print(f"    • DJERJ [{q}]: ✅ Sem publicações no período (01 a 25/09/2026).", flush=True)
                results["djerj"][q] = "Sem publicações no período (01 a 25/09/2026)"
            else:
                print(f"    🚨 DJERJ [{q}]: PUBLICAÇÃO ENCONTRADA!\n{djerj_body[:500]}", flush=True)
                results["djerj"][q] = djerj_body[:2000]
        except Exception as e:
            print(f"    Erro DJERJ {q}: {e}", flush=True)
            results["djerj"][q] = f"Erro: {e}"

    browser.close()

# Salvar snapshot JSON atualizado
json_out_path = r"C:\Projetos\superJus\consulta_ao_vivo_25_09_2026.json"
with open(json_out_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"\n[✓] Snapshot JSON salvo com sucesso em: {json_out_path}", flush=True)

for d in TARGET_DIRS:
    try:
        with open(os.path.join(d, "consulta_ao_vivo_25_09_2026.json"), "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

print("\n=== ATUALIZAÇÃO CONCLUÍDA COM SUCESSO! ===", flush=True)
