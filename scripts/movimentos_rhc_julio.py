# -*- coding: utf-8 -*-
"""Tentar variações do número para o endpoint de movimentos (2ª instância)."""
import os, sys, time, json, logging
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
sys.stdout.reconfigure(encoding="utf-8")
os.environ["PYTHONIOENCODING"] = "utf-8"

processos = [
    ("2026.141.00580", "RHC", 146358827),
    ("2026.059.10770", "HC", 145135296),
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

    for num, title, pid in processos:
        print(f"\n=== {title} ({num}) ===")
        # Variações de formato: 2026.141.00580 -> 2026.141.005800-0? ou 2026.141.580-1?
        variacoes = [
            num,
            num + "-0",
            num + "-1",
            num.replace(".", ""),          # 202614100580
            "2026.141.005800-0",
            "2026.141.005800-1",
        ]
        for v in variacoes:
            for tipo in [1, 2]:
                result = page.evaluate("""async (args) => {
                    const [procNumero, tipoP] = args;
                    try {
                        const resp = await fetch('/consultaprocessual/api/processos/por-numero/movimentos', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({
                                tipoProcesso: tipoP,
                                codigoProcesso: procNumero,
                                indProcVolumoso: 'N',
                                ultimaOrdemExibida: null
                            })
                        });
                        return JSON.stringify(await resp.json());
                    } catch(e) {
                        return 'ERRO_FETCH: ' + e.message;
                    }
                }""", [v, tipo])
                data = json.loads(result)
                if isinstance(data, list) and len(data) == 1 and isinstance(data[0], str):
                    continue  # inválido
                movs = data if isinstance(data, list) else (data.get("movimentosProc") or data.get("movimentos") or [])
                if movs:
                    print(f"  ✅ [{v}] tipo={tipo}: {len(movs)} movimentos!")
                    def fmt_mov(m):
                        dt = m.get("dtMovimento") or m.get("dt") or m.get("dtAlt") or ""
                        desc = m.get("descrMov") or m.get("descricao") or ""
                        extras = []
                        for ex in m.get("movimentosExibicao") or []:
                            t = ex.get("tipoMovimento", "")
                            dets = ex.get("detalhesMovimento") or []
                            det_str = "; ".join(f"{d.get('codigo','')}{d.get('descricao','')}" for d in dets)
                            extras.append(f"{t} [{det_str}]")
                        return f"[{dt}] {desc} | {' | '.join(extras)}"
                    for m in movs[:10]:
                        print("   ", fmt_mov(m)[:220])
                    out_file = rf"C:\Projetos\superJus\Clientes\Julio_Pereira_Marcos\Caso_Principal\analises\movimentos_{title}_11_08_2026.json"
                    with open(out_file, "w", encoding="utf-8") as f:
                        json.dump({"processo": v, "title": title, "total_movimentos": len(movs), "movimentos": movs}, f, ensure_ascii=False, indent=2)
                    print(f"   [OK] Salvo em {out_file}")
                    break
            else:
                continue
            break

    browser.close()