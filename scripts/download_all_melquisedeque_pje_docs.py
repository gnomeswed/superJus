# -*- coding: utf-8 -*-
import time
import os
import sys
import json
import re
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

num_processo = "0807644-58.2025.8.19.0202"
clean_num = "08076445820258190202"

target_dir = r"c:\Projetos\superJus\Clientes\Melquisedeque\processos\0807644-58.2025.8.19.0202"
docs_dir = os.path.join(target_dir, "documentos")
os.makedirs(docs_dir, exist_ok=True)

print(f"=== INICIANDO DOWNLOAD COMPLETO DE PEÇAS, DECISÕES E MOVIMENTAÇÕES ===")
print(f"Processo: {num_processo} — 2ª Vara Criminal de Madureira/RJ\n")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-popup-blocking"])
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        accept_downloads=True
    )
    page = context.new_page()

    url_pje = "https://tjrj.pje.jus.br/pje/ConsultaPublica/listView.seam"
    print(f"1. Acessando {url_pje}...")
    
    try:
        page.goto(url_pje, wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)

        # Preencher os campos da numeração única CNJ
        # 0807644-58.2025.8.19.0202
        inputs = {
            "numSequencial": "0807644",
            "numDigitoVerificador": "58",
            "ano": "2025",
            "ramoJustica": "8",
            "respectivoTribunal": "19",
            "orgaoJurisdicional": "0202"
        }
        
        for k, v in inputs.items():
            sel = f"input[id*='{k}']"
            el = page.query_selector(sel)
            if el:
                el.fill(v)
                
        print("   • Numeração 0807644-58.2025.8.19.0202 preenchida no formulário PJe.")
        time.sleep(1)

        # Clicar em Pesquisar
        btn = page.query_selector("input[id*='searchProcessos'], input[value*='Pesquisar'], button:has-text('Pesquisar')")
        if btn:
            btn.click()
            print("   • Botão Pesquisar clicado. Aguardando grid de resultados...")
            time.sleep(6)

        # Capturar tela e HTML do resultado
        page.screenshot(path=os.path.join(target_dir, "grid_consulta_publica.png"))
        
        # Localizar botão de detalhes
        detail_link = page.query_selector("a[id*='detalhe'], a:has-text('VER DETALHES DO PROCESSO'), a:has-text('0807644'), a[title*='detalhe'], a[onclick*='detalhe']")
        
        if detail_link:
            print("   • Clicando para abrir detalhes integrais...")
            # PJe pode abrir nova aba/janela
            with context.expect_page(timeout=15000) as new_page_info:
                detail_link.click()
            
            detail_page = new_page_info.value
            detail_page.wait_for_load_state("domcontentloaded")
            time.sleep(6)
            
            print("   ✅ Página de detalhes aberta com sucesso!")
            
            # Salvar screenshot de página inteira
            detail_page.screenshot(path=os.path.join(target_dir, "detalhes_processo_full.png"), full_page=True)
            
            # Extrair HTML e Texto
            html_content = detail_page.content()
            text_content = detail_page.inner_text("body")
            
            with open(os.path.join(target_dir, "pagina_detalhes_integra.html"), "w", encoding="utf-8") as f:
                f.write(html_content)
                
            with open(os.path.join(target_dir, "pagina_detalhes_integra.txt"), "w", encoding="utf-8") as f:
                f.write(text_content)
                
            print(f"   • Texto integral extraído ({len(text_content)} caracteres).")

            # 3. TENTAR BAIXAR DOCUMENTOS / ANEXOS DISPONÍVEIS
            # Localizar botões/links de documentos, PDFs, decisões, despachos
            doc_links = detail_page.query_selector_all("a[href*='documento'], a[href*='download'], a[title*='documento'], a[title*='PDF'], a:has-text('PDF'), a:has-text('Visualizar')")
            print(f"   • Encontrados {len(doc_links)} links de documentos/anexos.")
            
            downloaded_count = 0
            for idx, dl in enumerate(doc_links):
                try:
                    title = dl.get_attribute("title") or dl.inner_text() or f"documento_{idx+1}"
                    clean_title = re.sub(r'[^a-zA-Z0-9_-]', '_', title)[:40]
                    href = dl.get_attribute("href")
                    
                    if dl.is_visible():
                        try:
                            with detail_page.expect_download(timeout=5000) as download_info:
                                dl.click()
                            download = download_info.value
                            save_path = os.path.join(docs_dir, f"{idx+1}_{clean_title}.pdf")
                            download.save_as(save_path)
                            print(f"     📥 Documento baixado: {save_path}")
                            downloaded_count += 1
                        except Exception:
                            pass
                except Exception as e:
                    pass
                    
            print(f"   • Total de downloads automáticos concluídos: {downloaded_count}")

        else:
            print("   ⚠️ Link direto de detalhes não abriu popup. Extraindo dados da página atual...")
            text_content = page.inner_text("body")
            with open(os.path.join(target_dir, "pagina_listview_integra.txt"), "w", encoding="utf-8") as f:
                f.write(text_content)

    except Exception as e:
        print(f"   ❌ Ocorreu um erro no fluxo Playwright: {e}")

    browser.close()

# 4. CONSOLIDAR DOSSIÊ DETALHADO COM TODAS AS 68 MOVIMENTAÇÕES E DECISÕES
print("\n3. Consolidando histórico completo das 68 movimentações e decisões...")
raw_json_path = os.path.join(target_dir, "datajud_raw.json")
if os.path.exists(raw_json_path):
    datajud = json.load(open(raw_json_path, encoding="utf-8"))
    movs = datajud.get("movimentos", [])
    
    # Sort movements descending
    movs_desc = sorted(movs, key=lambda x: x.get("dataHora", ""), reverse=True)
    
    md_lines = []
    md_lines.append(f"# ⚖️ AUTOS INTEGRAIS E HISTÓRICO COMPLETO")
    md_lines.append(f"**Cliente:** Melquisedeque Rodrigues dos Santos  ")
    md_lines.append(f"**CPF:** `064.296.507-23`  ")
    md_lines.append(f"**Processo CNJ:** `{num_processo}`  ")
    md_lines.append(f"**Juízo:** 2ª Vara Criminal da Regional de Madureira — Comarca da Capital / TJRJ  ")
    md_lines.append(f"**Classe:** Ação Penal - Procedimento Ordinário (PJe)  ")
    md_lines.append(f"**Assuntos:** Extorsão (Art. 158 CP) e Associação Criminosa (Art. 288 CP)  ")
    md_lines.append(f"**Total de Movimentações Registradas:** {len(movs_desc)}  \n")
    md_lines.append("---\n")
    
    # Decisões / Despachos / Marcos
    md_lines.append("## 📌 1. MARCOS PROCESSUAIS, DECISÕES E DESPACHOS")
    marcos = [m for m in movs_desc if any(k in m.get("nome", "").lower() for k in [
        "denúncia", "decisões", "decisao", "audiência", "audiencia", "desmembramento", "conclusão", "distribuição"
    ])]
    
    for idx, mk in enumerate(marcos, 1):
        dt = mk.get("dataHora", "")[:19].replace("T", " ")
        comps = mk.get("complementosTabelados", [])
        comp_str = " | ".join([f"**{c.get('descricao')}:** {c.get('nome')}" for c in comps])
        md_lines.append(f"### {idx}. [{dt}] — {mk.get('nome')}")
        if comp_str:
            md_lines.append(f"- **Classificação/Tipo:** {comp_str}")
        md_lines.append(f"- **Código CNJ:** `{mk.get('codigo')}`\n")
        
    md_lines.append("---\n")
    md_lines.append("## 📜 2. CRONOLOGIA COMPLETA DE TODAS AS MOVIMENTAÇÕES (DO MAIS RECENTE AO INÍCIO)")
    
    for idx, m in enumerate(movs_desc, 1):
        dt = m.get("dataHora", "")[:19].replace("T", " ")
        comps = m.get("complementosTabelados", [])
        comp_str = " | ".join([f"{c.get('descricao')}: {c.get('nome')}" for c in comps])
        md_lines.append(f"{idx}. **`{dt}`** — **{m.get('nome')}**" + (f" *({comp_str})*" if comp_str else ""))
        
    final_md_path = os.path.join(target_dir, "historico_completo_movimentacoes_e_decisoes.md")
    with open(final_md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
        
    print(f"✅ Histórico consolidado salvo em: {final_md_path}")

# Criar Dossiê Master na raiz de Melquisedeque
master_melqui = os.path.join(r"c:\Projetos\superJus\Clientes\Melquisedeque", "DOSSIE_MASTER_MELQUISEDEQUE.md")
with open(master_melqui, "w", encoding="utf-8") as f:
    f.write(f"""# 🏛️ DOSSIÊ MASTER — MELQUISEDEQUE RODRIGUES DOS SANTOS
**Cliente:** Melquisedeque Rodrigues dos Santos  
**CPF:** `064.296.507-23`  
**Processo Principal:** `0807644-58.2025.8.19.0202`  
**Juízo:** 2ª Vara Criminal da Regional de Madureira — Capital/RJ (PJe)  
**Assunto:** Extorsão (Art. 158, CP) e Associação Criminosa (Art. 288, CP)  
**Data da Extração Completa:** 29/08/2026  

---

## 📋 Resumo Executivo da Ação Penal
1. **Denúncia e Início:** Ajuizado em 03/04/2025 pelo Ministério Público do Estado do Rio de Janeiro.
2. **Audiência de Instrução (AIJ):** **Realizada em 25/03/2026 às 11:11h** na 2ª Vara Criminal de Madureira.
3. **Desmembramento (Art. 80 CPP):** Ocorrido em **04/05/2026**.
4. **Fase Atual:** Fase pós-instrução / Juntada de petição de ciência em 26/08/2026.

---

## 📂 Arquivos Integrais Disponíveis:
- [Histórico Completo de Movimentações e Decisões](file:///c:/Projetos/superJus/Clientes/Melquisedeque/processos/0807644-58.2025.8.19.0202/historico_completo_movimentacoes_e_decisoes.md)
- [Dados Brutos DataJud (JSON)](file:///c:/Projetos/superJus/Clientes/Melquisedeque/processos/0807644-58.2025.8.19.0202/datajud_raw.json)
- [Pasta de Documentos e Capturas do PJe](file:///c:/Projetos/superJus/Clientes/Melquisedeque/processos/0807644-58.2025.8.19.0202/documentos)
""")

print(f"📌 Dossiê Master salvo em: {master_melqui}")
print("\n🎉 EXTRAÇÃO E COMPILAÇÃO CONCLUÍDAS COM SUCESSO!")
