"""Supplier controller"""
from utils.database import get_db_connection
from utils.validators import validate_required, sanitize_input

def get_all_suppliers():
    """Get all suppliers"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM supplier ORDER BY supplier_id DESC")
        suppliers = cursor.fetchall()
        cursor.close()
        return suppliers, None
    except Exception as e:
        return None, str(e)

def get_supplier_by_id(supplier_id):
    """Get supplier by ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM supplier WHERE supplier_id = %s", (supplier_id,))
        supplier = cursor.fetchone()
        cursor.close()
        if not supplier:
            return None, "Supplier not found"
        return supplier, None
    except Exception as e:
        return None, str(e)

def create_supplier(data):
    """Create supplier"""
    try:
        is_valid, error = validate_required(data, ['name'])
        if not is_valid:
            return None, error
        
        data = sanitize_input(data)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO supplier (name, contact, address) VALUES (%s, %s, %s)",
                      (data['name'], data.get('contact'), data.get('address')))
        supplier_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        
        return get_supplier_by_id(supplier_id)
    except Exception as e:
        return None, str(e)

def update_supplier(supplier_id, data):
    """Update supplier"""
    try:
        data = sanitize_input(data)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE supplier SET name = %s, contact = %s, address = %s WHERE supplier_id = %s",
                      (data.get('name'), data.get('contact'), data.get('address'), supplier_id))
        conn.commit()
        cursor.close()
        
        return get_supplier_by_id(supplier_id)
    except Exception as e:
        return None, str(e)

def delete_supplier(supplier_id):
    """Delete supplier"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM supplier WHERE supplier_id = %s", (supplier_id,))
        conn.commit()
        cursor.close()
        return True, None
    except Exception as e:
        return False, str(e)

