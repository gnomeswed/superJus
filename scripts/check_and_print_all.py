# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import re
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

PROCS_1A = [
    ("0023013-51.2021.8.19.0078", "1A_Principal_Julio", "Acao Penal Desmembrada - 2a Vara Buzios"),
    ("0001140-87.2024.8.19.0078", "1A_Apenso_RSE", "Recurso em Sentido Estrito / Apenso Buzios"),
    ("0022975-39.2021.8.19.0078", "1A_Original_Desmembrado", "Processo Originario / Co-reus Buzios")
]
PROC_2A = "0029845-67.2026.8.19.0000"
STJ_URL = "https://processo.stj.jus.br/processo/pesquisa/?tipoPesquisa=tipoPesquisaNumeroRegistro&termo=202603112107&totalRegistrosPorPagina=40&aplicacao=processos.ea"

print("================================================================================")
print("=== CONSULTA COMPLETA ONLINE AO VIVO TJRJ E STJ - JÚLIO (25/08/2026) ===")
print("================================================================================")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
    ctx = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36", locale="pt-BR")
    page = ctx.new_page()

    # 1. 1ª INSTANCIA
    for cnj, label, desc in PROCS_1A:
        print(f"\n==================== [1ª INSTÂNCIA] {desc} ({cnj}) ====================")
        try:
            page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000)
            time.sleep(3)
            frame = page.wait_for_selector("iframe#mainframe", timeout=25000).content_frame()
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
            
            body = frame.inner_text("body")
            lines = [l.strip() for l in body.split('\n') if l.strip()]
            for idx, l in enumerate(lines):
                if "Localização na Serventia" in l:
                    print(f">> LOCALIZAÇÃO: {lines[idx+1] if idx+1 < len(lines) else 'N/A'}")
                if "Tipo do Movimento:" in l:
                    chunk = lines[idx:min(len(lines), idx+8)]
                    print(f">> MOVIMENTO: {' | '.join(chunk)}")
        except Exception as e:
            print(f"Erro em {cnj}: {e}")

    # 2. 2ª INSTANCIA
    for sub_target, sub_label, sub_desc in [
        ("2026.059.10770", "2A_HC_10770", "Habeas Corpus - 7ª Câmara Criminal"),
        ("2026.141.00580", "2A_ROC_00580", "Recurso Ordinário Constitucional - 2ª Vice-Presidência")
    ]:
        print(f"\n==================== [2ª INSTÂNCIA] {sub_desc} ({sub_target}) ====================")
        try:
            page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000)
            time.sleep(3)
            frame = page.wait_for_selector("iframe#mainframe", timeout=25000).content_frame()
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
            time.sleep(7)

            frame.evaluate(f"""(target) => {{
                const links = Array.from(document.querySelectorAll('table a, .table a, a'));
                const l = links.find(a => (a.textContent||'').includes(target));
                if(l) l.click();
            }}""", sub_target)
            time.sleep(6)

            body = frame.inner_text("body")
            lines = [l.strip() for l in body.split('\n') if l.strip()]
            for idx, l in enumerate(lines):
                if "Localização na Serventia" in l:
                    print(f">> LOCALIZAÇÃO: {lines[idx+1] if idx+1 < len(lines) else 'N/A'}")
                if "Tipo do Movimento:" in l:
                    chunk = lines[idx:min(len(lines), idx+8)]
                    print(f">> MOVIMENTO: {' | '.join(chunk)}")
        except Exception as e:
            print(f"Erro em {sub_label}: {e}")

    # 3. DJERJ
    print("\n==================== [DJERJ - DIÁRIO DA JUSTIÇA RJ] ====================")
    for q in ["0023013-51.2021.8.19.0078", "0029845-67.2026.8.19.0000", "0001140-87.2024.8.19.0078", "Julio Pereira Marcos"]:
        is_name = (q == "Julio Pereira Marcos")
        safe_type = "NOME" if is_name else "PROC"
        safe_param = "Julio%20Pereira%20Marcos" if is_name else q
        dje_url = f"https://www3.tjrj.jus.br/consultadje/Result.aspx?dtInicio=15%2F08%2F2026&dtFim=25%2F08%2F2026&txtPesq={safe_param}&tipoPesq={safe_type}"
        try:
            page.goto(dje_url, timeout=35000)
            time.sleep(4)
            txt = page.evaluate("document.body.innerText")
            has_pub = "Não foram encontradas" not in txt and "Nenhum registro encontrado" not in txt and "0 registros" not in txt.lower()
            print(f">> DJERJ [{q}]: {'🚨 PUBLICAÇÃO ENCONTRADA!' if has_pub else '✅ Sem publicações no período (15 a 25/08/2026)'}")
            if has_pub:
                print(txt[:1000])
        except Exception as e:
            print(f"Erro DJERJ {q}: {e}")

    # 4. STJ
    print("\n==================== [STJ - BRASÍLIA - HC 1.116.750 / RJ] ====================")
    try:
        page.goto(STJ_URL, timeout=45000)
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
        lines = [l.strip() for l in stj_txt.split('\n') if l.strip()]
        for l in lines:
            if any(k in l.upper() for k in ["ÚLTIMA FASE", "CONCLUSOS", "DECISÃO", "JULGAMENTO", "LOCALIZAÇÃO", "RELATOR", "MINISTRO", "PARECER"]):
                print(f">> STJ: {l}")
    except Exception as e:
        print(f"Erro STJ: {e}")

    browser.close()

print("\n================================================================================")
print("=== FIM DA CONSULTA ===")
print("================================================================================")
