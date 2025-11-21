"""
Customer routes
"""
from flask import Blueprint, request, jsonify
from utils.auth import jwt_required, admin_required, employee_or_admin_required
from controllers.customer_controller import (
    get_all_customers, get_customer_by_id, create_customer, update_customer, delete_customer
)

customer_bp = Blueprint('customers', __name__)

@customer_bp.route('', methods=['GET'])
@jwt_required()
def get_customers():
    """Get all customers"""
    try:
        customers, error = get_all_customers()
        if error:
            return jsonify({'message': error, 'error': 'database_error'}), 500
        return jsonify({'customers': customers}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@customer_bp.route('/<int:customer_id>', methods=['GET'])
@jwt_required()
def get_customer(customer_id):
    """Get customer by ID"""
    try:
        customer, error = get_customer_by_id(customer_id)
        if error:
            return jsonify({'message': error, 'error': 'not_found'}), 404
        return jsonify({'customer': customer}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@customer_bp.route('', methods=['POST'])
@employee_or_admin_required
def add_customer():
    """Create new customer"""
    try:
        data = request.get_json()
        customer, error = create_customer(data)
        if error:
            return jsonify({'message': error, 'error': 'validation_error'}), 400
        return jsonify({'message': 'Customer created successfully', 'customer': customer}), 201
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@customer_bp.route('/<int:customer_id>', methods=['PUT'])
@employee_or_admin_required
def update_customer_route(customer_id):
    """Update customer"""
    try:
        data = request.get_json()
        customer, error = update_customer(customer_id, data)
        if error:
            return jsonify({'message': error, 'error': 'validation_error'}), 400
        return jsonify({'message': 'Customer updated successfully', 'customer': customer}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@customer_bp.route('/<int:customer_id>', methods=['DELETE'])
@employee_or_admin_required
def delete_customer_route(customer_id):
    """Delete customer"""
    try:
        success, error = delete_customer(customer_id)
        if error:
            return jsonify({'message': error, 'error': 'database_error'}), 500
        return jsonify({'message': 'Customer deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

