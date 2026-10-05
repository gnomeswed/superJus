# 🏛️ Catálogo de Endpoints e Engenharia Reversa de Tribunais (SuperJus)

> Documento gerado automaticamente pelo `mitmproxy_court_inspector.py`.
> **Última Atualização:** 02/09/2026 às 18:04:10 | **Total de Endpoints Mapeados:** 4

---

## 📋 Índice por Tribunal

- [PJe / PDPJ-Br (Processo Judicial Eletrônico)](#pje--pdpj-br-processo-judicial-eletrônico) (1 endpoints)
- [STJ (Superior Tribunal de Justiça)](#stj-superior-tribunal-de-justiça) (1 endpoints)
- [TJRJ (Tribunal de Justiça do Rio de Janeiro)](#tjrj-tribunal-de-justiça-do-rio-de-janeiro) (2 endpoints)

---

## PJe / PDPJ-Br (Processo Judicial Eletrônico)

### `POST` `/api/v1/comunicacao`
- **Host:** `https://comunica.pje.jus.br`
- **Status:** `200` | **Latência:** `510.0 ms`

**Request Schema:**
```json
{
  "siglaTribunal": "string",
  "numeroProcesso": "string",
  "meio": "string"
}
```

**Response Schema:**
```json
{
  "status": "string",
  "count": "integer",
  "items": [
    {
      "id": "integer",
      "data_disponibilizacao": "string",
      "tipoComunicacao": "string",
      "destinatario": "string"
    }
  ]
}
```

**Comando cURL Reproduzível:**
```bash
curl -X POST "https://comunica.pje.jus.br/api/v1/comunicacao" \
  -H "Content-Type: application/json" \
  -H "Origin: https://comunica.pje.jus.br" \
  -d "{\"siglaTribunal\": \"STJ\", \"numeroProcesso\": \"1116750\", \"meio\": \"D\"}"
```

---

## STJ (Superior Tribunal de Justiça)

### `POST` `/api_publica_stj/_search`
- **Host:** `https://api-publica.datajud.cnj.jus.br`
- **Status:** `200` | **Latência:** `640.8 ms`

**Request Schema:**
```json
{
  "query": {
    "match": {
      "numeroProcesso": "string"
    }
  },
  "size": "integer"
}
```

**Response Schema:**
```json
{
  "hits": {
    "total": {
      "value": "integer"
    },
    "hits": [
      {
        "_source": {
          "numeroProcesso": "string",
          "classe": {
            "codigo": "any",
            "nome": "any"
          },
          "orgaoJulgador": {
            "codigo": "any",
            "nome": "any"
          },
          "nivelSigilo": "integer"
        }
      }
    ]
  }
}
```

**Comando cURL Reproduzível:**
```bash
curl -X POST "https://api-publica.datajud.cnj.jus.br/api_publica_stj/_search" \
  -H "Authorization: APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==" \
  -H "Content-Type: application/json" \
  -d "{\"query\": {\"match\": {\"numeroProcesso\": \"00298456720268190000\"}}, \"size\": 5}"
```

---

## TJRJ (Tribunal de Justiça do Rio de Janeiro)

### `POST` `/consultaprocessual/api/processos/por-numeracao-unica`
- **Host:** `https://www3.tjrj.jus.br`
- **Status:** `200` | **Latência:** `420.5 ms`

**Request Schema:**
```json
{
  "tipoProcesso": "string",
  "codigoProcesso": "string"
}
```

**Response Schema:**
```json
[
  {
    "idProcesso": "integer",
    "numProcesso": "string",
    "classe": "string",
    "descricaoServentia": "string",
    "ultimoMovimento": "string",
    "dtUltimoMovimento": "string"
  }
]
```

**Comando cURL Reproduzível:**
```bash
curl -X POST "https://www3.tjrj.jus.br/consultaprocessual/api/processos/por-numeracao-unica" \
  -H "Content-Type: application/json" \
  -H "Origin: https://www3.tjrj.jus.br" \
  -H "Referer: https://www3.tjrj.jus.br/consultaprocessual/" \
  -d "{\"tipoProcesso\": \"1\", \"codigoProcesso\": \"0023013-51.2021.8.19.0078\"}"
```

---

### `POST` `/consultaprocessual/api/processos/por-numero/movimentos`
- **Host:** `https://www3.tjrj.jus.br`
- **Status:** `200` | **Latência:** `380.2 ms`

**Request Schema:**
```json
{
  "tipoProcesso": "integer",
  "codigoProcesso": "string",
  "indProcVolumoso": "string",
  "ultimaOrdemExibida": "null"
}
```

**Response Schema:**
```json
[
  {
    "ordem": "integer",
    "dtMovimento": "string",
    "dtJuntada": "string",
    "descrMov": "string",
    "movimentosExibicao": [
      {
        "tipoMovimento": "string",
        "detalhesMovimento": "string"
      }
    ]
  }
]
```

**Comando cURL Reproduzível:**
```bash
curl -X POST "https://www3.tjrj.jus.br/consultaprocessual/api/processos/por-numero/movimentos" \
  -H "Content-Type: application/json" \
  -H "Origin: https://www3.tjrj.jus.br" \
  -d "{\"tipoProcesso\": 1, \"codigoProcesso\": \"2021.078.023002-1\", \"indProcVolumoso\": \"N\", \"ultimaOrdemExibida\": null}"
```

---
