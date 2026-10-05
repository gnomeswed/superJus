import sys, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
# -*- coding: utf-8 -*-
import json
import urllib.request
import os
import time

clean_num = "00118579520248190002"
proc_fmt = "0011857-95.2024.8.19.0002"

url = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'
headers = {
    'Authorization': __import__('core.config', fromlist=['datajud_headers']).datajud_headers()['Authorization'],
    'Content-Type': 'application/json'
}

target_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas\Caso_Principal\documentos_processo"
case_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas\Caso_Principal"

os.makedirs(target_dir, exist_ok=True)

out_md = []
out_md.append(f"# ATUALIZAÇÃO PROCESSUAL EM TEMPO REAL — MOTOBOY LUCAS")
out_md.append(f"**Processo Nº:** `{proc_fmt}`")
out_md.append(f"**Data da Consulta:** 24/07/2026\n")

# 1. Consulta Datajud API
req_data = json.dumps({"query": {"match": {"numeroProcesso": clean_num}}, "size": 50}).encode('utf-8')
req = urllib.request.Request(url, data=req_data, headers=headers)

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        hits = res.get('hits', {}).get('hits', [])
        out_md.append(f"**Registros Encontrados no Datajud:** {len(hits)}\n")
        
        # Salvar JSON bruto
        with open(os.path.join(target_dir, "datajud_raw_lucas.json"), "w", encoding="utf-8") as f:
            json.dump(res, f, indent=2, ensure_ascii=False)
            
        all_events = []
        
        for idx, hit in enumerate(hits, start=1):
            src = hit['_source']
            classe = src.get('classe', {}).get('nome', 'N/I')
            orgao = src.get('orgaoJulgador', {}).get('nome', 'N/I')
            dt_at = src.get('dataHoraUltimaAtualizacao', 'N/I')
            movs = src.get('movimentos', [])
            
            out_md.append(f"## {idx}. Instância / Órgão: {classe} ({orgao})")
            out_md.append(f"- **Data Última Atualização:** `{dt_at}`")
            out_md.append(f"- **Total de Movimentos:** {len(movs)}\n")
            out_md.append("### Últimas Movimentações (ordem cronológica recente):")
            
            movs_sorted = sorted(movs, key=lambda m: m.get('dataHora', ''), reverse=True)
            for m in movs_sorted[:15]:
                dt = m.get('dataHora', '')
                nome = m.get('nome', '')
                code = m.get('codigo', '')
                comps = m.get('complementosTabelados', [])
                comp_str = ""
                if comps:
                    comp_str = " (" + ", ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in comps]) + ")"
                out_md.append(f"- **`{dt[:19].replace('T', ' ')}`** — **{nome}**{comp_str} *(Cód: {code})*")
                
                all_events.append({
                    "date": dt[:10],
                    "event": f"[{orgao}] {nome}{comp_str}",
                    "orgao": orgao,
                    "codigo": code
                })
            out_md.append("\n" + "="*50 + "\n")
            
        # Salvar timeline
        all_events_sorted = sorted(all_events, key=lambda x: x["date"])
        with open(os.path.join(case_dir, "timeline.json"), "w", encoding="utf-8") as f:
            json.dump(all_events_sorted, f, indent=2, ensure_ascii=False)
            
except Exception as e:
    out_md.append(f"Erro Datajud: {e}\n")

# 2. Tentar consulta Playwright live no TJRJ
try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1280, "height": 800})
        page = ctx.new_page()
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=30000, wait_until="domcontentloaded")
        time.sleep(2)
        iframe_el = page.query_selector("iframe#mainframe")
        if iframe_el:
            frame = iframe_el.content_frame()
            if frame:
                inp = frame.query_selector("input[name='numeroProcesso']")
                if inp:
                    inp.fill(proc_fmt)
                    btns = frame.query_selector_all("button")
                    for b in btns:
                        if "pesquisar" in b.inner_text().lower() or "buscar" in b.inner_text().lower():
                            b.click()
                            time.sleep(5)
                            body_txt = frame.inner_text("body")
                            out_md.append("## Captura ao Vivo do Portal TJRJ\n```text\n" + body_txt[:2000] + "\n```\n")
                            break
        browser.close()
except Exception as e:
    out_md.append(f"Aviso Playwright: {e}\n")

out_file = os.path.join(target_dir, "movimentacoes_atualizadas_lucas.md")
with open(out_file, "w", encoding="utf-8") as f:
    f.write("\n".join(out_md))

print(f"Sucesso! Relatório salvo em {out_file}")
