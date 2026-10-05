# -*- coding: utf-8 -*-
import sys, os
import unicodedata
from fpdf import FPDF

# Garantir UTF-8 no stdout
sys.stdout.reconfigure(encoding="utf-8")

def clean_latin(t):
    """Substitui caracteres tipográficos especiais por equivalentes seguros no FPDF."""
    if not t:
        return ""
    replacements = {
        '—': '-', '–': '-', '“': '"', '”': '"', '‘': "'", '’': "'",
        '•': '>', 'º': 'o.', 'ª': 'a.', '§': 'Art. ', '…': '...',
        '🚨': '[!]', '⚖️': '', '🏛️': '', '📌': '', '✅': '[OK]', '⚠️': '[ATENCAO]',
        '🎯': '', '🛡️': '', '💡': '', '👥': '', '📜': '', '🔮': '', '💾': ''
    }
    for k, v in replacements.items():
        t = t.replace(k, v)
    # Converter para latin-1 seguro substituindo caracteres que não existem no latin-1
    return t.encode('latin-1', 'replace').decode('latin-1')

class RelatorioJuridicoPDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_margins(15, 18, 15)
        self.set_auto_page_break(auto=True, margin=18)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(26, 54, 93)
        self.cell(0, 5, "SUPERJUS | DOSSIE EXECUTIVO DE DEFESA CRIMINAL - JULIO PEREIRA MARCOS", align="L")
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 5, "CONFIDENCIAL / USO DA ADVOCACIA", align="R")
        self.ln(6)
        self.set_draw_color(43, 108, 176)
        self.set_line_width(0.4)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-14)
        self.set_draw_color(203, 213, 224)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(2)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, clean_latin("SuperJus Inteligência Jurídica | Caso Júlio Pereira Marcos (Ação Penal 0023013-51.2021.8.19.0078)"), align="L")
        self.cell(0, 5, f"Pagina {self.page_no()}/{{nb}}", align="R")

    def section_h1(self, title):
        self.ln(3)
        self.set_font("Helvetica", "B", 12)
        self.set_fill_color(26, 54, 93)
        self.set_text_color(255, 255, 255)
        self.cell(0, 7.5, "  " + clean_latin(title), fill=True, ln=True)
        self.ln(2.5)

    def section_h2(self, title):
        self.ln(2)
        self.set_font("Helvetica", "B", 10.5)
        self.set_text_color(43, 108, 176)
        self.cell(0, 6, clean_latin(title), ln=True)
        self.set_draw_color(43, 108, 176)
        self.set_line_width(0.2)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(2)

    def paragraph(self, text):
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(45, 55, 72)
        self.multi_cell(0, 5, clean_latin(text))
        self.ln(1.5)

    def bullet_point(self, label, text):
        self.set_font("Helvetica", "B", 9.5)
        self.set_text_color(26, 54, 93)
        self.cell(5, 5, ">", ln=False)
        self.cell(self.get_string_width(clean_latin(label)) + 2, 5, clean_latin(label), ln=False)
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(45, 55, 72)
        self.multi_cell(0, 5, clean_latin(f" {text}"))
        self.ln(1)

    def highlight_box(self, title, text, bg=(240, 245, 255), border=(43, 108, 176), text_color=(26, 54, 93)):
        self.set_fill_color(*bg)
        self.set_draw_color(*border)
        self.set_line_width(0.4)
        x = self.get_x()
        y = self.get_y()
        self.rect(self.l_margin, y, self.w - self.l_margin - self.r_margin, 0, 'F')
        
        self.set_font("Helvetica", "B", 9.5)
        self.set_text_color(*text_color)
        self.cell(0, 5.5, clean_latin(title), ln=True)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(45, 55, 72)
        self.multi_cell(0, 4.8, clean_latin(text))
        self.ln(3)

    def alert_box(self, title, text):
        self.highlight_box(title, text, bg=(255, 245, 245), border=(229, 62, 62), text_color=(197, 48, 48))

    def make_table(self, headers, rows, col_widths, align_list=None):
        self.set_font("Helvetica", "B", 8.5)
        self.set_fill_color(26, 54, 93)
        self.set_text_color(255, 255, 255)
        self.set_draw_color(203, 213, 224)
        self.set_line_width(0.2)
        
        # Header
        for i, h in enumerate(headers):
            al = align_list[i] if align_list else "C"
            self.cell(col_widths[i], 6.5, clean_latin(h), border=1, fill=True, align=al)
        self.ln()

        # Rows
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(45, 55, 72)
        for r_idx, row in enumerate(rows):
            fill = (r_idx % 2 == 1)
            if fill:
                self.set_fill_color(247, 250, 252)
            else:
                self.set_fill_color(255, 255, 255)
            for i, val in enumerate(row):
                al = align_list[i] if align_list else "L"
                self.cell(col_widths[i], 5.8, clean_latin(str(val)), border=1, fill=True, align=al)
            self.ln()
        self.ln(2.5)

def build_pdf():
    pdf = RelatorioJuridicoPDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    # ══════════════════════════════════════════════════════════════════════
    # CAPA / CABEÇALHO EXECUTIVO
    # ══════════════════════════════════════════════════════════════════════
    pdf.set_fill_color(26, 54, 93)
    pdf.rect(pdf.l_margin, 18, pdf.w - pdf.l_margin - pdf.r_margin, 32, 'F')
    
    pdf.set_xy(pdf.l_margin + 5, 22)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 8, clean_latin("RELATÓRIO EXECUTIVO & PARECER DE DEFESA TÉCNICA"), ln=True)
    pdf.set_font("Helvetica", "", 10.5)
    pdf.set_text_color(203, 213, 224)
    pdf.cell(0, 6, clean_latin("Dossiê Estratégico para Análise da Advocacia e Atuação Perante o STJ / 1ª Instância"), ln=True)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(160, 174, 192)
    pdf.cell(0, 5, clean_latin("Data de Fechamento: Agosto de 2026 | Documento Auditado e 100% Validado"), ln=True)

    pdf.set_y(54)
    
    # BOX IDENTIFICAÇÃO DO CASO
    pdf.make_table(
        ["Parâmetro Processual", "Identificação / Dados Oficiais"],
        [
            ["Cliente / Paciente", "JÚLIO PEREIRA MARCOS (vulgo 'Julião') - Preso preventivamente em 12/05/2026"],
            ["Ação Penal Desmembrada", "Proc. 0023013-51.2021.8.19.0078 (2ª Vara Criminal de Armação dos Búzios - TJRJ)"],
            ["Ação Penal Originária", "Proc. 0022975-39.2021.8.19.0078 (Todos os 5 corréus respondem em liberdade)"],
            ["Habeas Corpus TJRJ", "HC 0029845-67.2026.8.19.0000 (7ª Câmara Criminal - Rel. Des. Sidney Rosa)"],
            ["RHC no Superior Tribunal de Justiça", "HC 1.116.750 / RJ (Registro 2026/0311210-7) - 6ª Turma - Rel. Min. Og Fernandes"],
            ["Imputação Acusatória", "Arts. 33 e 35 da Lei 11.343/2006 (Tráfico e Associação para o Tráfico)"],
            ["Situação Cautelar Atual", "Conclusos para Decisão ao Min. Og Fernandes (Gabinete STJ) desde 13/08/2026"]
        ],
        [60, 120],
        ["L", "L"]
    )

    # ══════════════════════════════════════════════════════════════════════
    # SEÇÃO 1: RESUMO DOS FATOS E ORIGEM DA INVESTIGAÇÃO
    # ══════════════════════════════════════════════════════════════════════
    pdf.section_h1("1. SÍNTESE FÁTICA E ORIGEM DA OPERAÇÃO 'DELIVERY'")
    pdf.paragraph(
        "A investigação policial teve início em março de 2021 na comarca de Armação dos Búzios/RJ, quando a Polícia Militar "
        "abordou o corréu José Guilherme na posse de aproximadamente 218g de maconha. Na delegacia, José Guilherme declarou que "
        "a substância seria para consumo próprio e indicou um número telefônico de onde partira o contato."
    )
    pdf.paragraph(
        "A partir de pesquisas cadastrais em bancos de dados de operadoras telefônicas (banco Credlink), apurou-se que a linha telefônica "
        "estava registrada em nome de Júlio Pereira Marcos (com endereço em São Paulo). O juízo de Búzios deferiu quatro rodadas de "
        "interceptação telefônica contra diversos terminais, deflagrando a chamada 'Operação Delivery'."
    )
    
    pdf.section_h2("1.1 O que Restou Efetivamente Comprovado na Audiência de Instrução (Feito Originário)")
    pdf.bullet_point("Ausência Absoluta de Apreensão com Júlio:", "Nenhuma grama de entorpecente, balança, dinheiro ou arma foi apreendida em poder de Júlio ou em sua residência. A afirmação foi confirmada expressamente em juízo pelo Delegado Dr. Rodrigo Moreira (16:47).")
    pdf.bullet_point("Inexistência de Perícia de Voz:", "O Delegado confirmou sob juramento que NÃO FOI REALIZADO EXAME PERICIAL DE CONFRONTO VOCÁLICO nas gravações (19:31). A imputação apoia-se exclusivamente no cadastro de chip de operadora.")
    pdf.bullet_point("Confissão Policial de Ausência de Facção / Hierarquia:", "O Delegado Dr. Nelson Esquiba asseverou em depoimento: 'Não havia facção criminosa, não ostentavam armas, não tinham estrutura armada nem subdivisões... era uma relação de usuários que também vendiam drogas' (114:03).")
    pdf.bullet_point("Destruição do Chip e Fim do Vínculo:", "O paciente deixou de utilizar a linha telefônica investigada ainda no primeiro semestre de 2021, de modo que as rodadas posteriores de escuta já não captaram qualquer diálogo seu.")

    # ══════════════════════════════════════════════════════════════════════
    # SEÇÃO 2: CRONOLOGIA PROCESSUAL E TRATAMENTO ASSIMÉTRICO
    # ══════════════════════════════════════════════════════════════════════
    pdf.section_h1("2. CRONOLOGIA PROCESSUAL E QUEBRA DA ISONOMIA (ART. 580 CPP)")
    pdf.make_table(
        ["Data", "Ato Processual / Instância", "Conteúdo e Efeito Prático"],
        [
            ["27/01/2022", "2ª Vara de Búzios", "Decretada a prisão preventiva de todos os 7 denunciados."],
            ["17/05/2022", "2ª Vara de Búzios", "Desmembramento do processo quanto a Júlio (Proc. 0023013-51.2021.8.19.0078)."],
            ["02/08/2022", "Feito Originário", "Juíza concedeu Liberdade Provisória a TODOS os 5 corréus (José Guilherme, Cristiano, Paulo Henrique, Emerson e Juliano) por excesso de prazo."],
            ["07/10/2024", "Cartório de Búzios", "Certidão cartorária atestando que o mandado de Júlio não constava do BNMP por erro do sistema judiciário."],
            ["05/05/2026", "TJRJ (7ª Câmara)", "Impetração de Habeas Corpus preventivo pela defesa de Júlio (réu em liberdade)."],
            ["12/05/2026", "Polícia Civil", "Cumprimento do mandado de prisão preventiva após 4 anos dos fatos."],
            ["11/06/2026", "TJRJ (Acórdão)", "Denegação do HC pelo TJRJ sob o argumento genérico de 'fuga prolongada'."],
            ["24/07/2026", "2ª Vara de Búzios", "Indeferimento de pedido de revogação da preventiva (decisão per relationem à fl. 1297)."],
            ["29/07/2026", "STJ (6ª Turma)", "Remessa do RHC ao STJ e autuação sob o HC 1.116.750/RJ (Rel. Min. Og Fernandes)."],
            ["13/08/2026", "STJ (Gabinete)", "Autos conclusos para decisão ao Min. Og Fernandes após juntada de informações e vista ao MPF."]
        ],
        [22, 45, 113],
        ["C", "L", "L"]
    )

    pdf.add_page()

    # ══════════════════════════════════════════════════════════════════════
    # SEÇÃO 3: OS 5 PILARES DE ATAQUE DA DEFESA TÉCNICA
    # ══════════════════════════════════════════════════════════════════════
    pdf.section_h1("3. MATRIZ DE TESES JURÍDICAS E LINHAS DE DEFESA")

    pdf.section_h2("Pilar 1: Quebra Injustificável de Isonomia Processual (Art. 580 do CPP)")
    pdf.paragraph(
        "Todos os 5 corréus do processo originário respondem em liberdade desde 02/08/2022. O único corréu flagrado com drogas "
        "(José Guilherme, 218g de maconha) está solto. A fundamentação que liberou os corréus baseou-se na desnecessidade da custódia "
        "extrema e demora instrutória (motivos objetivos). Manter Júlio preso isoladamente viola a isonomia e a jurisprudência do STJ."
    )

    pdf.section_h2("Pilar 2: Ausência de Materialidade Direta do Crime de Tráfico (STJ HC 686.312/MS)")
    pdf.paragraph(
        "Conforme fixado pela Terceira Seção do STJ no leading case HC 686.312/MS, a comprovação da materialidade do tráfico (Art. 33) "
        "exige a apreensão da droga e laudo pericial. Mensagens e escutas telefônicas sem apreensão da droga em poder do paciente "
        "são inaptas a sustentar a materialidade do tráfico ou a justificar a prisão cautelar."
    )

    pdf.section_h2("Pilar 3: Descaracterização do Crime de Associação (Art. 35 da Lei 11.343/06)")
    pdf.paragraph(
        "A jurisprudência pacífica da 6ª Turma do STJ exige a comprovação do vínculo associativo estável e permanente (animus associativo). "
        "O próprio Delegado que presidiu o inquérito atestou em juízo que não havia facção, hierarquia nem organização estruturada."
    )

    pdf.section_h2("Pilar 4: Excesso de Prazo na Prisão Preventiva sem Realização de AIJ (Art. 400 CPP)")
    pdf.paragraph(
        "O paciente está encarcerado preventivamente desde 12/05/2026 (mais de 90 dias de segregação ininterrupta) sem que a Audiência "
        "de Instrução e Julgamento (AIJ) do processo desmembrado tenha sido sequer realizada, sem nenhuma contribuição da defesa."
    )

    pdf.section_h2("Pilar 5: Desconstrução da Tese de 'Fuga' e Boa-Fé do Paciente")
    pdf.paragraph(
        "O mandado de prisão de 2022 não constava do BNMP por falha exclusiva do Judiciário (certidão de 07/10/2024). Além disso, Júlio "
        "contratou advogado e impetrou Habeas Corpus de forma PREVENTIVA no TJRJ em 05/05/2026 enquanto estava em liberdade. A captura "
        "ocorreu apenas em 12/05/2026. Quem impetra HC preventivo submete-se ao crivo da Justiça e não se encontra em fuga deliberada."
    )

    # ══════════════════════════════════════════════════════════════════════
    # SEÇÃO 4: AUDITORIA JURISPRUDENCIAL VALIDADA (6ª TURMA STJ)
    # ══════════════════════════════════════════════════════════════════════
    pdf.section_h1("4. COMPOSIÇÃO DA 6ª TURMA DO STJ & PRECEDENTES VINCULANTES")
    pdf.paragraph(
        "Abaixo estão os precedentes oficiais e auditados dos Ministros que julgarão o recurso no Superior Tribunal de Justiça:"
    )

    pdf.make_table(
        ["Ministro / Órgão", "Precedente Oficial Auditado", "Tese Firmada Aplicável ao Caso"],
        [
            ["Min. Og Fernandes\n(Relator)", "STJ HC 232.842/RJ\ne HC 142.062/RJ", "Concessão da ordem por excesso de prazo na instrução e aplicação do Art. 580 CPP por isonomia entre corréus."],
            ["Min. Sebastião Reis Jr.\n(Presidente)", "STJ HC 686.312/MS\n(3ª Seção Penal)", "Imprescindibilidade de apreensão da droga e laudo pericial para a materialidade do Art. 33. Extensão a corréus (PExt no HC 497.699/MG)."],
            ["Min. Rogerio Schietti\n(6ª Turma)", "STJ AgRg RHC 167.473/SP\ne AgRg REsp 1.984.770/RJ", "Não localização não se confunde com fuga nem autoriza preventiva. Art. 35 exige comprovação cabal de estabilidade."],
            ["Min. Antonio Saldanha\n(6ª Turma)", "STJ AgRg HC 850.569/SP\ne HC 755.819/RJ", "Extensão de liberdade por identidade fática e necessidade de comprovação de ciência inequívoca de mandado."],
            ["Des. Otávio Toledo\n(Convocado TJSP)", "STJ AgRg HC 915.228/SP\ne AgRg HC 890.093/RJ", "Comunicação de motivos objetivos de soltura e absolvição do crime de associação por ausência de permanência."]
        ],
        [40, 48, 92],
        ["L", "L", "L"]
    )

    # ══════════════════════════════════════════════════════════════════════
    # SEÇÃO 5: PLANO DE AÇÃO E PROVIDÊNCIAS IMEDIATAS DA ADVOCACIA
    # ══════════════════════════════════════════════════════════════════════
    pdf.section_h1("5. PLANO DE AÇÃO E RECOMENDAÇÕES PARA O ADVOGADO")
    pdf.bullet_point("1. Atuação no STJ (HC 1.116.750/RJ):", "Despacho presencial / entrega de memoriais no Gabinete do Relator Min. Og Fernandes, ressaltando que o feito está concluso e enfatizando a quebra de isonomia (Art. 580 CPP) e o excesso de prazo (mais de 90 dias sem AIJ).")
    pdf.bullet_point("2. Atuação na 1ª Instância (2ª Vara de Búzios):", "Protocolar petição de relaxamento de prisão por excesso de prazo injustificado (Art. 400 CPP c/c Art. 5º, LXXVIII da CF), requerendo a extensão da liberdade provisória concedida aos demais 5 corréus.")
    pdf.bullet_point("3. Traslado de Prova Emprestada:", "Requerer a juntada da gravação integral e transcrição dos depoimentos dos Delegados Dr. Rodrigo Moreira e Dr. Nelson Esquiba produzidos na audiência da Ação Originária (0022975-39.2021.8.19.0078).")
    pdf.bullet_point("4. Postulação Subsidiária de Cautelares Diversas:", "Formular pedido subsidiário de medidas alternativas (Art. 319 do CPP), como comparecimento periódico e monitoramento eletrônico, diante da primariedade e residência fixa.")

    pdf.ln(3)
    pdf.alert_box(
        "CONSIDERAÇÃO ESTRATÉGICA FINAL",
        "O quadro processual de Júlio é tecnicamente excelente no STJ: há violação evidente de isonomia fática (Art. 580 CPP), "
        "ausência absoluta de apreensão de entorpecentes em seu poder (HC 686.312/MS) e confissão policial em audiência de ausência de "
        "vínculo associativo armado/hierárquico. A manutenção da prisão decorre exclusivamente da inércia burocrática dos tribunais locais."
    )

    # SALVAR ARQUIVO
    out_dir = os.path.join(os.getcwd(), "Clientes", "Júlio_Pereira_Marcos", "Caso_Principal", "analises")
    os.makedirs(out_dir, exist_ok=True)
    out_pdf = os.path.join(out_dir, "Relatorio_Executivo_Julio_Pereira_Marcos_Advocacia.pdf")
    pdf.output(out_pdf)
    print(f"Sucesso: PDF gerado em: {out_pdf}")
    return out_pdf

if __name__ == "__main__":
    build_pdf()
