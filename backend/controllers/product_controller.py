"""Product controller"""
from utils.database import get_db_connection
from utils.validators import validate_required, validate_positive_number, sanitize_input

def get_all_products():
    """Get all products"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.*, c.name as category_name, s.name as supplier_name
            FROM product p
            LEFT JOIN category c ON p.category_id = c.category_id
            LEFT JOIN supplier s ON p.supplier_id = s.supplier_id
            ORDER BY p.product_id DESC
        """)
        products = cursor.fetchall()
        cursor.close()
        return products, None
    except Exception as e:
        return None, str(e)

def get_product_by_id(product_id):
    """Get product by ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.*, c.name as category_name, s.name as supplier_name
            FROM product p
            LEFT JOIN category c ON p.category_id = c.category_id
            LEFT JOIN supplier s ON p.supplier_id = s.supplier_id
            WHERE p.product_id = %s
        """, (product_id,))
        product = cursor.fetchone()
        cursor.close()
        if not product:
            return None, "Product not found"
        return product, None
    except Exception as e:
        return None, str(e)

def create_product(data):
    """Create product using stored procedure"""
    try:
        is_valid, error = validate_required(data, ['name', 'price'])
        if not is_valid:
            return None, error
        
        is_valid, error = validate_positive_number(data['price'], 'Price')
        if not is_valid:
            return None, error
        
        data = sanitize_input(data)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.callproc('sp_create_product', [
            data['name'],
            data.get('description'),
            float(data['price']),
            data.get('availability', True),
            data.get('category_id'),
            data.get('supplier_id'),
            0  # OUT parameter
        ])
        
        for result in cursor.stored_results():
            pass
        
        cursor.execute("SELECT LAST_INSERT_ID() as product_id")
        result = cursor.fetchone()
        product_id = result[0] if result else None
        
        conn.commit()
        cursor.close()
        
        if product_id:
            return get_product_by_id(product_id)
        return None, "Failed to create product"
    except Exception as e:
        return None, str(e)

def update_product(product_id, data):
    """Update product using stored procedure"""
    try:
        is_valid, error = validate_required(data, ['name', 'price'])
        if not is_valid:
            return None, error
        
        is_valid, error = validate_positive_number(data['price'], 'Price')
        if not is_valid:
            return None, error
        
        data = sanitize_input(data)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.callproc('sp_update_product', [
            product_id,
            data['name'],
            data.get('description'),
            float(data['price']),
            data.get('availability', True),
            data.get('category_id'),
            data.get('supplier_id')
        ])
        
        conn.commit()
        cursor.close()
        
        return get_product_by_id(product_id)
    except Exception as e:
        return None, str(e)

def delete_product(product_id):
    """Delete product using stored procedure"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.callproc('sp_delete_product', [product_id])
        conn.commit()
        cursor.close()
        return True, None
    except Exception as e:
        return False, str(e)

