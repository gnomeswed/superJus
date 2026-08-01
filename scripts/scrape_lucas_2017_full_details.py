# -*- coding: utf-8 -*-
import time
import os
from playwright.sync_api import sync_playwright

proc_num = "0000253-78.2017.8.19.0004"
hc_num = "0046418-98.2017.8.19.0000"

target_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas\Caso_Principal\documentos_processo"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    
    print(f"1. Acessando processo {proc_num} no TJRJ...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=35000)
    time.sleep(3)
    
    frame = page.frame_locator("iframe#mainframe")
    frame.locator("input[name='numeroProcesso']").fill(proc_num)
    time.sleep(1)
    frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first.click()
    time.sleep(6)
    
    # Clicar em "Listar todos os personagens" se visivel
    try:
        print("Clicando em 'Listar todos os personagens'...")
        frame.locator("text=Listar todos os personagens").click()
        time.sleep(4)
    except Exception as e:
        print("Aviso personagens:", e)
        
    real_frame = page.query_selector("iframe#mainframe").content_frame()
    personagens_txt = real_frame.inner_text("body")
    
    # Clicar em "Todos os Movimentos" se visivel
    try:
        print("Clicando em 'Todos os Movimentos'...")
        frame.locator("text=Todos Os Movimentos").click()
        time.sleep(4)
    except Exception as e:
        print("Aviso movimentos:", e)
        
    movimentos_txt = real_frame.inner_text("body")
    
    # 2. Consultar o HC 0046418-98.2017.8.19.0000 no TJRJ
    print(f"2. Acessando HC de 2ª Instância {hc_num}...")
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=35000)
    time.sleep(3)
    frame2 = page.frame_locator("iframe#mainframe")
    frame2.locator("input[name='numeroProcesso']").fill(hc_num)
    time.sleep(1)
    frame2.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first.click()
    time.sleep(6)
    
    real_frame2 = page.query_selector("iframe#mainframe").content_frame()
    hc_txt = real_frame2.inner_text("body")
    
    # Consolidação
    full_report = []
    full_report.append(f"# DADOS COMPLETOS DO PROCESSO ANTERIOR DO LUCAS")
    full_report.append(f"**Processo (2ª Vara Criminal de Niterói):** `{proc_num}`")
    full_report.append(f"**Habeas Corpus (TJRJ 2ª Instância):** `{hc_num}`")
    full_report.append(f"**Infração Imputada:** Roubo Majorado (Art. 157, § 2º, II do CP)\n")
    full_report.append("## 1. Personagens e Qualificação Completa\n```text\n" + personagens_txt[:4000] + "\n```\n")
    full_report.append("## 2. Histórico de Movimentos e Soltura por Alvará\n```text\n" + movimentos_txt[:4000] + "\n```\n")
    full_report.append("## 3. Acórdão do Habeas Corpus nº 0046418-98.2017.8.19.0000\n```text\n" + hc_txt[:4000] + "\n```\n")
    
    out_file = os.path.join(target_dir, "detalhes_processo_2017_lucas.md")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(full_report))
        
    print(f"Relatório detalhado salvo em {out_file}")
    browser.close()
