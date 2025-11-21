"""
Cash & Carry Mart Management System - Flask Backend
Main application entry point
"""
import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from utils.database import init_database, db
from utils.auth import jwt
from routes.auth_routes import auth_bp
from routes.customer_routes import customer_bp
from routes.store_routes import store_bp
from routes.employee_routes import employee_bp
from routes.category_routes import category_bp
from routes.supplier_routes import supplier_bp
from routes.product_routes import product_bp
from routes.inventory_routes import inventory_bp
from routes.cart_routes import cart_bp
from routes.order_routes import order_bp
from routes.dashboard_routes import dashboard_bp

# Load environment variables
load_dotenv()

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400  # 24 hours
    
    # Database configuration
    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
    app.config['MYSQL_DATABASE'] = os.getenv('MYSQL_DATABASE', 'mini')
    app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT', 3306))
    
    # Enable CORS
    CORS(app, origins="*", supports_credentials=True)
    
    # Initialize JWT
    jwt.init_app(app)
    
    # Initialize database
    init_database(app)
    
    # Register teardown function to close database connections
    from utils.database import close_db_connection
    app.teardown_appcontext(close_db_connection)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(customer_bp, url_prefix='/api/customers')
    app.register_blueprint(store_bp, url_prefix='/api/stores')
    app.register_blueprint(employee_bp, url_prefix='/api/employees')
    app.register_blueprint(category_bp, url_prefix='/api/categories')
    app.register_blueprint(supplier_bp, url_prefix='/api/suppliers')
    app.register_blueprint(product_bp, url_prefix='/api/products')
    app.register_blueprint(inventory_bp, url_prefix='/api/inventory')
    app.register_blueprint(cart_bp, url_prefix='/api/cart')
    app.register_blueprint(order_bp, url_prefix='/api/orders')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    
    @app.route('/', methods=['GET'])
    def root():
        """Root endpoint"""
        return {
            'message': 'Cash & Carry Mart Management System API',
            'version': '1.0.0',
            'endpoints': {
                'health': '/api/health',
                'auth': '/api/auth',
                'customers': '/api/customers',
                'products': '/api/products',
                'orders': '/api/orders',
                'dashboard': '/api/dashboard'
            }
        }, 200
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return {'status': 'ok', 'message': 'Cash & Carry Mart API is running'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

