# -*- coding: utf-8 -*-
"""
Consulta específica do processo principal de Júlio Pereira Marcos (0023013-51.2021.8.19.0078)
no Portal do TJRJ com retry e timeout adequado.
"""
import sys, os, time, json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

OUT_DIR = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"
proc_target = "0023013-51.2021.8.19.0078"
save_fname = "julio_tjrj_1A_Principal_Julio_19set.txt"

print(f"Iniciando consulta focada em {proc_target}...")

result_data = None
for attempt in range(1, 4):
    print(f"Tentativa {attempt}/3...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
            ctx = browser.new_context(
                viewport={"width": 1366, "height": 900},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
                locale="pt-BR"
            )
            ctx.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
            page = ctx.new_page()

            page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", wait_until="commit", timeout=60000)
            page.wait_for_selector("iframe#mainframe", timeout=45000)
            frame = page.query_selector("iframe#mainframe").content_frame()
            time.sleep(3)

            frame.evaluate(f"""() => {{
                const inp = Array.from(document.querySelectorAll('input')).find(i => i.name==='numeroProcesso' || i.id==='numeroProcesso');
                if(inp) {{
                    inp.value = '{proc_target}';
                    inp.dispatchEvent(new Event('input', {{bubbles:true}}));
                    inp.dispatchEvent(new Event('change', {{bubbles:true}}));
                }}
            }}""")
            time.sleep(1)
            frame.evaluate("""() => {
                const btn = Array.from(document.querySelectorAll('button')).find(b => b.offsetWidth>0 && (b.textContent||'').toLowerCase().includes('pesquisar'));
                if(btn) btn.click();
            }""")
            time.sleep(8)

            try:
                frame.evaluate("""() => {
                    const todosBtn = Array.from(document.querySelectorAll('a, button, span')).find(el => (el.textContent||'').trim().toLowerCase() === 'todos os movimentos' || (el.textContent||'').trim().toLowerCase() === 'todos');
                    if(todosBtn) todosBtn.click();
                }""")
                time.sleep(3)
            except Exception:
                pass

            body_txt = frame.inner_text("body")
            print(f"Capturados {len(body_txt)} caracteres.")
            
            fpath = os.path.join(OUT_DIR, save_fname)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(body_txt)

            loc_str = "N/A"
            if "Localização na Serventia" in body_txt:
                idx = body_txt.index("Localização na Serventia")
                loc_str = body_txt[idx:idx+300].replace('\n', ' | ')
            
            mov_str = "N/A"
            if "Tipo do Movimento:" in body_txt:
                idx = body_txt.index("Tipo do Movimento:")
                mov_str = body_txt[idx:idx+300].replace('\n', ' | ')

            result_data = {
                "status": "sucesso",
                "data_hora_consulta": time.strftime("%d/%m/%Y %H:%M:%S"),
                "localizacao": loc_str,
                "ultimo_movimento": mov_str,
                "fpath": fpath,
                "raw": body_txt
            }
            print("Sucesso! Localização:", loc_str[:100])
            print("Último movimento:", mov_str[:100])
            browser.close()
            break
    except Exception as e:
        print(f"Falha na tentativa {attempt}: {e}")
        time.sleep(3)

if result_data:
    # Atualiza nos arquivos JSON
    for jpath in [
        r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\consulta_ao_vivo_19_09_2026.json",
        r"C:\Projetos\swedsystem\docs\consulta_ao_vivo_19_09_2026.json"
    ]:
        if os.path.exists(jpath):
            with open(jpath, "r", encoding="utf-8") as f:
                d = json.load(f)
            d.setdefault("portal_tjrj", {})[proc_target] = result_data
            with open(jpath, "w", encoding="utf-8") as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
            print(f"JSON atualizado em: {jpath}")
