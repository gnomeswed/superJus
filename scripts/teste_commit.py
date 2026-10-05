import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

cnj = "0023013-51.2021.8.19.0078"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
    ctx = b.new_context(
        viewport={"width": 1366, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        locale="pt-BR"
    )
    page = ctx.new_page()
    print("Navegando com wait_until='commit'...", flush=True)
    page.goto('https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica', wait_until='commit', timeout=30000)
    print("Commit recebido! Aguardando iframe#mainframe...", flush=True)
    
    frame_el = page.wait_for_selector("iframe#mainframe", timeout=30000)
    time.sleep(3)
    frame = frame_el.content_frame()
    print("Frame mainframe obtido!", flush=True)

    # Espera o input numeroProcesso estar visível no frame
    print("Aguardando input no frame...", flush=True)
    frame.wait_for_selector("input[name='numeroProcesso'], #numeroProcesso, input[name='tipoNumeracao']", timeout=25000)
    print("Input carregado no frame!", flush=True)

    # Preenche o input
    frame.evaluate(f"""() => {{
        const inp = Array.from(document.querySelectorAll('input')).find(i => i.name==='numeroProcesso' || i.id==='numeroProcesso');
        if(inp) {{
            inp.value = '{cnj}';
            inp.dispatchEvent(new Event('input', {{bubbles:true}}));
            inp.dispatchEvent(new Event('change', {{bubbles:true}}));
        }}
    }}""")
    time.sleep(1)

    # Clica em Pesquisar
    frame.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.offsetWidth>0 && (b.textContent||'').toLowerCase().includes('pesquisar'));
        if(btn) btn.click();
    }""")
    print("Botão Pesquisar clicado, aguardando 10s...", flush=True)
    time.sleep(10)

    # Clica em Todos Os Movimentos se existir
    frame.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('a, button')).find(el => (el.textContent||'').toLowerCase().includes('todos os movimentos') || (el.textContent||'').toLowerCase().includes('todos'));
        if(btn) btn.click();
    }""")
    time.sleep(4)

    body = frame.inner_text("body")
    print(f"Sucesso! Texto capturado ({len(body)} caracteres).", flush=True)
    
    lines = [l.strip() for l in body.split('\n') if l.strip()]
    for idx, l in enumerate(lines):
        if "Localização na Serventia" in l:
            print(f">> LOCALIZAÇÃO: {lines[idx+1] if idx+1 < len(lines) else 'N/A'}", flush=True)
        if "Tipo do Movimento:" in l:
            chunk = lines[idx:min(len(lines), idx+8)]
            print(f">> MOVIMENTO: {' | '.join(chunk)}", flush=True)

    b.close()
