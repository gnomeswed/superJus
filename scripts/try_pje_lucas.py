#!/usr/bin/env python3
"""Try accessing PJe for Lucas taxista process - 0808595-36.2026.8.19.0002"""
import os, sys, time, json

PROC = "0808595-36.2026.8.19.0002"
CLIENT_DIR = os.path.join("C:", os.sep, "Projetos", "superJus", "Clientes", "Lucas_Dias_Oliveira")
DOCS_DIR = os.path.join(CLIENT_DIR, "03_Documentos_do_Processo")
RASPED_DIR = os.path.join(DOCS_DIR, "_raspagem_2026-08-16")

os.makedirs(DOCS_DIR, exist_ok=True)
os.makedirs(RASPED_DIR, exist_ok=True)

from playwright.sync_api import sync_playwright

results = {
    "processo": PROC,
    "cliente": "Lucas Dias Oliveira (Taxista)",
    "data_raspagem": "2026-08-16",
    "metodos_tentados": [],
    "erros": [],
}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1366, "height": 900})
    
    # Method 1: Try DataJud API
    print("[1/4] Tentando DataJud API...")
    page = ctx.new_page()
    try:
        resp = page.goto(f"https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search?q={PROC}", timeout=15000)
        if resp and resp.status == 200:
            content = page.inner_text("body")
            results["metodos_tentados"].append({"metodo": "DataJud", "status": "ok", "tamanho": len(content)})
            print(f"  ✅ DataJud OK: {len(content)} chars")
            with open(os.path.join(RASPED_DIR, "datajud_response.json"), "w", encoding="utf-8") as f:
                f.write(content)
        else:
            status = resp.status if resp else "no response"
            results["metodos_tentados"].append({"metodo": "DataJud", "status": f"HTTP {status}"})
            print(f"  ❌ DataJud HTTP {status}")
    except Exception as e:
        results["metodos_tentados"].append({"metodo": "DataJud", "status": str(e)[:200]})
        print(f"  ❌ DataJud: {e}")
    page.close()

    # Method 2: Try PJe TJRJ direct
    print("[2/4] Tentando PJe TJRJ...")
    page = ctx.new_page()
    try:
        resp = page.goto(f"https://pje.tjrj.jus.br/pje/login.seam", timeout=15000, wait_until="domcontentloaded")
        status = resp.status if resp else "no response"
        print(f"  PJe status: {status}")
        results["metodos_tentados"].append({"metodo": "PJe TJRJ", "status": f"HTTP {status}"})
    except Exception as e:
        print(f"  ❌ PJe TJRJ: {e}")
        results["metodos_tentados"].append({"metodo": "PJe TJRJ", "status": str(e)[:200]})
    page.close()

    # Method 3: Try Google search for the process
    print("[3/4] Buscando no Google...")
    page = ctx.new_page()
    try:
        page.goto(f"https://www.google.com/search?q=%22{PROC}%22+site:tjrj.jus.br", timeout=15000, wait_until="domcontentloaded")
        time.sleep(3)
        content = page.inner_text("body")
        if PROC in content:
            results["metodos_tentados"].append({"metodo": "Google", "status": "encontrado", "tamanho": len(content)})
            print(f"  ✅ Google encontrou referências: {len(content)} chars")
            with open(os.path.join(RASPED_DIR, "google_results.txt"), "w", encoding="utf-8") as f:
                f.write(content[:20000])
        else:
            results["metodos_tentados"].append({"metodo": "Google", "status": "nao_encontrado"})
            print(f"  ❌ Google não encontrou")
    except Exception as e:
        results["metodos_tentados"].append({"metodo": "Google", "status": str(e)[:200]})
        print(f"  ❌ Google: {e}")
    page.close()

    # Method 4: Try TJRJ API directly (the /api/processos/ endpoint)
    print("[4/4] Tentando API TJRJ...")
    page = ctx.new_page()
    try:
        # Try the internal API that the portal uses
        resp = page.goto(f"https://www3.tjrj.jus.br/ejud/api/PesquisaProcessualApi/listarProcessos?numero={PROC}", timeout=15000, wait_until="domcontentloaded")
        if resp:
            content = page.inner_text("body")
            results["metodos_tentados"].append({"metodo": "TJRJ API", "status": f"HTTP {resp.status}", "tamanho": len(content)})
            print(f"  TJRJ API status: {resp.status}, tamanho: {len(content)}")
            if len(content) > 100:
                with open(os.path.join(RASPED_DIR, "tjrj_api_response.json"), "w", encoding="utf-8") as f:
                    f.write(content)
    except Exception as e:
        results["metodos_tentados"].append({"metodo": "TJRJ API", "status": str(e)[:200]})
        print(f"  ❌ TJRJ API: {e}")
    page.close()

    browser.close()

with open(os.path.join(RASPED_DIR, "resultado_pje.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print("RESULTADO:")
print(json.dumps(results, ensure_ascii=False, indent=2))
