# -*- coding: utf-8 -*-
"""
SUPERJUS — VERIFICADOR LIVE DE ATUALIZAÇÕES DO PROCESSO DE LUCAS DE SOUZA FREITAS
Consulta em tempo real:
1. DataJud API (CNJ / TJRJ) - Movimentações de 1ª e 2ª Instância
2. TJRJ Portal Web (2ª Câmara Criminal / Apelação / Parecer PGJ)
3. DJERJ (Diário da Justiça Eletrônico)
"""

import sys, os, json, time, urllib.request
from datetime import datetime
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

proc_num_clean = "00118579520248190002"
proc_fmt = "0011857-95.2024.8.19.0002"

results = {
    "timestamp": datetime.now().strftime("%d/%m/%Y às %H:%M:%S"),
    "processo": proc_fmt,
    "datajud": {},
    "tjrj_web_2inst": {},
    "novidades": []
}

# ============================================================
# 1. CONSULTA DATAJUD CNJ / TJRJ
# ============================================================
print("🔍 1. Consultando API DataJud CNJ/TJRJ...")
try:
    sys.path.append(r"c:\Projetos\superJus")
    from core.config import datajud_headers
    headers = datajud_headers()
except Exception:
    headers = {
        'Authorization': 'APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTkxScUZSV南海',
        'Content-Type': 'application/json'
    }

url = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'
req_data = json.dumps({"query": {"match": {"numeroProcesso": proc_num_clean}}, "size": 10}).encode('utf-8')
req = urllib.request.Request(url, data=req_data, headers=headers)

try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        hits = data.get('hits', {}).get('hits', [])
        results["datajud"]["total_hits"] = len(hits)
        results["datajud"]["detalhes"] = []
        for hit in hits:
            src = hit['_source']
            classe = src.get('classe', {}).get('nome', 'N/I')
            orgao = src.get('orgaoJulgador', {}).get('nome', 'N/I')
            dt_at = src.get('dataHoraUltimaAtualizacao', 'N/I')
            grau = src.get('grau', 'N/I')
            movs = src.get('movimentos', [])
            movs_sorted = sorted(movs, key=lambda m: m.get('dataHora', ''), reverse=True)
            
            top_movs = []
            for m in movs_sorted[:8]:
                dt = m.get('dataHora', '')
                nome = m.get('nome', '')
                code = m.get('codigo', '')
                comps = m.get('complementosTabelados', [])
                comp_str = " (" + ", ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in comps]) + ")" if comps else ""
                top_movs.append({
                    "dataHora": dt,
                    "nome": nome,
                    "codigo": code,
                    "complemento": comp_str
                })
                
            results["datajud"]["detalhes"].append({
                "grau": grau,
                "classe": classe,
                "orgao": orgao,
                "ultima_atualizacao": dt_at,
                "total_movimentos": len(movs),
                "ultimas_movimentacoes": top_movs
            })
            print(f"  ✓ DataJud OK: Grau {grau} | {orgao} | {len(movs)} movimentos")
except Exception as e:
    results["datajud"]["erro"] = str(e)
    print(f"  ✗ Erro DataJud: {e}")

# ============================================================
# 2. CONSULTA WEB TJRJ VIA PLAYWRIGHT
# ============================================================
print("🔍 2. Consultando Portal do TJRJ (Web 1ª e 2ª Instância)...")
try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_context(viewport={"width": 1366, "height": 900}).new_page()
        
        # Consulta Direta do Número do Processo no TJRJ
        target_url = f"https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica#processo={proc_num_clean}"
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=30000)
        time.sleep(2)
        page.wait_for_selector("iframe#mainframe", timeout=20000)
        fr = page.query_selector("iframe#mainframe").content_frame()
        time.sleep(2)
        
        # Preencher campo de pesquisa
        fr.evaluate(f"""() => {{
            const el = document.getElementById('numeroProcesso') || document.querySelector('input[name="numProcesso"]') || document.querySelector('input[type="text"]');
            if (el) {{
                el.value = '{proc_num_clean}';
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                el.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
            const btn = document.getElementById('btnPesquisar') || document.querySelector('button[type="submit"]') || Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Pesquisar'));
            if (btn) btn.click();
        }}""")
        time.sleep(4)
        
        # Capturar texto do frame
        frame_text = fr.evaluate("() => document.body.innerText")
        results["tjrj_web_2inst"]["status"] = "OK"
        results["tjrj_web_2inst"]["resumo_web"] = frame_text[:2500] if frame_text else "Sem retorno textual"
        print("  ✓ TJRJ Web consultado com sucesso")
        browser.close()
except Exception as e:
    results["tjrj_web_2inst"]["erro"] = str(e)
    print(f"  ✗ Erro TJRJ Web: {e}")

# Salvar snapshot do resultado
output_json = Path(r"c:\Projetos\superJus\Clientes\Lucas_Freitas\03_Documentos_do_Processo\_varredura_21_08_2026\resultado_lucas_live.json")
output_json.parent.mkdir(parents=True, exist_ok=True)
with open(output_json, "w", encoding="utf-8") as fp:
    json.dump(results, fp, indent=2, ensure_ascii=False)

print("\n" + "=" * 80)
print(f"📊 RELATÓRIO DE VARREDURA AO VIVO — LUCAS DE SOUZA FREITAS")
print(f"⏰ Consulta Realizada em: {results['timestamp']}")
print(f"⚖️ Processo: {proc_fmt}")
print("=" * 80)

for d in results.get("datajud", {}).get("detalhes", []):
    print(f"\n🏛️ Órgão: {d['orgao']} ({d['classe']}) — Grau: {d['grau']}")
    print(f"🔄 Última Atualização no Banco: {d['ultima_atualizacao']}")
    print(f"📑 Total de Movimentações: {d['total_movimentos']}")
    print("Últimos atos registrados:")
    for m in d["ultimas_movimentacoes"]:
        print(f"  • {m['dataHora'][:19].replace('T', ' ')} — {m['nome']}{m['complemento']}")

print("\n" + "=" * 80)
