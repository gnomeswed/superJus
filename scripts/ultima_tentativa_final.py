# -*- coding: utf-8 -*-
"""Última tentativa: Chrome profile + URLs PJe 2.x + DataJud + Bing."""
import sys, os, time, json, re, urllib.request, ssl
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
PROC = "0821248-17.2025.8.19.0031"
PROC_LIMPO = PROC.replace("-", "").replace(".", "")
RAW_DIR = Path(r"C:\Projetos\superJus\Clientes\Renan\03_Documentos_do_Processo\_raspagem_10_08_2026")
RAW_DIR.mkdir(parents=True, exist_ok=True)

resultados = {"processo": PROC, "tentativas": []}


def safe_urlopen(url, headers=None, data=None, timeout=15):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, data=data, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            return resp.status, resp.url, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.url, e.read()
    except Exception as e:
        return None, None, str(e).encode()


def main() -> None:
    # ============================================================
    # 1. URLs PJe 2.x
    # ============================================================
    print("\n=== 1. URLs PJe 2.x ===")
    pje_urls = [
        "https://pje2.tjrj.jus.br/pje/login.seam",
        "https://pje2.tjrj.jus.br/pje/",
        "https://consultapje.tjrj.jus.br/",
        "https://www.pje.tjrj.jus.br/",
        "https://tj-rj.pje.jus.br/",
        "https://pje.trf2.jus.br/",
    ]
    for url in pje_urls:
        status, final, _ = safe_urlopen(url, timeout=10)
        print(f"  {status or 'ERR'}  {url[:70]:70} -> {final[:60] if final else '-'}")
        resultados["tentativas"].append({"metodo": f"URL {url}", "status": status, "final": final})

    # ============================================================
    # 2. DataJud com API keys
    # ============================================================
    print("\n=== 2. DataJud API keys ===")
    api_keys = [
        "cDZHYzlSd0drRzR0eHBpVzU4czd1VnViU3BhVlpMOTY=",
        "APIKey cDZHYzlSd0drRzR0eHBpVzU4czd1VnViU3BhVlpMOTY=",
        "Bearer cDZHYzlSd0drRzR0eHBpVzU4czd1VnViU3BhVlpMOTY=",
        "Basic cDZHYzlSd0drRzR0eHBpVzU4czd1VnViU3BhVlpMOTY=",
    ]
    url_datajud = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
    payload = json.dumps({"query": {"match": {"numeroProcesso": PROC_LIMPO}}, "size": 10}).encode()
    for key in api_keys:
        status, _, body = safe_urlopen(url_datajud, headers={
            "Content-Type": "application/json",
            "Authorization": key,
        }, data=payload, timeout=15)
        body_txt = body.decode("utf-8", errors="replace")[:300] if body else ""
        if status == 200:
            try:
                data = json.loads(body)
                hits = data.get("hits", {}).get("hits", [])
                print(f"  ✓ HTTP 200  key {key[:20]}... -> {len(hits)} hits")
                resultados["tentativas"].append({"metodo": f"DataJud {key[:20]}", "status": 200, "hits": len(hits)})
                if hits:
                    json_path = RAW_DIR / f"datajud_renan_success_{int(time.time())}.json"
                    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
                    src = hits[0]["_source"]
                    print(f"  Salvo: {json_path.name}")
                    print(f"  Classe: {src.get('classe', {}).get('nome')}")
                    print(f"  Órgão: {src.get('orgaoJulgador', {}).get('nome')}")
                    print(f"  Movimentos: {len(src.get('movimentos', []))}")
                    for m in src.get("movimentos", []):
                        nome = (m.get("nome") or "").lower()
                        if "senten" in nome:
                            print(f"\n  >>> SENTENÇA ENCONTRADA:")
                            print(f"      Data: {m.get('dataHora')}")
                            print(f"      Nome: {m.get('nome')}")
                            comps = m.get("complementosTabelados", [])
                            for c in comps:
                                print(f"      {c.get('nome')}: {c.get('descricao')}")
                            resultados["sentenca"] = {
                                "data": m.get("dataHora"),
                                "nome": m.get("nome"),
                                "complementos": comps,
                            }
                    break
            except Exception as e:
                print(f"  ERRO parse: {e}")
        else:
            print(f"  HTTP {status}  key {key[:20]}...")
            resultados["tentativas"].append({"metodo": f"DataJud {key[:20]}", "status": status, "body": body_txt[:200]})

    # ============================================================
    # 3. Bing indexado
    # ============================================================
    print("\n=== 3. Bing indexado ===")
    bing_url = f"https://www.bing.com/search?q=%22{PROC}%22+senten%C3%A7a+maric%C3%A1"
    status, final, body = safe_urlopen(bing_url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    })
    if status == 200 and body:
        html = body.decode("utf-8", errors="replace")
        # Extrair links com texto relevante
        links = re.findall(r'<a[^>]+href="(https?://[^"]+)"[^>]*>([^<]+)</a>', html)
        relevantes = [(u, t) for u, t in links
                      if PROC.replace("-", "") in t or "renan" in t.lower() or "maricá" in t.lower()
                      or "0821248" in u][:15]
        print(f"  {len(links)} links totais, {len(relevantes)} relevantes")
        for u, t in relevantes[:5]:
            print(f"    - {t[:80]}")
            print(f"      {u[:100]}")
        resultados["tentativas"].append({
            "metodo": "Bing search",
            "total_links": len(links),
            "relevantes": len(relevantes),
            "samples": [(t[:80], u[:100]) for u, t in relevantes[:5]],
        })
    else:
        print(f"  ERRO Bing: HTTP {status}")

    # ============================================================
    # 4. DuckDuckGo (menos restritivo)
    # ============================================================
    print("\n=== 4. DuckDuckGo ===")
    ddg_url = f"https://html.duckduckgo.com/html/?q=%22{PROC}%22+senten%C3%A7a"
    status, _, body = safe_urlopen(ddg_url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    })
    if status == 200 and body:
        html = body.decode("utf-8", errors="replace")
        results_ddg = re.findall(r'<a[^>]+href="([^"]+)"[^>]*class="result__a"[^>]*>([^<]+)</a>', html)
        print(f"  {len(results_ddg)} resultados DuckDuckGo")
        for u, t in results_ddg[:5]:
            t_clean = re.sub(r'<[^>]+>', '', t)
            print(f"    - {t_clean[:80]}")
            print(f"      {u[:100]}")
        resultados["tentativas"].append({
            "metodo": "DuckDuckGo",
            "total": len(results_ddg),
            "samples": [(re.sub(r'<[^>]+>', '', t)[:80], u[:100]) for u, t in results_ddg[:5]],
        })

    # ============================================================
    # Salvar
    # ============================================================
    results_file = RAW_DIR / f"tentativas_finais_{int(time.time())}.json"
    results_file.write_text(json.dumps(resultados, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(f"\n[OK] Salvo: {results_file.name}")
    if resultados.get("sentenca"):
        print(f"\n=== SENTENÇA ENCONTRADA ===")
        print(json.dumps(resultados["sentenca"], ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
