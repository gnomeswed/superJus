# -*- coding: utf-8 -*-
"""
SUPERJUS — BUSCA ONLINE DE AUDIÊNCIA DO PASTOR JUNEO
Processo: 0810659-95.2026.8.19.0203
Nome: Juneo Luciano de Oliveira
Vara: 2ª Vara Criminal da Regional de Jacarepaguá
"""

import sys, time, os
from datetime import datetime
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

proc_fmt = "0810659-95.2026.8.19.0203"
proc_clean = "08106599520268190203"
nome = "Juneo Luciano de Oliveira"

print("=" * 85)
print(f"🔍 VERIFICAÇÃO ONLINE DE AUDIÊNCIA — PASTOR JUNEO")
print(f"⚖️ Processo: {proc_fmt} | Réu: {nome}")
print(f"⏰ Consulta: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
print("=" * 85)

results = {}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    page = browser.new_page(viewport={"width": 1280, "height": 850})

    # 1. Consulta no Portal do DJERJ
    print("\n[1] Consultando publicações no DJERJ (Diário da Justiça Eletrônico do RJ)...", flush=True)
    try:
        url_djerj = "https://www3.tjrj.jus.br/consultadjerj/consulta.aspx"
        page.goto(url_djerj, timeout=25000)
        time.sleep(2)
        
        # Preencher processo
        inp = page.query_selector("input[id*='txtProcesso'], input[name*='Processo'], input[id*='Processo']")
        if inp:
            inp.fill(proc_fmt)
            time.sleep(1)
            btn = page.query_selector("input[type='submit'], input[value*='Pesquisar'], button:has-text('Pesquisar')")
            if btn:
                btn.click()
                time.sleep(5)
                
        txt_djerj = page.inner_text("body")
        lines_djerj = [l.strip() for l in txt_djerj.splitlines() if l.strip()]
        results["djerj_processo"] = lines_djerj[:35]
        print(f"  ✓ Retorno DJERJ pelo número ({len(lines_djerj)} linhas):")
        for l in lines_djerj[:15]:
            print(f"    • {l}")
    except Exception as e:
        print(f"  ✗ Erro DJERJ: {e}")
        results["djerj_erro"] = str(e)

    # 2. Consulta pelo nome no DJERJ
    print("\n[2] Consultando por Nome 'Juneo Luciano de Oliveira' no DJERJ...", flush=True)
    try:
        url_djerj = "https://www3.tjrj.jus.br/consultadjerj/consulta.aspx"
        page.goto(url_djerj, timeout=25000)
        time.sleep(2)
        
        inp_nome = page.query_selector("input[id*='txtNome'], input[name*='Nome'], input[id*='Parte']")
        if inp_nome:
            inp_nome.fill(nome)
            time.sleep(1)
            btn = page.query_selector("input[type='submit'], input[value*='Pesquisar'], button:has-text('Pesquisar')")
            if btn:
                btn.click()
                time.sleep(5)
                
        txt_djerj_nome = page.inner_text("body")
        lines_djerj_nome = [l.strip() for l in txt_djerj_nome.splitlines() if l.strip()]
        results["djerj_nome"] = lines_djerj_nome[:35]
        print(f"  ✓ Retorno DJERJ por nome ({len(lines_djerj_nome)} linhas):")
        for l in lines_djerj_nome[:15]:
            print(f"    • {l}")
    except Exception as e:
        print(f"  ✗ Erro DJERJ Nome: {e}")

    # 3. Consulta no Portal de Consulta Pública TJRJ
    print("\n[3] Consultando no Portal de Consulta Pública TJRJ...", flush=True)
    try:
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=20000)
        time.sleep(2)
        fr = page.query_selector("iframe#mainframe").content_frame()
        fr.evaluate(f"""() => {{
            const el = document.getElementById('numeroProcesso') || document.querySelector('input[type="text"]');
            if (el) {{
                el.value = '{proc_clean}';
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                el.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
            const btn = document.getElementById('btnPesquisar') || document.querySelector('button[type="submit"]');
            if (btn) btn.click();
        }}""")
        time.sleep(5)
        txt_tjrj = fr.evaluate("() => document.body.innerText")
        lines_t = [l.strip() for l in txt_tjrj.splitlines() if l.strip()]
        results["tjrj_portal"] = lines_t[:40]
        print(f"  ✓ Retorno Portal TJRJ ({len(lines_t)} linhas):")
        for l in lines_t[:20]:
            print(f"    • {l}")
    except Exception as e:
        print(f"  ✗ Erro Portal TJRJ: {e}")
        results["tjrj_portal_erro"] = str(e)

    browser.close()

with open(r"c:\Projetos\superJus\Clientes\Pastor_Juneo\resultado_verificacao_audiencia_online.json", "w", encoding="utf-8") as fp:
    json.dump(results, fp, indent=2, ensure_ascii=False)

print("\n" + "=" * 85)
print("✅ Varredura online concluída.")
print("=" * 85)
