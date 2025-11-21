"""Category controller"""
from utils.database import get_db_connection
from utils.validators import validate_required, sanitize_input

def get_all_categories():
    """Get all categories"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM category ORDER BY category_id DESC")
        categories = cursor.fetchall()
        cursor.close()
        return categories, None
    except Exception as e:
        return None, str(e)

def get_category_by_id(category_id):
    """Get category by ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM category WHERE category_id = %s", (category_id,))
        category = cursor.fetchone()
        cursor.close()
        if not category:
            return None, "Category not found"
        return category, None
    except Exception as e:
        return None, str(e)

def create_category(data):
    """Create category"""
    try:
        is_valid, error = validate_required(data, ['name'])
        if not is_valid:
            return None, error
        
        data = sanitize_input(data)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO category (name) VALUES (%s)", (data['name'],))
        category_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        
        return get_category_by_id(category_id)
    except Exception as e:
        return None, str(e)

def update_category(category_id, data):
    """Update category"""
    try:
        is_valid, error = validate_required(data, ['name'])
        if not is_valid:
            return None, error
        
        data = sanitize_input(data)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE category SET name = %s WHERE category_id = %s",
                      (data['name'], category_id))
        conn.commit()
        cursor.close()
        
        return get_category_by_id(category_id)
    except Exception as e:
        return None, str(e)

def delete_category(category_id):
    """Delete category"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM category WHERE category_id = %s", (category_id,))
        conn.commit()
        cursor.close()
        return True, None
    except Exception as e:
        return False, str(e)

