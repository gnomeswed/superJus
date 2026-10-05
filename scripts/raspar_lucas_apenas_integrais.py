# -*- coding: utf-8 -*-
"""
Re-raspagem focada: capturar APENAS as integrais (modais abertos de fato).
Processo: 0011857-95.2024.8.19.0002 (Lucas de Souza Freitas)
"""

def main() -> None:
    import sys, time, json, re
    from datetime import datetime
    from pathlib import Path
    from playwright.sync_api import sync_playwright

    sys.stdout.reconfigure(encoding="utf-8")
    PROC = "0011857-95.2024.8.19.0002"
    HOJE = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    RAW_DIR = Path(r"C:\Projetos\superJus\Clientes\Lucas_Freitas\03_Documentos_do_Processo\_raspagem_10_08_2026")
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    integrais = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = browser.new_context(viewport={"width": 1366, "height": 900})
        page = ctx.new_page()
        print(f"[{HOJE}] Reabrindo processo {PROC}")

        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000)
        page.wait_for_selector("iframe#mainframe", timeout=30000)
        fr = page.query_selector("iframe#mainframe").content_frame()
        time.sleep(2)

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
        time.sleep(8)
        fr.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button'))
              .find(b => (b.textContent || '').toLowerCase().includes('todos os movimentos'));
            if (btn) btn.click();
        }""")
        time.sleep(15)

        # Encontrar os botões REAIS que abrem modal: são <a> ou <button> com texto EXATO
        # "Ver íntegra do(a) Decisão (Original)" / "(Simplificado)" / "Visualizar Ato Assinado Digitalmente"
        botoes_reais = fr.evaluate("""() => {
            const t_exatos = [
              'ver íntegra do(a) decisão (original)',
              'ver íntegra do(a) decisão (simplificado)',
              'ver íntegra',
              'visualizar ato assinado digitalmente',
              'visualizar ato'
            ];
            return Array.from(document.querySelectorAll('a, button'))
              .filter(el => {
                const t = (el.textContent || '').toLowerCase().trim();
                return el.offsetWidth > 0 && t_exatos.some(te => t.startsWith(te) || t === te);
              })
              .map((el, idx) => ({idx_global: idx, text: (el.textContent||'').trim(), tag: el.tagName}));
        }""")
        print(f"\nBotões de íntegra REAIS encontrados: {len(botoes_reais)}")
        for b in botoes_reais:
            print(f"  - [{b['idx_global']}] <{b['tag']}> {b['text']!r}")

        # Para cada botão, clicar e capturar o modal que abrir
        # Estratégia: re-localizar pelo texto (mais robusto que índice)
        for b in botoes_reais:
            text = b["text"]
            try:
                # Re-localizar o botão pelo texto (passar como argumento para evitar conflito de quoting)
                txt_json = json.dumps(text)  # produz string JSON válida para JS
                clicked = fr.evaluate(f"""(t) => {{
                    const alvo = Array.from(document.querySelectorAll('a, button'))
                      .find(el => el.offsetWidth > 0 && (el.textContent || '').trim() === t);
                    if (alvo) {{ alvo.click(); return true; }}
                    return false;
                }}""", text)
                if not clicked:
                    print(f"  ! não consegui clicar: {text}")
                    continue

                # Esperar modal abrir (qualquer .modal, .ui-dialog, [role=dialog])
                try:
                    fr.wait_for_selector(
                        '.modal-body, .ui-dialog-content, div[role="dialog"], .modal.show, .modal-content',
                        timeout=10000, state="visible"
                    )
                except Exception:
                    # Tenta sem wait_for_selector — alguns modais são inline
                    pass
                time.sleep(4)

                modal_text = fr.evaluate("""() => {
                    // Priorizar conteúdo dentro de containers de modal
                    const containers = Array.from(document.querySelectorAll(
                      '.modal-body, .ui-dialog-content, div[role="dialog"] .modal-body, .modal.show .modal-body'
                    )).filter(c => c.offsetWidth > 0 && c.offsetHeight > 0);

                    if (containers.length > 0) {
                        // Pegar texto DENTRO do container, excluindo botões
                        const txt = containers.map(c => c.innerText || c.textContent).join('\\n\\n---\\n\\n');
                        if (txt && txt.trim().length > 30) return txt;
                    }

                    // Fallback: tentar .modal-content direto
                    const mc = Array.from(document.querySelectorAll('.modal.show .modal-content, .modal-content'));
                    if (mc.length > 0) {
                        return mc.map(c => c.innerText || c.textContent).join('\\n\\n---\\n\\n');
                    }

                    // Último fallback: body
                    return document.body.innerText;
                }""")

                integrais.append({
                    "botao": text,
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "conteudo": modal_text[:15000],
                    "tamanho": len(modal_text),
                })

                # Fechar modal
                fr.evaluate("""() => {
                    // Tenta fechar via botão
                    const close = document.querySelector('.modal.show .btn-close, .modal.show .close, .modal.show button[aria-label="Close"], .ui-dialog-titlebar-close');
                    if (close) { close.click(); return; }
                    // Tenta ESC
                    ['keydown','keyup'].forEach(t => {
                      const e = new KeyboardEvent(t, {key:'Escape', code:'Escape', keyCode:27, which:27, bubbles:true});
                      document.dispatchEvent(e); window.dispatchEvent(e);
                    });
                }""")
                time.sleep(3)
            except Exception as e:
                integrais.append({"botao": text, "erro": str(e)})
        browser.close()

    # Salvar
    out = RAW_DIR / f"integrais_lucas_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.json"
    out.write_text(json.dumps(integrais, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[OK] Salvo em: {out}")
    print(f"     Integrais capturadas: {sum(1 for i in integrais if 'conteudo' in i)}")
    print(f"     Erros: {sum(1 for i in integrais if 'erro' in i)}")
    for i, ig in enumerate(integrais, 1):
        if "erro" in ig:
            print(f"     [{i}] ERRO: {ig['botao']!r}: {ig['erro'][:80]}")
        else:
            # mostrar primeiras 100 chars reais
            c = ig["conteudo"].strip()[:150]
            print(f"     [{i}] {ig['botao']!r}: {c!r}")


if __name__ == "__main__":
    main()
