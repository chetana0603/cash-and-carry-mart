"""Order controller"""
import json
from utils.database import get_db_connection
from utils.validators import validate_required, sanitize_input

def get_all_orders():
    """Get all orders"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT o.*, 
                   c.first_name, c.last_name, c.email as customer_email,
                   e.name as employee_name,
                   s.name as store_name, s.location as store_location
            FROM orders o
            LEFT JOIN customer c ON o.customer_id = c.customer_id
            LEFT JOIN employee e ON o.employee_id = e.employee_id
            LEFT JOIN store s ON o.store_id = s.store_id
            ORDER BY o.order_date DESC
        """)
        orders = cursor.fetchall()
        cursor.close()
        return orders, None
    except Exception as e:
        return None, str(e)

def get_order_by_id(order_id):
    """Get order by ID with items"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get order details
        cursor.execute("""
            SELECT o.*, 
                   c.first_name, c.last_name, c.email as customer_email,
                   e.name as employee_name,
                   s.name as store_name, s.location as store_location
            FROM orders o
            LEFT JOIN customer c ON o.customer_id = c.customer_id
            LEFT JOIN employee e ON o.employee_id = e.employee_id
            LEFT JOIN store s ON o.store_id = s.store_id
            WHERE o.order_id = %s
        """, (order_id,))
        order = cursor.fetchone()
        
        if not order:
            cursor.close()
            return None, "Order not found"
        
        # Get order items
        cursor.execute("""
            SELECT oi.*, p.name as product_name
            FROM order_item oi
            JOIN product p ON oi.product_id = p.product_id
            WHERE oi.order_id = %s
        """, (order_id,))
        items = cursor.fetchall()
        
        order['items'] = items
        cursor.close()
        
        return order, None
    except Exception as e:
        return None, str(e)

def create_order(data):
    """Create order using stored procedure"""
    try:
        is_valid, error = validate_required(data, ['customer_id', 'store_id', 'items'])
        if not is_valid:
            return None, error
        
        if not isinstance(data['items'], list) or len(data['items']) == 0:
            return None, "Order must have at least one item"
        
        # Validate items
        for item in data['items']:
            if 'product_id' not in item or 'quantity' not in item or 'unit_price' not in item:
                return None, "Each item must have product_id, quantity, and unit_price"
        
        data = sanitize_input(data)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Prepare items JSON
        items_json = json.dumps(data['items'])
        
        # Call stored procedure
        cursor.callproc('sp_create_order', [
            data['customer_id'],
            data.get('employee_id'),
            data['store_id'],
            items_json,
            0  # OUT parameter
        ])
        
        for result in cursor.stored_results():
            pass
        
        cursor.execute("SELECT LAST_INSERT_ID() as order_id")
        result = cursor.fetchone()
        order_id = result[0] if result else None
        
        conn.commit()
        cursor.close()
        
        if order_id:
            return get_order_by_id(order_id)
        return None, "Failed to create order"
    except Exception as e:
        return None, str(e)

def update_order_status(order_id, status):
    """Update order status"""
    try:
        valid_statuses = ['PENDING', 'PAID', 'CANCELLED', 'SHIPPED']
        if status not in valid_statuses:
            return None, f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET status = %s WHERE order_id = %s",
                      (status, order_id))
        conn.commit()
        cursor.close()
        
        return get_order_by_id(order_id)
    except Exception as e:
        return None, str(e)

def delete_order(order_id):
    """Delete order"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
        conn.commit()
        cursor.close()
        return True, None
    except Exception as e:
        return False, str(e)

