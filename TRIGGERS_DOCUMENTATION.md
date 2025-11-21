# Database Triggers Documentation
## Cash & Carry Mart Management System

This document provides comprehensive information about all database triggers implemented in the system.

---

## Overview

The system implements **10 triggers** to ensure data integrity, automate calculations, and maintain audit trails. These triggers are categorized into:

- **Calculation Triggers** (3) - Automatic order total updates
- **Validation Triggers** (5) - Data integrity enforcement
- **Automation Triggers** (1) - Cart clearing
- **Audit Triggers** (1) - Status change logging

---

## 1. Order Total Calculation Triggers

### 1.1 trg_update_order_total

**Purpose:** Automatically update order total when a new item is added

**Event:** AFTER INSERT ON order_item

**Logic:**
```sql
CREATE TRIGGER trg_update_order_total
AFTER INSERT ON order_item
FOR EACH ROW
BEGIN
    UPDATE orders
    SET total_amount = fn_order_total(NEW.order_id)
    WHERE order_id = NEW.order_id;
END
```

**Example Scenario:**
- Customer adds Samsung Galaxy S23 (₹79,999) to order
- Trigger automatically updates order total to ₹79,999
- No manual calculation needed

---

### 1.2 trg_update_order_total_on_update

**Purpose:** Update order total when item quantity or price changes

**Event:** AFTER UPDATE ON order_item

**Logic:**
```sql
CREATE TRIGGER trg_update_order_total_on_update
AFTER UPDATE ON order_item
FOR EACH ROW
BEGIN
    UPDATE orders
    SET total_amount = fn_order_total(NEW.order_id)
    WHERE order_id = NEW.order_id;
END
```

**Example Scenario:**
- Employee changes quantity from 2 to 3 units
- Trigger recalculates order total automatically
- Ensures accuracy without manual intervention

---

### 1.3 trg_update_order_total_on_delete

**Purpose:** Update order total when an item is removed from order

**Event:** AFTER DELETE ON order_item

**Logic:**
```sql
CREATE TRIGGER trg_update_order_total_on_delete
AFTER DELETE ON order_item
FOR EACH ROW
BEGIN
    UPDATE orders
    SET total_amount = fn_order_total(OLD.order_id)
    WHERE order_id = OLD.order_id;
END
```

**Example Scenario:**
- Customer removes an item from order
- Trigger recalculates total excluding removed item
- Order total stays accurate

---

## 2. Validation Triggers

### 2.1 trg_check_inventory_before_update

**Purpose:** Prevent negative inventory quantities

**Event:** BEFORE UPDATE ON inventory

**Logic:**
```sql
CREATE TRIGGER trg_check_inventory_before_update
BEFORE UPDATE ON inventory
FOR EACH ROW
BEGIN
    IF NEW.quantity_in_stock < 0 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Inventory quantity cannot be negative';
    END IF;
END
```

**Example Scenario:**
- Attempt to set inventory to -5 units
- Trigger raises error: "Inventory quantity cannot be negative"
- Update is blocked, data integrity maintained

---

### 2.2 trg_validate_product_price_insert

**Purpose:** Validate product price on creation

**Event:** BEFORE INSERT ON product

**Logic:**
```sql
CREATE TRIGGER trg_validate_product_price_insert
BEFORE INSERT ON product
FOR EACH ROW
BEGIN
    IF NEW.price < 0 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Product price cannot be negative';
    END IF;
END
```

**Example Scenario:**
- Attempt to create product with price = -100
- Trigger raises error: "Product price cannot be negative"
- Invalid product creation prevented

---

### 2.3 trg_validate_product_price_update

**Purpose:** Validate product price on modification

**Event:** BEFORE UPDATE ON product

**Logic:**
```sql
CREATE TRIGGER trg_validate_product_price_update
BEFORE UPDATE ON product
FOR EACH ROW
BEGIN
    IF NEW.price < 0 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Product price cannot be negative';
    END IF;
END
```

**Example Scenario:**
- Attempt to update product price to -50
- Trigger blocks update with error message
- Pricing integrity maintained

---

### 2.4 trg_prevent_product_delete_with_inventory

**Purpose:** Prevent deletion of products with existing stock

**Event:** BEFORE DELETE ON product

**Logic:**
```sql
CREATE TRIGGER trg_prevent_product_delete_with_inventory
BEFORE DELETE ON product
FOR EACH ROW
BEGIN
    DECLARE inventory_count INT;
    SELECT COUNT(*) INTO inventory_count 
    FROM inventory 
    WHERE product_id = OLD.product_id AND quantity_in_stock > 0;
    
    IF inventory_count > 0 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Cannot delete product with existing inventory. Clear inventory first.';
    END IF;
END
```

**Example Scenario:**
- Attempt to delete product with 50 units in stock
- Trigger raises error: "Cannot delete product with existing inventory"
- Prevents accidental data loss

---

### 2.5 trg_validate_employee_salary

**Purpose:** Validate employee salary on creation

**Event:** BEFORE INSERT ON employee

**Logic:**
```sql
CREATE TRIGGER trg_validate_employee_salary
BEFORE INSERT ON employee
FOR EACH ROW
BEGIN
    IF NEW.salary IS NOT NULL AND NEW.salary < 0 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Employee salary cannot be negative';
    END IF;
END
```

**Example Scenario:**
- Attempt to create employee with salary = -5000
- Trigger blocks insertion with error
- Payroll data integrity maintained

---

## 3. Automation Triggers

### 3.1 trg_clear_cart_after_order

**Purpose:** Automatically clear customer cart after order creation

**Event:** AFTER INSERT ON orders

**Logic:**
```sql
CREATE TRIGGER trg_clear_cart_after_order
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    DELETE FROM cart WHERE customer_id = NEW.customer_id;
END
```

**Example Scenario:**
- Customer completes checkout
- Order is created in database
- Trigger automatically clears all items from customer's cart
- Clean slate for next shopping session

**Benefits:**
- Prevents duplicate orders
- Improves user experience
- Reduces manual cleanup operations

---

## 4. Audit Triggers

### 4.1 trg_log_order_status_change

**Purpose:** Create audit trail for order status changes

**Event:** AFTER UPDATE ON orders

**Audit Table:**
```sql
CREATE TABLE order_status_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    old_status ENUM('PENDING','PAID','CANCELLED','SHIPPED'),
    new_status ENUM('PENDING','PAID','CANCELLED','SHIPPED'),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
```

**Trigger Logic:**
```sql
CREATE TRIGGER trg_log_order_status_change
AFTER UPDATE ON orders
FOR EACH ROW
BEGIN
    IF OLD.status != NEW.status THEN
        INSERT INTO order_status_log (order_id, old_status, new_status)
        VALUES (NEW.order_id, OLD.status, NEW.status);
    END IF;
END
```

**Example Scenario:**
- Order status changes from PENDING to PAID
- Trigger logs: order_id=123, old_status=PENDING, new_status=PAID, timestamp
- Complete audit trail maintained

**Benefits:**
- Compliance and accountability
- Track order lifecycle
- Investigate status change history
- Business analytics

---

## Testing Triggers

### Test Case 1: Order Total Calculation

```sql
-- Create order
INSERT INTO orders (customer_id, store_id) VALUES (1, 1);
SET @order_id = LAST_INSERT_ID();

-- Add items
INSERT INTO order_item (order_id, product_id, quantity, unit_price)
VALUES (@order_id, 1, 2, 79999.00);

-- Check if total was updated automatically
SELECT order_id, total_amount FROM orders WHERE order_id = @order_id;
-- Expected: total_amount = 159998.00
```

### Test Case 2: Negative Inventory Prevention

```sql
-- Attempt to set negative inventory
UPDATE inventory SET quantity_in_stock = -10 WHERE inventory_id = 1;
-- Expected: Error - "Inventory quantity cannot be negative"
```

### Test Case 3: Cart Clearing

```sql
-- Add items to cart
INSERT INTO cart (customer_id, product_id, quantity) VALUES (1, 1, 2);

-- Create order
INSERT INTO orders (customer_id, store_id) VALUES (1, 1);

-- Check if cart was cleared
SELECT COUNT(*) FROM cart WHERE customer_id = 1;
-- Expected: 0 (cart is empty)
```

### Test Case 4: Status Change Logging

```sql
-- Update order status
UPDATE orders SET status = 'PAID' WHERE order_id = 1;

-- Check audit log
SELECT * FROM order_status_log WHERE order_id = 1;
-- Expected: Record showing status change with timestamp
```

---

## Trigger Performance Considerations

1. **Minimal Logic:** Triggers contain only essential validation and calculations
2. **Indexed Columns:** All foreign keys and frequently queried columns are indexed
3. **Avoid Cascading:** Triggers don't call other triggers to prevent infinite loops
4. **Error Handling:** Clear error messages for debugging
5. **Audit Efficiency:** Status log only records actual changes (IF OLD != NEW)

---

## Benefits of Trigger Implementation

### Data Integrity
- Automatic validation prevents invalid data
- Referential integrity maintained
- Business rules enforced at database level

### Automation
- Reduces manual calculations
- Eliminates human error
- Consistent behavior across all applications

### Audit Trail
- Complete history of changes
- Compliance and accountability
- Business intelligence data

### Performance
- Calculations done at database level
- Reduces application logic complexity
- Atomic operations ensure consistency

---

## Maintenance Notes

**Adding New Triggers:**
1. Define clear purpose and event
2. Test thoroughly in development
3. Document expected behavior
4. Consider performance impact
5. Update this documentation

**Modifying Existing Triggers:**
1. Drop existing trigger first
2. Create new version
3. Test with existing data
4. Verify no side effects
5. Update documentation

**Disabling Triggers (if needed):**
```sql
-- Temporarily disable trigger
DROP TRIGGER IF EXISTS trigger_name;

-- Re-enable by recreating
CREATE TRIGGER trigger_name ...
```

---

## Summary

| Trigger Name | Event | Table | Purpose |
|-------------|-------|-------|---------|
| trg_update_order_total | AFTER INSERT | order_item | Calculate order total |
| trg_update_order_total_on_update | AFTER UPDATE | order_item | Recalculate on item change |
| trg_update_order_total_on_delete | AFTER DELETE | order_item | Recalculate on item removal |
| trg_check_inventory_before_update | BEFORE UPDATE | inventory | Prevent negative stock |
| trg_validate_product_price_insert | BEFORE INSERT | product | Validate price on create |
| trg_validate_product_price_update | BEFORE UPDATE | product | Validate price on update |
| trg_clear_cart_after_order | AFTER INSERT | orders | Auto-clear cart |
| trg_log_order_status_change | AFTER UPDATE | orders | Audit status changes |
| trg_prevent_product_delete_with_inventory | BEFORE DELETE | product | Prevent data loss |
| trg_validate_employee_salary | BEFORE INSERT | employee | Validate salary |

**Total Triggers:** 10
**Tables with Triggers:** 5 (order_item, inventory, product, orders, employee)
**Audit Tables:** 1 (order_status_log)

---

*Last Updated: November 2024*
*Cash & Carry Mart Management System*
