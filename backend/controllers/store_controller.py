"""Store controller"""
from utils.database import get_db_connection
from utils.validators import validate_required, sanitize_input

def get_all_stores():
    """Get all stores"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM store ORDER BY store_id DESC")
        stores = cursor.fetchall()
        cursor.close()
        return stores, None
    except Exception as e:
        return None, str(e)

def get_store_by_id(store_id):
    """Get store by ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM store WHERE store_id = %s", (store_id,))
        store = cursor.fetchone()
        cursor.close()
        if not store:
            return None, "Store not found"
        return store, None
    except Exception as e:
        return None, str(e)

def create_store(data):
    """Create store"""
    try:
        is_valid, error = validate_required(data, ['name', 'location'])
        if not is_valid:
            return None, error
        
        data = sanitize_input(data)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO store (name, location) VALUES (%s, %s)", 
                      (data['name'], data['location']))
        store_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        
        return get_store_by_id(store_id)
    except Exception as e:
        return None, str(e)

def update_store(store_id, data):
    """Update store"""
    try:
        is_valid, error = validate_required(data, ['name', 'location'])
        if not is_valid:
            return None, error
        
        data = sanitize_input(data)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE store SET name = %s, location = %s WHERE store_id = %s",
                      (data['name'], data['location'], store_id))
        conn.commit()
        cursor.close()
        
        return get_store_by_id(store_id)
    except Exception as e:
        return None, str(e)

def delete_store(store_id):
    """Delete store"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM store WHERE store_id = %s", (store_id,))
        conn.commit()
        cursor.close()
        return True, None
    except Exception as e:
        return False, str(e)

