import sys
import time
import os
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

procs = [
    ("0001140-87.2024.8.19.0078", "julio_tjrj_1A_Apenso_RSE_24set.txt", "Apenso RSE"),
    ("0022975-39.2021.8.19.0078", "julio_tjrj_1A_Original_Desmembrado_24set.txt", "Processo Originário"),
]

out_dir = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"
os.makedirs(out_dir, exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
    ctx = b.new_context(
        viewport={"width": 1366, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        locale="pt-BR"
    )
    page = ctx.new_page()

    for cnj, fname, label in procs:
        print(f"\n==========================================", flush=True)
        print(f"Consultando {cnj} ({label})...", flush=True)
        try:
            page.goto('https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica', wait_until='commit', timeout=30000)
            frame_el = page.wait_for_selector("iframe#mainframe", timeout=30000)
            time.sleep(2)
            frame = frame_el.content_frame()
            frame.wait_for_selector("input[name='numeroProcesso'], #numeroProcesso", timeout=25000)

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
            time.sleep(8)

            frame.evaluate("""() => {
                const btn = Array.from(document.querySelectorAll('a, button')).find(el => (el.textContent||'').toLowerCase().includes('todos os movimentos') || (el.textContent||'').toLowerCase().includes('todos'));
                if(btn) btn.click();
            }""")
            time.sleep(3)

            body = frame.inner_text("body")
            print(f"Sucesso {cnj}! Tamanho: {len(body)} chars", flush=True)
            
            fpath = os.path.join(out_dir, fname)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(body)
            print(f"Salvo em: {fpath}", flush=True)

            lines = [l.strip() for l in body.split('\n') if l.strip()]
            for idx, l in enumerate(lines):
                if "Localização na Serventia" in l:
                    print(f">> LOCALIZAÇÃO: {lines[idx+1] if idx+1 < len(lines) else 'N/A'}", flush=True)
                if "Tipo do Movimento:" in l:
                    chunk = lines[idx:min(len(lines), idx+8)]
                    print(f">> MOVIMENTO: {' | '.join(chunk)}", flush=True)

        except Exception as e:
            print(f"Erro em {cnj}: {e}", flush=True)

    b.close()
print("\nCONCLUÍDO!", flush=True)
