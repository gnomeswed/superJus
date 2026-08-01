# -*- coding: utf-8 -*-
import json
import urllib.request
import os
import time

procs = [
    ("0023013-51.2021.8.19.0078", "00230135120218190078", "Ação Penal - Búzios"),
    ("0022975-39.2021.8.19.0078", "00229753920218190078", "Processo Principal - Búzios"),
    ("0029845-67.2026.8.19.0000", "00298456720268190000", "Habeas Corpus - TJRJ"),
    ("0001140-87.2024.8.19.0078", "00011408720248190078", "Execução / Medida - Búzios"),
    ("0001492-25.2016.8.19.0046", "00014922520168190046", "Processo Antigo - Rio Bonito")
]

url = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'
headers = {
    'Authorization': 'APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==',
    'Content-Type': 'application/json'
}

target_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"
os.makedirs(target_dir, exist_ok=True)

out_md = []
out_md.append(f"# RELATÓRIO DE MOVIMENTAÇÕES ATUALIZADAS — JÚLIO PEREIRA MARCOS")
out_md.append(f"**Data da Atualização:** 28/07/2026\n")

for formatted, clean, label in procs:
    out_md.append(f"## Processo: `{formatted}` ({label})")
    req_data = json.dumps({"query": {"match": {"numeroProcesso": clean}}, "size": 100}).encode('utf-8')
    req = urllib.request.Request(url, data=req_data, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            hits = res.get('hits', {}).get('hits', [])
            if not hits:
                out_md.append("*(Nenhum evento registrado no Datajud público)*\n")
                continue
                
            out_md.append(f"**Total de eventos Datajud:** {len(hits)}")
            for hit in hits:
                src = hit['_source']
                orgao = src.get('orgaoJulgador', {}).get('nome', 'N/I')
                classe = src.get('classe', {}).get('nome', 'N/I')
                movs = src.get('movimentos', [])
                out_md.append(f"- **Órgão Julgador:** {orgao} | **Classe:** {classe}")
                out_md.append(f"- **Total de Movimentos:** {len(movs)}")
                
                movs_sorted = sorted(movs, key=lambda m: m.get('dataHora', ''), reverse=True)
                out_md.append("\n**Últimos 10 movimentos:**")
                for m in movs_sorted[:10]:
                    dt = m.get('dataHora', '')
                    nome = m.get('nome', '')
                    code = m.get('codigo', '')
                    comps = m.get('complementosTabelados', [])
                    comp_str = ""
                    if comps:
                        comp_str = " (" + ", ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in comps]) + ")"
                    out_md.append(f"  * `{dt[:19].replace('T', ' ')}` — **{nome}**{comp_str}")
                out_md.append("")
    except Exception as e:
        out_md.append(f"Erro ao consultar Datajud: {e}\n")

# TJRJ Scrape ao vivo via Playwright para o processo principal 0023013-51.2021.8.19.0078
try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1280, "height": 800})
        page = ctx.new_page()
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=30000)
        time.sleep(3)
        
        frame = page.frame_locator("iframe#mainframe")
        frame.locator("input[name='numeroProcesso']").fill("0023013-51.2021.8.19.0078")
        time.sleep(1)
        frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first.click()
        time.sleep(6)
        
        real_frame = page.query_selector("iframe#mainframe").content_frame()
        tjrj_live_txt = real_frame.inner_text("body")
        
        out_md.append("\n## Espelho Oficial em Tempo Real do TJRJ (0023013-51.2021.8.19.0078)\n```text\n")
        out_md.append(tjrj_live_txt[:4000])
        out_md.append("\n```\n")
        browser.close()
except Exception as e:
    out_md.append(f"Erro Playwright TJRJ: {e}\n")

out_file = os.path.join(target_dir, "andamento_atualizado_28_07_2026_julio.md")
with open(out_file, "w", encoding="utf-8") as f:
    f.write("\n".join(out_md))

print(f"Sucesso! Relatório de andamentos do Júlio salvo em {out_file}")
