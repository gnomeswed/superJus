# -*- coding: utf-8 -*-
"""Descobrir URL atual do DJERJ via home TJRJ"""
import time
from playwright.sync_api import sync_playwright
import sys
sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    page.goto("https://www.tjrj.jus.br", timeout=40000, wait_until="domcontentloaded")
    time.sleep(5)
    links = page.query_selector_all("a")
    print(f"Total links: {len(links)}")
    for a in links:
        href = a.get_attribute("href") or ""
        txt = (a.inner_text() or "").strip()
        if any(k in href.lower() for k in ["diario", "djerj", "dj"]) or any(k in txt.lower() for k in ["diário", "djerj", "diario oficial"]):
            print(f" - [{txt[:40]}] => {href}")
    browser.close()
