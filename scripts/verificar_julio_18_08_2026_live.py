# -*- coding: utf-8 -*-
"""
Varredura AO VIVO - Processos de Júlio Pereira Marcos
Data: 18/08/2026
Fontes: TJRJ 1ª Instância (Búzios), TJRJ 2ª Instância (HC / ROC), DJERJ Novo, STJ (HC 1.116.750/RJ)
"""
import os
import sys
import time
import json
import re
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')
os.environ["PYTHONIOENCODING"] = "utf-8"

from playwright.sync_api import sync_playwright

OUT_DIR = r"C:\Projetos\superJus\Clientes\Julio_Pereira_Marcos\Caso_Principal\documentos_processo\_varredura_18_08_2026"
os.makedirs(OUT_DIR, exist_ok=True)

PROCS_1A = [
    ("0023013-51.2021.8.19.0078", "1A-Desmembrado-Julio-Principal"),
    ("0001140-87.2024.8.19.0078", "1A-Apenso-Medida"),
    ("0022975-39.2021.8.19.0078", "1A-Original-Correu")
]

PROC_2A = "0029845-67.2026.8.19.0000"
STJ_REG_URL = "https://processo.stj.jus.br/processo/pesquisa/?tipoPesquisa=tipoPesquisaNumeroRegistro&termo=202603112107&totalRegistrosPorPagina=40&aplicacao=processos.ea"

results = {}

def slug(s):
    return re.sub(r'[^0-9A-Za-z._-]+', '_', s)[:120]

def save_text(path, txt):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(txt)

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

    # =========================================================================
    # 1. 1ª INSTÂNCIA TJRJ
    # =========================================================================
    for cnj, label in PROCS_1A:
        print(f"\n{'='*60}\n[TJRJ 1ª INSTÂNCIA] {label} ({cnj})\n{'='*60}")
        sub_dir = os.path.join(OUT_DIR, slug(f"{label}__{cnj}"))
        os.makedirs(sub_dir, exist_ok=True)
        try:
            page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000, wait_until="domcontentloaded")
            time.sleep(4)
            iframe_el = page.wait_for_selector("iframe#mainframe", timeout=25000)
            fr = iframe_el.content_frame()
            if not fr:
                raise RuntimeError("iframe#mainframe content_frame not found")

            fr.evaluate(f"""() => {{
                const inp = Array.from(document.querySelectorAll('input')).find(i => i.name==='numeroProcesso' || i.id==='numeroProcesso');
                if(inp){{ inp.value='{cnj}'; inp.dispatchEvent(new Event('input',{{bubbles:true}})); inp.dispatchEvent(new Event('change',{{bubbles:true}})); }}
            }}""")
            time.sleep(1)
            fr.evaluate("""() => {
                const btn = Array.from(document.querySelectorAll('button')).find(b => b.offsetWidth>0 && (b.textContent||'').toLowerCase().includes('pesquisar'));
                if(btn) btn.click();
            }""")
            time.sleep(8)

            pje = fr.evaluate("""() => {
                const el = Array.from(document.querySelectorAll('h4, div, p')).find(e => (e.innerText||'').includes('Mensagem Processo do PJe'));
                return !!el;
            }""")
            if pje:
                body = fr.inner_text("body")
                print(">> AVISO: Processo no PJe / Bloqueio")
                save_text(os.path.join(sub_dir, "espelho.txt"), body)
                results[f"1a_{label}"] = {"tipo": "pje", "texto": body}
                continue

            expanded = False
            for attempt in range(2):
                has_btn = fr.evaluate("""() => Array.from(document.querySelectorAll('button')).some(b => (b.textContent||'').toLowerCase().includes('todos os movimentos'))""")
                if has_btn:
                    fr.evaluate("""() => {
                        const btn = Array.from(document.querySelectorAll('button')).find(b => (b.textContent||'').toLowerCase().includes('todos os movimentos'));
                        if(btn) btn.click();
                    }""")
                    time.sleep(6)
                    expanded = True
                else:
                    time.sleep(2)

            body = fr.inner_text("body")
            html = fr.evaluate("document.documentElement.outerHTML")
            save_text(os.path.join(sub_dir, "espelho.txt"), body)
            save_text(os.path.join(sub_dir, "espelho.html"), html)
            try:
                page.screenshot(path=os.path.join(sub_dir, "screenshot.png"), full_page=True)
            except:
                pass

            results[f"1a_{label}"] = {
                "cnj": cnj,
                "expanded": expanded,
                "texto": body,
                "len": len(body)
            }
            print(f"Sucesso 1ª Instância {cnj}: {len(body)} chars")
            lines = [l.strip() for l in body.split('\n') if l.strip()]
            for l in lines[:25]:
                print("  >", l[:120])
        except Exception as e:
            print(f"ERRO 1ª Instância {cnj}: {e}")
            results[f"1a_{label}"] = {"erro": str(e)}

    # =========================================================================
    # 2. 2ª INSTÂNCIA TJRJ
    # =========================================================================
    print(f"\n{'='*60}\n[TJRJ 2ª INSTÂNCIA] {PROC_2A}\n{'='*60}")
    def busca_e_abre_2a(rotulo):
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000, wait_until="domcontentloaded")
        time.sleep(4)
        frame_el = page.wait_for_selector("iframe#mainframe", timeout=25000)
        frame = frame_el.content_frame()
        frame.evaluate(f"""() => {{
            const inp = Array.from(document.querySelectorAll('input')).find(i => i.name==='numeroProcesso' || i.id==='numeroProcesso');
            if(inp){{ inp.value='{PROC_2A}'; inp.dispatchEvent(new Event('input',{{bubbles:true}})); inp.dispatchEvent(new Event('change',{{bubbles:true}})); }}
        }}""")
        time.sleep(1)
        frame.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.offsetWidth>0 && (b.textContent||'').toLowerCase().includes('pesquisar'));
            if(btn) btn.click();
        }""")
        time.sleep(6)

        real_frame = page.query_selector("iframe#mainframe").content_frame()
        links = real_frame.locator("table a")
        n = links.count()
        target = None
        for i in range(n):
            t = links.nth(i).inner_text(timeout=3000)
            if rotulo in t:
                target = i
                break
        if target is None:
            return f"[{rotulo}] link não encontrado na tabela de 2ª instância"

        links.nth(target).click()
        time.sleep(6)
        real_frame = page.query_selector("iframe#mainframe").content_frame()
        try:
            btn_todos = real_frame.locator("button:has-text('Todos Os Movimentos'), a:has-text('Todos Os Movimentos')").first
            btn_todos.click(timeout=6000)
            time.sleep(4)
        except Exception:
            pass
        return real_frame.inner_text("body")

    try:
        print("Consultando HC 2026.059.10770...")
        hc_txt = busca_e_abre_2a("2026.059.10770")
        results["2a_instancia_hc"] = hc_txt
        save_text(os.path.join(OUT_DIR, "2A_HC_0029845.txt"), hc_txt)
        print(f"HC capturado: {len(hc_txt)} chars")
    except Exception as e:
        print(f"Erro HC: {e}")
        results["2a_instancia_hc"] = f"ERRO HC: {e}"

    try:
        print("Consultando ROC/RHC 2026.141.00580...")
        roc_txt = busca_e_abre_2a("2026.141.00580")
        results["2a_instancia_roc"] = roc_txt
        save_text(os.path.join(OUT_DIR, "2A_ROC_2026_141_00580.txt"), roc_txt)
        print(f"ROC capturado: {len(roc_txt)} chars")
    except Exception as e:
        print(f"Erro ROC: {e}")
        results["2a_instancia_roc"] = f"ERRO ROC: {e}"

    # =========================================================================
    # 3. DJERJ NOVO
    # =========================================================================
    print(f"\n{'='*60}\n[DJERJ NOVO] Consulta 01/08/2026 a 18/08/2026\n{'='*60}")
    dje_procs = ["0023013-51.2021.8.19.0078", "0029845-67.2026.8.19.0000", "0001140-87.2024.8.19.0078"]
    for d_cnj in dje_procs:
        dje_url = (
            f"https://www3.tjrj.jus.br/consultadje/Result.aspx"
            f"?dtInicio=01%2F08%2F2026"
            f"&dtFim=18%2F08%2F2026"
            f"&txtPesq={d_cnj}"
            f"&tipoPesq=PROC"
        )
        try:
            page.goto(dje_url, wait_until="domcontentloaded", timeout=45000)
            time.sleep(6)
            dje_txt = page.evaluate("document.body.innerText")
            results[f"djerj_{d_cnj}"] = dje_txt
            save_text(os.path.join(OUT_DIR, f"DJERJ_{d_cnj}.txt"), dje_txt)
            print(f"DJERJ {d_cnj}: {len(dje_txt)} chars | Tem publicação? {'Nenhum registro encontrado' not in dje_txt}")
        except Exception as e:
            print(f"Erro DJERJ {d_cnj}: {e}")
            results[f"djerj_{d_cnj}"] = f"ERRO: {e}"

    # =========================================================================
    # 4. STJ (HC 1.116.750/RJ)
    # =========================================================================
    print(f"\n{'='*60}\n[STJ] HC 1.116.750 / RJ (Registro 2026/0311210-7)\n{'='*60}")
    try:
        page.goto(STJ_REG_URL, wait_until="domcontentloaded", timeout=45000)
        time.sleep(6)
        stj_body = page.evaluate("document.body.innerText")
        save_text(os.path.join(OUT_DIR, "STJ_HC1116750_body.txt"), stj_body)
        try:
            page.screenshot(path=os.path.join(OUT_DIR, "STJ_screenshot.png"), full_page=True)
        except:
            pass

        for tab_name in ["Fases", "Decisões"]:
            try:
                page.evaluate(f"""(name)=> {{
                    const el = Array.from(document.querySelectorAll('a, button, li, span')).find(e=>(e.textContent||'').trim().toLowerCase()===name.toLowerCase() && e.offsetWidth>0);
                    if(el) el.click();
                }}""", tab_name)
                time.sleep(4)
                tab_txt = page.evaluate("document.body.innerText")
                save_text(os.path.join(OUT_DIR, f"STJ_tab_{tab_name}.txt"), tab_txt)
                results[f"stj_{tab_name.lower()}"] = tab_txt
            except Exception as te:
                print(f"Aviso tab STJ {tab_name}: {te}")

        results["stj_completo"] = stj_body
        print(f"STJ capturado: {len(stj_body)} chars")
    except Exception as e:
        print(f"Erro STJ: {e}")
        results["stj_completo"] = f"ERRO: {e}"

    browser.close()

json_path = os.path.join(OUT_DIR, "resultado_consolidado_18_08_2026.json")
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n=======================================================")
print(f"VARREDURA CONCLUÍDA! Arquivos salvos em:\n{OUT_DIR}")
print(f"=======================================================")
