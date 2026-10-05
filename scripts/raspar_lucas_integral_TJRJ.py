# -*- coding: utf-8 -*-
"""
Raspagem integral do processo Lucas de Souza Freitas.
Processo principal: 0011857-95.2024.8.19.0002

- 1ª instância TJRJ com lista expandida (Todos os Movimentos)
- Captura de modais 'Ver Íntegra' e 'Visualizar Ato Assinado Digitalmente'
- 2ª instância via busca por nome
- Tentativas STJ/DJEN

Salva em Clientes/Lucas_Freitas/02_Movimentacoes_Individuais/ e 03_Documentos_do_Processo/
"""

def main() -> None:
    import sys, time, json, re
    from datetime import datetime
    from pathlib import Path
    from playwright.sync_api import sync_playwright

    sys.stdout.reconfigure(encoding="utf-8")

    OUT_DIR = Path(r"C:\Projetos\superJus\Clientes\Lucas_Freitas\02_Movimentacoes_Individuais")
    DOC_INTEGRA = Path(r"C:\Projetos\superJus\Clientes\Lucas_Freitas\03_Documentos_do_Processo\Decisoes_na_Integra")
    RAW_DIR = Path(r"C:\Projetos\superJus\Clientes\Lucas_Freitas\03_Documentos_do_Processo\_raspagem_10_08_2026")
    for d in (OUT_DIR, DOC_INTEGRA, RAW_DIR):
        d.mkdir(parents=True, exist_ok=True)

    PROC = "0011857-95.2024.8.19.0002"
    NOME = "Lucas de Souza Freitas"
    TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    HOJE = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    HOJE_SHORT = datetime.now().strftime("%Y-%m-%d")

    resultados = {
        "timestamp": HOJE,
        "processo_principal": PROC,
        "1_instancia": {"dados_cabecalho": {}, "movimentos_estruturados": [], "integrais": []},
        "2_instancia_busca_nome": {},
        "stj_tentativas": [],
        "djen_tentativas": [],
    }

    # ============================================================
    # 1ª INSTÂNCIA — TJRJ
    # ============================================================
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = browser.new_context(viewport={"width": 1366, "height": 900})
        page = ctx.new_page()
        print(f"\n[{HOJE}] 1ª INSTÂNCIA: {PROC}")

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

        # Capturar dados do cabeçalho (antes de expandir movimentos)
        body_header = fr.inner_text("body")
        resultados["1_instancia"]["dados_cabecalho"]["texto"] = body_header

        # Expandir "Todos os Movimentos" e aguardar request /api/processos/por-numero/movimentos
        fr.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button'))
              .find(b => (b.textContent || '').toLowerCase().includes('todos os movimentos'));
            if (btn) btn.click();
        }""")
        time.sleep(12)  # espera request AJAX dos movimentos

        # Re-capturar texto completo com lista expandida
        body_full = fr.inner_text("body")
        html_full = fr.evaluate("() => document.documentElement.outerHTML")
        (RAW_DIR / "1_instancia_movimentos_full.html").write_text(html_full, encoding="utf-8")
        (RAW_DIR / "1_instancia_movimentos_full.txt").write_text(body_full, encoding="utf-8")
        try:
            page.screenshot(path=str(RAW_DIR / "1_instancia_movimentos_full.png"), full_page=True)
        except Exception:
            pass

        # Extrair Localização na Serventia
        linhas = body_full.split("\n")
        for i, ln in enumerate(linhas):
            if "Localização" in ln or "Localizacao" in ln:
                if i + 1 < len(linhas):
                    resultados["1_instancia"]["dados_cabecalho"]["localizacao_serventia"] = linhas[i+1].strip()
                break

        # Extrair blocos de movimento (cada bloco começa com "Tipo do Movimento: X")
        blocos = []
        bloco_atual = None
        for ln in linhas:
            s = ln.strip()
            if s.startswith("Tipo do Movimento:"):
                if bloco_atual:
                    blocos.append(bloco_atual)
                bloco_atual = {"tipo": s.replace("Tipo do Movimento:", "").strip(), "linhas": []}
            elif bloco_atual is not None and s:
                bloco_atual["linhas"].append(s)
        if bloco_atual:
            blocos.append(bloco_atual)

        # Resumir blocos: data + texto principal
        movs_resumidos = []
        for b in blocos:
            data = ""
            texto = " ".join(b["linhas"])
            m = re.search(r"\d{2}/\d{2}/\d{4}", texto)
            if m:
                data = m.group(0)
            movs_resumidos.append({"data": data, "tipo": b["tipo"], "texto": texto[:600]})
        resultados["1_instancia"]["movimentos_estruturados"] = movs_resumidos

        # Capturar integrais: clicar nos links "Ver Íntegra Do(A) Decisão (Original)" e "Visualizar Ato Assinado Digitalmente"
        print(f"   -> Capturando modais (até 30)...")
        integrais = []
        # Mapear todos os botões/links que abrem modal
        botoes_integrais = fr.evaluate("""() => {
            const all = Array.from(document.querySelectorAll('a, button, span, div'))
              .filter(el => el.offsetWidth > 0 && el.offsetHeight > 0);
            return all.map((el, idx) => {
                const t = (el.textContent || '').toLowerCase().trim();
                if (t.includes('ver íntegra') || t.includes('ver integra') ||
                    t.includes('visualizar ato assinado') ||
                    t.includes('visualizar ato')) {
                  return {idx, tag: el.tagName, text: (el.textContent||'').trim().slice(0, 80)};
                }
                return null;
            }).filter(Boolean);
        }""")
        print(f"      {len(botoes_integrais)} botões integrais detectados")
        for bi in botoes_integrais[:30]:
            idx = bi["idx"]
            try:
                # Re-localizar pelo índice
                fr.evaluate(f"""(i) => {{
                    const all = Array.from(document.querySelectorAll('a, button, span, div'))
                      .filter(el => el.offsetWidth > 0 && el.offsetHeight > 0);
                    if (all[i]) all[i].click();
                }}""", idx)
                time.sleep(6)
                modal_text = fr.evaluate("""() => {
                    const modals = Array.from(document.querySelectorAll(
                      '.modal-body, .ui-dialog-content, div[role="dialog"], .modal.show, .modal-content, .modal-dialog'
                    ));
                    if (modals.length) return modals.map(m => m.innerText.trim()).join('\\n\\n---\\n\\n');
                    // se não acha modal, dump do body
                    return document.body.innerText;
                }""")
                integrais.append({
                    "botao": bi["text"],
                    "conteudo": modal_text[:10000]
                })
                # Fechar modal
                fr.evaluate("""() => {
                    const close = document.querySelector('.modal.show .close, .modal.show button[aria-label="Close"], .modal.show button.btn-close, .ui-dialog-titlebar-close');
                    if (close) close.click();
                    const esc = new KeyboardEvent('keydown', {key: 'Escape', code: 'Escape', keyCode: 27, bubbles: true});
                    document.dispatchEvent(esc); window.dispatchEvent(esc);
                }""")
                time.sleep(2)
            except Exception as e:
                integrais.append({"botao": bi["text"], "erro": str(e)})
        resultados["1_instancia"]["integrais"] = integrais

        browser.close()

    # ============================================================
    # 2ª INSTÂNCIA — busca por nome (sem saber o número ainda)
    # ============================================================
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = browser.new_context(viewport={"width": 1366, "height": 900})
        page = ctx.new_page()
        print(f"\n[{HOJE}] 2ª INSTÂNCIA: busca por nome '{NOME}'")

        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000)
        page.wait_for_selector("iframe#mainframe", timeout=30000)
        fr = page.query_selector("iframe#mainframe").content_frame()
        time.sleep(2)

        # Clica "Por Nome"
        fr.evaluate("""() => {
            const alvo = Array.from(document.querySelectorAll('label, span, a, div, button'))
              .find(c => (c.textContent || '').trim().toLowerCase() === 'por nome');
            if (alvo) alvo.click();
        }""")
        time.sleep(2)
        # Preencher campo de nome
        fr.evaluate(f"""() => {{
            const inputs = Array.from(document.querySelectorAll('input[type=text], input:not([type])'))
              .filter(i => i.offsetWidth > 50);
            const target = inputs[inputs.length - 1] || inputs[0];
            if (target) {{
              target.value = '{NOME}';
              target.dispatchEvent(new Event('input', {{ bubbles: true }}));
              target.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
        }}""")
        fr.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button'))
              .find(b => b.offsetWidth > 0 && b.textContent.toLowerCase().includes('pesquisar'));
            if (btn) btn.click();
        }""")
        time.sleep(10)
        body_2 = fr.inner_text("body")
        (RAW_DIR / "2_instancia_busca_nome.txt").write_text(body_2, encoding="utf-8")
        try:
            page.screenshot(path=str(RAW_DIR / "2_instancia_busca_nome.png"), full_page=True)
        except Exception:
            pass
        resultados["2_instancia_busca_nome"]["texto"] = body_2[:8000]
        resultados["2_instancia_busca_nome"]["url_final"] = fr.url
        browser.close()

    # ============================================================
    # Salvar JSON consolidado
    # ============================================================
    out_json = RAW_DIR / f"raspagem_lucas_{TIMESTAMP}.json"
    out_json.write_text(json.dumps(resultados, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[OK] JSON: {out_json}")
    print(f"     Movimentos estruturados: {len(resultados['1_instancia']['movimentos_estruturados'])}")
    print(f"     Integrais capturadas:    {len(resultados['1_instancia']['integrais'])}")
    print(f"     Localização: {resultados['1_instancia']['dados_cabecalho'].get('localizacao_serventia', 'N/I')}")


if __name__ == "__main__":
    main()
