# -*- coding: utf-8 -*-
"""Extração direta e completa dos movimentos via API do TJRJ para confirmação minuciosa."""
import os, sys, time, json
from playwright.sync_api import sync_playwright

NUM_INTERNO = "2021.078.023002-1"
ID_PROC = 133666226

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
    ctx = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    page = ctx.new_page()
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000, wait_until="domcontentloaded")
    time.sleep(3)
    page.wait_for_selector("iframe#mainframe", timeout=20000)

    result = page.evaluate("""async (payload) => {
        try {
            const resp = await fetch('/consultaprocessual/api/processos/por-numero/movimentos', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            });
            return JSON.stringify(await resp.json());
        } catch(e) {
            return 'ERRO_FETCH: ' + e.message;
        }
    }""", {"tipoProcesso": 1, "codigoProcesso": NUM_INTERNO, "indProcVolumoso": "N", "ultimaOrdemExibida": None})

    data = json.loads(result)
    movs = data if isinstance(data, list) else (data.get("movimentosProc") or data.get("movimentos") or [])
    
    out_file = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\analises\movimentos_completos_14_08_2026.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({"total": len(movs), "movimentos": movs}, f, ensure_ascii=False, indent=2)

    print(f"Total de movimentos extraídos: {len(movs)}")
    print("\n--- 10 ÚLTIMOS MOVIMENTOS NA 1ª INSTÂNCIA (BÚZIOS) ---")
    for m in movs[-10:]:
        print(json.dumps(m, ensure_ascii=False))

    browser.close()
