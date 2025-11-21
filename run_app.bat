@echo off
REM Run MovieExplorer using venv python and keep the console open so you can see errors
cd /d "%~dp0"
".venv\Scripts\python.exe" main.py
if %ERRORLEVEL% neq 0 pause
