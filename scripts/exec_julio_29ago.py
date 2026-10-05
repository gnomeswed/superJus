# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import urllib.request
import re
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
os.environ["PYTHONIOENCODING"] = "utf-8"

DATAJUD_API_KEY = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
HEADERS = {
    'Authorization': f'APIKey {DATAJUD_API_KEY}',
    'Content-Type': 'application/json'
}

OUT_DIR = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"
os.makedirs(OUT_DIR, exist_ok=True)

PROCS_1A = [
    ("0023013-51.2021.8.19.0078", "00230135120218190078", "1A_Principal_Julio", "Ação Penal Desmembrada - 2ª Vara Búzios"),
    ("0001140-87.2024.8.19.0078", "00011408720248190078", "1A_Apenso_RSE", "Recurso em Sentido Estrito / Apenso Búzios"),
    ("0022975-39.2021.8.19.0078", "00229753920218190078", "1A_Original_Desmembrado", "Processo Originário / Co-réus Búzios")
]

PROC_2A = "0029845-67.2026.8.19.0000"
PROC_2A_CLEAN = "00298456720268190000"
STJ_URL = "https://processo.stj.jus.br/processo/pesquisa/?tipoPesquisa=tipoPesquisaNumeroRegistro&termo=202603112107&totalRegistrosPorPagina=40&aplicacao=processos.ea"

print("="*80)
print("=== CONSULTA AO VIVO ONLINE — JÚLIO PEREIRA MARCOS (29/08/2026) ===")
print("="*80)

def parse_movements(text):
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    loc = "Não identificada"
    movs = []
    for i, l in enumerate(lines):
        if "Localização na Serventia" in l and i+1 < len(lines):
            loc = lines[i+1]
        if "Tipo do Movimento:" in l:
            bloco = lines[i:min(len(lines), i+8)]
            movs.append(" | ".join(bloco))
    return loc, movs

report = {
    "data_consulta": "29/08/2026 22:56",
    "1a_instancia": {},
    "2a_instancia": {},
    "stj": {}
}

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--disable-blink-features=AutomationControlled", "--no-sandbox", "--disable-dev-shm-usage"]
    )
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        viewport={"width": 1366, "height": 900},
        locale="pt-BR"
    )
    ctx.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    page = ctx.new_page()

    # 1. PRIMEIRA INSTÂNCIA TJRJ
    for cnj, clean, tag, desc in PROCS_1A:
        print(f"\n--- [1ª Instância] Consultando {cnj} ({desc}) ---")
        url_1a = f"http://www4.tjrj.jus.br/consultaProcessoWebV2/consultaMov.do?v=2&numProcesso={cnj}&tipoConsulta=publica"
        try:
            page.goto(url_1a, wait_until="domcontentloaded", timeout=25000)
            time.sleep(3)
            txt = page.inner_text("body")
            
            with open(os.path.join(OUT_DIR, f"julio_tjrj_{tag}_29ago.txt"), "w", encoding="utf-8") as f:
                f.write(txt)
                
            loc, movs = parse_movements(txt)
            print(f"   • Localização na Serventia: {loc}")
            print(f"   • Total de movimentos capturados: {len(movs)}")
            if movs:
                print(f"   • Último Movimento: {movs[0][:150]}")
                
            report["1a_instancia"][cnj] = {
                "descricao": desc,
                "localizacao": loc,
                "total_movs": len(movs),
                "ultimos_movs": movs[:3]
            }
        except Exception as e:
            print(f"   ❌ Erro ao consultar {cnj}: {e}")
            report["1a_instancia"][cnj] = {"erro": str(e)}

    # 2. SEGUNDA INSTÂNCIA TJRJ (HC / ROC)
    print(f"\n--- [2ª Instância] Consultando HC {PROC_2A} (7ª Câmara) ---")
    url_2a = f"http://www4.tjrj.jus.br/consultaProcessoWebV2/consultaMov.do?v=2&numProcesso={PROC_2A}&tipoConsulta=publica"
    try:
        page.goto(url_2a, wait_until="domcontentloaded", timeout=25000)
        time.sleep(3)
        txt_2a = page.inner_text("body")
        
        with open(os.path.join(OUT_DIR, "julio_tjrj_2A_HC_29ago.txt"), "w", encoding="utf-8") as f:
            f.write(txt_2a)
            
        loc_2a, movs_2a = parse_movements(txt_2a)
        print(f"   • Localização na Serventia (2ª Instância): {loc_2a}")
        print(f"   • Total de movimentos: {len(movs_2a)}")
        if movs_2a:
            print(f"   • Último Movimento: {movs_2a[0][:150]}")
            
        report["2a_instancia"][PROC_2A] = {
            "localizacao": loc_2a,
            "total_movs": len(movs_2a),
            "ultimos_movs": movs_2a[:3]
        }
    except Exception as e:
        print(f"   ❌ Erro ao consultar HC 2ª Instância: {e}")
        report["2a_instancia"][PROC_2A] = {"erro": str(e)}

    # 3. STJ (HC 1.116.750 / 202603112107)
    print(f"\n--- [STJ] Consultando RHC HC 1.116.750 / RJ (Registro 2026/0311210-7) ---")
    try:
        page.goto(STJ_URL, wait_until="domcontentloaded", timeout=40000)
        time.sleep(6)
        
        # Clica no processo se estiver na lista
        page.evaluate("""() => {
            const links = document.querySelectorAll('a, span, td');
            for(const el of links) {
                if((el.textContent||'').includes('1116750') && el.offsetParent !== null) {
                    el.click(); return true;
                }
            }
            return false;
        }""")
        time.sleep(6)
        
        stj_txt = page.inner_text("body")
        stj_html = page.content()
        
        with open(os.path.join(OUT_DIR, "julio_stj_live_direct_29ago.txt"), "w", encoding="utf-8") as f:
            f.write(stj_txt)
        with open(os.path.join(OUT_DIR, "julio_stj_live_direct_29ago.html"), "w", encoding="utf-8") as f:
            f.write(stj_html)
            
        print(f"   • STJ capturado! ({len(stj_txt)} caracteres)")
        
        # Parse STJ key phases
        stj_lines = [l.strip() for l in stj_txt.splitlines() if l.strip()]
        fases = []
        for i, l in enumerate(stj_lines):
            if re.match(r'^\d{2}/\d{2}/\d{4}', l):
                fases.append(f"{l} - {stj_lines[i+1] if i+1 < len(stj_lines) else ''}")
                
        print(f"   • Fases capturadas no STJ: {len(fases)}")
        for f_item in fases[:5]:
            print(f"     -> {f_item[:120]}")
            
        report["stj"] = {
            "registro": "2026/0311210-7",
            "processo": "HC 1.116.750 / RJ",
            "relator": "Min. Og Fernandes - 6ª Turma",
            "total_fases": len(fases),
            "ultimas_fases": fases[:5]
        }
    except Exception as e:
        print(f"   ❌ Erro ao consultar STJ: {e}")
        report["stj"] = {"erro": str(e)}

    browser.close()

# Salvar relatório consolidado em JSON e Markdown
report_json_path = os.path.join(r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\07_RELATORIOS_ESTRATEGICOS_E_ANALISES", "andamento_julio_29_08_2026.json")
os.makedirs(os.path.dirname(report_json_path), exist_ok=True)
with open(report_json_path, "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print("\n" + "="*80)
print(f"🎉 RELATÓRIO AO VIVO CONCLUÍDO COM SUCESSO! Salvo em: {report_json_path}")
print("="*80)
