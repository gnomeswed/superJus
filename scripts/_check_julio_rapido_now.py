# -*- coding: utf-8 -*-
"""Check rápido ao vivo — Júlio Pereira Marcos — 15/08/2026 afternoon
Foco: STJ HC 1116750 decisões novas + TJRJ 1ª inst movimentação + DJERJ 08-15/08
"""
import time, sys, os
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

OUT = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"
os.makedirs(OUT, exist_ok=True)

def check_stj(page):
    print("="*60 + "\n[STJ] HC 1116750 — verificações decisões/fases\n" + "="*60)
    # Semente + fases
    URL_RE = "https://processo.stj.jus.br/processo/pesquisa/?tipoPesquisa=tipoPesquisaNumeroRegistro&termo=202603112107&totalRegistrosPorPagina=40&aplicacao=processos.ea"
    URL_DETALHE = "https://processo.stj.jus.br/processo/pesquisa/?aplicacao=processos.ea&tipoPesquisa=tipoPesquisaGenerica&termo=1116750&totalRegistrosPorPagina=40"
    try:
        page.goto(URL_RE, wait_until="domcontentloaded", timeout=45000)
        time.sleep(5)
        # Clica no resultado
        page.evaluate("""() => {
            const links = document.querySelectorAll('a, span, td');
            for(const el of links) {
                if((el.textContent||'').includes('1116750') && el.offsetParent !== null) {
                    el.click(); return true;
                }
            }
            return false;
        }""")
        time.sleep(8)
        html = page.content()
        txt = page.evaluate("document.body.innerText")
        print(f"STJ body chars: {len(txt)}")
        # Procura decisões novas (sequenciais diferentes de 389054957)
        import re
        sequenciais = re.findall(r'sequencial=(\d+)', html)
        decisoes_previas = set(sequenciais) - {'389054957'}
        if decisoes_previas:
            print(f"🚨 DECISÕES NOVAS DETECTADAS: {decisoes_previas}")
        else:
            print(f"Sem decisões novas (sequenciais: {set(sequenciais)})")
        # Procura "Conclusos" na data mais recente
        if "Conclusos" in txt:
            idx = txt.index("Conclusos")
            print(f">>> Conclusos contexto: {txt[max(0,idx-100):idx+200]}")
        # Baixa HTML
        with open(os.path.join(OUT, "_stj_hc1116750_check_latest.html"), "w", encoding="utf-8") as f:
            f.write(html)
        with open(os.path.join(OUT, "_stj_hc1116750_check_latest.txt"), "w", encoding="utf-8") as f:
            f.write(txt)
        # Salva a aba Decisões se existir
        page.evaluate("""() => {
            const tabs = document.querySelectorAll('[onclick*="mostraBloco"], a[data-toggle], li a');
            for(const t of tabs) {
                if((t.textContent||'').includes('Decisões') || (t.textContent||'').includes('Decisoes')) {
                    t.click(); return true;
                }
            }
            return false;
        }""")
        time.sleep(5)
        txt_dec = page.evaluate("document.body.innerText")
        if "Decisão Monocrática" in txt_dec or "Acórdão" in txt_dec:
            print(f">>> DECISÕES (aba):\n{txt_dec[:5000]}")
        else:
            print(f">>> Sem aba decisões visível — conteúdo: {txt_dec[:2000]}")
        return {"html_len": len(html), "txt_len": len(txt), "novas_decisoes": len(decisoes_previas)}
    except Exception as e:
        print(f"ERRO STJ: {e}")
        return {"error": str(e)}

def check_tjrj_1a(page):
    print("\n" + "="*60 + "\n[TJRJ 1ª] 0023013-51.2021 — movimentação nova\n" + "="*60)
    PROC = "0023013-51.2021.8.19.0078"
    try:
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", wait_until="domcontentloaded", timeout=45000)
        time.sleep(3)
        page.wait_for_selector("iframe#mainframe", timeout=30000)
        fr = page.query_selector("iframe#mainframe").content_frame()
        time.sleep(2)
        fr.evaluate(f"""() => {{
            const inp = Array.from(document.querySelectorAll('input')).find(i => i.name==='numeroProcesso' || i.id==='numeroProcesso');
            if(inp){{ inp.value='{PROC}'; inp.dispatchEvent(new Event('input',{{bubbles:true}})); inp.dispatchEvent(new Event('change',{{bubbles:true}})); }}
        }}""")
        time.sleep(1)
        fr.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.offsetWidth>0 && (b.textContent||'').toLowerCase().includes('pesquisar'));
            if(btn) btn.click();
        }""")
        time.sleep(8)
        body = fr.inner_text("body")
        print(body[:4000])
        if "Localização na Serventia" in body:
            idx = body.index("Localização na Serventia")
            print(f">>> Localização: {body[idx:idx+500].replace(chr(10),' | ')}")
        if "Última Movimentação" in body or "Tipo do Movimento" in body:
            idx = body.index("Tipo do Movimento:")
            print(f">>> Última: {body[idx:idx+300].replace(chr(10),' | ')}")
        return {"body_len": len(body)}
    except Exception as e:
        print(f"ERRO TJRJ 1ª: {e}")
        return {"error": str(e)}

def check_djerj(page):
    print("\n" + "="*60 + "\n[DJERJ] publicações 08-15/08/2026\n" + "="*60)
    for proc in ["0023013-51.2021.8.19.0078", "0029845-67.2026.8.19.0000", "0022975-39.2021.8.19.0078"]:
        url = f"https://www3.tjrj.jus.br/consultadje/Result.aspx?dtInicio=08%2F08%2F2026&dtFim=15%2F08%2F2026&txtPesq={proc}&tipoPesq=PROC"
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=45000)
            time.sleep(5)
            body = page.evaluate("document.body.innerText")
            if "Não foram encontradas" in body:
                print(f"  {proc}: SEM publicação 08-15/08")
            else:
                print(f"  {proc}: POSSÍVEL PUBLICAÇÃO!\n{body[:2000]}")
        except Exception as e:
            print(f"  {proc}: Erro DJERJ: {e}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled","--no-sandbox"])
    ctx = browser.new_context(viewport={"width":1366,"height":900}, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/127.0.0.0 Safari/537.36", locale="pt-BR")
    ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined});")
    page = ctx.new_page()
    r1 = check_stj(page)
    time.sleep(2)
    r2 = check_tjrj_1a(page)
    time.sleep(2)
    check_djerj(page)
    browser.close()
print(f"\n=== FIM CHECK {r1} {r2} ===")
