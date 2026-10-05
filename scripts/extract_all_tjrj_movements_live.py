# -*- coding: utf-8 -*-
"""
Extração Completa e Detalhada de Todos os Movimentos no Portal TJRJ para Júlio Pereira Marcos.
Data da Execução: 22/08/2026
"""
import time
import sys
import os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"
os.makedirs(OUT_DIR, exist_ok=True)

PROCS = [
    ("0023013-51.2021.8.19.0078", "tjrj_1a_instancia_buzios_completo.txt", "Ação Penal Desmembrada 1ª Instância - 2ª Vara Búzios"),
    ("0029845-67.2026.8.19.0000", "tjrj_2a_instancia_hc_completo.txt", "Habeas Corpus 7ª Câmara Criminal TJRJ"),
    ("0001140-87.2024.8.19.0078", "tjrj_apenso_completo.txt", "Recurso em Sentido Estrito / Apenso Búzios"),
    ("0022975-39.2021.8.19.0078", "tjrj_originario_completo.txt", "Processo Originário Co-réus Búzios")
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1366, "height": 900}, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/127.0.0.0 Safari/537.36")
    page = ctx.new_page()

    for proc_num, fname, label in PROCS:
        print(f"\n=======================================================")
        print(f"Buscando: {proc_num} ({label})")
        print(f"=======================================================")
        try:
            page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", wait_until="domcontentloaded", timeout=45000)
            time.sleep(3)
            page.wait_for_selector("iframe#mainframe", timeout=30000)
            frame = page.query_selector("iframe#mainframe").content_frame()
            time.sleep(2)

            frame.evaluate(f"""() => {{
                const inp = Array.from(document.querySelectorAll('input')).find(i => i.name==='numeroProcesso' || i.id==='numeroProcesso');
                if(inp) {{
                    inp.value = '{proc_num}';
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

            # Clicar em "Todos Os Movimentos" se disponível
            clicked_all = frame.evaluate("""() => {
                const links = Array.from(document.querySelectorAll('a, button, span'));
                const target = links.find(l => (l.textContent||'').toLowerCase().includes('todos os movimentos') || (l.textContent||'').toLowerCase().includes('todos movimentos'));
                if(target) {
                    target.click();
                    return true;
                }
                return false;
            }""")
            if clicked_all:
                print("   • Clicou em 'Todos Os Movimentos' com sucesso.")
                time.sleep(5)

            body_text = frame.inner_text("body")
            print(f"   • Total de texto capturado: {len(body_text)} caracteres")
            
            fpath = os.path.join(OUT_DIR, fname)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(body_text)
            print(f"   • Salvo com sucesso em: {fname}")

            # Mostrar resumo das linhas
            lines = [l.strip() for l in body_text.splitlines() if l.strip()]
            for l in lines[:15]:
                print(f"     {l}")

        except Exception as e:
            print(f"   • Erro ao processar {proc_num}: {e}")

    browser.close()
print("\n>>> EXTRAÇÃO TJRJ FINALIZADA COM SUCESSO <<<")
