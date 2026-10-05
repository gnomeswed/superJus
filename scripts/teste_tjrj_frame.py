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
    print("Navegando para o portal TJRJ...", flush=True)
    page.goto('https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica', wait_until='domcontentloaded', timeout=45000)
    time.sleep(3)
    
    frame = page.wait_for_selector("iframe#mainframe", timeout=25000).content_frame()
    print("Frame mainframe localizado com sucesso!", flush=True)

    # Preenche o input dentro do frame
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
    print("Botão Pesquisar clicado, aguardando 8s...", flush=True)
    time.sleep(8)

    # Verifica se apareceu botão 'Todos Os Movimentos'
    frame.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('a, button')).find(el => (el.textContent||'').toLowerCase().includes('todos os movimentos') || (el.textContent||'').toLowerCase().includes('todos'));
        if(btn) btn.click();
    }""")
    time.sleep(3)

    body = frame.inner_text("body")
    print(f"Resultado obtido! Tamanho do texto: {len(body)}", flush=True)

    lines = [l.strip() for l in body.split('\n') if l.strip()]
    for idx, l in enumerate(lines):
        if "Localização na Serventia" in l:
            print(f">> LOCALIZAÇÃO: {lines[idx+1] if idx+1 < len(lines) else 'N/A'}", flush=True)
        if "Tipo do Movimento:" in l:
            chunk = lines[idx:min(len(lines), idx+8)]
            print(f">> MOVIMENTO: {' | '.join(chunk)}", flush=True)

    with open("c:/Projetos/superJus/teste_principal_out.txt", "w", encoding="utf-8") as f:
        f.write(body)

    b.close()
