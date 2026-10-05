# -*- coding: utf-8 -*-
"""Verificação em tempo real dos processos do Júlio Pereira Marcos — 13/08/2026."""
import os, sys, time, json, logging
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
sys.stdout.reconfigure(encoding="utf-8")
os.environ["PYTHONIOENCODING"] = "utf-8"

processes = [
    ("0023013-51.2021.8.19.0078", "Ação Penal 1ª Instância Búzios"),
    ("0029845-67.2026.8.19.0000", "HC 2ª Instância TJRJ (7ª Câmara)"),
]

results = {}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        viewport={"width": 1366, "height": 850},
    )
    page = ctx.new_page()
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    for proc_num, title in processes:
        logging.info(f"Verificando portal TJRJ para: {title} ({proc_num})...")
        try:
            page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000, wait_until="domcontentloaded")
            time.sleep(3)
            iframe_el = page.wait_for_selector("iframe#mainframe", timeout=20000)
            frame = iframe_el.content_frame()
            if not frame:
                raise RuntimeError("iframe#mainframe sem content_frame")
            inp = frame.query_selector("input[name='numeroProcesso']")
            if not inp:
                raise RuntimeError("input numeroProcesso não encontrado")
            inp.fill(proc_num)
            btns = frame.query_selector_all("button")
            btn = None
            for b in btns:
                txt = b.inner_text().strip()
                if any(w in txt.lower() for w in ["pesquisar", "buscar", "consultar"]):
                    btn = b; break
            if not btn and btns: btn = btns[0]
            if btn:
                btn.click()
                time.sleep(5)
                results[proc_num] = frame.inner_text("body")
                logging.info(f"OK — texto capturado ({len(results[proc_num])} chars)")
        except Exception as e:
            logging.error(f"Erro ao verificar {title}: {e}")
            results[proc_num] = f"ERRO: {e}"
        time.sleep(2)
    browser.close()

out_file = r"C:\Projetos\superJus\Clientes\Julio_Pereira_Marcos\Caso_Principal\analises\verificacao_live_13_08_2026.txt"
os.makedirs(os.path.dirname(out_file), exist_ok=True)
with open(out_file, "w", encoding="utf-8") as f:
    for proc, txt in results.items():
        f.write(f"=== PROCESSO {proc} ===\n{txt}\n\n" + "="*70 + "\n\n")

print(f"Concluído! Salvos em {out_file}")
print(json.dumps({k: v[:200] for k, v in results.items()}, ensure_ascii=False, indent=2))
