# -*- coding: utf-8 -*-
import json
import urllib.request
import os
import re
import time

clean_num = "00002537820178190004"
proc_fmt = "0000253-78.2017.8.19.0004"

url = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'
headers = {
    'Authorization': 'APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==',
    'Content-Type': 'application/json'
}

target_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas\Caso_Principal\documentos_processo"
os.makedirs(target_dir, exist_ok=True)

out_md = []
out_md.append(f"# RELATÓRIO DO PROCESSO ANTERIOR DA COMARCA DE SÃO GONÇALO")
out_md.append(f"**Processo Nº:** `{proc_fmt}`")
out_md.append(f"**Réu:** Lucas de Souza Freitas")
out_md.append(f"**Data da Consulta:** 24/07/2026\n")

# 1. Consulta Datajud API
req_data = json.dumps({"query": {"match": {"numeroProcesso": clean_num}}, "size": 50}).encode('utf-8')
req = urllib.request.Request(url, data=req_data, headers=headers)

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        hits = res.get('hits', {}).get('hits', [])
        out_md.append(f"**Registros no Datajud:** {len(hits)}\n")
        
        with open(os.path.join(target_dir, "datajud_lucas_2017_raw.json"), "w", encoding="utf-8") as f:
            json.dump(res, f, indent=2, ensure_ascii=False)
            
        for idx, hit in enumerate(hits, start=1):
            src = hit['_source']
            classe = src.get('classe', {}).get('nome', 'N/I')
            orgao = src.get('orgaoJulgador', {}).get('nome', 'N/I')
            dt_aj = src.get('dataAjuizamento', 'N/I')
            movs = src.get('movimentos', [])
            
            out_md.append(f"## {idx}. Órgão Julgador: {classe} ({orgao})")
            out_md.append(f"- **Data Ajuizamento:** `{dt_aj}`")
            out_md.append(f"- **Total de Movimentos:** {len(movs)}\n")
            
            # Buscar partes e qualificações
            polos = src.get('polo', [])
            for p in polos:
                tipo = p.get('polo', '')
                partes = p.get('parte', [])
                for pt in partes:
                    pess = pt.get('pessoa', {})
                    nome = pess.get('nome', '')
                    num_doc = pess.get('numeroDocumentoPrincipal', '')
                    tipo_doc = pess.get('tipoDocumento', '')
                    out_md.append(f"- **Parte ({tipo}):** {nome} | {tipo_doc}: `{num_doc}`")
                    
            out_md.append("\n### Movimentações Processuais (Mais recentes primeiro):")
            movs_sorted = sorted(movs, key=lambda m: m.get('dataHora', ''), reverse=True)
            for m in movs_sorted:
                dt = m.get('dataHora', '')
                nome = m.get('nome', '')
                code = m.get('codigo', '')
                comps = m.get('complementosTabelados', [])
                comp_str = ""
                if comps:
                    comp_str = " (" + ", ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in comps]) + ")"
                out_md.append(f"- **`{dt[:19].replace('T', ' ')}`** — **{nome}**{comp_str} *(Cód: {code})*")
            out_md.append("\n" + "="*50 + "\n")
except Exception as e:
    out_md.append(f"Erro Datajud: {e}\n")

# 2. Raspagem Playwright ao Vivo no TJRJ para o processo 0000253-78.2017.8.19.0004
try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1280, "height": 800})
        page = ctx.new_page()
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=30000)
        time.sleep(3)
        
        frame = page.frame_locator("iframe#mainframe")
        # Preencher numeroProcesso
        frame.locator("input[name='numeroProcesso']").fill(proc_fmt)
        time.sleep(1)
        frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first.click()
        time.sleep(8)
        
        real_frame = page.query_selector("iframe#mainframe").content_frame()
        tjrj_live_txt = real_frame.inner_text("body")
        
        out_md.append("## Espelho Oficial Extraído ao Vivo do TJRJ\n```text\n")
        out_md.append(tjrj_live_txt[:4000])
        out_md.append("\n```\n")
        browser.close()
except Exception as e:
    out_md.append(f"Erro Playwright TJRJ: {e}\n")

out_file = os.path.join(target_dir, "processo_antigo_0000253_2017_lucas.md")
with open(out_file, "w", encoding="utf-8") as f:
    f.write("\n".join(out_md))

print(f"Sucesso total! Relatório salvo em {out_file}")
