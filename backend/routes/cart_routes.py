"""Cart routes"""
from flask import Blueprint, request, jsonify
from utils.auth import jwt_required, employee_or_admin_required
from controllers.cart_controller import (
    get_cart_by_customer, add_to_cart, update_cart_item, remove_from_cart, clear_cart
)

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/customer/<int:customer_id>', methods=['GET'])
@jwt_required()
def get_cart(customer_id):
    """Get cart items for a customer"""
    try:
        items, error = get_cart_by_customer(customer_id)
        if error:
            return jsonify({'message': error, 'error': 'database_error'}), 500
        return jsonify({'cart': items}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@cart_bp.route('', methods=['POST'])
@employee_or_admin_required
def add_cart_item():
    """Add item to cart"""
    try:
        data = request.get_json()
        result, error = add_to_cart(data)
        if error:
            return jsonify({'message': error, 'error': 'validation_error'}), 400
        return jsonify({'message': 'Item added to cart', 'result': result}), 201
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@cart_bp.route('/<int:cart_id>', methods=['PUT'])
@employee_or_admin_required
def update_cart(cart_id):
    """Update cart item quantity"""
    try:
        data = request.get_json()
        result, error = update_cart_item(cart_id, data)
        if error:
            return jsonify({'message': error, 'error': 'validation_error'}), 400
        return jsonify({'message': 'Cart item updated', 'result': result}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@cart_bp.route('/<int:cart_id>', methods=['DELETE'])
@employee_or_admin_required
def remove_cart_item(cart_id):
    """Remove item from cart"""
    try:
        success, error = remove_from_cart(cart_id)
        if error:
            return jsonify({'message': error, 'error': 'database_error'}), 500
        return jsonify({'message': 'Item removed from cart'}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@cart_bp.route('/customer/<int:customer_id>', methods=['DELETE'])
@employee_or_admin_required
def clear_customer_cart(customer_id):
    """Clear all items from customer's cart"""
    try:
        success, error = clear_cart(customer_id)
        if error:
            return jsonify({'message': error, 'error': 'database_error'}), 500
        return jsonify({'message': 'Cart cleared successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

