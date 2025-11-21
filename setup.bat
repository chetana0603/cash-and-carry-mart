@echo off
REM Cash & Carry Mart Management System - Setup Script for Windows

echo ==================================
echo Cash ^& Carry Mart Setup
echo ==================================
echo.

REM Check Python
echo Checking prerequisites...
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)
echo + Python found

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo X Node.js is not installed. Please install Node.js 16 or higher.
    pause
    exit /b 1
)
echo + Node.js found

REM Check MySQL
mysql --version >nul 2>&1
if errorlevel 1 (
    echo X MySQL is not installed. Please install MySQL 8.0 or higher.
    pause
    exit /b 1
)
echo + MySQL found

echo.
echo ==================================
echo Setting up Backend...
echo ==================================

cd backend

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Check if .env exists
if not exist .env (
    echo.
    echo ! .env file not found!
    echo Please create a .env file with the following content:
    echo.
    echo MYSQL_HOST=localhost
    echo MYSQL_USER=root
    echo MYSQL_PASSWORD=your_password
    echo MYSQL_DATABASE=mini
    echo MYSQL_PORT=3306
    echo JWT_SECRET_KEY=your-secret-key-change-in-production
    echo.
    pause
)

cd ..

echo.
echo ==================================
echo Setting up Frontend...
echo ==================================

cd frontend

REM Install Node dependencies
echo Installing Node.js dependencies...
call npm install

cd ..

echo.
echo ==================================
echo Setup Complete!
echo ==================================
echo.
echo To start the application:
echo.
echo 1. Start Backend (Terminal 1):
echo    cd backend
echo    venv\Scripts\activate
echo    python app.py
echo.
echo 2. Start Frontend (Terminal 2):
echo    cd frontend
echo    npm run dev
echo.
echo 3. Access the application:
echo    Frontend: http://localhost:3000
echo    Backend:  http://localhost:5000
echo.
echo Default Login:
echo    Username: admin
echo    Password: admin123
echo.
echo ==================================
pause
