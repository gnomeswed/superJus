---
name: Auditar Pasta do Cliente em Busca de Brechas e Nulidades
description: "Varre e analisa exaustivamente todos os arquivos (PDFs, textos, transcrições de audiências, inquéritos e denúncias) contidos na pasta de um cliente, identificando nulidades processuais (CPP art. 564), quebras de cadeia de custódia, inépcia acusatória, teses de dosimetria e vícios de isonomia (art. 580 CPP)."
---

# Auditar Pasta do Cliente em Busca de Brechas e Nulidades

Esta skill realiza uma varredura heurística e jurídica exaustiva por toda a estrutura de arquivos da pasta de um cliente, identificando pontos cegos, nulidades processuais, quebras de prova e teses defensivas de alto impacto.

---

## 🎯 Padrões e Brechas Investigadas

1. **Vício de Isonomia (Art. 580 do CPP):**
   - Identifica se corréus da mesma ação penal receberam liberdade provisória ou revogação de cautelar sem que o benefício tenha sido estendido ao cliente.
2. **Quebra de Cadeia de Custódia da Prova (Arts. 158-A a 158-F do CPP):**
   - Audita autos de apreensão, conferência de lacres, extratos de perícia e relatórios policiais.
3. **Nulidade na Extração de WhatsApp e Dados Telemáticos (Tema 1.062/STF):**
   - Verifica transcrições de conversas sem preservação de hash ou espelhamento sem autorização judicial motivada.
4. **Nulidade por Reconhecimento Pessoal Irregular (Art. 226 do CPP / HC 598.886 STJ):**
   - Mapeia reconhecimentos por foto ou sem alinhamento de suspeitos.
5. **Inviolabilidade de Domicílio e Busca sem Mandado (Tema 280/STF):**
   - Mapeia ingressos domiciliares baseados exclusivamente em denúncia anônima ou sem justa causa documentada.
6. **Inépcia da Acusação por Associação Genericamente Imputada (Art. 41 CPP / Art. 35 Lei 11.343/06):**
   - Detecta denúncias que imputam associação criminosa sem demonstrar o vínculo estável e permanente.

---

## 🛠️ Como Executar a Varredura

Para auditar a pasta de qualquer cliente e gerar o **Relatório de Diagnóstico de Brechas (`Relatorio_Diagnostico_Brechas_Nulidades.md`)**:

```bash
python c:\Projetos\superJus\.agents\skills\auditar_pasta_cliente_brechas\scripts\brechas_analyzer.py "c:\Projetos\superJus\Clientes\Nome_Do_Cliente"
```
