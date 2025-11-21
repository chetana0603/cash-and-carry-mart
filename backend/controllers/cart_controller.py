"""Cart controller"""
from utils.database import get_db_connection
from utils.validators import validate_required, validate_positive_number, sanitize_input

def get_cart_by_customer(customer_id):
    """Get cart items for a customer"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.*, p.name as product_name, p.price, p.description
            FROM cart c
            JOIN product p ON c.product_id = p.product_id
            WHERE c.customer_id = %s
            ORDER BY c.created_at DESC
        """, (customer_id,))
        items = cursor.fetchall()
        cursor.close()
        return items, None
    except Exception as e:
        return None, str(e)

def add_to_cart(data):
    """Add item to cart"""
    try:
        is_valid, error = validate_required(data, ['customer_id', 'product_id', 'quantity'])
        if not is_valid:
            return None, error
        
        is_valid, error = validate_positive_number(data['quantity'], 'Quantity')
        if not is_valid:
            return None, error
        
        data = sanitize_input(data)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if item already exists in cart
        cursor.execute("""
            SELECT cart_id, quantity FROM cart 
            WHERE customer_id = %s AND product_id = %s
        """, (data['customer_id'], data['product_id']))
        existing = cursor.fetchone()
        
        if existing:
            # Update quantity
            new_quantity = existing[1] + int(data['quantity'])
            cursor.execute("""
                UPDATE cart SET quantity = %s WHERE cart_id = %s
            """, (new_quantity, existing[0]))
            cart_id = existing[0]
        else:
            # Insert new item
            cursor.execute("""
                INSERT INTO cart (customer_id, product_id, quantity)
                VALUES (%s, %s, %s)
            """, (data['customer_id'], data['product_id'], data['quantity']))
            cart_id = cursor.lastrowid
        
        conn.commit()
        cursor.close()
        
        return {'cart_id': cart_id, 'message': 'Item added to cart'}, None
    except Exception as e:
        return None, str(e)

def update_cart_item(cart_id, data):
    """Update cart item quantity"""
    try:
        is_valid, error = validate_positive_number(data.get('quantity', 0), 'Quantity')
        if not is_valid:
            return None, error
        
        data = sanitize_input(data)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE cart SET quantity = %s WHERE cart_id = %s",
                      (data['quantity'], cart_id))
        conn.commit()
        cursor.close()
        
        return {'message': 'Cart item updated'}, None
    except Exception as e:
        return None, str(e)

def remove_from_cart(cart_id):
    """Remove item from cart"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cart WHERE cart_id = %s", (cart_id,))
        conn.commit()
        cursor.close()
        return True, None
    except Exception as e:
        return False, str(e)

def clear_cart(customer_id):
    """Clear all items from customer's cart"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cart WHERE customer_id = %s", (customer_id,))
        conn.commit()
        cursor.close()
        return True, None
    except Exception as e:
        return False, str(e)

