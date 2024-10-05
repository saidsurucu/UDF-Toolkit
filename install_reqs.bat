@echo off
:: This script installs the packages listed in requirements.txt

REM Check if requirements file exists
IF NOT EXIST requirements.txt (
    echo Requirements file not found!
    exit /b 1
)

REM Install the packages using pip
pip install -r requirements.txt

REM Check if the installation was successful
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to install some packages.
    exit /b 1
)

echo Packages installed successfully.
pause