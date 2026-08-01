# 🛡️ Guia Oficial de Restauração Pós-Formatação (SuperJus + Antigravity + memU)

Este guia garante que **NENHUMA INFORMAÇÃO, MEMÓRIA OU REGRA** seja perdida ao formatar o seu computador.

---

### 📦 O que foi Salvo no seu Backup:

1. **Repositório GitHub (`superJus`):**  
   * **URL:** `https://github.com/gnomeswed/superJus.git`
   * Contém todo o código-fonte, scripts, clientes (Júlio, Ecildo, Lucas), teses jurídicas e habilidades.

2. **Pacote de Segurança Compactado:**  
   * **Local 1 (Área de Trabalho):** `C:\Users\Administrator\Desktop\BACKUP_COMPLETO_ANTIGRAVITY_MEMU.zip`
   * **Local 2 (Raiz do Projeto):** `c:\Projetos\Super Analista Jurídico\BACKUP_COMPLETO_ANTIGRAVITY_MEMU.zip`
   * **Conteúdo do .ZIP:**
     * `dot_memu/`: Banco de Dados `memu.sqlite3` com todas as memórias salvas e `config.env`.
     * `dot_agents/`: Pasta `.agents` contendo `AGENTS.md` e todas as Skills especializadas.
     * `brain_artifacts/`: Relatórios e análises executivas (Júlio e Ecildo).

---

### 🚀 3 Passos para Restaurar Tudo Após Formatar o Windows:

#### Passo 1 — Clonar os Projetos do GitHub
Abra o terminal no novo Windows e rode:
```powershell
cd C:\Projetos
git clone https://github.com/gnomeswed/superJus.git
# Se desejar restaurar o swedsystem também:
# git clone https://github.com/gnomeswed/swedsystem.git
```

#### Passo 2 — Extrair a Memória do memU e as Skills
Extraia o arquivo `BACKUP_COMPLETO_ANTIGRAVITY_MEMU.zip` e mova as pastas extraídas para seus locais originais:
1. Copie a pasta `dot_memu` para: `C:\Users\<SeuUsuario>\.memu` (renomeando para `.memu`).
2. Copie a pasta `dot_agents` para dentro do projeto: `C:\Projetos\superJus\.agents`.

#### Passo 3 — Reinstalar o memU no Python
No terminal da nova máquina, rode:
```powershell
pip install memu-cli
```

Pronto! Todos os seus projetos de IA, históricos de conversas, regras jurídicas e bancos do Júlio e do Ecildo estarão **100% restaurados e prontos para uso**!
