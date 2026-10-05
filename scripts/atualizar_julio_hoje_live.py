# -*- coding: utf-8 -*-
"""
Atualização Online em Tempo Real — Júlio Pereira Marcos (Data: 05/09/2026)
========================================================================
Varredura completa em todas as instâncias:
- TJRJ 1ª Instância (Búzios - Ação Penal Desmembrada 0023013-51.2021.8.19.0078 e apenso)
- TJRJ 2ª Instância (7ª Câmara Criminal / 2VP 0029845-67.2026.8.19.0000)
- DJERJ (Publicações de 25/08/2026 a 05/09/2026)
- STJ 6ª Turma (HC 1.116.750 / RJ - Min. Og Fernandes)
"""

import os
import sys
import time
import json
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
os.environ["PYTHONIOENCODING"] = "utf-8"

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

OUT_DIR = ROOT_DIR / "Clientes" / "Júlio_Pereira_Marcos" / "Caso_Principal" / "documentos_processo"
OUT_DIR.mkdir(parents=True, exist_ok=True)

PROCS_1A = [
    ("0023013-51.2021.8.19.0078", "1A_Principal_Julio", "Ação Penal Desmembrada - 2ª Vara Búzios"),
    ("0001140-87.2024.8.19.0078", "1A_Apenso_RSE", "Recurso em Sentido Estrito / Apenso Búzios"),
    ("0022975-39.2021.8.19.0078", "1A_Original_Desmembrado", "Processo Originário / Co-réus Búzios")
]

PROC_2A = "0029845-67.2026.8.19.0000"
STJ_URL = "https://processo.stj.jus.br/processo/pesquisa/?tipoPesquisa=tipoPesquisaNumeroRegistro&termo=202603112107&totalRegistrosPorPagina=40&aplicacao=processos.ea"

print("=" * 80)
print("🔍 CONSULTA AO VIVO EM TEMPO REAL — JÚLIO PEREIRA MARCOS (05/09/2026)")
print("=" * 80)

def parse_movements(text):
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    loc = "Não identificada"
    movs = []
    for i, l in enumerate(lines):
        if "Localização na Serventia" in l and i + 1 < len(lines):
            loc = lines[i + 1]
        if "Tipo do Movimento:" in l:
            bloco = lines[i:min(len(lines), i + 8)]
            movs.append(" | ".join(bloco))
    return loc, movs

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
    ctx.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    page = ctx.new_page()

    # -------------------------------------------------------------------------
    # 1. TJRJ 1ª INSTÂNCIA - BÚZIOS
    # -------------------------------------------------------------------------
    print("\n------------------------------------------------------------")
    print("1. TJRJ 1ª INSTÂNCIA - BÚZIOS (CONSULTA AO VIVO)")
    print("------------------------------------------------------------")
    for cnj, label, desc in PROCS_1A:
        print(f"\n>>> Consultando: {desc} ({cnj})...")
        try:
            page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=50000, wait_until="domcontentloaded")
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
            time.sleep(7)

            body_txt = frame.inner_text("body")
            loc, movs = parse_movements(body_txt)
            print(f"Localização na Serventia: {loc}")
            print(f"Total de Blocos de Movimento: {body_txt.count('Tipo do Movimento:')}")
            print("Últimos Movimentos:")
            for m in movs[:4]:
                print(f"  * {m}")

            out_file = OUT_DIR / f"julio_tjrj_{label}_05set.txt"
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(body_txt)
        except Exception as e:
            print(f"⚠️ Erro ao consultar {cnj}: {e}")

    # -------------------------------------------------------------------------
    # 2. TJRJ 2ª INSTÂNCIA - 7ª CÂMARA CRIMINAL / 2VP
    # -------------------------------------------------------------------------
    print("\n------------------------------------------------------------")
    print("2. TJRJ 2ª INSTÂNCIA - 7ª CÂMARA CRIMINAL / 2VP (CONSULTA AO VIVO)")
    print("------------------------------------------------------------")
    for sub_target, sub_label, sub_desc in [
        ("2026.059.10770", "2A_HC_10770", "Habeas Corpus - 7ª Câmara Criminal"),
        ("2026.141.00580", "2A_ROC_00580", "Recurso Ordinário Constitucional - 2ª Vice-Presidência")
    ]:
        print(f"\n>>> Consultando: {sub_desc} ({sub_target})...")
        try:
            page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=50000, wait_until="domcontentloaded")
            time.sleep(3)
            iframe_el = page.wait_for_selector("iframe#mainframe", timeout=30000)
            frame = iframe_el.content_frame()
            time.sleep(2)
            frame.evaluate(f"""() => {{
                const inp = Array.from(document.querySelectorAll('input')).find(i => i.name==='numeroProcesso' || i.id==='numeroProcesso');
                if(inp) {{
                    inp.value = '{PROC_2A}';
                    inp.dispatchEvent(new Event('input', {{bubbles:true}}));
                    inp.dispatchEvent(new Event('change', {{bubbles:true}}));
                }}
            }}""")
            time.sleep(1)
            frame.evaluate("""() => {
                const btn = Array.from(document.querySelectorAll('button')).find(b => b.offsetWidth>0 && (b.textContent||'').toLowerCase().includes('pesquisar'));
                if(btn) btn.click();
            }""")
            time.sleep(6)

            frame.evaluate(f"""(target) => {{
                const links = Array.from(document.querySelectorAll('table a, .table a, a'));
                const l = links.find(a => (a.textContent||'').includes(target));
                if(l) l.click();
            }}""", sub_target)
            time.sleep(6)

            proc_txt = frame.inner_text("body")
            loc_2, movs_2 = parse_movements(proc_txt)
            print(f"Localização na Serventia: {loc_2}")
            print(f"Total de Blocos de Movimento: {proc_txt.count('Tipo do Movimento:')}")
            print("Últimos Movimentos:")
            for m in movs_2[:4]:
                print(f"  * {m}")

            out_file = OUT_DIR / f"julio_tjrj_{sub_label}_05set.txt"
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(proc_txt)
        except Exception as e:
            print(f"⚠️ Erro ao consultar {sub_label}: {e}")

    # -------------------------------------------------------------------------
    # 3. DJERJ - DIÁRIO DA JUSTIÇA RJ (25/08/2026 até 05/09/2026)
    # -------------------------------------------------------------------------
    print("\n------------------------------------------------------------")
    print("3. DJERJ - DIÁRIO DA JUSTIÇA RJ (25/08/2026 até 05/09/2026)")
    print("------------------------------------------------------------")
    for q in ["0023013-51.2021.8.19.0078", "0029845-67.2026.8.19.0000", "0001140-87.2024.8.19.0078", "Julio Pereira Marcos"]:
        is_name = (q == "Julio Pereira Marcos")
        safe_type = "NOME" if is_name else "PROC"
        safe_param = "Julio%20Pereira%20Marcos" if is_name else q
        dje_url = f"https://www3.tjrj.jus.br/consultadje/Result.aspx?dtInicio=25%2F08%2F2026&dtFim=05%2F09%2F2026&txtPesq={safe_param}&tipoPesq={safe_type}"
        try:
            page.goto(dje_url, timeout=35000, wait_until="domcontentloaded")
            time.sleep(4)
            txt = page.evaluate("document.body.innerText")
            has_pub = "Não foram encontradas" not in txt and "Nenhum registro encontrado" not in txt and "0 registros" not in txt.lower()
            print(f"Consulta [{q}]: {'🚨 PUBLICAÇÃO LOCALIZADA NO DJERJ!' if has_pub else '✅ Nenhuma publicação pendente'}")
        except Exception as e:
            print(f"⚠️ Erro DJERJ {q}: {e}")

    # -------------------------------------------------------------------------
    # 4. STJ - BRASÍLIA (HC 1.116.750 / RJ - 6ª TURMA - REL. MIN. OG FERNANDES)
    # -------------------------------------------------------------------------
    print("\n------------------------------------------------------------")
    print("4. STJ - BRASÍLIA (HC 1.116.750 / RJ - 6ª TURMA)")
    print("------------------------------------------------------------")
    try:
        page.goto(STJ_URL, timeout=50000, wait_until="domcontentloaded")
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
        time.sleep(6)

        stj_txt = page.evaluate("document.body.innerText")
        out_stj = OUT_DIR / "julio_stj_live_direct_05set.txt"
        with open(out_stj, "w", encoding="utf-8") as f:
            f.write(stj_txt)

        stj_lines = [l.strip() for l in stj_txt.split('\n') if l.strip()]
        for l in stj_lines:
            if any(k in l.upper() for k in ["ÚLTIMA FASE", "CONCLUSOS", "DECISÃO", "JULGAMENTO", "LOCALIZAÇÃO", "RELATOR", "MINISTRO", "PETIÇÃO", "PARECER"]):
                print(f"  • {l}")
    except Exception as e:
        print(f"⚠️ Erro STJ: {e}")

    browser.close()

print("\n" + "=" * 80)
print("✅ VARREDURA AO VIVO DO CASO JÚLIO PEREIRA MARCOS CONCLUÍDA")
print("=" * 80)
