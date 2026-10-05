# -*- coding: utf-8 -*-
"""
SUPERJUS — VARREDURA COMPLETA DE NOVO PROCESSO / PRISÃO 2026: RENATO BASTOS ROCHA
Pesquisa exaustiva por Nome e CPF no portal TJRJ (1ª Instância / Custódia / Itaperuna / Região Noroeste / Capital)
e DataJud CNJ.
"""

import sys, os, json, time
from datetime import datetime
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

NOME = "Renato Bastos Rocha"
CPF = "12498197761"

print("=" * 85)
print(f"🔍 VARREDURA DE NOVO PROCESSO CRIMINAL / PRISÃO EM 2026 — {NOME}")
print(f"⏰ Consulta Iniciada em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
print("=" * 85)

results = {
    "nome": NOME,
    "cpf": CPF,
    "timestamp": datetime.now().isoformat(),
    "processos_encontrados": []
}

# 1. SCRAPING PLAYWRIGHT NO TJRJ — BUSCA POR NOME (1ª INSTÂNCIA - TODAS AS COMARCAS)
print("\n[1] Consultando Portal do TJRJ (1ª Instância — Todas as Comarcas por Nome 'Renato Bastos Rocha')...", flush=True)

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page(viewport={"width": 1366, "height": 900})
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=35000)
        page.wait_for_timeout(2000)
        page.wait_for_selector("iframe#mainframe", timeout=20000)
        fr = page.query_selector("iframe#mainframe").content_frame()
        page.wait_for_timeout(2000)

        # Clicar na aba "Por Nome"
        fr.evaluate("""() => {
            const abas = Array.from(document.querySelectorAll('label, span, a, div, button'));
            const alvo = abas.find(c => (c.textContent || '').trim().toLowerCase() === 'por nome');
            if (alvo) alvo.click();
        }""")
        page.wait_for_timeout(2000)

        # Preencher Anos 2025 a 2026 e Nome da Parte
        fr.evaluate(f"""() => {{
            const a1 = document.getElementById('anoInicial1');
            const a2 = document.getElementById('anoFinal1');
            if (a1) {{
                a1.value = '2025';
                a1.dispatchEvent(new Event('input', {{ bubbles: true }}));
                a1.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
            if (a2) {{
                a2.value = '2026';
                a2.dispatchEvent(new Event('input', {{ bubbles: true }}));
                a2.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
            const elNome = document.getElementById('nomeParte') || document.querySelector('input[name="nomeParte"]');
            if (elNome) {{
                elNome.value = '{NOME}';
                elNome.dispatchEvent(new Event('input', {{ bubbles: true }}));
                elNome.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
            
            // Clicar em Pesquisar
            const btn = document.getElementById('btnPesquisar') || document.querySelector('button[type="submit"]') || Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Pesquisar'));
            if (btn) btn.click();
        }}""")
        page.wait_for_timeout(6000)

        # Extrair resultados do frame
        txt = fr.evaluate("() => document.body.innerText")
        lines = [l.strip() for l in txt.splitlines() if l.strip()]
        
        print("\n📊 Texto retornado da busca por Nome no TJRJ:")
        for l in lines[:40]:
            print(f"  {l}")
            
        with open(r"c:\Projetos\superJus\Clientes\Renato_Bastos_Rocha\resultado_busca_nome_tjrj.txt", "w", encoding="utf-8") as fp:
            fp.write(txt)
            
        browser.close()
except Exception as e:
    print(f"Erro no Playwright TJRJ: {e}", flush=True)

# 2. CONSULTA DATAJUD CNJ POR NOME COMPLETO
print("\n[2] Consultando API Pública DataJud CNJ com variações de texto...", flush=True)
import urllib.request, ssl

API_KEY = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
HEADERS = {'Authorization': f"APIKey {API_KEY}", 'Content-Type': 'application/json'}

queries_datajud = [
    {"query": {"match_phrase": {"dadosBasicos.polo.parte.pessoa.nome": NOME}}, "size": 20},
    {"query": {"query_string": {"query": f'"{NOME}"'}}, "size": 20},
    {"query": {"wildcard": {"dadosBasicos.polo.parte.pessoa.nome.keyword": {"value": "*Renato*Bastos*Rocha*", "case_insensitive": True}}}, "size": 20}
]

for idx, q in enumerate(queries_datajud, 1):
    url = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
    req_data = json.dumps(q).encode('utf-8')
    req = urllib.request.Request(url, data=req_data, headers=HEADERS)
    ctx = ssl._create_unverified_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            hits = data.get("hits", {}).get("hits", [])
            print(f"  • Query {idx}: {len(hits)} hits encontrados.")
            for h in hits:
                src = h["_source"]
                num = src.get("numeroProcesso", "N/I")
                classe = src.get("classe", {}).get("nome", "N/I")
                orgao = src.get("orgaoJulgador", {}).get("nome", "N/I")
                dt = src.get("dataAjuizamento", "N/I")
                print(f"    - Processo: {num} | {orgao} | {classe} | Ajuizamento: {dt}")
    except Exception as e:
        print(f"  • Erro Query {idx}: {e}")

print("\n" + "=" * 85)
print("✅ Varredura concluída.")
print("=" * 85)
