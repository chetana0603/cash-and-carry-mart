"""Dashboard routes"""
from flask import Blueprint, request, jsonify
from utils.auth import jwt_required
from controllers.dashboard_controller import (
    get_dashboard_stats, get_best_selling_products, get_recent_orders, get_sales_by_date_range
)

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """Get dashboard statistics"""
    try:
        stats, error = get_dashboard_stats()
        if error:
            return jsonify({'message': error, 'error': 'database_error'}), 500
        return jsonify({'stats': stats}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@dashboard_bp.route('/best-selling', methods=['GET'])
@jwt_required()
def get_best_selling():
    """Get best selling products"""
    try:
        limit = request.args.get('limit', 10, type=int)
        products, error = get_best_selling_products(limit)
        if error:
            return jsonify({'message': error, 'error': 'database_error'}), 500
        return jsonify({'products': products}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@dashboard_bp.route('/recent-orders', methods=['GET'])
@jwt_required()
def get_recent():
    """Get recent orders"""
    try:
        limit = request.args.get('limit', 10, type=int)
        orders, error = get_recent_orders(limit)
        if error:
            return jsonify({'message': error, 'error': 'database_error'}), 500
        return jsonify({'orders': orders}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@dashboard_bp.route('/sales', methods=['GET'])
@jwt_required()
def get_sales():
    """Get sales data for date range"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not start_date or not end_date:
            return jsonify({'message': 'start_date and end_date are required', 'error': 'validation_error'}), 400
        
        sales, error = get_sales_by_date_range(start_date, end_date)
        if error:
            return jsonify({'message': error, 'error': 'database_error'}), 500
        return jsonify({'sales': sales}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

