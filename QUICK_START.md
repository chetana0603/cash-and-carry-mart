# Quick Start Guide

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.8+ installed
- ✅ Node.js 16+ installed
- ✅ MySQL 8.0+ installed and running
- ✅ MySQL root password (or create a user with appropriate permissions)

## Step-by-Step Setup

### 1. Database Setup

Ensure MySQL is running and you have the root password (or create a user).

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
# Edit .env file with your MySQL credentials:
# MYSQL_HOST=localhost
# MYSQL_USER=root
# MYSQL_PASSWORD=your_password
# MYSQL_DATABASE=mini
# MYSQL_PORT=3306
# JWT_SECRET_KEY=your-secret-key

# Start the backend server
python app.py
```

The backend will:
- Automatically create the database if it doesn't exist
- Run the SQL file to create all tables, triggers, and stored procedures
- Create a default admin user (username: `admin`, password: `admin123`)

Backend should be running at: `http://localhost:5000`

### 3. Frontend Setup

Open a new terminal:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
# or
npm run dev
```

Frontend should be running at: `http://localhost:3000`

### 4. Access the Application

1. Open your browser and go to `http://localhost:3000`
2. Login with:
   - Username: `admin`
   - Password: `admin123`

## Troubleshooting

### Backend Issues

**MySQL Connection Error:**
- Verify MySQL is running: `mysql -u root -p`
- Check `.env` file has correct credentials
- Ensure MySQL port is correct (default: 3306)

**Database Creation Error:**
- Ensure MySQL user has CREATE DATABASE privileges
- Check if database `mini` already exists and drop it if needed

**Module Import Errors:**
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Frontend Issues

**Port Already in Use:**
- Change port in `vite.config.js` or kill the process using port 3000

**API Connection Errors:**
- Verify backend is running on port 5000
- Check CORS settings in `backend/app.py`
- Verify proxy configuration in `frontend/vite.config.js`

**Module Not Found:**
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again

## Testing the Application

1. **Login**: Use admin credentials to log in
2. **Dashboard**: View statistics and charts
3. **Add Customer**: Go to Customers → Add New
4. **Add Product**: Go to Products → Add New
5. **Add Inventory**: Go to Inventory → Add New
6. **Create Order**: 
   - Go to Cart
   - Select a customer
   - Add items to cart
   - Click Checkout
   - Fill in store and employee details
   - Create order

## Default Data

The SQL file includes sample data:
- 3 Customers
- 3 Stores
- 3 Employees
- 3 Categories
- 3 Suppliers
- 3 Products
- Inventory records

## Next Steps

- Create additional users via the Register endpoint (Admin only)
- Add more products, customers, and inventory
- Test the order creation and inventory updates
- Explore the dashboard analytics

## Production Deployment

Before deploying to production:

1. Change `JWT_SECRET_KEY` to a strong random string
2. Update MySQL credentials in `.env`
3. Set `debug=False` in `app.py`
4. Use environment variables for all sensitive data
5. Set up proper CORS origins
6. Use a production-grade WSGI server (e.g., Gunicorn)
7. Build frontend: `npm run build`
8. Serve frontend build with a web server (e.g., Nginx)

## Support

For issues or questions:
- Check the API documentation in `API_DOCUMENTATION.md`
- Review the README.md for detailed information
- Check console logs for error messages

