# 🛒 Cash & Carry Mart Management System

A comprehensive full-stack web application for managing retail cash and carry operations with real-time inventory tracking, order processing, and analytics dashboard.

![MySQL](https://img.shields.io/badge/MySQL-8.0+-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8+-green.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-lightgrey.svg)
![React](https://img.shields.io/badge/React-18.2.0-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Database Design](#database-design)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Team](#team)
- [Documentation](#documentation)
- [License](#license)

## 🎯 Overview

The Cash & Carry Mart Management System is a database-driven web application designed to streamline retail operations. It provides complete business workflow management from customer registration to order fulfillment, with automated inventory tracking and real-time analytics.

**Key Highlights:**
- 🔐 JWT-based authentication with role-based access control
- 📊 Real-time analytics dashboard with interactive charts
- 🛍️ Shopping cart and order processing system
- 📦 Multi-store inventory management
- 🔄 Automated inventory updates using database triggers
- 📈 Business intelligence and reporting

## ✨ Features

### Core Functionality
- **Customer Management** - Complete CRUD operations with validation
- **Product Catalog** - Organized by categories and suppliers
- **Inventory Tracking** - Real-time stock levels across multiple stores
- **Order Processing** - Automated order creation with inventory deduction
- **Shopping Cart** - Persistent cart with checkout functionality
- **Employee Management** - Staff records with store assignments
- **Analytics Dashboard** - Revenue metrics, best sellers, and trends

### Database Features
- **10 Triggers** - Automated calculations and validations
- **7 Stored Procedures** - Complex transactional operations
- **1 Function** - Order total calculation
- **Audit Trail** - Order status change logging
- **Data Integrity** - Foreign keys, constraints, and validations

### Security
- JWT token-based authentication
- Password hashing with werkzeug
- Role-based access control (Admin/Employee)
- Protected API endpoints
- Input validation and sanitization

## 🛠️ Tech Stack

### Backend
- **Framework:** Flask 3.0.0
- **Database:** MySQL 8.0+
- **Authentication:** Flask-JWT-Extended 4.6.0
- **Database Connector:** MySQL Connector Python 8.2.0
- **Security:** Werkzeug 3.0.1

### Frontend
- **Library:** React 18.2.0
- **Build Tool:** Vite 5.4.21
- **Routing:** React Router DOM 6.x
- **HTTP Client:** Axios 1.6.x
- **Charts:** Recharts 2.x
- **Notifications:** React Toastify 9.x

### Database
- **RDBMS:** MySQL 8.0+
- **Design:** Normalized to 3NF
- **Objects:** 13 Tables, 10 Triggers, 7 Procedures, 1 Function

## 🗄️ Database Design

### Entity Relationship Diagram

The system includes 13 tables with comprehensive relationships:

**Core Entities:**
- Customer, Store, Employee, User
- Product, Category, Supplier
- Inventory, Cart, Orders, Order_Item
- Payment, Order_Status_Log (Audit)

**Key Relationships:**
- One customer → Many orders
- One store → Many employees, inventory records
- One product → Many inventory records (multi-store)
- One order → Many order items
- Automated cart clearing on order creation

### Database Objects

**Triggers (10):**
1. Order total auto-calculation (INSERT/UPDATE/DELETE)
2. Inventory validation (prevent negative stock)
3. Product price validation
4. Cart auto-clearing after order
5. Order status change logging
6. Product deletion prevention with inventory
7. Employee salary validation

**Stored Procedures (7):**
- Customer CRUD (Create, Update, Delete)
- Product CRUD (Create, Update, Delete)
- Order Creation (Transactional with inventory management)

**Function (1):**
- `fn_order_total()` - Calculate order total from items

For detailed schema, see [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md)

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- MySQL 8.0 or higher
- Git

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/cash-carry-mart.git
cd cash-carry-mart
```

### Step 2: Database Setup

1. Start MySQL server
2. The application will automatically create the database on first run
3. Or manually run the schema:

```bash
mysql -u root -p < database/mini_database_schema.sql
```

### Step 3: Backend Setup

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
# Copy .env.example to .env and update with your MySQL credentials
```

**Configure `.env` file:**
```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=mini
MYSQL_PORT=3306
JWT_SECRET_KEY=your-secret-key-change-in-production
```

**Start backend server:**
```bash
python app.py
```

Backend will run at: `http://localhost:5000`

### Step 4: Frontend Setup

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run at: `http://localhost:3000`

## 📖 Usage

### Default Login Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`
- Access: Full CRUD operations on all entities

### Quick Start Guide

1. **Login** - Use admin credentials to access the system
2. **Dashboard** - View analytics and business metrics
3. **Add Products** - Navigate to Products → Add New
4. **Add Inventory** - Go to Inventory → Add stock for stores
5. **Create Order** - Use Cart → Add items → Checkout

For detailed instructions, see [QUICK_START.md](QUICK_START.md)

## 📡 API Documentation

### Authentication Endpoints

```
POST /api/auth/login          - User login
POST /api/auth/register       - User registration (Admin only)
```

### Resource Endpoints

All resources follow RESTful conventions:

```
GET    /api/{resource}        - Get all
GET    /api/{resource}/:id    - Get by ID
POST   /api/{resource}        - Create new
PUT    /api/{resource}/:id    - Update
DELETE /api/{resource}/:id    - Delete
```

**Resources:** customers, products, orders, employees, stores, suppliers, categories, inventory, cart

### Dashboard Endpoints

```
GET /api/dashboard/stats              - Overall statistics
GET /api/dashboard/best-selling       - Top products
GET /api/dashboard/recent-orders      - Recent orders
GET /api/inventory/low-stock          - Low stock items
```

For complete API documentation, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

## 📁 Project Structure

```
cash-carry-mart/
├── backend/                    # Flask backend
│   ├── app.py                 # Main application
│   ├── controllers/           # Business logic
│   ├── routes/                # API endpoints
│   ├── utils/                 # Utilities (DB, auth, validators)
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables
│
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # Reusable components
│   │   ├── pages/             # Page components
│   │   ├── context/           # React Context
│   │   ├── services/          # API integration
│   │   └── App.jsx            # Main app component
│   ├── package.json           # Node dependencies
│   └── vite.config.js         # Vite configuration
│
├── database/                   # Database scripts
│   ├── mini_database_schema.sql    # Schema only
│   └── mini_database.sql           # Schema + sample data
│
├── docs/                       # Documentation
│   ├── PROJECT_REPORT.md      # Comprehensive project report
│   ├── DATABASE_SCHEMA.md     # Database documentation
│   ├── TRIGGERS_DOCUMENTATION.md   # Trigger details
│   └── API_DOCUMENTATION.md   # API reference
│
├── ALL_SQL_QUERIES.sql        # All SQL queries used
├── QUICK_START.md             # Quick setup guide
└── README.md                  # This file
```

## 👥 Team

**Project Team:**
- **Chetana Vijayakumar** - SRN: PES1UG23CS162
- **Chetana K** - SRN: PES1UG23CS164

**Course:** Database Management Systems (DBMS)  
**Institution:** PES University  
**Academic Year:** 2023-2024

## 📚 Documentation

Comprehensive documentation is available in the following files:

- **[PROJECT_REPORT.md](PROJECT_REPORT.md)** - Complete project report with all deliverables
- **[DATABASE_SCHEMA.md](DATABASE_SCHEMA.md)** - Detailed database design and schema
- **[TRIGGERS_DOCUMENTATION.md](TRIGGERS_DOCUMENTATION.md)** - All 10 triggers explained
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Complete API reference
- **[QUICK_START.md](QUICK_START.md)** - Quick setup and usage guide
- **[ALL_SQL_QUERIES.sql](ALL_SQL_QUERIES.sql)** - All SQL queries (DDL, DML, Triggers, Procedures)

## 🎓 Learning Outcomes

This project demonstrates:
- Database design and normalization (up to 3NF)
- SQL programming (Triggers, Procedures, Functions)
- Complex queries (Joins, Nested, Aggregates)
- Full-stack web development
- RESTful API design
- Authentication and authorization
- Transaction management
- Frontend-backend integration

## 🔧 Development

### Running Tests

```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
```

### Building for Production

```bash
# Frontend build
cd frontend
npm run build

# Backend (use production WSGI server)
pip install gunicorn
gunicorn -w 4 app:app
```

## 🐛 Known Issues

- None currently reported

## 🚀 Future Enhancements

- [ ] Payment gateway integration
- [ ] Email/SMS notifications
- [ ] Mobile application
- [ ] Advanced reporting with PDF export
- [ ] Barcode scanning
- [ ] Supplier portal
- [ ] Multi-language support
- [ ] Predictive analytics

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Course Instructor for guidance on database design
- PES University for the learning environment
- Open source community for excellent tools and frameworks

## 📞 Contact

For questions or feedback:
- Create an issue in this repository
- Contact team members via university email

---

**⭐ If you find this project useful, please consider giving it a star!**

---

*Built with ❤️ by Team Cash & Carry Mart*
