# -*- coding: utf-8 -*-
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

target_dir = r"c:\Projetos\superJus\Clientes\Renato_Bastos_Rocha"
os.makedirs(target_dir, exist_ok=True)

f_origem = os.path.join(target_dir, "acao_penal_08016300420258190026_G1.json")
f_hc = os.path.join(target_dir, "hc_00237193520258190000_raw.json")
f_stj = os.path.join(target_dir, "stj_00237574720258190000_raw.json")

src_origem = json.load(open(f_origem, encoding="utf-8")) if os.path.exists(f_origem) else {}
src_hc = json.load(open(f_hc, encoding="utf-8")) if os.path.exists(f_hc) else {}
src_stj = json.load(open(f_stj, encoding="utf-8")) if os.path.exists(f_stj) else {}

dossie = [
    "# 🏛️ DOSSIÊ PROCESSUAL COMPLETO: RENATO BASTOS ROCHA",
    "**Cliente:** Renato Bastos Rocha  ",
    "**CPF:** `124.981.977-61` (12498197761)  ",
    "**Comarca de Origem:** Itaperuna / RJ (2ª Vara)  ",
    "**Data da Extração:** 01/09/2026  \n",
    "---\n",
    "## 📌 1. RESUMO EXECUTIVO DO CASO\n",
    "Renato Bastos Rocha responde à **Ação Penal nº 0801630-04.2025.8.19.0026** perante a **2ª Vara da Comarca de Itaperuna/RJ**, sob imputação do crime de **Furto (Art. 155 do Código Penal)**, instaurada em **23/03/2025**.",
    "Durante a fase instrutória, a Defensoria Pública impetrou o **Habeas Corpus nº 0023719-35.2025.8.19.0000** na 7ª Câmara Criminal do TJRJ (Rel. Des. Marcus Henrique Pinto Basilio), com julgamento em 10/04/2025.",
    "Em **24/11/2025**, o Juízo da 2ª Vara de Itaperuna proferiu **SENTENÇA CONDENATÓRIA DE PROCEDÊNCIA (Código CNJ 219)**. O feito segue com movimentações e expedição de guias e recursos em 2026.\n",
    "---\n",
    "## ⚖️ 2. AÇÃO PENAL PRINCIPAL DE 1ª INSTÂNCIA (ITAPERUNA)",
    "- **Processo:** `0801630-04.2025.8.19.0026`",
    "- **Órgão Julgador:** 2ª Vara da Comarca de Itaperuna / TJRJ",
    "- **Classe:** Ação Penal - Procedimento Ordinário",
    "- **Assunto Principal:** Furto (Art. 155 do CP)",
    "- **Data de Ajuizamento:** 23/03/2025",
    "- **Total de Movimentações:** 102 movimentações",
    "- **Sentença:** Proferida em **24/11/2025 às 19:31h** (Procedência / Condenação)\n",
    "### 📜 Principais Marcos Processuais da 1ª Instância:"
]

movs_origem = src_origem.get("movimentos", [])
movs_sorted = sorted(movs_origem, key=lambda m: m.get("dataHora", ""), reverse=True)

for m in movs_sorted:
    nm = m.get("nome", "")
    if any(k in nm.lower() for k in ["sentença", "procedência", "audiência", "decisão", "despacho", "conclusão", "recebimento", "denúncia", "prisão", "liberdade", "alvará", "definitivo"]):
        dt = m.get("dataHora", "")[:19].replace("T", " ")
        comps = m.get("complementosTabelados", [])
        comp_str = " | ".join([f"{c.get('descricao')}: {c.get('nome')}" for c in comps])
        dossie.append(f"- **`{dt}`** — **{nm}** (Cód. `{m.get('codigo')}`)" + (f" *({comp_str})*" if comp_str else ""))

dossie.append("\n---\n")
dossie.append("## 🏛️ 3. HABEAS CORPUS NA 2ª INSTÂNCIA (TJRJ)")
dossie.append("- **Processo:** `0023719-35.2025.8.19.0000`")
dossie.append("- **Órgão Julgador:** 7ª Câmara Criminal do TJRJ")
dossie.append("- **Relator:** Desembargador Marcus Henrique Pinto Basilio")
dossie.append("- **Paciente:** Renato Bastos Rocha")
dossie.append("- **Impetrante:** Defensoria Pública Geral do Estado do Rio de Janeiro")
dossie.append("- **Data de Ajuizamento:** 26/03/2025")
dossie.append("- **Julgamento do Acórdão:** 10/04/2025")
dossie.append("- **Publicação do Acórdão:** 14/04/2025")
dossie.append("- **Baixa Definitiva:** 23/05/2025\n")

dossie.append("---\n")
dossie.append("## 🎯 4. DIAGNÓSTICO DEFENSIVO E OPORTUNIDADES")
dossie.append("""
1. **Verificação de Apelação Criminal ou Trânsito em Julgado:**
   - Com a sentença condenatória prolatada em 24/11/2025, deve-se verificar se houve interposição de Recurso de Apelação pela Defensoria Pública ou Defesa Constituída, ou se houve a expedição da Carta de Execução de Sentença (Guia de Execução) para a VEP.
2. **Revisão da Dosimetria da Pena (Furto - Art. 155 CP):**
   - Analisar os critérios de cálculo da pena fixados na sentença de 24/11/2025 (Pena-base, atenuantes de confissão espontânea e menoridade relativa, regime inicial de cumprimento e substituição por penas restritivas de direitos - Art. 44 do CP).
3. **Execução Penal / VEP:**
   - Caso a pena já esteja em fase executória, verificar detração penal do período em que permaneceu preso provisoriamente, cabimento de regime aberto/semiaberto e indulto/comutação.
""")

out_dossie_path = os.path.join(target_dir, "DOSSIE_MASTER_RENATO_BASTOS_ROCHA.md")
with open(out_dossie_path, "w", encoding="utf-8") as f:
    f.write("\n".join(dossie))

print(f"✅ Dossiê Master consolidado em: {out_dossie_path}")
