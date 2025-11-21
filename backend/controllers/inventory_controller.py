"""Inventory controller"""
from utils.database import get_db_connection
from utils.validators import validate_required, validate_positive_number, sanitize_input

def get_all_inventory():
    """Get all inventory records"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT i.*, p.name as product_name, s.name as store_name, s.location as store_location
            FROM inventory i
            JOIN product p ON i.product_id = p.product_id
            JOIN store s ON i.store_id = s.store_id
            ORDER BY i.inventory_id DESC
        """)
        inventory = cursor.fetchall()
        cursor.close()
        return inventory, None
    except Exception as e:
        return None, str(e)

def get_inventory_by_id(inventory_id):
    """Get inventory by ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT i.*, p.name as product_name, s.name as store_name, s.location as store_location
            FROM inventory i
            JOIN product p ON i.product_id = p.product_id
            JOIN store s ON i.store_id = s.store_id
            WHERE i.inventory_id = %s
        """, (inventory_id,))
        inventory = cursor.fetchone()
        cursor.close()
        if not inventory:
            return None, "Inventory not found"
        return inventory, None
    except Exception as e:
        return None, str(e)

def get_inventory_by_product_store(product_id, store_id):
    """Get inventory by product and store"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT i.*, p.name as product_name, s.name as store_name
            FROM inventory i
            JOIN product p ON i.product_id = p.product_id
            JOIN store s ON i.store_id = s.store_id
            WHERE i.product_id = %s AND i.store_id = %s
        """, (product_id, store_id))
        inventory = cursor.fetchone()
        cursor.close()
        return inventory, None
    except Exception as e:
        return None, str(e)

def create_inventory(data):
    """Create inventory record"""
    try:
        is_valid, error = validate_required(data, ['product_id', 'store_id', 'quantity_in_stock'])
        if not is_valid:
            return None, error
        
        is_valid, error = validate_positive_number(data['quantity_in_stock'], 'Quantity')
        if not is_valid:
            return None, error
        
        data = sanitize_input(data)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO inventory (product_id, store_id, quantity_in_stock)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE quantity_in_stock = quantity_in_stock + %s
        """, (data['product_id'], data['store_id'], data['quantity_in_stock'], data['quantity_in_stock']))
        inventory_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        
        return get_inventory_by_product_store(data['product_id'], data['store_id'])
    except Exception as e:
        return None, str(e)

def update_inventory(inventory_id, data):
    """Update inventory"""
    try:
        is_valid, error = validate_positive_number(data.get('quantity_in_stock', 0), 'Quantity')
        if not is_valid:
            return None, error
        
        data = sanitize_input(data)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE inventory 
            SET quantity_in_stock = %s
            WHERE inventory_id = %s
        """, (data.get('quantity_in_stock'), inventory_id))
        conn.commit()
        cursor.close()
        
        return get_inventory_by_id(inventory_id)
    except Exception as e:
        return None, str(e)

def delete_inventory(inventory_id):
    """Delete inventory"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventory WHERE inventory_id = %s", (inventory_id,))
        conn.commit()
        cursor.close()
        return True, None
    except Exception as e:
        return False, str(e)

def get_low_stock_items(threshold=10):
    """Get items with low stock"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT i.*, p.name as product_name, s.name as store_name
            FROM inventory i
            JOIN product p ON i.product_id = p.product_id
            JOIN store s ON i.store_id = s.store_id
            WHERE i.quantity_in_stock <= %s
            ORDER BY i.quantity_in_stock ASC
        """, (threshold,))
        items = cursor.fetchall()
        cursor.close()
        return items, None
    except Exception as e:
        return None, str(e)

