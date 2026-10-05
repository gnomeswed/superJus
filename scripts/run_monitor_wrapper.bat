@echo off
setlocal enabledelayedexpansion
for %%I in ("%~dp0..") do set "ROOT=%%~fI"
set "PYTHONIOENCODING=utf-8"
if not defined DATAJUD_API_KEY if exist "%ROOT%\.env" for /f "usebackq tokens=1,* delims==" %%a in ("%ROOT%\.env") do if /I "%%a"=="DATAJUD_API_KEY" set "DATAJUD_API_KEY=%%b"
set LOGDIR=%ROOT%\temp_logs_e_resultados
if not exist "%LOGDIR%" mkdir "%LOGDIR%" 2>nul
set _ts=%date:~6,4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set _ts=%_ts: =0%
set LOG=%LOGDIR%\monitor_%_ts%.log
set PY=C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe
if not exist "%PY%" set PY=python
echo [%_ts%] Iniciando monitor... >> "%LOG%"
"%PY%" "%ROOT%\scripts\telegram_monitor_julio.py" >> "%LOG%" 2>&1
echo [%_ts%] concluido (exit %errorlevel%) >> "%LOG%"
exit /b 0
