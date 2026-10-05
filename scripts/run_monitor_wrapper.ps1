# run_monitor_wrapper.ps1 - Monitor Julio via Task Scheduler
$ErrorActionPreference = "Continue"
$ROOT = "C:\Projetos\superJus"
$PY = "C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe"
$env:PYTHONIOENCODING = "utf-8"

# Carrega DATAJUD_API_KEY do .env se nao definida
if (-not $env:DATAJUD_API_KEY) {
    $envFile = Join-Path $ROOT ".env"
    if (Test-Path $envFile) {
        Get-Content $envFile | ForEach-Object {
            if ($_ -match "^DATAJUD_API_KEY=(.+)$") {
                $env:DATAJUD_API_KEY = $Matches[1].Trim('"').Trim("'")
            }
        }
    }
}

$logDir = Join-Path $ROOT "temp_logs_e_resultados"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }

$ts = Get-Date -Format "yyyyMMdd_HHmmss"
$logFile = Join-Path $logDir "monitor_$ts.log"

"[$ts] Iniciando monitor Julio..." | Out-File -FilePath $logFile -Encoding utf8

try {
    # Timeout de 300s para permitir que todas as consultas terminem com folga
    $proc = Start-Process -FilePath $PY -ArgumentList "-X", "utf8", (Join-Path $ROOT "scripts\telegram_monitor_julio.py") -NoNewWindow -PassThru -RedirectStandardOutput (Join-Path $logDir "monitor_stdout_$ts.tmp") -RedirectStandardError (Join-Path $logDir "monitor_stderr_$ts.tmp")
    $exited = $proc.WaitForExit(300000)
    if (-not $exited) {
        "[$ts] TIMEOUT 300s - matando processo" | Out-File -FilePath $logFile -Append -Encoding utf8
        $proc.Kill()
    } else {
        "[$ts] Processo concluido (exit $($proc.ExitCode))" | Out-File -FilePath $logFile -Append -Encoding utf8
    }
    # Anexa stdout/stderr ao log
    $stdout = Join-Path $logDir "monitor_stdout_$ts.tmp"
    $stderr = Join-Path $logDir "monitor_stderr_$ts.tmp"
    if (Test-Path $stdout) { Get-Content $stdout -ErrorAction SilentlyContinue | Out-File -FilePath $logFile -Append -Encoding utf8; Remove-Item $stdout -Force -ErrorAction SilentlyContinue }
    if (Test-Path $stderr) { Get-Content $stderr -ErrorAction SilentlyContinue | Out-File -FilePath $logFile -Append -Encoding utf8; Remove-Item $stderr -Force -ErrorAction SilentlyContinue }
} catch {
    "[$ts] ERRO: $_" | Out-File -FilePath $logFile -Append -Encoding utf8
}
