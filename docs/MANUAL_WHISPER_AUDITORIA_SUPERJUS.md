# Manual de Transcrição e Auditoria de Audiências e Interceptações Telefônicas com Whisper — SuperJus

## 1. Visão Geral
O módulo forense `scripts/transcrever_audiencias_whisper.py` automatiza o processamento, decodificação, degravação, auditoria penal e formatação jurídica de mídias audiovisuais em processos criminais do escritório SuperJus.

### Suporte a Mídias:
- **Áudios:** MP3, WAV, M4A, OGG, OPUS, FLAC, AAC, WMA.
- **Vídeos:** MP4, MKV, AVI, MOV, WEBM (gravações de AIJ em Teams, PJe Mídias, Zoom, Webex, Tribunal do Júri e celulares).
- **Extração e Normalização:** Integração nativa com FFmpeg para normalização de áudio em 16kHz mono (otimizando a precisão do Whisper).

---

## 2. Instalação e Requisitos

O módulo utiliza o `faster-whisper` (CTranslate2) por padrão, proporcionando velocidade de até 4x a 5x superior e menor consumo de memória RAM/VRAM, além de manter fallback automático para `openai-whisper`.

```bash
pip install faster-whisper
```

*Nota: O binário do `ffmpeg` já se encontra instalado e configurado no PATH do sistema.*

---

## 3. Comandos de Uso

### A) Transcrever Audiência de Instrução e Julgamento (AIJ) com Depoente Principal
```bash
python scripts/transcrever_audiencias_whisper.py ^
    --input "Clientes/Júlio_Pereira_Marcos/05_AUDIENCIAS_E_PROVAS/Audiencia_Instrucao_e_Julgamento/Audio_Integral_Audiencia_Instrucao_Policias.mp3" ^
    --depoente "Del. Rodrigo Moreira" ^
    --processo "0023013-51.2021.8.19.0078" ^
    --vara "1ª Vara da Comarca de Armação dos Búzios/RJ" ^
    --output-dir "Clientes/Júlio_Pereira_Marcos/05_AUDIENCIAS_E_PROVAS/Audiencia_Instrucao_e_Julgamento"
```

### B) Transcrever Trecho Fatiado com Offset de Tempo (ex: trecho que começa aos 20m35s da audiência)
```bash
python scripts/transcrever_audiencias_whisper.py ^
    --input "caminho/trecho_audiencia.mp3" ^
    --offset-seconds 1235 ^
    --depoente "Del. Rodrigo Moreira" ^
    --processo "0023013-51.2021.8.19.0078" ^
    --vara "1ª Vara da Comarca de Armação dos Búzios/RJ"
```

### C) Transcrever Interceptação Telefônica / Áudios de WhatsApp
```bash
python scripts/transcrever_audiencias_whisper.py ^
    --input "Clientes/Júlio_Pereira_Marcos/05_AUDIENCIAS_E_PROVAS/Audios_WhatsApp_Advogados/AUD-20260601-WA0005.mp3" ^
    --mode interceptacao ^
    --speakers "Investigado Júlio,Advogado" ^
    --processo "0023013-51.2021.8.19.0078" ^
    --output-dir "exemplos_auditoria_whisper"
```

### D) Processamento em Lote de uma Pasta Inteira
```bash
python scripts/transcrever_audiencias_whisper.py ^
    --dir "Clientes/Júlio_Pereira_Marcos/05_AUDIENCIAS_E_PROVAS/Audios_WhatsApp_Advogados" ^
    --mode interceptacao ^
    --processo "0023013-51.2021.8.19.0078"
```

### E) Usar Modelo de Alta Precisão (Large-v3 ou Turbo) com Termos Personalizados
```bash
python scripts/transcrever_audiencias_whisper.py ^
    --input "caminho/video_juri.mp4" ^
    --model large-v3 ^
    --mode tribunal_juri ^
    --keywords "homicídio qualificado,motivo fútil,legítima defesa,in dubio pro reo" ^
    --memu
```

---

## 4. Parâmetros da Linha de Comando (CLI)

| Parâmetro | Tipo | Descrição |
| :--- | :--- | :--- |
| `--input`, `-i` | Arquivo | Caminho do áudio ou vídeo a transcrever. |
| `--dir`, `-d` | Diretório | Pasta com múltiplos áudios/vídeos para processar em lote. |
| `--output-dir`, `-o` | Diretório | Pasta de saída dos relatórios (default: mesma pasta do arquivo). |
| `--model`, `-m` | String | Modelo do Whisper: `tiny`, `base`, `small`, `medium`, `large-v2`, `large-v3`, `turbo` (default: `base`). |
| `--device` | String | `auto`, `cpu`, `cuda` (default: `auto`). |
| `--language`, `-l` | String | Idioma do áudio (default: `pt`). |
| `--beam-size` | Inteiro | Tamanho do feixe de decodificação (default: `5`). |
| `--offset-seconds` | Float | Deslocamento temporal em segundos para mídias cortadas (ex: `1235.0`). |
| `--mode` | String | Modo de operação: `audiencia`, `interceptacao`, `tribunal_juri`, `reuniao_teams` (default: `audiencia`). |
| `--depoente` | String | Nome ou qualificação do depoente principal (ex: `Del. Rodrigo Moreira`). |
| `--speakers` | String | Lista de oradores separados por vírgula (ex: `Juiz,Promotor,Depoente,Defensor`). |
| `--processo` | String | Número CNJ do processo para indexação e cabeçalho de citação. |
| `--vara` | String | Identificação do Juízo / Vara Criminal. |
| `--keywords` | String | Termos sensíveis adicionais separados por vírgula para auditoria. |
| `--memu` | Flag | Grava automaticamente os achados e teses no banco de memória persistente SQLite memU. |

---

## 5. Estrutura dos Arquivos Forenses Gerados

Para cada mídia processada (`nome_arquivo.ext`), o módulo gera simultaneamente 6 arquivos:

1. **`[nome]_transcricao_completa.txt`**: Transcrição linear completa com carimbos milissegundos `[HH:MM:SS,mmm -> HH:MM:SS,mmm]` e oradores.
2. **`[nome]_transcricao_formatada.md`**: Transcrição estruturada em Markdown, dividida por blocos de fala, oradores e links para fácil leitura pelo advogado.
3. **`[nome]_auditoria_termos_chave.md`**: Dossiê penal que agrupa todas as ocorrências de termos por categoria (Drogas/Tráfico, Facção/Associação, Armas, Flagrante, Confissão, Materialidade, Nulidades) e calcula o impacto estratégico (tese defensiva vs. ponto acusatório).
4. **`[nome]_citacoes_juridicas.md`**: Citações formatadas no padrão dos Tribunais Superiores prontas para copiar e colar diretamente nas peças:
   ```markdown
   > *"[00:20:41] Del. Rodrigo Moreira: \"Não, foi identificado a facção criminosa, doutora, o que foi identificado foi uma venda de drogas de forma escamoteada, de forma bem organizada, para não se expor, exatamente o contrário...\""*
   > *(Fonte: Mídia da Audiência de Instrução e Julgamento — Ação Penal 0023013-51.2021.8.19.0078, 1ª Vara da Comarca de Armação dos Búzios/RJ, evento aos [00:20:41])*
   ```
5. **`[nome]_legendas.srt`**: Arquivo de legendas compatível com players de vídeo (VLC, Media Player, Teams) com sincronia precisa.
6. **`[nome]_transcricao.json`**: Metadados completos, probabilidades acústicas, logprob e todas as palavras com timestamps (`word_timestamps`) para integração com RAG, IA e indexação de busca.

---

## 6. Integração com a Memória Persistente (memU)

Quando acionado com `--memu` (ou automaticamente quando referenciar o caso `0023013-51.2021.8.19.0078` de Júlio Pereira Marcos), o módulo aciona o `scripts/memu_store.py` e persiste os achados favoráveis à defesa e pontos críticos na trilha `Julio_Pereira_Marcos_Caso_Principal` do memU.

Dessa forma, os outros agentes do escritório (**Hermes Agent**, **OpenCode** e **Antigravity**) têm acesso imediato às declarações do delegado ou testemunhas nas próximas redações de Habeas Corpus e Memoriais.
