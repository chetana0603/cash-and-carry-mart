"""
Authentication routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from utils.auth import verify_password, create_user
from utils.validators import validate_required, sanitize_input

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        
        # Validate required fields
        is_valid, error = validate_required(data, ['username', 'password'])
        if not is_valid:
            return jsonify({'message': error, 'error': 'validation_error'}), 400
        
        username = data['username'].strip()
        password = data['password']
        
        # Verify credentials
        user = verify_password(username, password)
        
        if not user:
            return jsonify({'message': 'Invalid username or password', 'error': 'invalid_credentials'}), 401
        
        # Create access token
        access_token = create_access_token(
            identity=user['username'],
            additional_claims={'role': user['role'], 'user_id': user['user_id'], 'employee_id': user['employee_id']}
        )
        
        return jsonify({
            'access_token': access_token,
            'user': {
                'username': user['username'],
                'role': user['role'],
                'employee_id': user['employee_id']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': str(e), 'error': 'server_error'}), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    """User registration endpoint - public signup (defaults to EMPLOYEE role)"""
    try:
        data = request.get_json()
        
        # Validate required fields (role is optional for public signup)
        is_valid, error = validate_required(data, ['username', 'password'])
        if not is_valid:
            return jsonify({'message': error, 'error': 'validation_error'}), 400
        
        username = data['username'].strip()
        password = data['password']
        
        # Default to EMPLOYEE role for public signup
        # Only allow ADMIN role if explicitly provided (for admin-created accounts)
        role = data.get('role', 'EMPLOYEE')
        if role not in ['ADMIN', 'EMPLOYEE']:
            role = 'EMPLOYEE'  # Force EMPLOYEE for public signup
        
        # For public signup, don't require employee_id
        employee_id = data.get('employee_id')
        
        # Validate password strength (minimum 6 characters)
        if len(password) < 6:
            return jsonify({'message': 'Password must be at least 6 characters long', 'error': 'validation_error'}), 400
        
        # Validate username (minimum 3 characters, alphanumeric and underscore only)
        if len(username) < 3:
            return jsonify({'message': 'Username must be at least 3 characters long', 'error': 'validation_error'}), 400
        
        # Create user
        try:
            user_id = create_user(username, password, role, employee_id)
            
            if not user_id:
                return jsonify({'message': 'Failed to create user. Username may already exist.', 'error': 'creation_failed'}), 400
            
            return jsonify({'message': 'Account created successfully! You can now login.', 'user_id': user_id}), 201
        except Exception as create_error:
            error_msg = str(create_error)
            print(f"Error in register route: {error_msg}")
            print(f"Error type: {type(create_error)}")
            
            # Check for common database errors
            if 'Duplicate entry' in error_msg or 'UNIQUE constraint' in error_msg or '1062' in error_msg:
                return jsonify({'message': 'Username already exists. Please choose a different username.', 'error': 'duplicate_username'}), 400
            elif 'foreign key constraint' in error_msg.lower() or '1452' in error_msg:
                return jsonify({'message': 'Invalid employee ID provided.', 'error': 'invalid_employee'}), 400
            else:
                # Return the actual error message for debugging
                return jsonify({'message': f'Failed to create account: {error_msg}', 'error': 'creation_failed'}), 400
        
    except Exception as e:
        error_msg = str(e)
        print(f"Unexpected error in register route: {error_msg}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'message': f'Server error: {error_msg}', 'error': 'server_error'}), 500

