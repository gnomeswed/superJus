# -*- coding: utf-8 -*-
"""
Scraping Leandro da Silva — tenta TJRJ, DJERJ e Google.
PJe 0827233-23.2026.8.19.0001
"""
import time, json, os, sys
from playwright.sync_api import sync_playwright

PROC = "0827233-23.2026.8.19.0001"
CLIENT_DIR = r"C:\Projetos\superJus\Clientes\Leandro_Mecanico"
OUTPUT_DIR = os.path.join(CLIENT_DIR, "scraping_2026-08-16")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

results = {}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1366, "height": 900})
    page = ctx.new_page()

    # ===== 1: TJRJ Portal =====
    log("=== ETAPA 1: TJRJ Consulta Processual ===")
    try:
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica",
                   timeout=45000, wait_until="domcontentloaded")
        page.wait_for_selector("iframe#mainframe", timeout=30000)
        fr = page.query_selector("iframe#mainframe").content_frame()
        time.sleep(3)
        
        # Fill process number
        fr.evaluate(f"""() => {{
            const inp = Array.from(document.querySelectorAll('input'))
              .find(i => i.name === 'numeroProcesso' || i.id === 'numeroProcesso');
            if (inp) {{
                inp.value = '{PROC}';
                inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
                inp.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
        }}""")
        
        # Click search
        fr.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button'))
              .find(b => b.offsetWidth > 0 && b.textContent.toLowerCase().includes('pesquisar'));
            if (btn) btn.click();
        }""")
        time.sleep(10)
        
        # Check for PJe modal
        pje_modal = fr.evaluate("""() => {
            const el = Array.from(document.querySelectorAll('h4, div, p'))
              .find(e => (e.innerText || '').includes('Mensagem Processo do PJe'));
            return !!el;
        }""")
        
        if pje_modal:
            log("⚠️ Modal PJe detectado — portal TJRJ bloqueado para este processo")
            modal_text = fr.evaluate("""() => {
                const el = Array.from(document.querySelectorAll('.modal-body, .modal, div'))
                  .find(e => (e.innerText || '').includes('PJe'));
                return el ? el.innerText : '';
            }""")
            results["tjrj_modal"] = modal_text
            log(f"Modal: {modal_text[:200]}")
        else:
            # Get body text
            body = fr.inner_text("body")
            log(f"Body length: {len(body)} chars")
            results["tjrj_body"] = body[:5000]
            
            # Try to get espelho
            espelho = fr.evaluate("""() => {
                const el = document.querySelector('.espelho, .processo-dados, table');
                return el ? el.innerText : '';
            }""")
            if espelho:
                results["tjrj_espelho"] = espelho[:3000]
                log(f"Espelho: {len(espelho)} chars")
            
            # Try "Todos os Movimentos"
            fr.evaluate("""() => {
                const btn = Array.from(document.querySelectorAll('button'))
                  .find(b => (b.textContent || '').toLowerCase().includes('todos os movimentos'));
                if (btn) btn.click();
            }""")
            time.sleep(12)
            
            body2 = fr.inner_text("body")
            if len(body2) > len(body) + 500:
                log(f"Expandido: {len(body)} → {len(body2)} chars")
                results["tjrj_movimentos"] = body2[:10000]
            else:
                log(f"Sem expansão significativa: {len(body2)} chars")
                results["tjrj_movimentos"] = body2[:5000]
                
    except Exception as e:
        log(f"Erro TJRJ: {e}")
        results["tjrj_error"] = str(e)

    # ===== 2: DJERJ Consulta =====
    log("\n=== ETAPA 2: DJERJ Consulta de Publicações ===")
    try:
        # DJERJ new portal
        dje_url = f"https://www3.tjrj.jus.br/consultadje/Result.aspx?dtInicio=01%2F08%2F2026&dtFim=16%2F08%2F2026&txtPesq={PROC}&tipoPesq=PROC"
        page2 = ctx.new_page()
        page2.goto(dje_url, timeout=30000, wait_until="domcontentloaded")
        time.sleep(5)
        
        body_dje = page2.inner_text("body")
        log(f"DJERJ body: {len(body_dje)} chars")
        
        if "Não foram encontradas" in body_dje:
            log("DJERJ: Nenhuma publicação encontrada no período")
            results["djerj"] = "Nenhuma publicação encontrada (01/08 a 16/08/2026)"
        else:
            results["djerj"] = body_dje[:5000]
            log(f"DJERJ: {body_dje[:200]}")
        
        page2.close()
    except Exception as e:
        log(f"Erro DJERJ: {e}")
        results["djerj_error"] = str(e)

    # ===== 3: DJERJ período maior =====
    log("\n=== ETAPA 3: DJERJ período 01/03/2026 a 16/08/2026 ===")
    try:
        dje_url2 = f"https://www3.tjrj.jus.br/consultadje/Result.aspx?dtInicio=01%2F03%2F2026&dtFim=16%2F08%2F2026&txtPesq={PROC}&tipoPesq=PROC"
        page3 = ctx.new_page()
        page3.goto(dje_url2, timeout=30000, wait_until="domcontentloaded")
        time.sleep(5)
        
        body_dje2 = page3.inner_text("body")
        log(f"DJERJ (período maior): {len(body_dje2)} chars")
        
        if "Não foram encontradas" in body_dje2:
            results["djerj_periodo_maior"] = "Nenhuma publicação (01/03 a 16/08/2026)"
        else:
            results["djerj_periodo_maior"] = body_dje2[:5000]
            log(f"Encontrado: {body_dje2[:300]}")
        
        page3.close()
    except Exception as e:
        log(f"Erro DJERJ período maior: {e}")
        results["djerj_periodo_maior_error"] = str(e)

    # ===== 4: Google search =====
    log("\n=== ETAPA 4: Google — sentença/decisão do processo ===")
    try:
        google_url = f"https://www.google.com/search?q=%22{PROC}%22+senten%C3%A7a+OR+decis%C3%A3o+OR+despacho"
        page4 = ctx.new_page()
        page4.goto(google_url, timeout=20000, wait_until="domcontentloaded")
        time.sleep(3)
        
        # Extract search results
        google_results = page4.evaluate("""() => {
            const results = Array.from(document.querySelectorAll('div.g, div[data-sokoban-container]'));
            return results.slice(0, 5).map(r => {
                const title = r.querySelector('h3');
                const link = r.querySelector('a');
                const snippet = r.querySelector('.VwiC3b, [data-sncf]');
                return {
                    title: title ? title.innerText : '',
                    url: link ? link.href : '',
                    snippet: snippet ? snippet.innerText : ''
                };
            });
        }""")
        
        results["google"] = google_results
        log(f"Google: {len(google_results)} resultados")
        for g in google_results:
            if g['title']:
                log(f"  → {g['title'][:80]}")
        
        page4.close()
    except Exception as e:
        log(f"Erro Google: {e}")
        results["google_error"] = str(e)

    # ===== 5: DataJud API (tentar novamente com formato correto) =====
    log("\n=== ETAPA 5: DataJud API direto ===")
    try:
        import requests
        API_KEY = "APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
        headers = {"Authorization": API_KEY, "Content-Type": "application/json"}
        
        # Try exact number match
        clean = "08272332320268190001"
        r = requests.post("https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search",
            headers=headers,
            json={"query": {"term": {"numeroProcesso": clean}}, "size": 5},
            timeout=15)
        
        if r.status_code == 200:
            data = r.json()
            hits = data.get("hits", {}).get("hits", [])
            log(f"DataJud term search: {len(hits)} hits")
            for h in hits:
                src = h.get("_source", {})
                log(f"  → {src.get('numeroProcesso')} | {src.get('classe',{}).get('nome','')}")
            results["datajud_term"] = [h.get("_source", {}) for h in hits]
        else:
            log(f"DataJud: HTTP {r.status_code}")
            results["datajud_term_error"] = r.text[:200]
            
    except Exception as e:
        log(f"Erro DataJud: {e}")
        results["datajud_error"] = str(e)

    browser.close()

# ===== SALVAR =====
log("\n=== SALVANDO RESULTADOS ===")
out_file = os.path.join(OUTPUT_DIR, "scraping_resultados.json")
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
log(f"Salvo: {out_file}")

# Also save body text for analysis
for key in ["tjrj_movimentos", "tjrj_body", "tjrj_espelho", "djerj", "djerj_periodo_maior"]:
    if key in results and results[key]:
        txt_file = os.path.join(OUTPUT_DIR, f"{key}.txt")
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write(results[key])
        log(f"  Texto salvo: {txt_file}")

log("\n✓ Scraping finalizado!")
