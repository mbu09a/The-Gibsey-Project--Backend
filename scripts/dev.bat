@echo off
rem Windows helper for common dev workflows
if "%1"=="seed" (
    python -m scripts.seed %2 %3 %4
) else if "%1"=="test" (
    pytest -q
) else (
    echo usage: dev.bat [seed|test] [--force|--dry-run]
) 