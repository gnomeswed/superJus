# -*- coding: utf-8 -*-
"""Buscar movimentos completos do processo do Júlio usando numProcesso interno."""
import os, sys, time, json, logging
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
sys.stdout.reconfigure(encoding="utf-8")
os.environ["PYTHONIOENCODING"] = "utf-8"

NUM_INTERNO = "2021.078.023002-1"
ID_PROC = 133666226

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        viewport={"width": 1366, "height": 850},
    )
    page = ctx.new_page()
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000, wait_until="domcontentloaded")
    time.sleep(3)
    page.wait_for_selector("iframe#mainframe", timeout=20000)

    # Tenta o endpoint de movimentos com o número interno
    candidates = [
        ("por-numero/movimentos", {"tipoProcesso": 1, "codigoProcesso": NUM_INTERNO, "indProcVolumoso": "N", "ultimaOrdemExibida": None}),
        ("por-numero/movimentos", {"tipoProcesso": 1, "codigoProcesso": NUM_INTERNO, "indProcVolumoso": "N", "idProcesso": ID_PROC, "ultimaOrdemExibida": None}),
    ]

    for ep, payload in candidates:
        result = page.evaluate("""async (args) => {
            const [ep, payload] = args;
            try {
                const resp = await fetch('/consultaprocessual/api/processos/' + ep, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                });
                return JSON.stringify(await resp.json());
            } catch(e) {
                return 'ERRO_FETCH: ' + e.message;
            }
        }""", [ep, payload])

        if result.startswith("ERRO_FETCH"):
            print(f"[{ep}] ERRO: {result}")
            continue
        data = json.loads(result)
        if isinstance(data, list) and len(data) == 1 and isinstance(data[0], str):
            print(f"[{ep}] RESPOSTA: {data[0][:100]}")
            continue
        # Encontrou movimentos?
        movs = data if isinstance(data, list) else (data.get("movimentosProc") or data.get("movimentos") or [])
        print(f"[{ep}] OK — {len(movs)} movimentos")

        out_file = r"C:\Projetos\superJus\Clientes\Julio_Pereira_Marcos\Caso_Principal\analises\movimentos_julio_11_08_2026.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump({"processo": NUM_INTERNO, "total_movimentos": len(movs), "movimentos": movs}, f, ensure_ascii=False, indent=2)
        print(f"[OK] Salvo em {out_file}")

        # Mostrar últimos movimentos
        print("\n=== ÚLTIMOS MOVIMENTOS ===")
        for m in movs[-8:]:
            if isinstance(m, dict):
                dm = m.get("data") or m.get("dataMovimento") or m.get("dataPublicacao") or ""
                desc = m.get("descricao") or m.get("movimento") or ""
                comp = m.get("complemento") or m.get("observacao") or m.get("descricaoComplementar") or ""
                print(f"  [{dm}] {desc} {comp}")
            else:
                print(f"  {str(m)[:150]}")
        break

    browser.close()