"""
Extrator TJRJ - Wrapper genérico para todos os clientes/casos.
Requisito: Playwright instalado localmente para operar a janela do Chromium.
"""
from __future__ import annotations

import os
import re
import time
import ctypes
from typing import Optional

try:
    from playwright.sync_api import sync_playwright
except Exception:  # pragma: no cover
    sync_playwright = None  # type: ignore[misc,assignment]

PROCESSOS_CACHE_PATH = r"C:\Projetos\Super Analista Jurídico\scripts\.process_number_cache.json"


def _load_last_process() -> Optional[str]:
    try:
        import json
        if os.path.exists(PROCESSOS_CACHE_PATH):
            with open(PROCESSOS_CACHE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("process_number")
    except Exception:
        pass
    return None


def _save_last_process(process_number: str) -> None:
    try:
        import json
        os.makedirs(os.path.dirname(PROCESSOS_CACHE_PATH), exist_ok=True)
        with open(PROCESSOS_CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump({"process_number": process_number}, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def _check_playwright() -> None:
    if sync_playwright is None:
        raise RuntimeError(
            "Playwright não está instalado neste ambiente. "
            "Para usar a atualização do TJRJ, instale com: "
            "pip install playwright && python -m playwright install chromium"
        )


def _sanitize(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*\n\r]', '_', name).strip()[:120]


def extract_tjrj(process_number: str, save_dir: str, headless: bool = False) -> str:
    _check_playwright()

    clean_number = re.sub(r"\D", "", process_number)
    if not clean_number:
        raise ValueError("Número de processo inválido.")

    save_dir = os.path.abspath(save_dir)
    os.makedirs(save_dir, exist_ok=True)

    # Remove arquivos residuais pequenos
    for filename in os.listdir(save_dir):
        filepath = os.path.join(save_dir, filename)
        if os.path.isfile(filepath) and os.path.getsize(filepath) < 200:
            os.remove(filepath)

    ctypes.windll.user32.MessageBoxW(
        0,
        "Uma NOVA JANELA do Chromium será aberta.\n\n"
        "Por favor, procure ela na sua barra de tarefas!\n\n"
        "Você precisa pesquisar o processo NELA, e clicar em 'Todos Os Movimentos' e '500 por página'.\n\n"
        "O script vai esperar você fazer isso.",
        "Extrator TJRJ",
        0x40 | 0x10000,
    )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=bool(headless))
        ctx = browser.new_context(viewport={"width": 1280, "height": 800})
        page = ctx.new_page()

        page.goto(
            "https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica",
            timeout=60000,
            wait_until="networkidle",
        )

        frame = None
        for i in range(600):
            try:
                el = page.query_selector("iframe#mainframe")
                if el:
                    f = el.content_frame()
                    if f:
                        btns = f.query_selector_all("button")
                        originals = [
                            b
                            for b in btns
                            if "original" in (b.inner_text() or "").lower()
                            and "ver" in (b.inner_text() or "").lower()
                        ]
                        if len(originals) >= 10:
                            frame = f
                            print(f"\nDetectados {len(originals)} botoes 'Original'! Iniciando...")
                            time.sleep(5)
                            break
                        elif len(originals) > 0 and i % 10 == 0:
                            print(
                                f"  Vistos apenas {len(originals)} botoes. Por favor, "
                                "clique em 'Todos Os Movimentos' e mude a paginacao."
                            )
            except Exception:
                pass
            if i % 10 == 0 and i > 0:
                print(f"  Aguardando voce na JANELA DO CHROMIUM... ({i * 3}s)")
            time.sleep(3)

        if not frame:
            browser.close()
            return (
                "[-] Timeout atingido. Nao foi possivel detectar o frame do TJRJ.\n"
                f"Pasta: {save_dir}"
            )

        print("\nMapeando documentos...")

        btn_info = []
        btns_all = frame.query_selector_all("button")
        originals = [
            b for b in btns_all if "original" in (b.inner_text() or "").lower() and "ver" in (b.inner_text() or "").lower()
        ]

        for idx, btn in enumerate(originals):
            try:
                context = frame.evaluate(
                    """(el) => {
                        const mov = el.closest('app-movimento');
                        if (!mov) return {date: 'sem_data', tipo: 'documento'};
                        const txt = mov.textContent || '';
                        const dm = txt.match(/\\d{2}\\/\\d{2}\\/\\d{4}/);
                        let tipo = 'documento';
                        const titleEl = mov.querySelector('.titulo-movimentacao');
                        if (titleEl) {
                            tipo = titleEl.textContent.replace('Tipo do Movimento:', '').trim();
                        }
                        return {date: dm ? dm[0] : 'sem_data', tipo: tipo};
                    }""",
                    btn,
                )
                btn_info.append(context)
            except Exception:
                btn_info.append({"date": f"sem_data_{idx}", "tipo": "documento"})

        total = len(originals)
        saved = 0
        failed = 0

        old_content = frame.evaluate(
            """() => {
                const m = document.querySelector('#descricaoDetalhadaModal .modal-body');
                return m ? m.innerText.trim() : '';
            }"""
        )

        for i in range(total):
            date_str = btn_info[i]["date"].replace("/", "-")
            tipo = _sanitize(btn_info[i]["tipo"])
            print(f"[{i + 1}/{total}] {date_str} | {tipo}...")

            try:
                frame.evaluate(
                    """() => {
                        if (window.jQuery) {
                            const bsm = window.jQuery('#descricaoDetalhadaModal').data('bs.modal');
                            if (bsm) { bsm._isTransitioning = false; bsm._isShown = false; }
                        }
                    }"""
                )
                time.sleep(0.5)

                frame.evaluate(
                    f"""() => {{
                        const btns = Array.from(document.querySelectorAll('button')).filter(b => {{
                            const t = b.textContent.toLowerCase();
                            return t.includes('ver') && t.includes('ntegra') && t.includes('original');
                        }});
                        if (btns[{i}]) {{
                            btns[{i}].scrollIntoView({{block: 'center'}});
                            btns[{i}].click();
                        }}
                    }}"""
                )

                content = None
                for w in range(25):
                    time.sleep(1)
                    try:
                        txt = frame.evaluate(
                            """() => {
                                const m = document.querySelector("#descricaoDetalhadaModal .modal-body");
                                return m ? m.innerText.trim() : "";
                            }"""
                        )

                        if txt and len(txt) > 100 and txt != old_content:
                            for lixo in [
                                "Descricao Detalhada",
                                "Descrição Detalhada",
                                "Cancelar",
                                "Imprimir",
                            ]:
                                txt = txt.replace(lixo, "")
                            txt = txt.strip()
                            if len(txt) > 50:
                                content = txt
                                old_content = frame.evaluate(
                                    """() => {
                                        const m = document.querySelector('#descricaoDetalhadaModal .modal-body');
                                        return m ? m.innerText.trim() : '';
                                    }"""
                                )
                                break
                    except Exception:
                        pass

                if content:
                    fname = _sanitize(f"{date_str}_{tipo}.txt")
                    fpath = os.path.join(save_dir, fname)
                    if os.path.exists(fpath):
                        fname = _sanitize(f"{date_str}_{tipo}_{i + 1:03d}.txt")
                        fpath = os.path.join(save_dir, fname)

                    with open(fpath, "w", encoding="utf-8") as outf:
                        outf.write(f"Processo: {clean_number}\n")
                        outf.write(f"Data: {btn_info[i]['date']}\n")
                        outf.write(f"Tipo: {btn_info[i]['tipo']}\n")
                        outf.write("=" * 60 + "\n\n")
                        outf.write(content)
                    print(f"  [OK] Salvo ({len(content)} chars)")
                    saved += 1
                else:
                    print("  [FALHA] Modal vazio ou nao atualizou")
                    failed += 1

            except Exception as e:
                print(f"  [ERRO] {e}")
                failed += 1

            try:
                frame.evaluate(
                    """() => {
                        const cb = document.querySelector('.rodape-cancela');
                        if (cb) cb.click();

                        if (window.jQuery) {
                            window.jQuery('#descricaoDetalhadaModal').modal('hide');
                        }
                        setTimeout(() => {
                            document.querySelectorAll('.modal-backdrop').forEach(e => e.remove());
                            const m = document.getElementById('descricaoDetalhadaModal');
                            if (m) { m.classList.remove('show'); m.style.display = 'none'; }
                            document.body.classList.remove('modal-open');
                            document.body.style.overflow = '';
                            if (window.jQuery) {
                                const bsm = window.jQuery('#descricaoDetalhadaModal').data('bs.modal');
                                if (bsm) { bsm._isTransitioning = false; bsm._isShown = false; }
                            }
                        }, 500);
                    }"""
                )
            except Exception:
                pass

            time.sleep(1.5)

        browser.close()
        final_msg = f"\n{'=' * 60}\nCONCLUIDO! Salvos: {saved} | Falhas: {failed}\nPasta: {save_dir}\n{'=' * 60}\n"
        print(final_msg)
        return final_msg
