# 📖 Guia do Pipeline de OCR Automatizado — SuperJus

Este documento detalha o funcionamento, arquitetura, comandos e boas práticas do pipeline de OCR automatizado do **SuperJus**, desenvolvido com **OCRmyPDF**, **Tesseract-OCR** e **PyTesseract**.

---

## 🎯 Objetivo e Contexto Jurídico
Em processos criminais e inquéritos policiais (como no caso **Júlio Pereira Marcos** e demais clientes), é comum a juntada de termos de declaração, autos de apreensão, laudos periciais e relatórios de inteligência digitalizados como imagens puras (scans/bitmaps) sem camada de texto selecionável.

O pipeline resolve este problema ao:
1. Detectar automaticamente se um PDF é uma imagem escaneada pura (`PURE_SCAN`) ou possui anexos sem texto (`PARTIAL_SCAN`).
2. Aplicar OCR em **Português Brasileiro (`por`)** sem alterar o layout original.
3. **Preservar carimbos, rubricas e selos de protocolo:** O OCRmyPDF gera uma camada vetorial invisível sobre/sob o mapa de bits original ("sandwich PDF"), mantendo 100% da nitidez gráfica para fins de prova e autenticidade jurídica.
4. Tratar certificados digitais do **PJe/Projudi** (`invalidate_digital_signatures=True`) para evitar rejeições de arquivos assinados.
5. Criar **backup automático** de cada original em `_scanned_backups/` antes de qualquer alteração atômica.

---

## 🛠️ Status do Ambiente e Instalação

| Componente | Versão / Caminho | Status |
| :--- | :--- | :---: |
| **Tesseract-OCR (Binário)** | `C:\Program Files\Tesseract-OCR\tesseract.exe` | ✅ Instalado |
| **Pacote de Idioma Português** | `tessdata\por.traineddata` | ✅ Disponível |
| **OCRmyPDF** | `v17.11.0` | ✅ Instalado |
| **PyTesseract** | `v0.3.13` | ✅ Instalado |
| **PyMuPDF / pypdf** | Motores de inspeção rápida de texto e páginas | ✅ Operacionais |
| **Windows PATH** | `C:\Program Files\Tesseract-OCR` adicionado permanentemente | ✅ Configurado |

### Fallbacks Automáticos no Windows
O script implementa múltiplos mecanismos de detecção automática para garantir que funcione em qualquer terminal ou sessão de usuário:
1. Consulta variáveis de ambiente personalizadas (`TESSERACT_CMD`, `TESSERACT_PATH`).
2. Varre caminhos canônicos do Windows:
   - `C:\Program Files\Tesseract-OCR\tesseract.exe`
   - `C:\Program Files (x86)\Tesseract-OCR\tesseract.exe`
   - `%LOCALAPPDATA%\Programs\Tesseract-OCR\tesseract.exe`
   - `%USERPROFILE%\AppData\Local\Programs\Tesseract-OCR\tesseract.exe`
3. Injeta dinamicamente a pasta do binário no `os.environ["PATH"]` e configura `os.environ["TESSDATA_PREFIX"]` para que os subprocessos do OCRmyPDF localizem os modelos de linguagem sem conflitos.
4. Vincula o executável diretamente ao `pytesseract.pytesseract.tesseract_cmd`.

---

## 🚀 Como Executar o Pipeline

### 1. Diagnóstico do Ambiente
Verifica se todas as dependências estão presentes e funcionais:
```powershell
python c:\Projetos\superJus\scripts\ocrmypdf_sanitizer.py --check-env
```

### 2. Simulação de Varredura (Dry-Run)
Audita todos os PDFs de clientes e gera relatórios sem modificar nenhum arquivo:
```powershell
python c:\Projetos\superJus\scripts\ocrmypdf_sanitizer.py --dry-run
```

### 3. Processamento de um Cliente Específico
Executa o OCR em todos os PDFs escaneados da pasta do cliente:
```powershell
python c:\Projetos\superJus\scripts\ocrmypdf_sanitizer.py --client Julio_Pereira_Marcos
```

### 4. Processamento de um Arquivo PDF Específico
Aplica o OCR em um documento individual (ex.: inquérito ou termo de audiência):
```powershell
python c:\Projetos\superJus\scripts\ocrmypdf_sanitizer.py --file "c:\Projetos\superJus\Clientes\Julio_Pereira_Marcos\02_APENSOS_E_MEDIDAS_CAUTELARES\Inquerito_Policial_127_2021_Buzios_Digitalizado.pdf"
```

### 5. Forçar Reexecução de OCR (Redo-OCR)
Substitui camadas de texto antigas ou de baixa qualidade:
```powershell
python c:\Projetos\superJus\scripts\ocrmypdf_sanitizer.py --file "caminho\arquivo.pdf" --force
```

---

## 📊 Parâmetros do CLI

| Parâmetro | Descrição | Padrão |
| :--- | :--- | :---: |
| `--path`, `-p` | Diretório raiz para varredura | `c:\Projetos\superJus\Clientes` |
| `--client`, `-c` | Filtro por pasta de cliente | `None` (todos) |
| `--file`, `-f` | Caminho de um PDF individual | `None` |
| `--dry-run` | Apenas audita e gera relatório sem alterar arquivos | `False` |
| `--force`, `--redo-ocr` | Força re-OCR mesmo se já possuir texto | `False` |
| `--lang`, `-l` | Idioma de reconhecimento do Tesseract | `por` |
| `--threshold` | Quantidade mínima de caracteres por página | `40` |
| `--no-backup` | Desativa a criação de backups | `False` |
| `--no-deskew` | Desativa desinclinação automática de páginas | `False` |
| `--no-rotate` | Desativa rotação inteligente baseada em orientação | `False` |
| `--report-dir` | Pasta de destino dos relatórios | `c:\Projetos\superJus\docs\relatorios_ocr` |
| `--check-env` | Exibe diagnóstico de ambiente e encerra | `False` |

---

## 🧪 Testes Automatizados
O projeto conta com suíte de testes unitários e de integração em `tests/test_ocrmypdf_sanitizer.py`. Para executar:
```powershell
python -m pytest c:\Projetos\superJus\tests\test_ocrmypdf_sanitizer.py -v
```
Itens validados:
- Detecção de binários do Tesseract e pacotes de idioma.
- Classificação correta de PDF escaneado puro vs. digital.
- Execução de OCR em imagem com carimbo judicial e verificação de ganho de caracteres.
- Criação de backup de segurança e substituição atômica.
- Geração íntegra de relatórios JSON e Markdown.

---

## 📁 Estrutura de Arquivos Criados
- **Script:** [`c:\Projetos\superJus\scripts\ocrmypdf_sanitizer.py`](file:///c:/Projetos/superJus/scripts/ocrmypdf_sanitizer.py)
- **Testes:** [`c:\Projetos\superJus\tests\test_ocrmypdf_sanitizer.py`](file:///c:/Projetos/superJus/tests/test_ocrmypdf_sanitizer.py)
- **Documentação:** [`c:\Projetos\superJus\docs\GUIA_PIPELINE_OCR_SUPERJUS.md`](file:///c:/Projetos/superJus/docs/GUIA_PIPELINE_OCR_SUPERJUS.md)
- **Relatórios Gerados:** [`c:\Projetos\superJus\docs\relatorios_ocr\`](file:///c:/Projetos/superJus/docs/relatorios_ocr/)
