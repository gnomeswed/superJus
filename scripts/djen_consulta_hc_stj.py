# -*- coding: utf-8 -*-
"""Consulta DJEN (STJ) — HC 1.116.750/RJ — Júlio Pereira Marcos.
USO:
  Opção A (VPS com rota BR / celular 5G):
    python scripts/djen_consulta_hc_stj.py
  Opção B (via r.jina.ai - funciona de qualquer rede, se o DJEN estiver no ar):
    python scripts/djen_consulta_hc_stj.py --via-jina
"""
import sys
import json
import time
import urllib.request
import urllib.parse
import argparse

sys.stdout.reconfigure(encoding="utf-8")

OUT_FILE = r"c:\Projetos\superJus\djen_hc_stj_resultado.txt"


def via_playwright():
    from playwright.sync_api import sync_playwright
    out = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = browser.new_context(viewport={"width": 1366, "height": 900})
        page = ctx.new_page()
        url = "https://comunica.pje.jus.br/consulta?siglaTribunal=STJ&meio=D"
        page.goto(url, timeout=45000, wait_until="domcontentloaded")
        page.wait_for_timeout(6000)
        out.append("URL: " + page.url)
        txt = page.inner_text("body")
        out.append(txt[:3000])
        # Buscar pelo número
        try:
            campo = page.query_selector("input[type='text'], input[type='search']")
            if campo:
                campo.fill("HC 1.116.750")
                campo.press("Enter")
                page.wait_for_timeout(8000)
                out.append("\n=== RESULTADO BUSCA ===\n")
                out.append(page.inner_text("body")[:4000])
        except Exception as e:
            out.append(f"[busca: {e}]")
        browser.close()
    return "\n".join(out)


def via_jina():
    url = "https://r.jina.ai/https://comunica.pje.jus.br/consulta?siglaTribunal=STJ&meio=D"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "X-Return-Format": "markdown"})
    try:
        resp = urllib.request.urlopen(req, timeout=60)
        return resp.read().decode("utf-8", "replace")[:5000]
    except Exception as e:
        return f"[ERRO via jina: {e}]"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--via-jina", action="store_true", help="Usa r.jina.ai como proxy de leitura")
    args = parser.parse_args()

    if args.via_jina:
        resultado = via_jina()
    else:
        resultado = via_playwright()

    print(resultado)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(resultado)
    print(f"\n[Salvo em {OUT_FILE}]")


if __name__ == "__main__":
    main()
