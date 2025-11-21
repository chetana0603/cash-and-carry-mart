"""Order routes"""
from flask import Blueprint, request, jsonify
from utils.auth import jwt_required, admin_required, employee_or_admin_required
from controllers.order_controller import (
    get_all_orders, get_order_by_id, create_order, update_order_status, delete_order
)

order_bp = Blueprint('orders', __name__)

@order_bp.route('', methods=['GET'])
@jwt_required()
def get_orders():
    """Get all orders"""
    try:
        orders, error = get_all_orders()
        if error:
            return jsonify({'message': error, 'error': 'database_error'}), 500
        return jsonify({'orders': orders}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@order_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """Get order by ID"""
    try:
        order, error = get_order_by_id(order_id)
        if error:
            return jsonify({'message': error, 'error': 'not_found'}), 404
        return jsonify({'order': order}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@order_bp.route('', methods=['POST'])
@employee_or_admin_required
def add_order():
    """Create new order"""
    try:
        data = request.get_json()
        order, error = create_order(data)
        if error:
            return jsonify({'message': error, 'error': 'validation_error'}), 400
        return jsonify({'message': 'Order created successfully', 'order': order}), 201
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@order_bp.route('/<int:order_id>/status', methods=['PUT'])
@admin_required
def update_status(order_id):
    """Update order status"""
    try:
        data = request.get_json()
        status = data.get('status')
        if not status:
            return jsonify({'message': 'Status is required', 'error': 'validation_error'}), 400
        
        order, error = update_order_status(order_id, status)
        if error:
            return jsonify({'message': error, 'error': 'validation_error'}), 400
        return jsonify({'message': 'Order status updated successfully', 'order': order}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@order_bp.route('/<int:order_id>', methods=['DELETE'])
@admin_required
def delete_order_route(order_id):
    """Delete order"""
    try:
        success, error = delete_order(order_id)
        if error:
            return jsonify({'message': error, 'error': 'database_error'}), 500
        return jsonify({'message': 'Order deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

