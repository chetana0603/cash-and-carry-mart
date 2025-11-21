#!/bin/bash

# Cash & Carry Mart Management System - Setup Script
# This script automates the setup process for Unix/Linux/Mac systems

echo "=================================="
echo "Cash & Carry Mart Setup"
echo "=================================="
echo ""

# Check prerequisites
echo "Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi
echo "✅ Python 3 found: $(python3 --version)"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi
echo "✅ Node.js found: $(node --version)"

# Check MySQL
if ! command -v mysql &> /dev/null; then
    echo "❌ MySQL is not installed. Please install MySQL 8.0 or higher."
    exit 1
fi
echo "✅ MySQL found"

echo ""
echo "=================================="
echo "Setting up Backend..."
echo "=================================="

cd backend

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f .env ]; then
    echo ""
    echo "⚠️  .env file not found!"
    echo "Please create a .env file with the following content:"
    echo ""
    echo "MYSQL_HOST=localhost"
    echo "MYSQL_USER=root"
    echo "MYSQL_PASSWORD=your_password"
    echo "MYSQL_DATABASE=mini"
    echo "MYSQL_PORT=3306"
    echo "JWT_SECRET_KEY=your-secret-key-change-in-production"
    echo ""
    read -p "Press Enter after creating .env file..."
fi

cd ..

echo ""
echo "=================================="
echo "Setting up Frontend..."
echo "=================================="

cd frontend

# Install Node dependencies
echo "Installing Node.js dependencies..."
npm install

cd ..

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "To start the application:"
echo ""
echo "1. Start Backend (Terminal 1):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python app.py"
echo ""
echo "2. Start Frontend (Terminal 2):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "3. Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:5000"
echo ""
echo "Default Login:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "=================================="
