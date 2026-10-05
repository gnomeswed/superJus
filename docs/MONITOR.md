# Guia de Monitoramento 4h — Júlio Pereira Marcos

## Comandos de verificação ao vivo (portais)
```powershell
$env:PYTHONIOENCODING="utf-8"
C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe scripts/check_julio_fast_live.py

C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe scripts/read_stj_stealth.py
```

## Automação persistente (Windows)
- **Task Scheduler:** `SuperJus_Monitor_Julio_4h` executa `scripts/run_monitor_wrapper.bat` às 08:00, 12:00, 16:00 e 20:00 (diário, repetido a cada 4h).
- **Wrapper:** lê `DATAJUD_API_KEY` via `.env`, executa `telegram_monitor_julio.py` (sem `--force`), grava `temp_logs_e_resultados/monitor_*.log`. Para desativar: `schtasks /Change /TN "SuperJus_Monitor_Julio_4h" /Disable`.
- **Cron do Command Code:** backup da sessão `bce9be27` com `0 8,12,16,20 * * *`.

## Configuração do `.env`
```ini
DATAJUD_API_KEY=apikey xxx
TELEGRAM_BOT_TOKEN=xxx
TELEGRAM_CHAT_ID=-xxx
DEEPSEEK_API_KEY=xxx
```

## Telegram Alert Bridge (comandos do grupo Swd hermes)
`/check` `/status` `/djen` `/exec <cmd>` — bot `@Swedxbot` responde no grupo `-5578464034`.

