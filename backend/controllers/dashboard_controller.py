"""Dashboard controller - analytics and statistics"""
from utils.database import get_db_connection
from datetime import datetime, timedelta

def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        stats = {}
        
        # Total customers
        cursor.execute("SELECT COUNT(*) as count FROM customer")
        stats['total_customers'] = cursor.fetchone()['count']
        
        # Total products
        cursor.execute("SELECT COUNT(*) as count FROM product")
        stats['total_products'] = cursor.fetchone()['count']
        
        # Total stores
        cursor.execute("SELECT COUNT(*) as count FROM store")
        stats['total_stores'] = cursor.fetchone()['count']
        
        # Total employees
        cursor.execute("SELECT COUNT(*) as count FROM employee")
        stats['total_employees'] = cursor.fetchone()['count']
        
        # Total sales (orders)
        cursor.execute("SELECT COUNT(*) as count FROM orders")
        stats['total_orders'] = cursor.fetchone()['count']
        
        # Total revenue
        cursor.execute("SELECT COALESCE(SUM(total_amount), 0) as total FROM orders WHERE status = 'PAID'")
        stats['total_revenue'] = float(cursor.fetchone()['total'])
        
        # Today's revenue
        today = datetime.now().date()
        cursor.execute("""
            SELECT COALESCE(SUM(total_amount), 0) as total 
            FROM orders 
            WHERE DATE(order_date) = %s AND status = 'PAID'
        """, (today,))
        stats['today_revenue'] = float(cursor.fetchone()['total'])
        
        # This month's revenue
        first_day = datetime.now().replace(day=1).date()
        cursor.execute("""
            SELECT COALESCE(SUM(total_amount), 0) as total 
            FROM orders 
            WHERE DATE(order_date) >= %s AND status = 'PAID'
        """, (first_day,))
        stats['month_revenue'] = float(cursor.fetchone()['total'])
        
        # Low stock items
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM inventory 
            WHERE quantity_in_stock <= 10
        """)
        stats['low_stock_count'] = cursor.fetchone()['count']
        
        cursor.close()
        return stats, None
    except Exception as e:
        return None, str(e)

def get_best_selling_products(limit=10):
    """Get best selling products"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # Use LEFT JOIN to handle empty orders gracefully
        cursor.execute("""
            SELECT p.product_id, p.name, 
                   COALESCE(SUM(oi.quantity), 0) as total_sold,
                   COALESCE(SUM(oi.subtotal), 0) as total_revenue
            FROM product p
            LEFT JOIN order_item oi ON p.product_id = oi.product_id
            LEFT JOIN orders o ON oi.order_id = o.order_id AND o.status = 'PAID'
            GROUP BY p.product_id, p.name
            HAVING total_sold > 0
            ORDER BY total_sold DESC
            LIMIT %s
        """, (limit,))
        products = cursor.fetchall()
        cursor.close()
        # Return empty list if no products found (not an error)
        return products if products else [], None
    except Exception as e:
        # Return empty list on error instead of None
        print(f"Error getting best selling products: {e}")
        return [], str(e)

def get_recent_orders(limit=10):
    """Get recent orders"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT o.*, 
                   CONCAT(c.first_name, ' ', COALESCE(c.last_name, '')) as customer_name
            FROM orders o
            JOIN customer c ON o.customer_id = c.customer_id
            ORDER BY o.order_date DESC
            LIMIT %s
        """, (limit,))
        orders = cursor.fetchall()
        cursor.close()
        # Return empty list if no orders found (not an error)
        return orders if orders else [], None
    except Exception as e:
        # Return empty list on error instead of None
        print(f"Error getting recent orders: {e}")
        return [], str(e)

def get_sales_by_date_range(start_date, end_date):
    """Get sales data for date range"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT DATE(order_date) as date,
                   COUNT(*) as order_count,
                   COALESCE(SUM(total_amount), 0) as revenue
            FROM orders
            WHERE DATE(order_date) BETWEEN %s AND %s AND status = 'PAID'
            GROUP BY DATE(order_date)
            ORDER BY date ASC
        """, (start_date, end_date))
        sales = cursor.fetchall()
        cursor.close()
        return sales, None
    except Exception as e:
        return None, str(e)

