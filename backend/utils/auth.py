"""
Authentication utilities using JWT
"""
from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from werkzeug.security import check_password_hash, generate_password_hash
from utils.database import get_db_connection
import mysql.connector

jwt = JWTManager()

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({'message': 'Token has expired', 'error': 'token_expired'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'message': 'Invalid token', 'error': 'invalid_token'}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({'message': 'Authorization required', 'error': 'authorization_required'}), 401

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user = get_jwt_identity()
        claims = get_jwt()
        
        if claims.get('role') != 'ADMIN':
            return jsonify({'message': 'Admin access required', 'error': 'insufficient_permissions'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

def employee_or_admin_required(f):
    """Decorator to require employee or admin role"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user = get_jwt_identity()
        claims = get_jwt()
        
        if claims.get('role') not in ['ADMIN', 'EMPLOYEE']:
            return jsonify({'message': 'Employee or admin access required', 'error': 'insufficient_permissions'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

def verify_password(username, password):
    """Verify user credentials"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT user_id, username, password_hash, role, employee_id
            FROM user
            WHERE username = %s
        """, (username,))
        
        user = cursor.fetchone()
        cursor.close()
        
        if user and check_password_hash(user['password_hash'], password):
            return {
                'user_id': user['user_id'],
                'username': user['username'],
                'role': user['role'],
                'employee_id': user['employee_id']
            }
        
        return None
    except Exception as e:
        print(f"Error verifying password: {e}")
        return None

def create_user(username, password, role='EMPLOYEE', employee_id=None):
    """Create a new user"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        
        # Check if connection is still valid
        if not conn.is_connected():
            conn.reconnect()
        
        cursor = conn.cursor()
        
        password_hash = generate_password_hash(password)
        
        # Handle NULL employee_id properly - for public signup, employee_id should be NULL
        if employee_id is None or employee_id == '':
            cursor.execute("""
                INSERT INTO user (username, password_hash, role, employee_id)
                VALUES (%s, %s, %s, NULL)
            """, (username, password_hash, role))
        else:
            cursor.execute("""
                INSERT INTO user (username, password_hash, role, employee_id)
                VALUES (%s, %s, %s, %s)
            """, (username, password_hash, role, employee_id))
        
        conn.commit()
        user_id = cursor.lastrowid
        cursor.close()
        cursor = None
        
        return user_id
    except mysql.connector.Error as db_error:
        error_msg = str(db_error)
        error_code = db_error.errno
        print(f"Database error creating user: {error_msg} (Error code: {error_code})")
        
        # Rollback on error
        if conn and conn.is_connected():
            conn.rollback()
        
        # Raise with more specific error message
        raise Exception(f"Database error: {error_msg}")
    except Exception as e:
        error_msg = str(e)
        print(f"Error creating user: {error_msg}")
        
        # Rollback on error
        if conn and conn.is_connected():
            conn.rollback()
        
        raise Exception(f"Error creating user: {error_msg}")
    finally:
        # Clean up cursor if it wasn't closed
        if cursor:
            try:
                cursor.close()
            except:
                pass

