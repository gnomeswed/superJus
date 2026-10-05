# -*- coding: utf-8 -*-
import os, sys, time, json
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

PROCS = [
    ("0023013-51.2021.8.19.0078", "1A-Desmembrado-Julio-Principal"),
    ("0001140-87.2024.8.19.0078", "1A-Apenso-Medida"),
    ("0022975-39.2021.8.19.0078", "1A-Original-Correu")
]

OUT_DIR = r"C:\Projetos\superJus\Clientes\Julio_Pereira_Marcos\Caso_Principal\documentos_processo\_varredura_18_08_2026"
os.makedirs(OUT_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
    page = browser.new_page(viewport={"width": 1366, "height": 900})

    for cnj, label in PROCS:
        print(f"\n==========================================", flush=True)
        print(f"Consultando 1ª Instância: {label} ({cnj})", flush=True)
        print(f"==========================================", flush=True)
        try:
            page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=30000, wait_until="domcontentloaded")
            time.sleep(3)
            iframe = page.wait_for_selector("iframe#mainframe", timeout=15000).content_frame()
            
            iframe.evaluate(f"""() => {{
                const inp = Array.from(document.querySelectorAll('input')).find(i => i.name==='numeroProcesso' || i.id==='numeroProcesso');
                if(inp){{ inp.value='{cnj}'; inp.dispatchEvent(new Event('input',{{bubbles:true}})); inp.dispatchEvent(new Event('change',{{bubbles:true}})); }}
            }}""")
            time.sleep(1)
            iframe.evaluate("""() => {
                const btn = Array.from(document.querySelectorAll('button')).find(b => b.offsetWidth>0 && (b.textContent||'').toLowerCase().includes('pesquisar'));
                if(btn) btn.click();
            }""")
            time.sleep(6)

            # Clica em Todos Os Movimentos
            iframe.evaluate("""() => {
                const btn = Array.from(document.querySelectorAll('button, a')).find(b => (b.textContent||'').toLowerCase().includes('todos os movimentos'));
                if(btn) btn.click();
            }""")
            time.sleep(4)

            txt = iframe.inner_text("body")
            fname = os.path.join(OUT_DIR, f"{label}__{cnj}.txt")
            with open(fname, "w", encoding="utf-8") as f:
                f.write(txt)

            # Exibe localização e as 5 primeiras movimentações encontradas
            lines = [l.strip() for l in txt.split('\n') if l.strip()]
            loc = "Não encontrada"
            movs = []
            for i, l in enumerate(lines):
                if "Localização na Serventia" in l and i+1 < len(lines):
                    loc = lines[i+1]
                if "Tipo do Movimento:" in l:
                    mov_text = [l]
                    for j in range(1, 6):
                        if i+j < len(lines) and "Tipo do Movimento:" not in lines[i+j]:
                            mov_text.append(lines[i+j])
                        else:
                            break
                    movs.append(" | ".join(mov_text))

            print(f"Status / Localização: {loc}", flush=True)
            print(f"Total de Movimentos Capturados: {len(movs)}", flush=True)
            print("Últimos movimentos:", flush=True)
            for m in movs[:4]:
                print(f"  • {m}", flush=True)

        except Exception as e:
            print(f"Erro em {cnj}: {e}", flush=True)

    browser.close()
