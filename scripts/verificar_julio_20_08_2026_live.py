# -*- coding: utf-8 -*-
"""
Varredura AO VIVO - Processos de Júlio Pereira Marcos
Data: 20/08/2026
Fontes: TJRJ 1ª Instância (Búzios), TJRJ 2ª Instância (HC / ROC), DJERJ Novo, STJ (HC 1.116.750/RJ)
"""
import os
import sys
import time
import json
import re

sys.stdout.reconfigure(encoding='utf-8')
os.environ["PYTHONIOENCODING"] = "utf-8"

from playwright.sync_api import sync_playwright

OUT_DIR = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo\_varredura_20_08_2026"
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
    # 1. 1ª INSTÂNCIA TJRJ (BÚZIOS)
    # =========================================================================
    for cnj, label in PROCS_1A:
        print(f"\n{'='*60}\n[TJRJ 1ª INSTÂNCIA] {label} ({cnj})\n{'='*60}", flush=True)
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
                print(">> AVISO: Processo no PJe / Bloqueio", flush=True)
                save_text(os.path.join(sub_dir, "espelho.txt"), body)
                results[f"1a_{label}"] = {"tipo": "pje", "texto": body}
                continue

            expanded = False
            for attempt in range(2):
                has_btn = fr.evaluate("""() => Array.from(document.querySelectorAll('button, a')).some(b => (b.textContent||'').toLowerCase().includes('todos os movimentos'))""")
                if has_btn:
                    fr.evaluate("""() => {
                        const btn = Array.from(document.querySelectorAll('button, a')).find(b => (b.textContent||'').toLowerCase().includes('todos os movimentos'));
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

            loc, movs = parse_movements(body)
            results[f"1a_{label}"] = {
                "cnj": cnj,
                "expanded": expanded,
                "localizacao": loc,
                "movimentos": movs[:10],
                "len": len(body),
                "texto_completo": body
            }
            print(f"Status {cnj}: Local: {loc} | Total Movs: {body.count('Tipo do Movimento:')}", flush=True)
            print("--- Primeiros Movimentos Recentes ---", flush=True)
            for m in movs[:5]:
                print(f"  * {m}", flush=True)
        except Exception as e:
            print(f"ERRO 1ª Instância {cnj}: {e}", flush=True)
            results[f"1a_{label}"] = {"erro": str(e)}

    # =========================================================================
    # 2. 2ª INSTÂNCIA TJRJ (HABEAS CORPUS / RECURSO ORDINÁRIO)
    # =========================================================================
    print(f"\n{'='*60}\n[TJRJ 2ª INSTÂNCIA] {PROC_2A}\n{'='*60}", flush=True)
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
        time.sleep(7)

        real_frame = page.query_selector("iframe#mainframe").content_frame()
        table_html = real_frame.inner_text("body")
        
        links = real_frame.locator("table a, .table a, tbody tr td a")
        n = links.count()
        print(f"Links encontrados na tabela: {n}", flush=True)
        
        target = None
        for i in range(n):
            t = links.nth(i).inner_text(timeout=3000)
            if rotulo in t:
                target = i
                break
        if target is None:
            return f"[{rotulo}] link não encontrado na tabela de 2ª instância. Conteúdo tabela:\n{table_html[:2000]}"

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
        print("Consultando HC 2026.059.10770...", flush=True)
        hc_txt = busca_e_abre_2a("2026.059.10770")
        results["2a_instancia_hc"] = hc_txt
        save_text(os.path.join(OUT_DIR, "2A_HC_0029845.txt"), hc_txt)
        loc_hc, movs_hc = parse_movements(hc_txt)
        print(f"HC 2ª Instância - Local: {loc_hc} | Chars: {len(hc_txt)}", flush=True)
        for m in movs_hc[:3]:
            print(f"  * {m}", flush=True)
    except Exception as e:
        print(f"Erro HC: {e}", flush=True)
        results["2a_instancia_hc"] = f"ERRO HC: {e}"

    try:
        print("Consultando ROC/RHC 2026.141.00580...", flush=True)
        roc_txt = busca_e_abre_2a("2026.141.00580")
        results["2a_instancia_roc"] = roc_txt
        save_text(os.path.join(OUT_DIR, "2A_ROC_2026_141_00580.txt"), roc_txt)
        loc_roc, movs_roc = parse_movements(roc_txt)
        print(f"ROC 2ª Instância - Local: {loc_roc} | Chars: {len(roc_txt)}", flush=True)
        for m in movs_roc[:3]:
            print(f"  * {m}", flush=True)
    except Exception as e:
        print(f"Erro ROC: {e}", flush=True)
        results["2a_instancia_roc"] = f"ERRO ROC: {e}"

    # =========================================================================
    # 3. DJERJ NOVO (DIÁRIO DA JUSTIÇA ELETRÔNICO DO TJRJ)
    # =========================================================================
    print(f"\n{'='*60}\n[DJERJ NOVO] Consulta 15/08/2026 a 20/08/2026\n{'='*60}", flush=True)
    dje_procs = ["0023013-51.2021.8.19.0078", "0029845-67.2026.8.19.0000", "0001140-87.2024.8.19.0078", "0022975-39.2021.8.19.0078"]
    for d_cnj in dje_procs:
        dje_url = (
            f"https://www3.tjrj.jus.br/consultadje/Result.aspx"
            f"?dtInicio=15%2F08%2F2026"
            f"&dtFim=20%2F08%2F2026"
            f"&txtPesq={d_cnj}"
            f"&tipoPesq=PROC"
        )
        try:
            page.goto(dje_url, wait_until="domcontentloaded", timeout=45000)
            time.sleep(5)
            dje_txt = page.evaluate("document.body.innerText")
            results[f"djerj_{d_cnj}"] = dje_txt
            save_text(os.path.join(OUT_DIR, f"DJERJ_{d_cnj}.txt"), dje_txt)
            has_pub = "Não foram encontradas" not in dje_txt and "Nenhum registro encontrado" not in dje_txt
            print(f"DJERJ {d_cnj}: {'PUBLICAÇÃO ENCONTRADA!' if has_pub else 'Nenhuma publicação no período'}", flush=True)
            if has_pub:
                print(f"--- TEOR DJERJ ---\n{dje_txt[:1500]}\n------------------", flush=True)
        except Exception as e:
            print(f"Erro DJERJ {d_cnj}: {e}", flush=True)
            results[f"djerj_{d_cnj}"] = f"ERRO: {e}"

    # Busca no DJERJ por NOME do Júlio
    print(f"\n[DJERJ NOVO] Busca por Nome: 'Julio Pereira Marcos' (15/08 a 20/08/2026)", flush=True)
    dje_nome_url = "https://www3.tjrj.jus.br/consultadje/Result.aspx?dtInicio=15%2F08%2F2026&dtFim=20%2F08%2F2026&txtPesq=Julio%20Pereira%20Marcos&tipoPesq=NOME"
    try:
        page.goto(dje_nome_url, wait_until="domcontentloaded", timeout=45000)
        time.sleep(5)
        dje_nome_txt = page.evaluate("document.body.innerText")
        results["djerj_nome_julio"] = dje_nome_txt
        save_text(os.path.join(OUT_DIR, "DJERJ_nome_julio.txt"), dje_nome_txt)
        has_pub_nome = "Não foram encontradas" not in dje_nome_txt and "Nenhum registro encontrado" not in dje_nome_txt
        print(f"DJERJ por Nome: {'PUBLICAÇÃO ENCONTRADA!' if has_pub_nome else 'Nenhuma publicação no período'}", flush=True)
    except Exception as e:
        print(f"Erro DJERJ Nome: {e}", flush=True)

    # =========================================================================
    # 4. STJ (HC 1.116.750 / RJ - 6ª Turma - Og Fernandes)
    # =========================================================================
    print(f"\n{'='*60}\n[STJ] HC 1.116.750 / RJ (Registro 2026/0311210-7)\n{'='*60}", flush=True)
    try:
        page.goto(STJ_REG_URL, wait_until="domcontentloaded", timeout=45000)
        time.sleep(6)
        stj_body = page.evaluate("document.body.innerText")
        save_text(os.path.join(OUT_DIR, "STJ_HC1116750_body.txt"), stj_body)
        try:
            page.screenshot(path=os.path.join(OUT_DIR, "STJ_screenshot.png"), full_page=True)
        except:
            pass

        for tab_name in ["Fases", "Decisões", "Petições", "Pautas"]:
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
                print(f"Aviso tab STJ {tab_name}: {te}", flush=True)

        results["stj_completo"] = stj_body
        print(f"STJ capturado: {len(stj_body)} chars", flush=True)
        for l in stj_body.split('\n'):
            if "ÚLTIMA FASE" in l or "Conclusos" in l or "Decisão" in l or "Julgamento" in l:
                print(f"  [STJ Info] {l.strip()}", flush=True)
    except Exception as e:
        print(f"Erro STJ: {e}", flush=True)
        results["stj_completo"] = f"ERRO: {e}"

    browser.close()

json_path = os.path.join(OUT_DIR, "resultado_consolidado_20_08_2026.json")
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n=======================================================", flush=True)
print(f"VARREDURA CONCLUÍDA! Arquivos salvos em:\n{OUT_DIR}", flush=True)
print(f"=======================================================", flush=True)
