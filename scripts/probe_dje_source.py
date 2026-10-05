# -*- coding: utf-8 -*-
"""Baixa HTML fonte do consultadje e extrai names server-side dos controles"""
import time, sys, re
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1366, "height": 900},
                              user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
    page = ctx.new_page()
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    page.goto("https://www3.tjrj.jus.br/consultadje/", wait_until="domcontentloaded", timeout=45000)
    time.sleep(6)
    html = page.content()
    with open(r"c:\Projetos\superJus\dje_novo_source.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML salvo: {len(html)} bytes")

    # procurar names com ctl00 (server-side) e o botão pesquisar
    names = re.findall(r'name="([^"]*(?:ctl00|proc|num|drop|dt)[^"]*)"', html, re.I)
    names = sorted(set(names))
    print("=== NAMES RELEVANTES ===")
    for n in names[:60]:
        print(" ", n)

    # procurar handlers onclick do botão
    onclick = re.findall(r'onclick="([^"]*procBtn[^"]*)"', html)
    print("=== ONCLICK procBtn ===")
    for o in onclick:
        print(" ", o[:300])

    # __doPostBack references
    dpb = re.findall(r'__doPostBack\([^)]{0,120}\)', html)
    print("=== doPostBack refs ===")
    for d in dpb[:15]:
        print(" ", d[:200])
    browser.close()
