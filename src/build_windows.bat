@echo off

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Installing Python...
    choco install python3.12 --yes  REM Adjust Python version if needed
)

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo pip is not installed. Installing pip...
    python -m ensurepip
)

REM Check if virtualenv is installed
virtualenv --version >nul 2>&1
if errorlevel 1 (
    echo virtualenv is not installed. Installing virtualenv...
    pip install virtualenv
)

REM Create and activate virtual environment
echo Creating and activating virtual environment...
if not exist myenv (
    virtualenv myenv
)
call myenv\Scripts\activate

REM Install dependencies from requirements.txt
echo Installing dependencies...
pip install -r requirements.txt

REM Install Nuitka
echo Installing Nuitka...
pip install nuitka

REM Build the Python application using Nuitka
echo Building application with Nuitka...
python -m nuitka ^
    --windows-console-mode=disable ^
    --standalone ^
    --windows-icon-from-ico=windows.ico ^
    PS5-Toolbox.py

REM Deactivate virtual environment
echo Build completed.
deactivate
