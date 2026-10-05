# -*- coding: utf-8 -*-
"""Testar API de movimentos diretamente via urllib + Playwright pra capturar headers."""
import sys, time, json, urllib.request, urllib.error
from playwright.sync_api import sync_playwright


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    PROC = "0011857-95.2024.8.19.0002"

    # 1. Capturar sessão/cookies via Playwright, depois fazer requests diretas
    cookies = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = browser.new_context(viewport={"width": 1366, "height": 900})
        page = ctx.new_page()

        # Tentar pegar cookies após carregar a página
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000)
        page.wait_for_selector("iframe#mainframe", timeout=30000)
        time.sleep(3)
        cookies_list = ctx.cookies()
        cookies = {c["name"]: c["value"] for c in cookies_list}
        print(f"Cookies: {list(cookies.keys())}")
        browser.close()

    # 2. Tentar a URL direta (sem auth)
    urls = [
        f"https://www3.tjrj.jus.br/consultaprocessual/api/processos/por-numero/movimentos?numeroProcesso={PROC.replace('-','').replace('.','')}",
        f"https://www3.tjrj.jus.br/consultaprocessual/api/processos/por-numero/movimentos?numeroProcesso={PROC}",
        f"https://www3.tjrj.jus.br/consultaprocessual/api/processos/por-numero/publica?numeroProcesso={PROC}",
    ]
    for url in urls:
        print(f"\n>>> GET {url}")
        req = urllib.request.Request(url)
        if cookies:
            cookie_str = "; ".join(f"{k}={v}" for k, v in cookies.items())
            req.add_header("Cookie", cookie_str)
        req.add_header("Accept", "application/json")
        req.add_header("User-Agent", "Mozilla/5.0")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
                print(f"   status {resp.status}  content-length {resp.headers.get('content-length','?')}")
                print(f"   content-type {resp.headers.get('content-type','?')}")
                try:
                    j = json.loads(data)
                    if isinstance(j, dict):
                        print(f"   top keys: {list(j.keys())[:10]}")
                        if "movimentos" in j:
                            print(f"   movimentos: {len(j['movimentos'])}")
                        # Paginação?
                        for k in ["page", "size", "total", "totalPages", "hasNext", "paginacao"]:
                            if k in j:
                                print(f"   {k}: {j[k]}")
                    else:
                        print(f"   tipo: {type(j).__name__}, len={len(j)}")
                except json.JSONDecodeError:
                    print(f"   primeiros 300: {data[:300]!r}")
        except urllib.error.HTTPError as e:
            print(f"   HTTPError {e.code}: {e.reason}")
            print(f"   body: {e.read()[:500]!r}")
        except Exception as e:
            print(f"   {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
