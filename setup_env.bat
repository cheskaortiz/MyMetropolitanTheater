# setup_env.bat (Windows)
@echo off
echo Setting up Python virtual environment...

REM Create virtual environment
python -m venv .venv

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install requirements
pip install -r requirements.txt

echo Setup complete! Activate the environment with: .venv\Scripts\activate