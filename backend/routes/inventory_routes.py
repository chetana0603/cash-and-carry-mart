"""Inventory routes"""
from flask import Blueprint, request, jsonify
from utils.auth import jwt_required, admin_required, employee_or_admin_required
from controllers.inventory_controller import (
    get_all_inventory, get_inventory_by_id, create_inventory, 
    update_inventory, delete_inventory, get_low_stock_items
)

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('', methods=['GET'])
@jwt_required()
def get_inventory():
    """Get all inventory records"""
    try:
        inventory, error = get_all_inventory()
        if error:
            return jsonify({'message': error, 'error': 'database_error'}), 500
        return jsonify({'inventory': inventory}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@inventory_bp.route('/low-stock', methods=['GET'])
@jwt_required()
def get_low_stock():
    """Get low stock items"""
    try:
        threshold = request.args.get('threshold', 10, type=int)
        items, error = get_low_stock_items(threshold)
        if error:
            return jsonify({'message': error, 'error': 'database_error'}), 500
        return jsonify({'items': items}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@inventory_bp.route('/<int:inventory_id>', methods=['GET'])
@jwt_required()
def get_inventory_item(inventory_id):
    """Get inventory by ID"""
    try:
        inventory, error = get_inventory_by_id(inventory_id)
        if error:
            return jsonify({'message': error, 'error': 'not_found'}), 404
        return jsonify({'inventory': inventory}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@inventory_bp.route('', methods=['POST'])
@employee_or_admin_required
def add_inventory():
    """Create new inventory record"""
    try:
        data = request.get_json()
        inventory, error = create_inventory(data)
        if error:
            return jsonify({'message': error, 'error': 'validation_error'}), 400
        return jsonify({'message': 'Inventory record created successfully', 'inventory': inventory}), 201
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@inventory_bp.route('/<int:inventory_id>', methods=['PUT'])
@employee_or_admin_required
def update_inventory_route(inventory_id):
    """Update inventory"""
    try:
        data = request.get_json()
        inventory, error = update_inventory(inventory_id, data)
        if error:
            return jsonify({'message': error, 'error': 'validation_error'}), 400
        return jsonify({'message': 'Inventory updated successfully', 'inventory': inventory}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@inventory_bp.route('/<int:inventory_id>', methods=['DELETE'])
@employee_or_admin_required
def delete_inventory_route(inventory_id):
    """Delete inventory"""
    try:
        success, error = delete_inventory(inventory_id)
        if error:
            return jsonify({'message': error, 'error': 'database_error'}), 500
        return jsonify({'message': 'Inventory deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

