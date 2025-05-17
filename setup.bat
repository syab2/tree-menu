@echo off
:: Script for automatic configuration of Django project
:: Version 1.0
:: Author: Krylov Nikolay

echo #############################################
echo # Setting up a Django project               #
echo #############################################
echo.

:: Checking for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or added to PATH
    pause
    exit /b
)

:: Checking the Python version
for /f "tokens=2 delims= " %%A in ('python --version 2^>^&1') do set python_version=%%A
for /f "tokens=1,2 delims=." %%A in ("%python_version%") do (
    if %%A LSS 3 (
        echo ERROR: Python 3.8 or higher required
        pause
        exit /b
    )
    if %%A EQU 3 if %%B LSS 8 (
        echo ERROR: Python 3.8 or higher required
        pause
        exit /b
    )
)

:: Creating a virtual environment
echo Creating a virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b
)

:: Activation of the environment
echo Activation of the environment...
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b
)

:: Installing dependencies
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b
)

:: Applying migrations
echo Applying migrations...
cd testproject
python manage.py migrate
if %errorlevel% neq 0 (
    echo ERROR: Failed to run event
    pause
    exit /b
)

:: Create a superuser (optional)
set /p create_superuser="Create superuser? (y/n):"
if /i "%create_superuser%"=="y" (
    python manage.py createsuperuser
)

:: Запуск сервера
echo Launching development server...
start http://127.0.0.1:8000/
python manage.py runserver

pause
