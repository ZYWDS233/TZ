@echo off
python test_script.py
if %errorlevel% neq 0 (
    echo Error: Script failed
) else (
    echo Script executed successfully
)
dir /b
pause
