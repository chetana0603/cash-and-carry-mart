"""Category routes"""
from flask import Blueprint, request, jsonify
from utils.auth import jwt_required, admin_required, employee_or_admin_required
from controllers.category_controller import (
    get_all_categories, get_category_by_id, create_category, update_category, delete_category
)

category_bp = Blueprint('categories', __name__)

@category_bp.route('', methods=['GET'])
@jwt_required()
def get_categories():
    """Get all categories"""
    try:
        categories, error = get_all_categories()
        if error:
            return jsonify({'message': error, 'error': 'database_error'}), 500
        return jsonify({'categories': categories}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@category_bp.route('/<int:category_id>', methods=['GET'])
@jwt_required()
def get_category(category_id):
    """Get category by ID"""
    try:
        category, error = get_category_by_id(category_id)
        if error:
            return jsonify({'message': error, 'error': 'not_found'}), 404
        return jsonify({'category': category}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@category_bp.route('', methods=['POST'])
@employee_or_admin_required
def add_category():
    """Create new category"""
    try:
        data = request.get_json()
        category, error = create_category(data)
        if error:
            return jsonify({'message': error, 'error': 'validation_error'}), 400
        return jsonify({'message': 'Category created successfully', 'category': category}), 201
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@category_bp.route('/<int:category_id>', methods=['PUT'])
@admin_required
def update_category_route(category_id):
    """Update category"""
    try:
        data = request.get_json()
        category, error = update_category(category_id, data)
        if error:
            return jsonify({'message': error, 'error': 'validation_error'}), 400
        return jsonify({'message': 'Category updated successfully', 'category': category}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@category_bp.route('/<int:category_id>', methods=['DELETE'])
@admin_required
def delete_category_route(category_id):
    """Delete category"""
    try:
        success, error = delete_category(category_id)
        if error:
            return jsonify({'message': error, 'error': 'database_error'}), 500
        return jsonify({'message': 'Category deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

