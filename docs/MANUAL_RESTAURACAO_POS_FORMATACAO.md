# Guia de Restauração Pós-formatação (superJus)

## 1) Clonar e venv
```powershell
cd C:\Projetos
git clone https://github.com/gnomeswed/superJus.git superJus
cd superJus
py -3.11 -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m playwright install chromium
copy .env.example .env  # preencha DATAJUD_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
```
## 2) App
`.\.venv\Scripts\python -m streamlit run core/app.py` ou `scripts\INICIAR_SISTEMA.bat`
## 3) Monitor 4h
- Cron Command Code: `0 8,12,16,20 * * *` sem `--force` (veja `cron_list`)
- Task Scheduler: `schtasks /Create /TN SuperJus_Monitor_Julio_4h /TR C:\Projetos\superJus\scripts\run_monitor_wrapper.bat /SC DAILY /ST 08:00 /RI 240 /DU 24:00 /F`
- Logs: `temp_logs_e_resultados/monitor_*.log`, estado `.agents/telegram_last_state.json`

## 4) memU
Instale `pip install memu-cli` se necessário; use `scripts/memu_store.py`/`memu_retrieve.py` com `PYTHONIOENCODING=utf-8`.

## Backup
Se houver backup anterior em `C:\Projetos\Super Analista Jurídico`, copie apenas `.agents` e `brain_artifacts` relevantes; todos os caminhos do código já foram migrados para `C:\Projetos\superJus`.

