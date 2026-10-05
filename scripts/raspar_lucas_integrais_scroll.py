# -*- coding: utf-8 -*-
"""
FASE 3B: Capturar integrais via scroll+click por todos os blocos.
Assume que a fase 3a já foi executada (175 movimentos + 3 integrais).
"""
import sys, time, json, re
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
PROC = "0011857-95.2024.8.19.0002"
CLIENT_DIR = Path(r"C:\Projetos\superJus\Clientes\Lucas_Freitas")
MOV_DIR = CLIENT_DIR / "02_Movimentacoes_Individuais"
INTEGRA_DIR = CLIENT_DIR / "03_Documentos_do_Processo" / "Decisoes_na_Integra"
RAW_DIR = CLIENT_DIR / "03_Documentos_do_Processo" / "_raspagem_10_08_2026"
RAW_DIR.mkdir(parents=True, exist_ok=True)


def slug(s: str) -> str:
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE).strip()
    s = re.sub(r"[-\s]+", "_", s)
    s = s.replace("?", "").replace("*", "").replace(":", "")
    return s[:80]


def main() -> None:
    integrais_capturadas = []
    integrais_processadas = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = browser.new_context(viewport={"width": 1366, "height": 900})
        page = ctx.new_page()
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=60000)
        page.wait_for_selector("iframe#mainframe", timeout=30000)
        time.sleep(2)
        fr = page.query_selector("iframe#mainframe").content_frame()

        # Carregar processo
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
        # Expandir
        fr.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button'))
              .find(b => (b.textContent || '').toLowerCase().includes('todos os movimentos'));
            if (btn) btn.click();
        }""")
        time.sleep(15)

        # Pegar todos os blocos de movimento (cada um tem seus botões integrais)
        # Estratégia: rolar página inteira aos poucos, capturar todos os botões integrais visíveis
        print("\n=== Capturando integrais via scroll + clique em todos os botões visíveis ===\n")
        SCROLL_ITERATIONS = 40
        SCROLL_PX = 600
        for it in range(SCROLL_ITERATIONS):
            # Scroll para baixo
            fr.evaluate(f"""() => {{
                const all = document.querySelector('*');
                const scrollable = Array.from(document.querySelectorAll('*'))
                  .find(el => el.scrollHeight > el.clientHeight + 100 && el.clientHeight > 200);
                if (scrollable) scrollable.scrollTop += {SCROLL_PX};
                else window.scrollBy(0, {SCROLL_PX});
            }}""")
            time.sleep(1.5)
            # Capturar botões visíveis NOVOS (que ainda não processamos)
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
                  .map((el) => ({tag: el.tagName, text: (el.textContent||'').trim()}));
            }""")
            for b in botoes:
                if b["text"] in integrais_processadas:
                    continue
                integrais_processadas.add(b["text"])
                try:
                    clicked = fr.evaluate(f"""(t) => {{
                        const alvo = Array.from(document.querySelectorAll('a, button'))
                          .find(el => el.offsetWidth > 0 && el.offsetHeight > 0 && (el.textContent || '').trim() === t);
                        if (alvo) {{ alvo.click(); return true; }}
                        return false;
                    }}""", b["text"])
                    if not clicked:
                        continue
                    try:
                        fr.wait_for_selector(
                            '.modal-body, .ui-dialog-content, div[role="dialog"], .modal.show, .modal-content',
                            timeout=10000, state="visible",
                        )
                    except Exception:
                        pass
                    time.sleep(4)
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
                    datas = re.findall(r'\b(\d{2}/\d{2}/\d{4})\b', modal_text[:500])
                    data = datas[0] if datas else "?"
                    tipo = "?"
                    m = re.search(r'Tipo do Movimento: ([^\n]+)', modal_text[:500])
                    if m:
                        tipo = m.group(1).strip()
                    ordem = "?"
                    # Salvar
                    data_slug = data.replace("/", "-") if data else "data_desconhecida"
                    ordem_slug = str(ordem) if ordem and str(ordem).isdigit() else "SORD"
                    fname = f"{data_slug}_ORD{ordem_slug}_{(len(integrais_capturadas)+1):03d}_{slug(b['text'])}.txt"
                    fpath = INTEGRA_DIR / fname
                    lines = [
                        f"PROCESSO: {PROC}",
                        f"DATA: {data}",
                        f"TIPO: {tipo}",
                        f"ORDEM: {ordem}",
                        f"BOTÃO: {b['text']}",
                        f"CAPTURA: {time.strftime('%Y-%m-%d %H:%M:%S')}",
                        "",
                        "=" * 80,
                        "INTEGRAL",
                        "=" * 80,
                        "",
                        modal_text,
                    ]
                    fpath.write_text("\n".join(lines), encoding="utf-8")
                    integrais_capturadas.append({
                        "data": data, "tipo": tipo, "ordem": ordem,
                        "botao": b["text"], "arquivo": fname, "tamanho": len(modal_text),
                    })
                    print(f"    [{len(integrais_capturadas)}] {fname} ({len(modal_text)} chars)")
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
                    print(f"    ERRO: {e}")
            # Status a cada iteração
            if it % 5 == 0:
                print(f"  iter {it}/{SCROLL_ITERATIONS}  integrais={len(integrais_capturadas)}  processadas={len(integrais_processadas)}")
        browser.close()

    manifest = {
        "processo": PROC,
        "data": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total": len(integrais_capturadas),
        "integrais": integrais_capturadas,
    }
    mf = RAW_DIR / f"manifest_fase3b_{time.strftime('%Y-%m-%d_%H%M%S')}.json"
    mf.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[OK] {len(integrais_capturadas)} integrais capturadas via scroll")
    print(f"     Manifest: {mf.name}")


if __name__ == "__main__":
    main()
