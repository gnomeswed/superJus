# Resumo Executivo da Raspagem Integral — Lucas de Souza Freitas

**Data da Raspagem:** 10/08/2026 11:28:32

## � Achados Críticos

### 1. Decisão de 17/06/2026 agora disponível NA ÍNTEGRA
- Arquivo: `Decisoes_na_Integra/2026-06-17_Decisao_Manutricao_Prisao_Preventiva_INTEGRA.md`
- **6.160 caracteres** de fundamentação completa
- Capturada via botão "Ver íntegra do(a) Decisão (Original)" do TJRJ
- **Substitui** o extrato anterior (`17-06-2026_Recebimento.txt`) que tinha apenas ~400 caracteres

### 2. Status Processual Atualizado
- **Localização:** Processo Tramitando No Tribunal de Justiça
- **Última Mov:** Remessa em 06/08/2026 (prazo 15 dias = 21/08/2026)
- **2ª instância:** AINDA NÃO autuada (Protocolo 202600653257 aguardando)
- **STJ:** sem movimentação (CSID anti-bot ativo)

### 3. Movimentos Catalogados (10 blocos detectados)
A raspagem confirmou os 10 movimentos já existentes na pasta `02_Movimentacoes_Individuais/`. Nenhuma nova movimentação detectada desde 06/08/2026.

## 📋 Itens da Raspagem
- **1ª Instância (TJRJ):** ✅ Consulta OK + 10 movimentos estruturados + 3 modais integrais capturados
- **2ª Instância (TJRJ):** ✅ Busca por nome (Tribunal de Justiça, Niterói, 2024–2026) — **Nenhum registro** (esperado)
- **STJ:** ❌ Bloqueado (CSID)
- **DJEN:** ❌ Timeout (comunica.pje.jus.br)

## 📁 Arquivos Gerados
- `02_Movimentacoes_Individuais/2026-08-10_11_Confirmacao_Localizacao_Teor_Integral.md`
- `03_Documentos_do_Processo/Decisoes_na_Integra/2026-06-17_Decisao_Manutricao_Prisao_Preventiva_INTEGRA.md`
- `03_Documentos_do_Processo/Espelho_Processual_Integral_Online_10_08_2026.md`
- `03_Documentos_do_Processo/_raspagem_10_08_2026/` (raw: HTML, PNG, JSON)

## 🔧 Scripts Criados (reutilizáveis)
- `scripts/raspar_lucas_integral_TJRJ.py` — pipeline completo TJRJ
- `scripts/raspar_lucas_apenas_integrais.py` — captura apenas modais (re-entrante)
- `scripts/buscar_2_inst_lucas_v3.py` — busca 2ª instância por nome

## 💡 Implicações Estratégicas
1. **Recurso de apelação pendente de autuação** — TJRJ ainda não atribuiu número de 2ª instância. Monitorar diariamente.
2. **Prazo fatal:** 21/08/2026 (15 dias após remessa em 06/08/2026). Após essa data, urge verificar se houve distribuição ao Relator.
3. **STJ/DJEN inacessíveis localmente** — considerar (a) tentar via VPS nos EUA (skill `djen_acesso_vps_status` indica instabilidade também); (b) monitorar DJERJ caderno criminal para captura de publicação oficial.
4. **Decisão 17/06/2026 ÍNTEGRA** permite agora construir teses defensivas mais robustas para o recurso de apelação, especialmente refutando os argumentos do precedente citado (HC 0054200-54.2020).

## 🛠️ Próximas Ações Recomendadas
- [ ] Tentar novamente a consulta STJ/DJEN em horário de menor tráfego (manhã cedo)
- [ ] Acompanhar diariamente o TJRJ 2ª Instância para detectar autuação da apelação
- [ ] Elaborar peça de Razões de Apelação aproveitando a íntegra da decisão 17/06/2026
- [ ] Verificar eventual HC no STJ paralelo à apelação
