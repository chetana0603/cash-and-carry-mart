"""Employee routes"""
from flask import Blueprint, request, jsonify
from utils.auth import jwt_required, admin_required, employee_or_admin_required
from controllers.employee_controller import (
    get_all_employees, get_employee_by_id, create_employee, update_employee, delete_employee
)

employee_bp = Blueprint('employees', __name__)

@employee_bp.route('', methods=['GET'])
@jwt_required()
def get_employees():
    """Get all employees"""
    try:
        employees, error = get_all_employees()
        if error:
            return jsonify({'message': error, 'error': 'database_error'}), 500
        return jsonify({'employees': employees}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@employee_bp.route('/<int:employee_id>', methods=['GET'])
@jwt_required()
def get_employee(employee_id):
    """Get employee by ID"""
    try:
        employee, error = get_employee_by_id(employee_id)
        if error:
            return jsonify({'message': error, 'error': 'not_found'}), 404
        return jsonify({'employee': employee}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@employee_bp.route('', methods=['POST'])
@employee_or_admin_required
def add_employee():
    """Create new employee"""
    try:
        data = request.get_json()
        employee, error = create_employee(data)
        if error:
            return jsonify({'message': error, 'error': 'validation_error'}), 400
        return jsonify({'message': 'Employee created successfully', 'employee': employee}), 201
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@employee_bp.route('/<int:employee_id>', methods=['PUT'])
@employee_or_admin_required
def update_employee_route(employee_id):
    """Update employee"""
    try:
        data = request.get_json()
        employee, error = update_employee(employee_id, data)
        if error:
            return jsonify({'message': error, 'error': 'validation_error'}), 400
        return jsonify({'message': 'Employee updated successfully', 'employee': employee}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@employee_bp.route('/<int:employee_id>', methods=['DELETE'])
@employee_or_admin_required
def delete_employee_route(employee_id):
    """Delete employee"""
    try:
        success, error = delete_employee(employee_id)
        if error:
            return jsonify({'message': error, 'error': 'database_error'}), 500
        return jsonify({'message': 'Employee deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

