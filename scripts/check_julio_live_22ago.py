# -*- coding: utf-8 -*-
"""
Consulta online em tempo real — Júlio Pereira Marcos (22/08/2026)
Fontes consultadas:
1. Datajud API (CNJ) - TJRJ e STJ
2. Portal do TJRJ (1ª e 2ª Instâncias via Playwright)
3. Portal do STJ (Fases e Decisões do HC 1.116.750 / RJ)
4. DJERJ (Consulta de Publicações)
"""
import sys
import os
import json
import time
import urllib.request
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

DATAJUD_API_KEY = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
HEADERS = {
    'Authorization': f'APIKey {DATAJUD_API_KEY}',
    'Content-Type': 'application/json'
}

OUT_DIR = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"
os.makedirs(OUT_DIR, exist_ok=True)

PROCS_TJRJ = [
    ("0023013-51.2021.8.19.0078", "00230135120218190078", "Ação Penal Desmembrada - 2ª Vara de Búzios"),
    ("0029845-67.2026.8.19.0000", "00298456720268190000", "Habeas Corpus - 7ª Câmara Criminal TJRJ"),
    ("0001140-87.2024.8.19.0078", "00011408720248190078", "Recurso em Sentido Estrito / Apenso - Búzios"),
    ("0022975-39.2021.8.19.0078", "00229753920218190078", "Processo Originário / Co-réus - Búzios")
]

results = {
    "data_consulta": "22/08/2026 09:10",
    "datajud_tjrj": {},
    "datajud_stj": {},
    "portal_tjrj": {},
    "portal_stj": {},
    "djerj": {}
}

print("="*70)
print("🔍 1. CONSULTA DATAJUD CNJ — TJRJ (1ª E 2ª INSTÂNCIAS)")
print("="*70)

for proc_fmt, proc_clean, desc in PROCS_TJRJ:
    print(f"\n--- Consultando {proc_fmt} ({desc}) ---")
    url = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'
    payload = json.dumps({"query": {"match": {"numeroProcesso": proc_clean}}, "size": 10}).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            hits = data.get('hits', {}).get('hits', [])
            print(f"Registros encontrados: {len(hits)}")
            proc_entries = []
            for hit in hits:
                src = hit['_source']
                orgao = src.get('orgaoJulgador', {}).get('nome', 'N/A')
                classe = src.get('classe', {}).get('nome', 'N/A')
                dt_up = src.get('dataHoraUltimaAtualizacao', 'N/A')
                movs = src.get('movimentos', [])
                movs_sorted = sorted(movs, key=lambda m: m.get('dataHora', ''), reverse=True)
                
                print(f"  • Órgão: {orgao} | Classe: {classe}")
                print(f"  • Atualização no DataJud: {dt_up}")
                print(f"  • Total Movimentações: {len(movs)}")
                print("  • Últimas 5 Movimentações:")
                top_movs = []
                for m in movs_sorted[:5]:
                    dt_m = m.get('dataHora', '')[:19].replace('T', ' ')
                    nome_m = m.get('nome', '')
                    comps = m.get('complementosTabelados', [])
                    comp_text = ""
                    if comps:
                        comp_text = " (" + ", ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in comps]) + ")"
                    print(f"    - {dt_m} | {nome_m}{comp_text}")
                    top_movs.append({"dataHora": dt_m, "nome": nome_m, "complemento": comp_text})
                
                proc_entries.append({
                    "orgao": orgao,
                    "classe": classe,
                    "ultimaAtualizacao": dt_up,
                    "totalMovimentos": len(movs),
                    "ultimosMovimentos": top_movs
                })
            results["datajud_tjrj"][proc_fmt] = proc_entries
    except Exception as e:
        print(f"Erro ao consultar {proc_fmt}: {e}")
        results["datajud_tjrj"][proc_fmt] = {"erro": str(e)}

print("\n" + "="*70)
print("🔍 2. CONSULTA DATAJUD CNJ — STJ (HC 1.116.750 / RJ)")
print("="*70)

try:
    url_stj = 'https://api-publica.datajud.cnj.jus.br/api_publica_stj/_search'
    payload_stj = json.dumps({"query": {"match_phrase": {"pessoas.nome": "Julio Pereira Marcos"}}, "size": 5}).encode('utf-8')
    req_stj = urllib.request.Request(url_stj, data=payload_stj, headers=HEADERS)
    with urllib.request.urlopen(req_stj, timeout=20) as resp:
        data_stj = json.loads(resp.read().decode('utf-8'))
        hits_stj = data_stj.get('hits', {}).get('hits', [])
        print(f"Registros encontrados no STJ: {len(hits_stj)}")
        stj_entries = []
        for h in hits_stj:
            src = h['_source']
            proc_num = src.get('numeroProcesso')
            classe = src.get('classe', {}).get('nome')
            dt_up = src.get('dataHoraUltimaAtualizacao')
            movs = src.get('movimentos', [])
            movs_sorted = sorted(movs, key=lambda m: m.get('dataHora', ''), reverse=True)
            print(f"  • Processo: {proc_num} | Classe: {classe}")
            print(f"  • Última Atualização: {dt_up}")
            top_movs = []
            for m in movs_sorted[:6]:
                dt_m = m.get('dataHora', '')[:19].replace('T', ' ')
                nome_m = m.get('nome', '')
                print(f"    - {dt_m} | {nome_m}")
                top_movs.append({"dataHora": dt_m, "nome": nome_m})
            stj_entries.append({
                "numeroProcesso": proc_num,
                "classe": classe,
                "ultimaAtualizacao": dt_up,
                "ultimosMovimentos": top_movs
            })
        results["datajud_stj"] = stj_entries
except Exception as e:
    print(f"Erro STJ DataJud: {e}")
    results["datajud_stj"] = {"erro": str(e)}

print("\n" + "="*70)
print("🌐 3. RASPAGEM DIRETA PLAYWRIGHT (PORTAL TJRJ + STJ + DJERJ)")
print("="*70)

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
    )
    ctx = browser.new_context(
        viewport={"width": 1366, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        locale="pt-BR"
    )
    ctx.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
    page = ctx.new_page()

    # 3.1 Portal TJRJ 1ª Instância - Processo 0023013-51.2021.8.19.0078
    print("\n--- 3.1 Portal TJRJ Consulta Pública (0023013-51.2021.8.19.0078) ---")
    try:
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", wait_until="domcontentloaded", timeout=45000)
        time.sleep(3)
        page.wait_for_selector("iframe#mainframe", timeout=30000)
        frame = page.query_selector("iframe#mainframe").content_frame()
        time.sleep(2)
        
        proc_target = "0023013-51.2021.8.19.0078"
        frame.evaluate(f"""() => {{
            const inp = Array.from(document.querySelectorAll('input')).find(i => i.name==='numeroProcesso' || i.id==='numeroProcesso');
            if(inp) {{
                inp.value = '{proc_target}';
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
        
        tjrj_body = frame.inner_text("body")
        print(f"Capturados {len(tjrj_body)} caracteres da página do processo no TJRJ.")
        
        tjrj_file = os.path.join(OUT_DIR, "julio_tjrj_live_direct_22ago.txt")
        with open(tjrj_file, "w", encoding="utf-8") as f:
            f.write(tjrj_body)
            
        loc_str = "N/A"
        if "Localização na Serventia" in tjrj_body:
            idx = tjrj_body.index("Localização na Serventia")
            loc_str = tjrj_body[idx:idx+400].replace('\n', ' | ')
            print(f"Localização: {loc_str}")
            
        mov_str = "N/A"
        if "Tipo do Movimento:" in tjrj_body:
            idx = tjrj_body.index("Tipo do Movimento:")
            mov_str = tjrj_body[idx:idx+350].replace('\n', ' | ')
            print(f"Último Movimento: {mov_str}")
            
        results["portal_tjrj"]["0023013-51.2021.8.19.0078"] = {
            "status": "sucesso",
            "localizacao": loc_str,
            "ultimo_movimento": mov_str,
            "preview": tjrj_body[:2500]
        }
    except Exception as e:
        print(f"Erro ao capturar portal TJRJ: {e}")
        results["portal_tjrj"]["0023013-51.2021.8.19.0078"] = {"erro": str(e)}

    # 3.2 STJ Consulta de Processo ao vivo (HC 1.116.750 / 202603112107)
    print("\n--- 3.2 Portal STJ Consulta Processual (HC 1.116.750 / RJ) ---")
    URL_STJ_RE = "https://processo.stj.jus.br/processo/pesquisa/?tipoPesquisa=tipoPesquisaNumeroRegistro&termo=202603112107&totalRegistrosPorPagina=40&aplicacao=processos.ea"
    try:
        page.goto(URL_STJ_RE, wait_until="domcontentloaded", timeout=45000)
        time.sleep(5)
        page.evaluate("""() => {
            const links = document.querySelectorAll('a, span, td');
            for(const el of links) {
                if((el.textContent||'').includes('1116750') && el.offsetParent !== null) {
                    el.click(); return true;
                }
            }
            return false;
        }""")
        time.sleep(8)
        
        stj_txt = page.evaluate("document.body.innerText")
        stj_html = page.content()
        print(f"STJ Caracteres: {len(stj_txt)}")
        
        with open(os.path.join(OUT_DIR, "julio_stj_live_direct_22ago.txt"), "w", encoding="utf-8") as f:
            f.write(stj_txt)
            
        import re
        sequenciais = re.findall(r'sequencial=(\d+)', stj_html)
        print(f"Sequenciais de decisão encontrados: {set(sequenciais)}")
        
        for line in stj_txt.splitlines():
            if any(k in line.upper() for k in ["CONCLUSOS", "GABINETE", "FASE:", "ÚLTIMA FASE"]):
                print(f"  • STJ Linha Relevante: {line.strip()}")
        
        results["portal_stj"] = {
            "status": "sucesso",
            "sequenciais_decisao": list(set(sequenciais)),
            "preview": stj_txt[:3000]
        }
    except Exception as e:
        print(f"Erro STJ Scraping: {e}")
        results["portal_stj"] = {"erro": str(e)}

    # 3.3 DJERJ Consulta de Publicações recentes (15/08 a 22/08/2026)
    print("\n--- 3.3 DJERJ Consulta de Publicações (15/08/2026 a 22/08/2026) ---")
    for proc_fmt, _, _ in PROCS_TJRJ:
        url_djerj = f"https://www3.tjrj.jus.br/consultadje/Result.aspx?dtInicio=15%2F08%2F2026&dtFim=22%2F08%2F2026&txtPesq={proc_fmt}&tipoPesq=PROC"
        try:
            page.goto(url_djerj, wait_until="domcontentloaded", timeout=45000)
            time.sleep(4)
            djerj_body = page.evaluate("document.body.innerText")
            if "Não foram encontradas" in djerj_body:
                print(f"  • {proc_fmt}: Sem novas publicações no DJERJ.")
                results["djerj"][proc_fmt] = "Sem publicações no período (15 a 22/08/2026)"
            else:
                print(f"  🚨 {proc_fmt}: PUBLICAÇÃO LOCALIZADA!\n{djerj_body[:1000]}")
                results["djerj"][proc_fmt] = djerj_body[:2000]
        except Exception as e:
            print(f"Erro DJERJ {proc_fmt}: {e}")
            results["djerj"][proc_fmt] = f"Erro: {e}"

    browser.close()

json_out = os.path.join(r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal", "consulta_ao_vivo_22_08_2026.json")
with open(json_out, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\n" + "="*70)
print(f"✅ CHECAGEM CONCLUÍDA COM SUCESSO! DADOS SALVOS EM: {json_out}")
print("="*70)
