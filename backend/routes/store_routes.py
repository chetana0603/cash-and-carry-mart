"""Store routes"""
from flask import Blueprint, request, jsonify
from utils.auth import jwt_required, admin_required, employee_or_admin_required
from controllers.store_controller import (
    get_all_stores, get_store_by_id, create_store, update_store, delete_store
)

store_bp = Blueprint('stores', __name__)

@store_bp.route('', methods=['GET'])
@jwt_required()
def get_stores():
    """Get all stores"""
    try:
        stores, error = get_all_stores()
        if error:
            return jsonify({'message': error, 'error': 'database_error'}), 500
        return jsonify({'stores': stores}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@store_bp.route('/<int:store_id>', methods=['GET'])
@jwt_required()
def get_store(store_id):
    """Get store by ID"""
    try:
        store, error = get_store_by_id(store_id)
        if error:
            return jsonify({'message': error, 'error': 'not_found'}), 404
        return jsonify({'store': store}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@store_bp.route('', methods=['POST'])
@employee_or_admin_required
def add_store():
    """Create new store"""
    try:
        data = request.get_json()
        store, error = create_store(data)
        if error:
            return jsonify({'message': error, 'error': 'validation_error'}), 400
        return jsonify({'message': 'Store created successfully', 'store': store}), 201
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@store_bp.route('/<int:store_id>', methods=['PUT'])
@employee_or_admin_required
def update_store_route(store_id):
    """Update store"""
    try:
        data = request.get_json()
        store, error = update_store(store_id, data)
        if error:
            return jsonify({'message': error, 'error': 'validation_error'}), 400
        return jsonify({'message': 'Store updated successfully', 'store': store}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@store_bp.route('/<int:store_id>', methods=['DELETE'])
@employee_or_admin_required
def delete_store_route(store_id):
    """Delete store"""
    try:
        success, error = delete_store(store_id)
        if error:
            return jsonify({'message': error, 'error': 'database_error'}), 500
        return jsonify({'message': 'Store deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

