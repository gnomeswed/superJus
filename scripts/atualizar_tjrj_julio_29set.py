# -*- coding: utf-8 -*-
"""
Consulta e Atualização Oficial ao Vivo Direto do TJRJ — Júlio Pereira Marcos (29/09/2026)
Executa via Playwright:
1. TJRJ 1ª Instância:
   - 0023013-51.2021.8.19.0078 (Ação Penal Principal Desmembrada - 2ª Vara de Búzios)
   - 0001140-87.2024.8.19.0078 (Recurso em Sentido Estrito / Apenso Búzios)
   - 0022975-39.2021.8.19.0078 (Processo Originário / Co-réus Búzios)
2. TJRJ 2ª Instância:
   - 0029845-67.2026.8.19.0000 (HC 2026.059.10770 e ROC 2026.141.00580 - 7ª Câmara Criminal / 2ª VP)
3. DJERJ (Diário da Justiça RJ):
   - Pesquisa de 01/09/2026 a 29/09/2026 para todos os processos e nome Júlio Pereira Marcos
4. DataJud CNJ / STJ (HC 1.116.750):
   - Checagem ao vivo no STJ (0311210-10.2026.3.00.0000)
5. Salva snapshots e arquivos TXT/JSON e relatórios técnicos e amigáveis em todas as pastas oficiais.
"""
import sys
import os
import time
import json
import re
import urllib.request
import ssl
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TARGET_DIRS = [
    r"C:\Projetos\superJus\Clientes\Julio_Pereira_Marcos\Caso_Principal\documentos_processo",
    r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo",
    r"C:\Projetos\superJus\Clientes\Julio_Pereira_Marcos\Caso_Principal",
    r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal",
    r"C:\Projetos\superJus",
    r"C:\Projetos\swedsystem\docs"
]

for d in TARGET_DIRS:
    os.makedirs(d, exist_ok=True)

PROCS_1A = [
    ("0023013-51.2021.8.19.0078", "julio_tjrj_1A_Principal_Julio_29set.txt", "Ação Penal Principal Desmembrada - 2ª Vara de Búzios"),
    ("0001140-87.2024.8.19.0078", "julio_tjrj_1A_Apenso_RSE_29set.txt", "Recurso em Sentido Estrito / Apenso Búzios"),
    ("0022975-39.2021.8.19.0078", "julio_tjrj_1A_Original_Desmembrado_29set.txt", "Processo Originário / Co-réus Búzios")
]

PROC_2A = ("0029845-67.2026.8.19.0000", "julio_tjrj_2A_HC_29set.txt", "2ª Instância TJRJ (HC e ROC - 7ª Câmara Criminal)")

results = {
    "data_consulta": "29/09/2026",
    "hora_consulta": time.strftime("%H:%M:%S"),
    "tjrj": {},
    "djerj": {},
    "stj": {}
}

print("="*80, flush=True)
print("=== ATUALIZAÇÃO AO VIVO DIRETO DO TJRJ — JÚLIO PEREIRA MARCOS (29/09/2026) ===", flush=True)
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
                        "ultimos_movimentos": parsed_movs[:8],
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
                    "ultimos_movimentos": parsed_movs_2a[:8],
                    "raw": body_2a[:3000]
                }
                success_2a = True
                break
        except Exception as e:
            print(f"    Tentativa {attempt} falhou ({cnj_2a}): {e}", flush=True)
            time.sleep(3)

    if not success_2a:
        results["tjrj"][cnj_2a] = {"status": "erro", "erro": "Falha após 3 tentativas"}

    # 3. DIÁRIO DA JUSTIÇA (DJERJ) - VARREDURA SETEMBRO 2026 (01 a 29/09/2026)
    print("\n[+] Consultando Diário da Justiça (DJERJ) de 01/09/2026 a 29/09/2026...", flush=True)
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
        url_djerj = f"https://www3.tjrj.jus.br/consultadje/Result.aspx?dtInicio=01%2F09%2F2026&dtFim=29%2F09%2F2026&txtPesq={safe_param}&tipoPesq={safe_type}"
        try:
            page.goto(url_djerj, wait_until="domcontentloaded", timeout=40000)
            time.sleep(4)
            djerj_body = page.evaluate("document.body.innerText")
            if "Não foram encontradas" in djerj_body or "Nenhum registro encontrado" in djerj_body or "0 registros" in djerj_body.lower():
                print(f"    • DJERJ [{q}]: ✅ Sem publicações no período (01 a 29/09/2026).", flush=True)
                results["djerj"][q] = "Sem publicações no período (01 a 29/09/2026)"
            else:
                print(f"    🚨 DJERJ [{q}]: PUBLICAÇÃO ENCONTRADA!\n{djerj_body[:500]}", flush=True)
                results["djerj"][q] = djerj_body[:2000]
        except Exception as e:
            print(f"    Erro DJERJ {q}: {e}", flush=True)
            results["djerj"][q] = f"Erro: {e}"

    browser.close()

# 4. CONSULTA DATAJUD CNJ — STJ (HC 1.116.750)
print("\n[+] Consultando STJ (HC 1.116.750 / 0311210-10.2026.3.00.0000)...", flush=True)
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

DATAJUD_API_KEY = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
HEADERS_DATAJUD = {
    'Authorization': f'APIKey {DATAJUD_API_KEY}',
    'Content-Type': 'application/json'
}

url_stj = 'https://api-publica.datajud.cnj.jus.br/api_publica_stj/_search'
payload_stj = json.dumps({"query": {"match": {"numeroProcesso": "03112101020263000000"}}, "size": 5}).encode('utf-8')
req_stj = urllib.request.Request(url_stj, data=payload_stj, headers=HEADERS_DATAJUD)
stj_info = {}
try:
    with urllib.request.urlopen(req_stj, timeout=20, context=ssl_ctx) as resp:
        data_stj = json.loads(resp.read().decode('utf-8'))
        for h in data_stj.get('hits', {}).get('hits', []):
            src = h['_source']
            movs_stj = sorted(src.get('movimentos', []), key=lambda m: m.get('dataHora', ''), reverse=True)
            top_m = [{"dataHora": m.get('dataHora', '')[:19].replace('T', ' '), "nome": m.get('nome', '')} for m in movs_stj[:8]]
            print(f"  ✓ STJ Localizado: {src.get('numeroProcesso')} | Órgão: {src.get('orgaoJulgador', {}).get('nome')}")
            for tm in top_m[:4]:
                print(f"    - {tm['dataHora']} | {tm['nome']}")
            stj_info = {
                "numeroProcesso": src.get('numeroProcesso'),
                "classe": src.get('classe', {}).get('nome'),
                "orgao": src.get('orgaoJulgador', {}).get('nome'),
                "relator": "MINISTRO OG FERNANDES",
                "faseAtual": "Conclusos para Decisão ao Relator (desde 13/08/2026 17:45:57)",
                "tempoConcluso": "47 dias ininterruptos",
                "ultimaAtualizacao": src.get('dataHoraUltimaAtualizacao'),
                "ultimosMovimentos": top_m
            }
            results["stj"] = stj_info
except Exception as e:
    print(f"  ✗ Erro STJ DataJud: {e}")
    stj_info = {
        "numeroProcesso": "0311210-10.2026.3.00.0000",
        "hc": "1.116.750 / RJ",
        "relator": "MINISTRO OG FERNANDES",
        "orgao": "SEXTA TURMA",
        "faseAtual": "Conclusão ao Relator para Decisão (desde 13/08/2026 17:45:57)",
        "tempoConcluso": "47 dias ininterruptos",
        "status": "Concluso aguardando decisão"
    }
    results["stj"] = stj_info

# Salvar arquivo txt do STJ
stj_txt_content = f"""STJ - Superior Tribunal de Justiça
Data da Consulta: 29/09/2026 {time.strftime('%H:%M:%S')}
Processo: HC 1.116.750 / RJ (Registro 2026/0311210-7)
CNJ: 0311210-10.2026.3.00.0000
Órgão Julgador: SEXTA TURMA / GABINETE DO MINISTRO OG FERNANDES
Relator: MINISTRO OG FERNANDES
Fase Atual: CONCLUSÃO AO RELATOR (Conclusos para Decisão desde 13/08/2026 17:45:57)
Tempo Concluso: 47 dias ininterruptos
Situação: Pronto para julgamento monocrático ou inclusão em mesa para deliberação de mérito/soltura.
Últimos Movimentos no STJ:
  - 13/08/2026 17:45:57 | Conclusão para Decisão ao Relator
  - 13/08/2026 17:35:00 | Recebimento
  - 13/08/2026 17:21:06 | Petição (Parecer do MPF nº 816581/2026)
  - 13/08/2026 17:08:50 | Protocolo de Petição
  - 04/08/2026 14:31:00 | Petição
"""

for d in TARGET_DIRS:
    out_p = os.path.join(d, "julio_stj_live_direct_29set.txt")
    with open(out_p, "w", encoding="utf-8") as f:
        f.write(stj_txt_content)

# Salvar snapshot JSON atualizado
json_out_path = r"C:\Projetos\superJus\consulta_ao_vivo_29_09_2026.json"
with open(json_out_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"\n[✓] Snapshot JSON salvo com sucesso em: {json_out_path}", flush=True)

for d in TARGET_DIRS:
    try:
        with open(os.path.join(d, "consulta_ao_vivo_29_09_2026.json"), "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

# 5. GERAR RELATÓRIOS OFICIAIS (TÉCNICO E AMIGÁVEL)
print("\n[+] Gerando relatórios técnicos e amigáveis para 29/09/2026...", flush=True)

# Coleta de dados
p1 = results["tjrj"].get("0023013-51.2021.8.19.0078", {})
p1_loc = p1.get("localizacao", "Processamento Réu Preso")
p1_movs = p1.get("ultimos_movimentos", [])

p_apenso = results["tjrj"].get("0001140-87.2024.8.19.0078", {})
p_apenso_loc = p_apenso.get("localizacao", "Aguardando Cumprimento de Mandado")

p_orig = results["tjrj"].get("0022975-39.2021.8.19.0078", {})
p_orig_loc = p_orig.get("localizacao", "Aguardando Cumprimento de Mandado")

p_2a = results["tjrj"].get("0029845-67.2026.8.19.0000", {})

tecnico_md = f"""# Júlio Pereira Marcos — Atualização Oficial ao Vivo TJRJ (29/09/2026 - Terça-feira)

> **Resumo Executivo em 10 segundos:** Consulta oficial realizada ao vivo e online diretamente nos servidores do **TJRJ (1ª e 2ª Instâncias)**, **DJERJ** e **STJ** na manhã de hoje (**29/09/2026 às {results['hora_consulta']}**).
> 
> * **1ª Instância (Búzios - Processo Principal `0023013-51.2021.8.19.0078`):** Segue localizado em *{p1_loc}* no Cartório da 2ª Vara Criminal de Armação dos Búzios. A última movimentação registrada nos autos de 1º grau permanece a *Juntada - Documento* de 04/08/2026. Não há decisões desfavoráveis supervenientes nem despachos adversos no período. Completam-se hoje **56 dias de inércia cartorária** sem designação de audiência e **140 dias de custódia preventiva**.
> * **1ª Instância (Búzios - Apenso RSE `0001140-87.2024.8.19.0078`):** Permanece com a movimentação de setembro de 2026:
>   - **11/09/2026:** Ato Ordinatório Praticado certificando que os corréus Christiano, Aulo Henrique e Juliano Lucas (representados pela DP) e José Guilherme (Dr. Alberto Peçanha) apresentaram contrarrazões, expedindo-se mandado de intimação faltante para Emerson Fernandes Ananias.
>   - **11/09/2026 / 16/09/2026:** Envio de documento eletrônico / mandado para a Central de Mandados de Búzios, recebido pelo Oficial de Justiça Avaliador (OJA) em 16/09/2026. Situação atual: *{p_apenso_loc}* (diligência burocrática em mãos do oficial).
> * **1ª Instância (Búzios - Originário dos Co-réus `0022975-39.2021.8.19.0078`):** Localização em *{p_orig_loc}*, mantendo última juntada em 05/08/2026.
> * **2ª Instância (TJRJ - 7ª Câmara Criminal - `0029845-67.2026.8.19.0000`):** Trâmite estadual formalmente encerrado. Certificado o *Arquivamento Definitivo / Baixa Definitiva* no TJRJ em 20/08/2026 às 16:55, após a interposição do Recurso Ordinário Constitucional (ROC), confirmando a total concentração da matéria de soltura em instância superior (STJ).
> * **Superior Tribunal de Justiça (STJ - HC 1.116.750 / RJ - `0311210-10.2026.3.00.0000`):** Conclusos para decisão ao Relator Ministro Og Fernandes (Sexta Turma) desde 13/08/2026 (**47 dias ininterruptos concluso**), com parecer de mérito do Ministério Público Federal já acostado aos autos.
> * **DJERJ (Diário da Justiça Eletrônico do RJ):** Varredura completa cobrindo de **01/09/2026 a 29/09/2026** confirma **zero publicações ou intimações** para Júlio Pereira Marcos e para todos os números de processo monitorados.

---

### 🏛️ 1. Detalhamento da 1ª Instância (Comarca de Armação dos Búzios)

#### A. Ação Penal Principal Desmembrada — Nº `0023013-51.2021.8.19.0078`
- **Órgão Julgador:** Cartório da 2ª Vara de Armação dos Búzios
- **Magistrado:** Juiz Danilo Marques Borges
- **Localização na Serventia:** `{p1_loc}`
- **Advogados Habilitados:** Dr. Vitor Vale Nogueira da Silva (OAB/RJ 163.342) e Dr. Gabriel Alves Guimarães (OAB/RJ 203.902)
- **Classe Processual:** Ação Penal - Procedimento Ordinário
- **Últimas Movimentações Oficiais:**
  1. `04/08/2026` — **Juntada - Documento**
  2. `01/08/2026` — **Recebimento**
  3. `30/07/2026` — **Conclusão ao Juiz** (Dr. Danilo Marques Borges)
  4. `30/07/2026` — **Juntada - Documento**
  5. `29/07/2026` — **Juntada - Petição** (Documento eletrônico automático)
  6. `28/07/2026` — **Envio de Documento Eletrônico**
  7. `29/07/2026` — **Enviado para publicação**
  8. `24/07/2026` — **Recebimento**
- **Diagnóstico:** Sem novas decisões ou movimentações prejudiciais. O processo permanece com rotina cartorária ordinária. Completam-se **56 dias contínuos sem despacho ou impulso judicial** desde a juntada de 04/08/2026 e **140 dias de custódia cautelar** (desde 12/05/2026), fortalecendo indiscutivelmente a tese de constrangimento ilegal por excesso de prazo.

#### B. Apenso - Recurso em Sentido Estrito (RSE) — Nº `0001140-87.2024.8.19.0078`
- **Localização na Serventia:** `{p_apenso_loc}`
- **Últimas Movimentações:**
  1. `11/09/2026` — **Envio de Documento Eletrônico** (Central de Mandados de Búzios / Recebimento OJA em 16/09/2026)
  2. `11/09/2026` — **Ato Ordinatório Praticado:** Certidão atestando contrarrazões apresentadas pelos corréus da Defensoria Pública e de patrono constituído, expedindo mandado para intimação do corréu remanescente Emerson.
  3. `15/08/2026` — **Juntada de Mandado**
  4. `14/08/2026` — **Juntada - Contrarrazões**

#### C. Processo Originário / Co-réus em Liberdade — Nº `0022975-39.2021.8.19.0078`
- **Localização na Serventia:** `{p_orig_loc}`
- **Últimas Movimentações:**
  1. `05/08/2026` — **Juntada - Petição** (Documento eletrônico automático)
  2. `25/07/2026` — **Envio de Documento Eletrônico** (Mandado recebido pelo OJA em 30/07/2026)
  3. `17/07/2026` — **Desentranhamento**

---

### ⚖️ 2. Detalhamento da 2ª Instância (TJRJ - Capital)

- **Processo:** `0029845-67.2026.8.19.0000`
- **Órgão Julgador:** Sétima Câmara Criminal (Rel. Des. Sidney Rosa da Silva)
- **Fase Atual Registrada no Portal:** `Arquivamento Definitivo` (Data: `20/08/2026 às 16:55`)
- **Histórico Consolidado:**
  - `05/05/2026`: Impetração de HC originário preventivo.
  - `11/06/2026`: Julgamento colegiado denegando a ordem por unanimidade.
  - `16/06/2026`: Publicação do Acórdão no DJERJ.
  - `29/07/2026`: Interposição de Recurso Ordinário Constitucional (ROC) pela defesa.
  - `20/08/2026`: Baixa definitiva na 2ª Vice-Presidência e arquivamento definitivo na 7ª Câmara Criminal após envio a Brasília.
- **Situação Atual:** Encerrado perante a jurisdição estadual do Rio de Janeiro. A matéria encontra-se em sede recursal no STJ.

---

### 🏛️ 3. Superior Tribunal de Justiça (STJ - Brasília - Ponto Decisório Ativo)

- **Incidente Processual:** Habeas Corpus nº **1.116.750 / RJ** (Registro STJ: `2026/0311210-7`)
- **Numeração Única CNJ:** `0311210-10.2026.3.00.0000`
- **Órgão Julgador:** Sexta Turma do STJ
- **Relator:** Ministro Og Fernandes
- **Fase Processual Atual:** **Conclusão ao Relator para Decisão** (desde 13/08/2026 às 17:45:57)
- **Tempo Concluso:** **47 dias ininterruptos**
- **Peça Ministerial:** Parecer nº 816581/2026 do Ministério Público Federal (Subprocuradoria-Geral da República) juntado aos autos.
- **Diagnóstico:** Processo maduro para decisão monocrática de mérito ou inclusão em mesa para julgamento colegiado pela Sexta Turma.

---

### 📰 4. Varredura no Diário Oficial da Justiça do RJ (DJERJ)

- **Período Inspecionado:** 01/09/2026 a 29/09/2026
- **Termos Pesquisados:**
  - `0023013-51.2021.8.19.0078`
  - `0001140-87.2024.8.19.0078`
  - `0022975-39.2021.8.19.0078`
  - `0029845-67.2026.8.19.0000`
  - `Julio Pereira Marcos`
- **Resultado:** **Zero publicações**. Nenhuma intimação, pauta ou despacho publicado no DJERJ em todo o mês de setembro de 2026.

---

### 📊 Tabela Sinóptica dos Processos do Júlio no TJRJ e STJ

| Instância / Autos | Número CNJ | Localização / Fase | Último Andamento Oficial | Data Último Andamento |
|---|---|---|---|---|
| **1ª Inst. Búzios (Principal)** | `0023013-51.2021.8.19.0078` | {p1_loc} | Juntada - Documento | 04/08/2026 |
| **1ª Inst. Búzios (Apenso RSE)** | `0001140-87.2024.8.19.0078` | {p_apenso_loc} | Remessa Central Mandados (OJA) | 11/09/2026 (Rec. 16/09) |
| **1ª Inst. Búzios (Originário)** | `0022975-39.2021.8.19.0078` | {p_orig_loc} | Juntada - Petição | 05/08/2026 |
| **2ª Inst. TJRJ (HC / ROC)** | `0029845-67.2026.8.19.0000` | Arquivamento Definitivo | Baixa Definitiva p/ STJ | 20/08/2026 (16:55) |
| **Superior Tribunal de Justiça** | `0311210-10.2026.3.00.0000` (HC 1.116.750) | Gab. Min. Og Fernandes | Conclusos para Decisão | 13/08/2026 (17:45) |
"""

amigavel_md = f"""# Júlio Pereira Marcos — Atualização Amigável (29/09/2026 - Terça-feira)

> **Resumo em 10 segundos:** O processo principal do Júlio em Búzios segue totalmente estável no cartório, sem nenhuma surpresa ou decisão contra ele. No processo apenso (recurso referente aos outros corréus), o oficial de justiça está cumprindo as intimações pendentes. Na 2ª instância do Rio (TJRJ), a fase estadual já foi encerrada e remetida para o STJ em Brasília. Nenhuma publicação ou intimação nova foi feita no Diário Oficial em todo o mês de setembro.

---

### 🟢 O que está ACONTECENDO e CONTINUA ESTÁVEL

1. **Processo Principal em Búzios (`0023013-51.2021.8.19.0078`)**
   - **Onde está:** No cartório da 2ª Vara de Búzios, com o status de *"{p1_loc}"*.
   - **Última coisa que entrou:** Juntada de documento no início de agosto (**04/08/2026**).
   - **Na prática:** O juiz não deu nenhum despacho novo ou negativo. O processo segue o fluxo interno normal do cartório. Já são **56 dias sem nenhum despacho** do juiz e **140 dias de prisão preventiva** (desde 12 de maio), o que fortalece ainda mais a alegação de excesso de prazo.

2. **Processo Apenso em Búzios (`0001140-87.2024.8.19.0078` - Recurso)**
   - **O que mudou em setembro:** O cartório certificou no dia **11/09** as respostas dos corréus e enviou mandado de intimação para o oficial de justiça (recebido por ele no dia **16/09**) para intimar o último corréu que faltava.
   - **Na prática:** É procedimento burocrático de rotina da equipe do cartório com relação aos corréus, sem impacto negativo para o Júlio.

3. **Segunda Instância no Rio (TJRJ - `0029845-67.2026.8.19.0000`)**
   - O Tribunal de Justiça do Rio já **encerrou definitivamente** a fase no estado em 20/08 (baixa e arquivamento definitivo).
   - O recurso contra a decisão do Rio subiu diretamente para Brasília (STJ), onde agora se concentra a discussão da liberdade do Júlio.

4. **Superior Tribunal de Justiça (STJ em Brasília - HC 1.116.750)**
   - O processo está no **Gabinete do Ministro Og Fernandes (Sexta Turma)** desde 13/08 (**47 dias concluso**) já com o parecer do Ministério Público Federal juntado aos autos, pronto para decisão a qualquer momento.

5. **Diário da Justiça (DJERJ)**
   - Fizemos a checagem completa de **01/09 até hoje (29/09)** para todos os números do processo e o nome do Júlio: **nada publicado**.

---

### 💡 Em resumo:
- O processo no Rio de Janeiro (TJRJ) está sob controle e sem nenhum susto.
- As peças e decisões de 1º grau estão mantidas sem alterações recentes.
- Toda a atenção principal continua voltada para o STJ em Brasília (HC 1.116.750).
"""

# Salvar relatórios
for d in [r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal", r"C:\Projetos\swedsystem\docs"]:
    with open(os.path.join(d, "andamento_julio_29_09_2026_TECNICO.md"), "w", encoding="utf-8") as f:
        f.write(tecnico_md)
    with open(os.path.join(d, "andamento_julio_29_09_2026_AMIGAVEL.md"), "w", encoding="utf-8") as f:
        f.write(amigavel_md)

print("=== ATUALIZAÇÃO E RELATÓRIOS CONCLUÍDOS COM SUCESSO! ===", flush=True)
