@echo off
:: Скрипт для автоматической настройки Django-проекта
:: Версия 1.0
:: Автор: Ваше Имя

echo #############################################
echo # Настройка Django-проекта                  #
echo #############################################
echo.

:: Проверка наличия Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ОШИБКА: Python не установлен или не добавлен в PATH
    pause
    exit /b
)

:: Проверка версии Python
for /f "tokens=2 delims= " %%A in ('python --version 2^>^&1') do set python_version=%%A
for /f "tokens=1,2 delims=." %%A in ("%python_version%") do (
    if %%A LSS 3 (
        echo ОШИБКА: Требуется Python 3.8 или выше
        pause
        exit /b
    )
    if %%A EQU 3 if %%B LSS 8 (
        echo ОШИБКА: Требуется Python 3.8 или выше
        pause
        exit /b
    )
)

:: Создание виртуального окружения
echo Создание виртуального окружения...
python -m venv venv
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось создать виртуальное окружение
    pause
    exit /b
)

:: Активация окружения
echo Активация виртуального окружения...
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось активировать виртуальное окружение
    pause
    exit /b
)

:: Установка зависимостей
echo Установка зависимостей...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось установить зависимости
    pause
    exit /b
)

:: Применение миграций
echo Применение миграций...
python manage.py migrate
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось применить миграции
    pause
    exit /b
)

:: Создание суперпользователя (опционально)
set /p create_superuser="Создать суперпользователя? (y/n): "
if /i "%create_superuser%"=="y" (
    python manage.py createsuperuser
)

:: Запуск сервера
echo Запуск сервера разработки...
start http://127.0.0.1:8000/
python manage.py runserver

pause