# Códigos TPU Ambíguos — Referência de Validação

Este arquivo documenta os códigos da Tabela Processual Unificada (TPU/CNJ) que
**NÃO indicam resultado** e requerem leitura do campo `complementosTabelados[]`
ou do teor integral da decisão antes de qualquer interpretação.

## Caso Real que Motivou Este Documento

**Processo:** 0808595-36.2026.8.19.0002 (Lucas Dias Oliveira — Taxista)
**Data:** 10/08/2026
**Erro:** O DataJud retornou código `12146` com nome "Liberdade Provisória".
O sistema interpretou como *concessão de soltura*. Na realidade, a juíza
Dra. Juliana Grillo El Jaick **INDEFERIU** o pedido e manteve a prisão preventiva.
O mesmo código 12146 já havia sido usado em 10/04/2026 para outro indeferimento.

**Causa raiz:** O código 12146 identifica o *gênero do incidente apreciado*
(pedido de liberdade provisória), e não o *resultado* (deferido vs indeferido).
O resultado está no array `complementosTabelados` (ex: código 100 = Concedida,
código 101 = Negada) ou no texto da decisão judicial.

## Tabela de Códigos Ambíguos

| Código TPU | Nome Oficial CNJ | O que Parece | O que Realmente É |
|:----------:|:-----------------|:-------------|:------------------|
| `12146` | Liberdade Provisória | Réu foi solto | Pedido de LP foi *apreciado* (pode ser deferido OU indeferido) |
| `12068` | Prisão Preventiva | Réu foi preso | Incidente de PP foi *apreciado* (pode ser decretação OU revogação) |
| `198` | Decisão | Algo foi decidido | Qualquer decisão interlocutória — sem indicar conteúdo |
| `581` | Documento | Documento juntado | Juntada genérica — pode ser alvará, certidão, ofício ou mandado |
| `60` | Expedição de Documento | Documento expedido | Não diferencia alvará de soltura de ofício de rotina |
| `11383` | Ato Ordinatório | Ato do juiz | Mero expediente de cartório, sem conteúdo decisório |
| `51` | Conclusão | Concluso ao juiz | Processo foi para o gabinete — não indica qual decisão será proferida |
| `85` | Petição | Manifestação juntada | Não indica se é da defesa, acusação, perito ou terceiro |
| `219` | Condenação | Réu foi condenado | Veredito do Júri ou sentença — mas pode ser parcial ou com atenuantes |
| `326` | Absolvição | Réu foi absolvido | Pode ser absolvição própria (485) ou imprópria (medida de segurança) |
| `385` | Extinção da Punibilidade | Processo acabou | Pode ser prescrição, morte, perdão ou outra causa do Art. 107 CP |

## Regra de Validação Obrigatória

```python
CODIGOS_AMBIGUOS = {12146, 12068, 198, 581, 60, 11383, 51, 85, 219, 326, 385}

def interpretar_movimento(mov: dict) -> str:
    codigo = mov.get("codigo")
    nome = mov.get("nome", "")
    complementos = mov.get("complementosTabelados", [])
    
    if codigo in CODIGOS_AMBIGUOS:
        if complementos:
            # Usar o complemento para determinar o resultado real
            resultado = " | ".join(
                f"{c.get('nome')}: {c.get('descricao')}" for c in complementos
            )
            return f"⚠️ {nome} → Resultado: {resultado}"
        else:
            return f"⚠️ {nome} → APRECIAÇÃO SEM RESULTADO EXPLÍCITO (verificar teor da decisão)"
    else:
        return f"✅ {nome}"
```
