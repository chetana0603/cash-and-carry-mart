"""
Customer controller - handles business logic for customers
"""
from utils.database import get_db_connection
from utils.validators import validate_required, validate_email, validate_phone, sanitize_input

def get_all_customers():
    """Get all customers"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM customer ORDER BY customer_id DESC")
        customers = cursor.fetchall()
        cursor.close()
        return customers, None
    except Exception as e:
        return None, str(e)
    finally:
        if conn and conn.is_connected():
            conn.close()

def get_customer_by_id(customer_id):
    """Get customer by ID"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM customer WHERE customer_id = %s", (customer_id,))
        customer = cursor.fetchone()
        cursor.close()
        if not customer:
            return None, "Customer not found"
        return customer, None
    except Exception as e:
        return None, str(e)
    finally:
        if conn and conn.is_connected():
            conn.close()

def create_customer(data):
    """Create customer using stored procedure"""
    conn = None
    try:
        # Validate required fields
        is_valid, error = validate_required(data, ['first_name', 'phone', 'email', 'address'])
        if not is_valid:
            return None, error
        
        # Validate email and phone
        if not validate_email(data['email']):
            return None, "Invalid email format"
        if not validate_phone(data['phone']):
            return None, "Invalid phone number (must be 10 digits)"
        
        # Sanitize input
        data = sanitize_input(data)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Call stored procedure
        cursor.callproc('sp_create_customer', [
            data.get('first_name', ''),
            data.get('middle_name'),
            data.get('last_name'),
            data.get('phone'),
            data.get('email'),
            data.get('address'),
            0  # OUT parameter
        ])
        
        # Get the output parameter
        for result in cursor.stored_results():
            pass
        
        # Get the last insert ID
        cursor.execute("SELECT LAST_INSERT_ID() as customer_id")
        result = cursor.fetchone()
        customer_id = result[0] if result else None
        
        conn.commit()
        cursor.close()
        
        if customer_id:
            return get_customer_by_id(customer_id)
        return None, "Failed to create customer"
        
    except Exception as e:
        if conn:
            conn.rollback()
        return None, str(e)
    finally:
        if conn and conn.is_connected():
            conn.close()

def update_customer(customer_id, data):
    """Update customer using stored procedure"""
    conn = None
    try:
        # Validate required fields
        is_valid, error = validate_required(data, ['first_name', 'phone', 'email', 'address'])
        if not is_valid:
            return None, error
        
        # Validate email and phone
        if not validate_email(data['email']):
            return None, "Invalid email format"
        if not validate_phone(data['phone']):
            return None, "Invalid phone number (must be 10 digits)"
        
        # Sanitize input
        data = sanitize_input(data)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Call stored procedure
        cursor.callproc('sp_update_customer', [
            customer_id,
            data.get('first_name', ''),
            data.get('middle_name'),
            data.get('last_name'),
            data.get('phone'),
            data.get('email'),
            data.get('address')
        ])
        
        conn.commit()
        cursor.close()
        
        return get_customer_by_id(customer_id)
        
    except Exception as e:
        if conn:
            conn.rollback()
        return None, str(e)
    finally:
        if conn and conn.is_connected():
            conn.close()

def delete_customer(customer_id):
    """Delete customer using stored procedure"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Call stored procedure
        cursor.callproc('sp_delete_customer', [customer_id])
        
        conn.commit()
        cursor.close()
        
        return True, None
        
    except Exception as e:
        if conn:
            conn.rollback()
        return False, str(e)
    finally:
        if conn and conn.is_connected():
            conn.close()

