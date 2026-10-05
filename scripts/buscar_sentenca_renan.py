# -*- coding: utf-8 -*-
"""Buscar sentença do Renan (0821248-17.2025.8.19.0031) em 3 fontes."""
import sys, time, json, re
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
PROC = "0821248-17.2025.8.19.0031"
PROC_LIMPO = PROC.replace("-", "").replace(".", "")
COD_INTERNO = None  # vai ser capturado
RAW_DIR = Path(r"C:\Projetos\superJus\Clientes\Renan\03_Documentos_do_Processo\_raspagem_10_08_2026")
RAW_DIR.mkdir(parents=True, exist_ok=True)
INTEGRA_DIR = Path(r"C:\Projetos\superJus\Clientes\Renan\03_Documentos_do_Processo\Decisoes_na_Integra")
INTEGRA_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    resultados = {"processo": PROC, "fontes_tentadas": []}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = browser.new_context(viewport={"width": 1366, "height": 900})
        page = ctx.new_page()

        # ================================================================
        # FONTE 1: TJRJ consulta pública
        # ================================================================
        print(f"\n=== FONTE 1: TJRJ consulta pública ===")
        try:
            page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=60000)
            page.wait_for_selector("iframe#mainframe", timeout=30000)
            time.sleep(2)
            fr = page.query_selector("iframe#mainframe").content_frame()
            # Preencher número
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
            # Pegar dados do frame
            fr_url = fr.url
            resultados["fontes_tentadas"].append({"fonte": "TJRJ", "url": fr_url})
            # Extrair codigoProcesso
            m = re.search(r"codigoProcesso=([^&]+)", fr_url)
            cod_interno = m.group(1) if m else None
            resultados["tjrj_codigo_interno"] = cod_interno
            # Body inicial (resumo)
            body_inicial = fr.inner_text("body")
            resultados["tjrj_body_inicial"] = body_inicial[:1500]
            # Expandir "Todos os Movimentos"
            fr.evaluate("""() => {
                const btn = Array.from(document.querySelectorAll('button'))
                  .find(b => (b.textContent || '').toLowerCase().includes('todos os movimentos'));
                if (btn) btn.click();
            }""")
            time.sleep(15)
            # Pegar via API (mais confiável)
            if cod_interno:
                api_body = f"""(args) => {{
                    return fetch('/consultaprocessual/api/processos/por-numero/movimentos', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify(args)
                    }}).then(r => r.text()).then(t => JSON.parse(t));
                }}"""
                payload = {
                    "tipoProcesso": "1",
                    "codigoProcesso": cod_interno,
                    "indProcVolumoso": "N",
                    "ultimaOrdemExibida": None,
                }
                resp = fr.evaluate(api_body, payload)
                movs = resp.get("movimentosProc") or []
                resultados["tjrj_movimentos_count"] = len(movs)
                # Procurar sentença
                sent_idx = None
                for i, m in enumerate(movs):
                    tipo = (m.get("descrMov") or "").lower()
                    if "senten" in tipo or "sentença" in (m.get("movimentosExibicao", [{}])[0].get("tipoMovimento", "").lower() if m.get("movimentosExibicao") else ""):
                        sent_idx = i
                        break
                resultados["tjrj_sentenca_idx"] = sent_idx
                if sent_idx is not None:
                    sent = movs[sent_idx]
                    resultados["tjrj_sentenca"] = sent
                    # Capturar UI modal (Ver íntegra)
                    # Primeiro: extrair ordem/data
                    ordem_sent = sent.get("ordem")
                    data_sent = sent.get("dtMovimento") or sent.get("dt")
                    print(f"  Sentença encontrada: ordem={ordem_sent}, data={data_sent}")
                    # Tentar abrir modal via clique
                    botoes = fr.evaluate("""() => {
                        return Array.from(document.querySelectorAll('a, button'))
                          .filter(el => {
                            const t = (el.textContent || '').toLowerCase().trim();
                            return el.offsetWidth > 0 && el.offsetHeight > 0 && (
                              t.startsWith('ver íntegra do(a) decisão (original)') ||
                              t.startsWith('ver íntegra do(a) decisão (simplificado)') ||
                              t.startsWith('visualizar ato assinado digitalmente')
                            );
                          })
                          .map(el => ({tag: el.tagName, text: (el.textContent||'').trim()}));
                    }""")
                    print(f"  Botões integrais visíveis: {len(botoes)}")
                    for bi, botao in enumerate(botoes):
                        try:
                            clicked = fr.evaluate(f"""(t) => {{
                                const alvo = Array.from(document.querySelectorAll('a, button'))
                                  .find(el => el.offsetWidth > 0 && (el.textContent || '').trim() === t);
                                if (alvo) {{ alvo.click(); return true; }}
                                return false;
                            }}""", botao["text"])
                            if not clicked:
                                continue
                            try:
                                fr.wait_for_selector('.modal-body, .ui-dialog-content, div[role="dialog"], .modal.show, .modal-content', timeout=10000, state="visible")
                            except Exception:
                                pass
                            time.sleep(5)
                            modal_text = fr.evaluate("""() => {
                                const c = Array.from(document.querySelectorAll(
                                  '.modal-body, .ui-dialog-content, div[role="dialog"] .modal-body, .modal.show .modal-body'
                                )).filter(el => el.offsetWidth > 0 && el.offsetHeight > 0);
                                if (c.length > 0) {
                                    const t = c.map(x => x.innerText || x.textContent).join('\\n\\n---\\n\\n');
                                    if (t && t.trim().length > 30) return t;
                                }
                                const mc = Array.from(document.querySelectorAll('.modal.show .modal-content, .modal-content'))
                                  .filter(el => el.offsetWidth > 0);
                                if (mc.length > 0) return mc.map(x => x.innerText || x.textContent).join('\\n\\n---\\n\\n');
                                return document.body.innerText;
                            }""")
                            # Salvar
                            slug_botao = re.sub(r"\W", "", botao["text"])[:50]
                            fname = f"2026-07-03_ORD{ordem_sent or '?'}_{bi+1:03d}_{slug_botao}.txt"
                            fpath = INTEGRA_DIR / fname
                            content = (
                                f"PROCESSO: {PROC}\n"
                                f"DATA: {data_sent}\n"
                                f"TIPO: Sentença\n"
                                f"ORDEM: {ordem_sent}\n"
                                f"BOTÃO: {botao['text']}\n"
                                f"CAPTURA: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                                f"FONTE: TJRJ (consultaprocessual)\n"
                                f"\n{'='*80}\nINTEGRAL\n{'='*80}\n\n"
                                f"{modal_text}"
                            )
                            fpath.write_text(content, encoding="utf-8")
                            print(f"  ✓ Salvo: {fname} ({len(modal_text)} chars)")
                            resultados.setdefault("integrais_tjrj", []).append({
                                "arquivo": fname, "tamanho": len(modal_text), "botao": botao["text"]
                            })
                            # Fechar modal
                            fr.evaluate("""() => {
                                const c = document.querySelector('.modal.show .btn-close, .modal.show .close, .modal.show button[aria-label="Close"], .ui-dialog-titlebar-close');
                                if (c) c.click();
                                ['keydown','keyup'].forEach(t => {
                                  const e = new KeyboardEvent(t, {key:'Escape', code:'Escape', keyCode:27, which:27, bubbles:true});
                                  document.dispatchEvent(e); window.dispatchEvent(e);
                                });
                            }""")
                            time.sleep(2)
                        except Exception as e:
                            print(f"  ERRO no botão {bi}: {e}")
            # Salvar screenshot
            try:
                page.screenshot(path=str(RAW_DIR / "tjrj_sentenca.png"), full_page=True)
            except Exception:
                pass
        except Exception as e:
            print(f"  TJRJ falhou: {e}")
            resultados["tjrj_error"] = str(e)

        # ================================================================
        # FONTE 2: DJEN / comunica.pje.jus.br
        # ================================================================
        print(f"\n=== FONTE 2: DJEN ===")
        try:
            page2 = ctx.new_page()
            page2.goto("https://comunica.pje.jus.br/consulta?siglaTribunal=TJRJ&meio=D", timeout=45000)
            time.sleep(10)
            djen_body = page2.inner_text("body")
            resultados["djen_body"] = djen_body[:1500]
            print(f"  DJEN body length: {len(djen_body)}")
            # Tentar busca direta no DJEN
            djen_url = f"https://comunica.pje.jus.br/consulta?siglaTribunal=TJRJ&meio=D&texto={PROC}"
            try:
                page2.goto(djen_url, timeout=45000)
                time.sleep(10)
                djen_search_body = page2.inner_text("body")
                resultados["djen_search_body"] = djen_search_body[:1500]
                print(f"  DJEN search body length: {len(djen_search_body)}")
            except Exception as e:
                print(f"  DJEN search err: {e}")
            page2.close()
        except Exception as e:
            print(f"  DJEN falhou: {e}")
            resultados["djen_error"] = str(e)

        # ================================================================
        # FONTE 3: PJe (pje.jus.br) - geralmente requer login
        # ================================================================
        print(f"\n=== FONTE 3: PJe ===")
        try:
            page3 = ctx.new_page()
            page3.goto("https://pje.tjrj.jus.br/pje/login.seam", timeout=45000)
            time.sleep(5)
            pje_url = page3.url
            pje_body = page3.inner_text("body")
            resultados["pje_login_url"] = pje_url
            resultados["pje_login_body"] = pje_body[:1000]
            print(f"  PJe URL: {pje_url}")
            print(f"  PJe body length: {len(pje_body)}")
            page3.close()
        except Exception as e:
            print(f"  PJe falhou: {e}")
            resultados["pje_error"] = str(e)

        browser.close()

    # Salvar manifest
    manifest_file = RAW_DIR / f"raspagem_sentenca_renan_{time.strftime('%Y-%m-%d_%H%M%S')}.json"
    # Truncar campos grandes
    for k, v in list(resultados.items()):
        if isinstance(v, str) and len(v) > 5000:
            resultados[k] = v[:5000] + "...[TRUNCADO]"
    manifest_file.write_text(json.dumps(resultados, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(f"\n[OK] Manifest: {manifest_file.name}")
    integrais_tjrj = resultados.get("integrais_tjrj", [])
    print(f"     Integrais TJRJ: {len(integrais_tjrj)}")
    print(f"     Movimentos TJRJ: {resultados.get('tjrj_movimentos_count', '?')}")


if __name__ == "__main__":
    main()
