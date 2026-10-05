#!/usr/bin/env python3
"""Access PJe public consultation for Lucas taxista - 0808595-36.2026.8.19.0002"""
import os, sys, time, json, re

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
    "documentos_encontrados": [],
    "erros": [],
}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1366, "height": 900})
    
    # Try PJe public consultation URL pattern
    print("[1/3] Tentando PJe Consulta Pública...")
    page = ctx.new_page()
    
    # The URL pattern from the MHTML files suggests this works:
    # https://tjrj.pje.jus.br/pje/ConsultaPublica/listView.seam
    pje_url = "https://tjrj.pje.jus.br/pje/ConsultaPublica/listView.seam"
    
    try:
        resp = page.goto(pje_url, timeout=30000, wait_until="domcontentloaded")
        print(f"  Status: {resp.status if resp else 'no response'}")
        time.sleep(5)
        
        body_text = page.inner_text("body")
        print(f"  Body length: {len(body_text)}")
        print(f"  First 500 chars: {body_text[:500]}")
        
        # Check if we can find a search form
        has_search = page.evaluate("""() => {
            const inputs = Array.from(document.querySelectorAll('input'));
            return inputs.map(i => ({id: i.id, name: i.name, type: i.type, placeholder: i.placeholder}));
        }""")
        print(f"  Inputs found: {json.dumps(has_search, indent=2)}")
        
    except Exception as e:
        print(f"  ❌ PJe: {e}")
        results["erros"].append(f"PJe: {str(e)[:200]}")
    
    page.close()
    
    # Try the direct document URL pattern from the MHTML
    print("\n[2/3] Tentando URL direta do documento...")
    page = ctx.new_page()
    
    # From the MHTML: idProcessoDoc=281122579
    doc_url = "https://tjrj.pje.jus.br/pje/ConsultaPublica/DetalheProcessoConsultaPublica/documentoSemLoginHTML.seam?idProcessoDoc=281122579"
    
    try:
        resp = page.goto(doc_url, timeout=30000, wait_until="domcontentloaded")
        print(f"  Status: {resp.status if resp else 'no response'}")
        time.sleep(5)
        
        body_text = page.inner_text("body")
        print(f"  Body length: {len(body_text)}")
        
        if len(body_text) > 200:
            with open(os.path.join(RASPED_DIR, "pje_documento_direto.txt"), "w", encoding="utf-8") as f:
                f.write(body_text)
            print(f"  ✅ Documento salvo: {len(body_text)} chars")
            
            # Extract key information
            results["documentos_encontrados"].append({
                "tipo": "Documento PJe",
                "id": "281122579",
                "tamanho": len(body_text),
                "preview": body_text[:500]
            })
        else:
            print(f"  ⚠️ Conteúdo muito curto")
            
    except Exception as e:
        print(f"  ❌ Documento: {e}")
        results["erros"].append(f"Documento: {str(e)[:200]}")
    
    page.close()
    
    # Try JusBrasil
    print("\n[3/3] Tentando JusBrasil...")
    page = ctx.new_page()
    
    try:
        # Search for the process on JusBrasil
        jus_url = f"https://www.jusbrasil.com.br/jurisprudencia/busca?q=%22{PROC}%22"
        resp = page.goto(jus_url, timeout=30000, wait_until="domcontentloaded")
        print(f"  Status: {resp.status if resp else 'no response'}")
        time.sleep(5)
        
        body_text = page.inner_text("body")
        print(f"  Body length: {len(body_text)}")
        
        if PROC in body_text or "Lucas" in body_text:
            with open(os.path.join(RASPED_DIR, "jusbrasil_results.txt"), "w", encoding="utf-8") as f:
                f.write(body_text[:20000])
            print(f"  ✅ JusBrasil results saved")
            results["metodos_tentados"].append({"metodo": "JusBrasil", "status": "ok"})
        else:
            print(f"  ❌ Processo não encontrado no JusBrasil")
            
    except Exception as e:
        print(f"  ❌ JusBrasil: {e}")
        results["erros"].append(f"JusBrasil: {str(e)[:200]}")
    
    page.close()
    browser.close()

with open(os.path.join(RASPED_DIR, "resultado_pje_direto.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print("RESULTADO:")
print(json.dumps(results, ensure_ascii=False, indent=2))
