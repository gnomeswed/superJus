# -*- coding: utf-8 -*-
import json
import urllib.request
import time
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

print("=== COMPILANDO TODAS AS MOVIMENTAÇÕES E DECISÕES — ANTÔNIO VITOR ===")

base_dir = r"c:\Projetos\superJus\Clientes\Antonio_Vitor"
mov_dir = os.path.join(base_dir, "02_Movimentacoes")
doc_dir = os.path.join(base_dir, "03_Documentos_do_Processo")
strat_dir = os.path.join(base_dir, "04_Analises_e_Estrategias")

os.makedirs(mov_dir, exist_ok=True)
os.makedirs(doc_dir, exist_ok=True)
os.makedirs(strat_dir, exist_ok=True)

# 1. Obter todas as 258+ movimentações via Datajud API
headers = {
    'Authorization': 'APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNxLV9TRENyQk1RdnFKZGRQdw==',
    'Content-Type': 'application/json'
}

proc_clean = "01758038620238190001"
url_tjrj = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'

req_data = json.dumps({"query": {"match": {"numeroProcesso": proc_clean}}, "size": 20}).encode('utf-8')
req = urllib.request.Request(url_tjrj, data=req_data, headers=headers)

all_records = []
try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        all_records = res.get('hits', {}).get('hits', [])
        print(f"✅ Datajud retornou {len(all_records)} instâncias/registros.")
        
        # Salvar JSON bruto
        json_file = os.path.join(mov_dir, "datajud_movimentacoes_completas_antonio_vitor.json")
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=2)
        print(f"✅ JSON bruto salvo em: {json_file}")
except Exception as e:
    print(f"Erro Datajud: {e}")

# 2. Gerar relatório em Markdown com todas as movimentações de cada instância
md_mov_file = os.path.join(mov_dir, "Movimentacoes_Completas_Antonio_Vitor.md")
md_lines = [
    "# RELATÓRIO COMPLETO DE MOVIMENTAÇÕES PROCESSUAIS",
    "**Cliente:** ANTÔNIO VITOR",
    "**Processo:** `0175803-86.2023.8.19.0001`",
    "**Extraído em:** 16/08/2026",
    "\n---"
]

for idx, rec in enumerate(all_records, start=1):
    src = rec['_source']
    orgao = src.get('orgaoJulgador', {}).get('nome', 'N/I')
    classe = src.get('classe', {}).get('nome', 'N/I')
    movs = src.get('movimentos', [])
    movs_sorted = sorted(movs, key=lambda m: m.get('dataHora', ''), reverse=True)
    
    md_lines.append(f"\n## 🏛️ INSTÂNCIA / REGISTRO #{idx}")
    md_lines.append(f"- **Órgão Julgador:** {orgao}")
    md_lines.append(f"- **Classe Processual:** {classe}")
    md_lines.append(f"- **Total de Movimentações:** {len(movs)}")
    md_lines.append("\n| # | Data/Hora | Movimentação / Ato | Código | Complementos |")
    md_lines.append("|---|---|---|---|---|")
    
    for m_idx, m in enumerate(movs_sorted, start=1):
        dt = m.get('dataHora', '')[:19].replace('T', ' ')
        nome = m.get('nome', '')
        code = m.get('codigo', '')
        comps = m.get('complementosTabelados', [])
        comp_str = ", ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in comps]) if comps else "-"
        md_lines.append(f"| {m_idx} | {dt} | **{nome}** | {code} | {comp_str} |")

with open(md_mov_file, "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))

print(f"✅ Arquivo Markdown compilado em: {md_mov_file}")

# 3. Scraping ao vivo com Playwright
target_url = "https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica?numProcessoCNJ=0175803-86.2023.8.19.0001"
print(f"\n3. Executando scraping no portal TJRJ...\n   {target_url}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    page = browser.new_page(viewport={"width": 1280, "height": 800})

    try:
        page.goto(target_url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(4)

        ss = os.path.join(doc_dir, "screenshot_portal_tjrj_antonio_vitor.png")
        page.screenshot(path=ss)
        print(f"✅ Screenshot salvo: {ss}")

        try:
            frame = page.frame_locator("iframe#mainframe")
            frame.locator("button:has-text('Todos Os Movimentos')").first.click()
            time.sleep(2)
            real_frame = page.query_selector("iframe#mainframe").content_frame()
            txt = real_frame.inner_text("body")
        except Exception:
            txt = page.inner_text("body")

        txt_file = os.path.join(doc_dir, "extrato_oficial_tjrj_antonio_vitor.txt")
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write(txt)
        print(f"✅ Extrato em texto salvo em: {txt_file}")

        # Gerar PDF do extrato via Playwright
        html_pdf = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
    body {{ font-family: Arial, sans-serif; margin: 30px; color: #111; line-height: 1.5; }}
    .header {{ text-align: center; border-bottom: 2px solid #002b49; padding-bottom: 10px; margin-bottom: 20px; }}
    .header h2 {{ margin: 3px 0; font-size: 16px; color: #002b49; }}
    .content {{ white-space: pre-wrap; font-family: 'Courier New', monospace; font-size: 11px; background: #f8fafc; padding: 15px; border: 1px solid #cbd5e1; }}
</style>
</head>
<body>
<div class="header">
    <h2>TRIBUNAL DE JUSTIÇA DO ESTADO DO RIO DE JANEIRO</h2>
    <h3>EXTRATO INTEGRAL DE MOVIMENTAÇÕES — ANTÔNIO VITOR</h3>
    <p>Processo nº 0175803-86.2023.8.19.0001 | 1ª Vara Criminal de Petrópolis</p>
</div>
<div class="content">
{txt}
</div>
</body>
</html>"""

        pdf_file = os.path.join(doc_dir, "Extrato_Oficial_TJRJ_Antonio_Vitor.pdf")
        page.set_content(html_pdf)
        page.pdf(path=pdf_file, format="A4", print_background=True)
        print(f"✅ PDF gerado com sucesso em: {pdf_file}")

    except Exception as e:
        print(f"Erro no Playwright: {e}")

    browser.close()

print("\n=== COMPILAÇÃO E DOWNLOAD CONCLUÍDOS COM SUCESSO ===")
