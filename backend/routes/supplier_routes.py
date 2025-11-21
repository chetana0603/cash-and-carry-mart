"""Supplier routes"""
from flask import Blueprint, request, jsonify
from utils.auth import jwt_required, admin_required, employee_or_admin_required
from controllers.supplier_controller import (
    get_all_suppliers, get_supplier_by_id, create_supplier, update_supplier, delete_supplier
)

supplier_bp = Blueprint('suppliers', __name__)

@supplier_bp.route('', methods=['GET'])
@jwt_required()
def get_suppliers():
    """Get all suppliers"""
    try:
        suppliers, error = get_all_suppliers()
        if error:
            return jsonify({'message': error, 'error': 'database_error'}), 500
        return jsonify({'suppliers': suppliers}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@supplier_bp.route('/<int:supplier_id>', methods=['GET'])
@jwt_required()
def get_supplier(supplier_id):
    """Get supplier by ID"""
    try:
        supplier, error = get_supplier_by_id(supplier_id)
        if error:
            return jsonify({'message': error, 'error': 'not_found'}), 404
        return jsonify({'supplier': supplier}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@supplier_bp.route('', methods=['POST'])
@employee_or_admin_required
def add_supplier():
    """Create new supplier"""
    try:
        data = request.get_json()
        supplier, error = create_supplier(data)
        if error:
            return jsonify({'message': error, 'error': 'validation_error'}), 400
        return jsonify({'message': 'Supplier created successfully', 'supplier': supplier}), 201
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@supplier_bp.route('/<int:supplier_id>', methods=['PUT'])
@employee_or_admin_required
def update_supplier_route(supplier_id):
    """Update supplier"""
    try:
        data = request.get_json()
        supplier, error = update_supplier(supplier_id, data)
        if error:
            return jsonify({'message': error, 'error': 'validation_error'}), 400
        return jsonify({'message': 'Supplier updated successfully', 'supplier': supplier}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@supplier_bp.route('/<int:supplier_id>', methods=['DELETE'])
@employee_or_admin_required
def delete_supplier_route(supplier_id):
    """Delete supplier"""
    try:
        success, error = delete_supplier(supplier_id)
        if error:
            return jsonify({'message': error, 'error': 'database_error'}), 500
        return jsonify({'message': 'Supplier deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

