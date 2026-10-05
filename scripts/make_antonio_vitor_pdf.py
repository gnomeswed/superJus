# -*- coding: utf-8 -*-
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

print("=== GERANDO PDF DO ESPELHO PROCESSUAL DO ANTÔNIO VITOR ===")

base_dir = r"c:\Projetos\superJus\Clientes\Antonio_Vitor"
doc_dir = os.path.join(base_dir, "03_Documentos_do_Processo")
mov_file = os.path.join(base_dir, "02_Movimentacoes", "Movimentacoes_Completas_Antonio_Vitor.md")

with open(mov_file, "r", encoding="utf-8") as f:
    md_text = f.read()

# Make clean HTML
html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
    body {{ font-family: Arial, sans-serif; margin: 30px; color: #111; line-height: 1.4; }}
    h1 {{ color: #002b49; border-bottom: 2px solid #002b49; padding-bottom: 8px; font-size: 20px; }}
    h2 {{ color: #004b87; font-size: 16px; margin-top: 25px; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 11px; }}
    th {{ background: #002b49; color: white; padding: 6px; text-align: left; }}
    td {{ border: 1px solid #ddd; padding: 5px; }}
    tr:nth-child(even) {{ background: #f9fafb; }}
</style>
</head>
<body>
{md_text.replace('# ', '<h1>').replace('## ', '<h2>').replace('\n', '<br>')}
</body>
</html>"""

pdf_out = os.path.join(doc_dir, "Espelho_Oficial_Processo_Antonio_Vitor.pdf")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_content(html)
    page.pdf(path=pdf_out, format="A4", print_background=True)
    browser.close()

print(f"✅ PDF Oficial do Processo gerado com sucesso: {pdf_out}")
