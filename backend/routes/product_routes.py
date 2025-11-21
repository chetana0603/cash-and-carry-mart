"""Product routes"""
from flask import Blueprint, request, jsonify
from utils.auth import jwt_required, admin_required, employee_or_admin_required
from controllers.product_controller import (
    get_all_products, get_product_by_id, create_product, update_product, delete_product
)

product_bp = Blueprint('products', __name__)

@product_bp.route('', methods=['GET'])
@jwt_required()
def get_products():
    """Get all products"""
    try:
        products, error = get_all_products()
        if error:
            return jsonify({'message': error, 'error': 'database_error'}), 500
        return jsonify({'products': products}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@product_bp.route('/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    """Get product by ID"""
    try:
        product, error = get_product_by_id(product_id)
        if error:
            return jsonify({'message': error, 'error': 'not_found'}), 404
        return jsonify({'product': product}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@product_bp.route('', methods=['POST'])
@employee_or_admin_required
def add_product():
    """Create new product"""
    try:
        data = request.get_json()
        product, error = create_product(data)
        if error:
            return jsonify({'message': error, 'error': 'validation_error'}), 400
        return jsonify({'message': 'Product created successfully', 'product': product}), 201
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@product_bp.route('/<int:product_id>', methods=['PUT'])
@employee_or_admin_required
def update_product_route(product_id):
    """Update product"""
    try:
        data = request.get_json()
        product, error = update_product(product_id, data)
        if error:
            return jsonify({'message': error, 'error': 'validation_error'}), 400
        return jsonify({'message': 'Product updated successfully', 'product': product}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@product_bp.route('/<int:product_id>', methods=['DELETE'])
@employee_or_admin_required
def delete_product_route(product_id):
    """Delete product"""
    try:
        success, error = delete_product(product_id)
        if error:
            return jsonify({'message': error, 'error': 'database_error'}), 500
        return jsonify({'message': 'Product deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

