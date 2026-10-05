# -*- coding: utf-8 -*-
"""Verificar o processo 0029845 (HC/RHC TJRJ) do Júlio — 2ª instância."""
import os, sys, time, json, logging
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
sys.stdout.reconfigure(encoding="utf-8")
os.environ["PYTHONIOENCODING"] = "utf-8"

# Processos da 2ª instância encontrados na busca
processos = [
    ("0029845-67.2026.8.19.0000", "HC 2ª Instância (Sétima Câmara)"),
]

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

    for proc_num, title in processos:
        print(f"\n=== {title} ({proc_num}) ===")
        # 1. Buscar por numeração única (2ª instância = tipo 2?)
        for tipo in ["1", "2"]:
            result = page.evaluate("""async (args) => {
                const [procNumero, tipoP] = args;
                try {
                    const resp = await fetch('/consultaprocessual/api/processos/por-numeracao-unica', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            tipoProcesso: tipoP,
                            codigoProcesso: procNumero
                        })
                    });
                    return JSON.stringify(await resp.json());
                } catch(e) {
                    return 'ERRO_FETCH: ' + e.message;
                }
            }""", [proc_num, tipo])
            data = json.loads(result)
            if isinstance(data, list) and len(data) == 1 and isinstance(data[0], str):
                print(f"  tipo={tipo}: {data[0]}")
            elif isinstance(data, list) and data:
                print(f"  tipo={tipo}: {len(data)} resultado(s)")
                for item in data:
                    if isinstance(item, dict):
                        print(f"    numProcesso={item.get('numProcesso')} | classe={item.get('classe')} | serventia={item.get('descricaoServentia')} | ultimoMovimento={item.get('ultimoMovimento')} | id={item.get('idProcesso')}")
            else:
                print(f"  tipo={tipo}: {str(data)[:150]}")

    browser.close()