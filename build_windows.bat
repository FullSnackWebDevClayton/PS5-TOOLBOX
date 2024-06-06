@echo off
setlocal

REM Define paths
set PYTHON_VERSION=3.12.0
set VENV_DIR=myenvwin
set PYTHON_INSTALLER=python-%PYTHON_VERSION%-amd64.exe
set REQUIREMENTS_FILE=requirements.txt
set SETUP_SCRIPT=windows-setup.py

REM Download Python installer if not present
if not exist %PYTHON_INSTALLER% (
    echo Downloading Python %PYTHON_VERSION% installer...
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/%PYTHON_VERSION%/%PYTHON_INSTALLER% -OutFile %PYTHON_INSTALLER%"
)

REM Install Python silently
if not exist "%ProgramFiles%\Python%PYTHON_VERSION%" (
    echo Installing Python %PYTHON_VERSION%...
    %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1
)

REM Ensure pip is installed
python -m ensurepip --upgrade

REM Create virtual environment
if not exist %VENV_DIR% (
    echo Creating virtual environment...
    python -m venv %VENV_DIR%
)

REM Activate virtual environment
echo Activating virtual environment...
call %VENV_DIR%\Scripts\activate

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install required packages
if exist %REQUIREMENTS_FILE% (
    echo Installing dependencies from %REQUIREMENTS_FILE%...
    pip install -r %REQUIREMENTS_FILE%
) else (
    echo %REQUIREMENTS_FILE% not found. Ensure it is in the same directory as this script.
    exit /b 1
)

REM Run the setup script to build the MSI installer
if exist %SETUP_SCRIPT% (
    echo Running setup script...
    python %SETUP_SCRIPT% bdist_msi
) else (
    echo %SETUP_SCRIPT% not found. Ensure it is in the same directory as this script.
    exit /b 1
)

echo Build process completed.
endlocal
pause
