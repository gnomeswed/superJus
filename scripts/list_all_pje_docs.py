# -*- coding: utf-8 -*-
import sys, time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
proc_fmt = "0821248-17.2025.8.19.0031"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    ctx = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    page = ctx.new_page()

    page.goto("https://tjrj.pje.jus.br/1g/ConsultaPublica/listView.seam", timeout=40000)
    time.sleep(2)

    page.fill("input[id*='inputNumeroProcesso']", proc_fmt)
    page.click("input[id*='searchProcessos'], button[id*='searchProcessos']")
    time.sleep(4)

    with ctx.expect_page(timeout=15000) as new_page_info:
        page.locator(f"a:has-text('{proc_fmt}')").first.click()
        time.sleep(2)

    dp = new_page_info.value
    dp.wait_for_load_state("domcontentloaded")
    time.sleep(3)

    # Pegar todos os links da página de detalhes
    links = dp.evaluate("""() => {
        return Array.from(document.querySelectorAll('a')).map(a => ({
            text: (a.textContent||'').trim(),
            href: a.href||'',
            title: a.title||'',
            id: a.id||''
        })).filter(x => x.text.length > 0)
    }""")

    print(f"Total de links no detalhe: {len(links)}")
    for L in links:
        t = L['text']
        if any(k in t.upper() for k in ["ATA", "CUSTÓDIA", "FAC", "FOLHA", "ANTECEDENTE", "DENÚNCIA", "RECOLHIMENTO", "MANDADO"]):
            print(f"  📌 {t} | href: {L['href'][:80]} | id: {L['id']}")

    # Tentar abrir link com Ata
    ata_link = dp.locator("a:has-text('Ata'), a:has-text('Custódia'), a:has-text('Audiência')").first
    if ata_link.is_visible():
        print(f"\nAbrindo link: {ata_link.inner_text()}...")
        try:
            with ctx.expect_page(timeout=8000) as doc_page_info:
                ata_link.click()
            p_doc = doc_page_info.value
            p_doc.wait_for_load_state("domcontentloaded")
            time.sleep(3)
            txt_ata = p_doc.inner_text("body")
            print("Texto da Ata (primeiros 2000 chars):")
            print(txt_ata[:2000])
            with open(r"c:\Projetos\superJus\Clientes\Renan\03_Documentos_do_Processo\ata_custodia.txt", "w", encoding="utf-8") as f:
                f.write(txt_ata)
        except Exception as e:
            print("Erro ao abrir ata:", e)

    browser.close()
