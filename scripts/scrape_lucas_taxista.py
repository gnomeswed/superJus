#!/usr/bin/env python3
"""Scrape TJRJ process for Lucas Dias Oliveira (taxista) - 0808595-36.2026.8.19.0002"""
import os, sys, time, json

PROC = "0808595-36.2026.8.19.0002"
CLIENT_DIR = os.path.join("C:", os.sep, "Projetos", "superJus", "Clientes", "Lucas_Dias_Oliveira")
DOCS_DIR = os.path.join(CLIENT_DIR, "03_Documentos_do_Processo")
INTEGRA_DIR = os.path.join(DOCS_DIR, "Decisoes_na_Integra")
MOV_DIR = os.path.join(CLIENT_DIR, "02_Movimentacoes_Individuais")
RASPED_DIR = os.path.join(DOCS_DIR, "_raspagem_2026-08-16")

for d in [DOCS_DIR, INTEGRA_DIR, MOV_DIR, RASPED_DIR]:
    os.makedirs(d, exist_ok=True)

from playwright.sync_api import sync_playwright

results = {
    "processo": PROC,
    "cliente": "Lucas Dias Oliveira (Taxista)",
    "data_raspagem": "2026-08-16",
    "movimentos": [],
    "integrais": [],
    "erros": [],
}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1366, "height": 900})
    page = ctx.new_page()
    
    print(f"[1/6] Navegando para TJRJ...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica",
              timeout=45000, wait_until="domcontentloaded")
    page.wait_for_selector("iframe#mainframe", timeout=30000)
    fr = page.query_selector("iframe#mainframe").content_frame()
    time.sleep(3)

    # Fill search form
    print(f"[2/6] Buscando processo {PROC}...")
    fr.evaluate(f"""() => {{
        const inp = Array.from(document.querySelectorAll('input'))
          .find(i => i.name === 'numeroProcesso' || i.id === 'numeroProcesso');
        if (inp) {{
            inp.value = '{PROC}';
            inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
            inp.dispatchEvent(new Event('change', {{ bubbles: true }}));
        }}
    }}""")
    fr.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button'))
          .find(b => b.offsetWidth > 0 && b.textContent.toLowerCase().includes('pesquisar'));
        if (btn) btn.click();
    }""")
    time.sleep(10)

    # Check for PJe modal
    pje_modal = fr.evaluate("""() => {
        const el = Array.from(document.querySelectorAll('h4, div'))
          .find(e => (e.innerText || '').includes('Mensagem Processo do PJe'));
        return !!el;
    }""")
    
    if pje_modal:
        print("⚠️ PROCESSO PJe DETECTADO - scraping público bloqueado!")
        body_text = fr.inner_text("body")[:3000]
        print(body_text)
        results["erros"].append("Processo PJe - scraping público bloqueado")
        browser.close()
        with open(os.path.join(RASPED_DIR, "resultado_scrape.json"), "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(json.dumps(results, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    # Save espelho before expand
    body_before = fr.inner_text("body")
    print(f"Body length before expand: {len(body_before)}")
    
    with open(os.path.join(RASPED_DIR, "espelho_antes_expansao.txt"), "w", encoding="utf-8") as f:
        f.write(body_before)
    
    # Save full HTML snapshot
    html_before = fr.content()
    with open(os.path.join(RASPED_DIR, "espelho_antes_expansao.html"), "w", encoding="utf-8") as f:
        f.write(html_before)

    # Click "Todos Os Movimentos"
    print("[3/6] Expandindo movimentações (Todos Os Movimentos)...")
    fr.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button'))
          .find(b => (b.textContent || '').toLowerCase().includes('todos os movimentos'));
        if (btn) btn.click();
    }""")
    time.sleep(15)
    
    body_after = fr.inner_text("body")
    print(f"Body length after expand: {len(body_after)}")
    
    mov_count = body_after.count("Tipo do Movimento:")
    print(f"Movimentações encontradas: {mov_count}")
    
    with open(os.path.join(RASPED_DIR, "espelho_apos_expansao.txt"), "w", encoding="utf-8") as f:
        f.write(body_after)
    
    html_after = fr.content()
    with open(os.path.join(RASPED_DIR, "espelho_apos_expansao.html"), "w", encoding="utf-8") as f:
        f.write(html_after)

    # Look for "Ver Íntegra" buttons
    print("[4/6] Procurando botões de íntegra...")
    botoes_reais = fr.evaluate("""() => {
        const t_exatos = [
          'ver íntegra do(a) decisão (original)',
          'ver íntegra do(a) decisão (simplificado)',
          'ver íntegra',
          'visualizar ato assinado digitalmente',
          'visualizar ato'
        ];
        return Array.from(document.querySelectorAll('a, button'))
          .filter(el => el.offsetWidth > 0 && el.offsetHeight > 0)
          .filter(el => {
            const t = (el.textContent || '').toLowerCase().trim();
            return t_exatos.some(te => t.startsWith(te) || t === te);
          })
          .map(el => ({text: (el.textContent||'').trim(), tag: el.tagName}));
    }""")
    print(f"Botões de íntegra encontrados: {len(botoes_reais)}")
    for b in botoes_reais:
        print(f"  - {b['text'][:100]}")

    # Capture each integral
    print("[5/6] Capturando íntegras...")
    integrais_capturadas = []
    for i, b in enumerate(botoes_reais):
        print(f"\n  [{i+1}/{len(botoes_reais)}] Clicando: {b['text'][:60]}...")
        clicked = fr.evaluate("""(t) => {
            const alvo = Array.from(document.querySelectorAll('a, button'))
              .find(el => el.offsetWidth > 0 && (el.textContent || '').trim() === t);
            if (alvo) { alvo.click(); return true; }
            return false;
        }""", b["text"])
        
        if not clicked:
            print(f"    ❌ Não conseguiu clicar")
            continue
        
        # Wait for modal
        try:
            fr.wait_for_selector(
                '.modal-body, .ui-dialog-content, div[role="dialog"], .modal.show, .modal-content',
                timeout=10000, state="visible"
            )
        except Exception:
            pass
        time.sleep(4)
        
        # Extract modal content
        modal_text = fr.evaluate("""() => {
            const containers = Array.from(document.querySelectorAll(
              '.modal-body, .ui-dialog-content, div[role="dialog"] .modal-body, .modal.show .modal-body'
            )).filter(c => c.offsetWidth > 0 && c.offsetHeight > 0);
            if (containers.length > 0) {
              const txt = containers.map(c => c.innerText || c.textContent).join('\\n\\n---\\n\\n');
              if (txt && txt.trim().length > 30) return txt;
            }
            const mc = Array.from(document.querySelectorAll('.modal.show .modal-content, .modal-content'));
            if (mc.length > 0) return mc.map(c => c.innerText || c.textContent).join('\\n\\n---\\n\\n');
            return document.body.innerText;
        }""")
        
        if len(modal_text) > 500:
            integrais_capturadas.append({
                "botao": b["text"],
                "conteudo": modal_text[:30000],
                "tamanho": len(modal_text)
            })
            print(f"    ✅ Capturado: {len(modal_text)} chars")
            
            # Save individual integral
            slug = b["text"].lower().replace(" ", "_").replace("/", "_")[:50]
            fname = f"2026-08-16_integral_{i+1}_{slug}.md"
            with open(os.path.join(INTEGRA_DIR, fname), "w", encoding="utf-8") as f:
                f.write(f"# Íntegra capturada em 2026-08-16\n\n")
                f.write(f"**Botão:** {b['text']}\n\n")
                f.write(f"**Tamanho:** {len(modal_text)} chars\n\n")
                f.write(f"---\n\n{modal_text}")
        else:
            print(f"    ⚠️ Conteúdo muito curto: {len(modal_text)} chars")
        
        # Close modal
        fr.evaluate("""() => {
            const close = document.querySelector('.modal.show .btn-close, .modal.show .close, button[aria-label="Close"], .ui-dialog-titlebar-close');
            if (close) { close.click(); return; }
            ['keydown','keyup'].forEach(t => {
              const e = new KeyboardEvent(t, {key:'Escape', code:'Escape', keyCode:27, which:27, bubbles:true});
              document.dispatchEvent(e); window.dispatchEvent(e);
            });
        }""")
        time.sleep(3)
    
    results["integrais"] = integrais_capturadas

    # Save full body text as movements summary
    print("[6/6] Salvando resumo das movimentações...")
    with open(os.path.join(DOCS_DIR, "2026-08-16_Movimentacoes_Todas.md"), "w", encoding="utf-8") as f:
        f.write(f"# Movimentações Processo {PROC}\n\n")
        f.write(f"**Cliente:** Lucas Dias Oliveira (Taxista)\n")
        f.write(f"**Data da raspagem:** 2026-08-16\n")
        f.write(f"**Total de movimentações:** {mov_count}\n\n")
        f.write(f"---\n\n")
        f.write(body_after[:50000])
    
    # Save result JSON
    results["movimentos_count"] = mov_count
    results["body_length_before"] = len(body_before)
    results["body_length_after"] = len(body_after)
    
    with open(os.path.join(RASPED_DIR, "resultado_scrape.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    browser.close()

print(f"\n{'='*60}")
print(f"RASPAGEM CONCLUÍDA!")
print(f"{'='*60}")
print(f"Processo: {PROC}")
print(f"Movimentações: {mov_count}")
print(f"Íntegras capturadas: {len(integrais_capturadas)}")
print(f"Arquivos salvos em:")
print(f"  - {DOCS_DIR}")
print(f"  - {INTEGRA_DIR}")
print(f"  - {RASPED_DIR}")
