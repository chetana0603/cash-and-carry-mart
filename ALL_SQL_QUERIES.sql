-- =====================================================
-- CASH & CARRY MART MANAGEMENT SYSTEM
-- ALL SQL QUERIES USED IN THE PROJECT
-- =====================================================

-- =====================================================
-- 1. DATABASE CREATION
-- =====================================================

CREATE DATABASE IF NOT EXISTS mini CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE mini;

-- =====================================================
-- 2. TABLE CREATION (DDL COMMANDS)
-- =====================================================

-- Customer Table
CREATE TABLE IF NOT EXISTS customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    address VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Store Table
CREATE TABLE IF NOT EXISTS store (
    store_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    location VARCHAR(255) NOT NULL
);

-- Employee Table
CREATE TABLE IF NOT EXISTS employee (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    job_title VARCHAR(100),
    hire_date DATE,
    salary DECIMAL(12,2) CHECK (salary >= 0),
    store_id INT,
    email VARCHAR(150),
    CONSTRAINT fk_employee_store FOREIGN KEY (store_id) REFERENCES store(store_id)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- Category Table
CREATE TABLE IF NOT EXISTS category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Supplier Table
CREATE TABLE IF NOT EXISTS supplier (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    contact VARCHAR(50) UNIQUE,
    address VARCHAR(255)
);


-- Product Table
CREATE TABLE IF NOT EXISTS product (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    availability BOOLEAN NOT NULL DEFAULT TRUE,
    category_id INT,
    supplier_id INT,
    CONSTRAINT fk_product_category FOREIGN KEY (category_id) REFERENCES category(category_id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_product_supplier FOREIGN KEY (supplier_id) REFERENCES supplier(supplier_id)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- Inventory Table
CREATE TABLE IF NOT EXISTS inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    store_id INT NOT NULL,
    quantity_in_stock INT NOT NULL DEFAULT 0 CHECK (quantity_in_stock >= 0),
    CONSTRAINT fk_inventory_product FOREIGN KEY (product_id) REFERENCES product(product_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_inventory_store FOREIGN KEY (store_id) REFERENCES store(store_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE KEY ux_inventory_product_store (product_id, store_id)
);

-- Cart Table
CREATE TABLE IF NOT EXISTS cart (
    cart_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_cart_customer FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_cart_product FOREIGN KEY (product_id) REFERENCES product(product_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Orders Table
CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    employee_id INT,
    store_id INT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(12,2) DEFAULT 0 CHECK (total_amount >= 0),
    status ENUM('PENDING','PAID','CANCELLED','SHIPPED') DEFAULT 'PENDING',
    CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_orders_employee FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_orders_store FOREIGN KEY (store_id) REFERENCES store(store_id)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- Order Item Table
CREATE TABLE IF NOT EXISTS order_item (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0),
    subtotal DECIMAL(12,2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    CONSTRAINT fk_orderitem_order FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_orderitem_product FOREIGN KEY (product_id) REFERENCES product(product_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Payment Table
CREATE TABLE IF NOT EXISTS payment (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    amount DECIMAL(12,2) NOT NULL CHECK (amount >= 0),
    payment_type ENUM('CASH','CARD','UPI','ONLINE') NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_payment_order FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- User Table (Authentication)
CREATE TABLE IF NOT EXISTS user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('ADMIN', 'EMPLOYEE') NOT NULL DEFAULT 'EMPLOYEE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user_employee FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
        ON DELETE SET NULL ON UPDATE CASCADE
);


-- =====================================================
-- 3. SAMPLE INSERT STATEMENTS
-- =====================================================

-- Insert Stores
INSERT INTO store (name, location) VALUES
('Downtown Branch', '123 Main Street, City Center'),
('Westside Mall', '456 West Avenue, Shopping District'),
('Eastside Plaza', '789 East Road, Business Park');

-- Insert Categories
INSERT INTO category (name) VALUES
('Electronics'),
('Groceries'),
('Clothing'),
('Home & Kitchen'),
('Sports & Fitness');

-- Insert Suppliers
INSERT INTO supplier (name, contact, address) VALUES
('TechSupply Co.', '9876543210', '100 Tech Park, Silicon Valley'),
('FreshFoods Ltd.', '9876543211', '200 Farm Road, Agricultural Zone'),
('Fashion Hub', '9876543212', '300 Textile Street, Garment District');

-- Insert Customers
INSERT INTO customer (first_name, middle_name, last_name, phone, email, address) VALUES
('Rajesh', 'Kumar', 'Sharma', '9123456789', 'rajesh.sharma@email.com', '10 MG Road, Bangalore'),
('Priya', NULL, 'Patel', '9123456790', 'priya.patel@email.com', '20 Park Street, Mumbai'),
('Amit', 'Singh', 'Verma', '9123456791', 'amit.verma@email.com', '30 Lake View, Delhi');

-- Insert Employees
INSERT INTO employee (name, job_title, hire_date, salary, store_id, email) VALUES
('Suresh Kumar', 'Store Manager', '2023-01-15', 50000.00, 1, 'suresh@cashcarry.com'),
('Anita Desai', 'Sales Associate', '2023-03-20', 30000.00, 1, 'anita@cashcarry.com'),
('Vikram Reddy', 'Inventory Manager', '2023-02-10', 45000.00, 2, 'vikram@cashcarry.com');

-- Insert Products
INSERT INTO product (name, description, price, availability, category_id, supplier_id) VALUES
('Samsung Galaxy S23', 'Latest smartphone with 5G', 79999.00, TRUE, 1, 1),
('Basmati Rice 5kg', 'Premium quality basmati rice', 450.00, TRUE, 2, 2),
('Nike Running Shoes', 'Comfortable sports shoes', 4999.00, TRUE, 5, 3),
('LG Refrigerator', '260L double door refrigerator', 25999.00, TRUE, 4, 1),
('Organic Milk 1L', 'Fresh organic milk', 65.00, TRUE, 2, 2);

-- Insert Inventory
INSERT INTO inventory (product_id, store_id, quantity_in_stock) VALUES
(1, 1, 50),
(2, 1, 200),
(3, 1, 75),
(4, 2, 30),
(5, 2, 150),
(1, 3, 40),
(2, 3, 180);

-- Insert User (Admin)
INSERT INTO user (username, password_hash, role) VALUES
('admin', 'scrypt:32768:8:1$hashed_password_here', 'ADMIN');


-- =====================================================
-- 4. FUNCTIONS
-- =====================================================

DELIMITER //

-- Function to calculate order total
DROP FUNCTION IF EXISTS fn_order_total //
CREATE FUNCTION fn_order_total(p_order_id INT)
RETURNS DECIMAL(12,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_total DECIMAL(12,2);
    SELECT IFNULL(SUM(subtotal),0) INTO v_total 
    FROM order_item 
    WHERE order_id = p_order_id;
    RETURN v_total;
END //

DELIMITER ;

-- =====================================================
-- 5. TRIGGERS
-- =====================================================

-- Trigger 1: Update order total after inserting order item
DROP TRIGGER IF EXISTS trg_update_order_total;
DELIMITER //
CREATE TRIGGER trg_update_order_total
AFTER INSERT ON order_item
FOR EACH ROW
BEGIN
    UPDATE orders
    SET total_amount = fn_order_total(NEW.order_id)
    WHERE order_id = NEW.order_id;
END //
DELIMITER ;

-- Trigger 2: Update order total after updating order item
DROP TRIGGER IF EXISTS trg_update_order_total_on_update;
DELIMITER //
CREATE TRIGGER trg_update_order_total_on_update
AFTER UPDATE ON order_item
FOR EACH ROW
BEGIN
    UPDATE orders
    SET total_amount = fn_order_total(NEW.order_id)
    WHERE order_id = NEW.order_id;
END //
DELIMITER ;

-- Trigger 3: Update order total after deleting order item
DROP TRIGGER IF EXISTS trg_update_order_total_on_delete;
DELIMITER //
CREATE TRIGGER trg_update_order_total_on_delete
AFTER DELETE ON order_item
FOR EACH ROW
BEGIN
    UPDATE orders
    SET total_amount = fn_order_total(OLD.order_id)
    WHERE order_id = OLD.order_id;
END //
DELIMITER ;

-- Trigger 4: Prevent negative inventory
DROP TRIGGER IF EXISTS trg_check_inventory_before_update;
DELIMITER //
CREATE TRIGGER trg_check_inventory_before_update
BEFORE UPDATE ON inventory
FOR EACH ROW
BEGIN
    IF NEW.quantity_in_stock < 0 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Inventory quantity cannot be negative';
    END IF;
END //
DELIMITER ;

-- Trigger 5: Validate product price before insert
DROP TRIGGER IF EXISTS trg_validate_product_price_insert;
DELIMITER //
CREATE TRIGGER trg_validate_product_price_insert
BEFORE INSERT ON product
FOR EACH ROW
BEGIN
    IF NEW.price < 0 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Product price cannot be negative';
    END IF;
END //
DELIMITER ;

-- Trigger 6: Validate product price before update
DROP TRIGGER IF EXISTS trg_validate_product_price_update;
DELIMITER //
CREATE TRIGGER trg_validate_product_price_update
BEFORE UPDATE ON product
FOR EACH ROW
BEGIN
    IF NEW.price < 0 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Product price cannot be negative';
    END IF;
END //
DELIMITER ;

-- Trigger 7: Clear customer cart after order is created
DROP TRIGGER IF EXISTS trg_clear_cart_after_order;
DELIMITER //
CREATE TRIGGER trg_clear_cart_after_order
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    DELETE FROM cart WHERE customer_id = NEW.customer_id;
END //
DELIMITER ;

-- Trigger 8: Create audit table for order status changes
CREATE TABLE IF NOT EXISTS order_status_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    old_status ENUM('PENDING','PAID','CANCELLED','SHIPPED'),
    new_status ENUM('PENDING','PAID','CANCELLED','SHIPPED'),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_log_order FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TRIGGER IF EXISTS trg_log_order_status_change;
DELIMITER //
CREATE TRIGGER trg_log_order_status_change
AFTER UPDATE ON orders
FOR EACH ROW
BEGIN
    IF OLD.status != NEW.status THEN
        INSERT INTO order_status_log (order_id, old_status, new_status)
        VALUES (NEW.order_id, OLD.status, NEW.status);
    END IF;
END //
DELIMITER ;

-- Trigger 9: Prevent deletion of products with existing inventory
DROP TRIGGER IF EXISTS trg_prevent_product_delete_with_inventory;
DELIMITER //
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
END //
DELIMITER ;

-- Trigger 10: Validate employee salary
DROP TRIGGER IF EXISTS trg_validate_employee_salary;
DELIMITER //
CREATE TRIGGER trg_validate_employee_salary
BEFORE INSERT ON employee
FOR EACH ROW
BEGIN
    IF NEW.salary IS NOT NULL AND NEW.salary < 0 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Employee salary cannot be negative';
    END IF;
END //
DELIMITER ;


-- =====================================================
-- 6. STORED PROCEDURES
-- =====================================================

DELIMITER //

-- Procedure to create customer
DROP PROCEDURE IF EXISTS sp_create_customer //
CREATE PROCEDURE sp_create_customer(
    IN p_first_name VARCHAR(100),
    IN p_middle_name VARCHAR(100),
    IN p_last_name VARCHAR(100),
    IN p_phone VARCHAR(20),
    IN p_email VARCHAR(150),
    IN p_address VARCHAR(255),
    OUT p_customer_id INT
)
BEGIN
    INSERT INTO customer(first_name, middle_name, last_name, phone, email, address)
    VALUES(p_first_name, p_middle_name, p_last_name, p_phone, p_email, p_address);
    SET p_customer_id = LAST_INSERT_ID();
END //

-- Procedure to update customer
DROP PROCEDURE IF EXISTS sp_update_customer //
CREATE PROCEDURE sp_update_customer(
    IN p_customer_id INT,
    IN p_first_name VARCHAR(100),
    IN p_middle_name VARCHAR(100),
    IN p_last_name VARCHAR(100),
    IN p_phone VARCHAR(20),
    IN p_email VARCHAR(150),
    IN p_address VARCHAR(255)
)
BEGIN
    UPDATE customer
    SET first_name=p_first_name, middle_name=p_middle_name, last_name=p_last_name,
        phone=p_phone, email=p_email, address=p_address
    WHERE customer_id=p_customer_id;
END //

-- Procedure to delete customer
DROP PROCEDURE IF EXISTS sp_delete_customer //
CREATE PROCEDURE sp_delete_customer(IN p_customer_id INT)
BEGIN
    DELETE FROM customer WHERE customer_id=p_customer_id;
END //

-- Procedure to create product
DROP PROCEDURE IF EXISTS sp_create_product //
CREATE PROCEDURE sp_create_product(
    IN p_name VARCHAR(150),
    IN p_description TEXT,
    IN p_price DECIMAL(10,2),
    IN p_availability BOOLEAN,
    IN p_category_id INT,
    IN p_supplier_id INT,
    OUT p_product_id INT
)
BEGIN
    INSERT INTO product(name, description, price, availability, category_id, supplier_id)
    VALUES(p_name, p_description, p_price, p_availability, p_category_id, p_supplier_id);
    SET p_product_id = LAST_INSERT_ID();
END //

-- Procedure to update product
DROP PROCEDURE IF EXISTS sp_update_product //
CREATE PROCEDURE sp_update_product(
    IN p_product_id INT,
    IN p_name VARCHAR(150),
    IN p_description TEXT,
    IN p_price DECIMAL(10,2),
    IN p_availability BOOLEAN,
    IN p_category_id INT,
    IN p_supplier_id INT
)
BEGIN
    UPDATE product
    SET name=p_name, description=p_description, price=p_price, 
        availability=p_availability, category_id=p_category_id, supplier_id=p_supplier_id
    WHERE product_id=p_product_id;
END //

-- Procedure to delete product
DROP PROCEDURE IF EXISTS sp_delete_product //
CREATE PROCEDURE sp_delete_product(IN p_product_id INT)
BEGIN
    DELETE FROM product WHERE product_id=p_product_id;
END //


-- Procedure to create order (Transactional)
DROP PROCEDURE IF EXISTS sp_create_order //
CREATE PROCEDURE sp_create_order(
    IN p_customer_id INT,
    IN p_employee_id INT,
    IN p_store_id INT,
    IN p_items JSON,
    OUT p_order_id INT
)
BEGIN
    DECLARE v_idx INT DEFAULT 0;
    DECLARE v_len INT DEFAULT 0;
    DECLARE v_prod INT;
    DECLARE v_qty INT;
    DECLARE v_price DECIMAL(10,2);
    DECLARE v_inventory INT;
    DECLARE v_msg TEXT;

    START TRANSACTION;

    -- Create order
    INSERT INTO orders(customer_id, employee_id, store_id) 
    VALUES(p_customer_id, p_employee_id, p_store_id);
    SET p_order_id = LAST_INSERT_ID();
    SET v_len = JSON_LENGTH(p_items);

    -- Process each item
    WHILE v_idx < v_len DO
        SET v_prod = JSON_UNQUOTE(JSON_EXTRACT(p_items, CONCAT('$[', v_idx, '].product_id')));
        SET v_qty = JSON_UNQUOTE(JSON_EXTRACT(p_items, CONCAT('$[', v_idx, '].quantity')));
        SET v_price = JSON_UNQUOTE(JSON_EXTRACT(p_items, CONCAT('$[', v_idx, '].unit_price')));

        -- Check inventory
        SELECT quantity_in_stock INTO v_inventory
        FROM inventory
        WHERE product_id = v_prod AND store_id = p_store_id
        FOR UPDATE;

        IF v_inventory IS NULL THEN
            SET v_msg = CONCAT('No inventory for product ', v_prod, ' at store ', p_store_id);
            ROLLBACK;
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = v_msg;
        END IF;

        IF v_inventory < v_qty THEN
            SET v_msg = CONCAT('Insufficient stock for product ', v_prod, '. Available: ', v_inventory);
            ROLLBACK;
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = v_msg;
        END IF;

        -- Insert order item
        INSERT INTO order_item(order_id, product_id, quantity, unit_price)
        VALUES(p_order_id, v_prod, v_qty, v_price);

        -- Update inventory
        UPDATE inventory
        SET quantity_in_stock = quantity_in_stock - v_qty
        WHERE product_id = v_prod AND store_id = p_store_id;

        SET v_idx = v_idx + 1;
    END WHILE;

    -- Update order total and mark as PAID (cash and carry)
    UPDATE orders
    SET total_amount = fn_order_total(p_order_id),
        status = 'PAID'
    WHERE order_id = p_order_id;

    COMMIT;
END //

DELIMITER ;


-- =====================================================
-- 7. JOIN QUERIES
-- =====================================================

-- Get all orders with customer and employee details
SELECT o.order_id, o.order_date, o.total_amount, o.status,
       CONCAT(c.first_name, ' ', COALESCE(c.last_name, '')) as customer_name,
       c.email as customer_email,
       e.name as employee_name,
       s.name as store_name
FROM orders o
JOIN customer c ON o.customer_id = c.customer_id
LEFT JOIN employee e ON o.employee_id = e.employee_id
LEFT JOIN store s ON o.store_id = s.store_id
ORDER BY o.order_date DESC;

-- Get all products with category and supplier information
SELECT p.product_id, p.name, p.price, p.availability,
       c.name as category_name,
       s.name as supplier_name,
       s.contact as supplier_contact
FROM product p
LEFT JOIN category c ON p.category_id = c.category_id
LEFT JOIN supplier s ON p.supplier_id = s.supplier_id
ORDER BY p.name;

-- Get inventory with product and store details
SELECT i.inventory_id, i.quantity_in_stock,
       p.name as product_name,
       p.price,
       s.name as store_name,
       s.location as store_location
FROM inventory i
JOIN product p ON i.product_id = p.product_id
JOIN store s ON i.store_id = s.store_id
ORDER BY i.quantity_in_stock ASC;

-- Get order items with product details
SELECT oi.order_item_id, oi.quantity, oi.unit_price, oi.subtotal,
       p.name as product_name,
       o.order_id, o.order_date
FROM order_item oi
JOIN product p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
ORDER BY o.order_date DESC;

-- Get employees with their store information
SELECT e.employee_id, e.name, e.job_title, e.salary,
       s.name as store_name,
       s.location as store_location
FROM employee e
LEFT JOIN store s ON e.store_id = s.store_id
ORDER BY e.name;


-- =====================================================
-- 8. NESTED QUERIES (SUBQUERIES)
-- =====================================================

-- Find customers who have placed orders worth more than average
SELECT c.customer_id, c.first_name, c.last_name, c.email
FROM customer c
WHERE c.customer_id IN (
    SELECT o.customer_id
    FROM orders o
    WHERE o.total_amount > (SELECT AVG(total_amount) FROM orders)
);

-- Find products that are out of stock in any store
SELECT p.product_id, p.name, p.price
FROM product p
WHERE p.product_id IN (
    SELECT i.product_id
    FROM inventory i
    WHERE i.quantity_in_stock = 0
);

-- Find stores with inventory below threshold (10 units)
SELECT s.store_id, s.name, s.location
FROM store s
WHERE s.store_id IN (
    SELECT DISTINCT i.store_id
    FROM inventory i
    WHERE i.quantity_in_stock <= 10
);

-- Find products never ordered
SELECT p.product_id, p.name, p.price
FROM product p
WHERE p.product_id NOT IN (
    SELECT DISTINCT oi.product_id
    FROM order_item oi
);

-- Find employees who have processed orders
SELECT e.employee_id, e.name, e.job_title
FROM employee e
WHERE e.employee_id IN (
    SELECT DISTINCT o.employee_id
    FROM orders o
    WHERE o.employee_id IS NOT NULL
);

-- Find customers with more orders than average
SELECT c.customer_id, c.first_name, c.last_name,
       (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.customer_id) as order_count
FROM customer c
WHERE (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.customer_id) > 
      (SELECT AVG(order_count) FROM (
          SELECT COUNT(*) as order_count 
          FROM orders 
          GROUP BY customer_id
      ) as avg_orders);


-- =====================================================
-- 9. AGGREGATE QUERIES
-- =====================================================

-- Total revenue by store
SELECT s.name as store_name, 
       COUNT(o.order_id) as total_orders,
       COALESCE(SUM(o.total_amount), 0) as total_revenue
FROM store s
LEFT JOIN orders o ON s.store_id = o.store_id AND o.status = 'PAID'
GROUP BY s.store_id, s.name
ORDER BY total_revenue DESC;

-- Best selling products
SELECT p.product_id, p.name,
       COUNT(oi.order_item_id) as times_ordered,
       SUM(oi.quantity) as total_quantity_sold,
       SUM(oi.subtotal) as total_revenue
FROM product p
JOIN order_item oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id AND o.status = 'PAID'
GROUP BY p.product_id, p.name
ORDER BY total_quantity_sold DESC
LIMIT 10;

-- Customer purchase statistics
SELECT c.customer_id,
       CONCAT(c.first_name, ' ', COALESCE(c.last_name, '')) as customer_name,
       COUNT(o.order_id) as total_orders,
       COALESCE(SUM(o.total_amount), 0) as total_spent,
       COALESCE(AVG(o.total_amount), 0) as avg_order_value
FROM customer c
LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.status = 'PAID'
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_spent DESC;

-- Monthly revenue report
SELECT DATE_FORMAT(order_date, '%Y-%m') as month,
       COUNT(order_id) as total_orders,
       SUM(total_amount) as monthly_revenue,
       AVG(total_amount) as avg_order_value
FROM orders
WHERE status = 'PAID'
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month DESC;

-- Category-wise sales
SELECT c.name as category_name,
       COUNT(DISTINCT p.product_id) as products_count,
       COALESCE(SUM(oi.quantity), 0) as total_units_sold,
       COALESCE(SUM(oi.subtotal), 0) as total_revenue
FROM category c
LEFT JOIN product p ON c.category_id = p.category_id
LEFT JOIN order_item oi ON p.product_id = oi.product_id
LEFT JOIN orders o ON oi.order_id = o.order_id AND o.status = 'PAID'
GROUP BY c.category_id, c.name
ORDER BY total_revenue DESC;

-- Inventory value by store
SELECT s.name as store_name,
       COUNT(i.inventory_id) as products_stocked,
       SUM(i.quantity_in_stock) as total_units,
       SUM(i.quantity_in_stock * p.price) as inventory_value
FROM store s
LEFT JOIN inventory i ON s.store_id = i.store_id
LEFT JOIN product p ON i.product_id = p.product_id
GROUP BY s.store_id, s.name
ORDER BY inventory_value DESC;

-- Employee performance (orders processed)
SELECT e.employee_id, e.name, e.job_title,
       COUNT(o.order_id) as orders_processed,
       COALESCE(SUM(o.total_amount), 0) as total_sales_value
FROM employee e
LEFT JOIN orders o ON e.employee_id = o.employee_id AND o.status = 'PAID'
GROUP BY e.employee_id, e.name, e.job_title
ORDER BY orders_processed DESC;

-- Low stock items count by store
SELECT s.name as store_name,
       COUNT(i.inventory_id) as low_stock_items
FROM store s
LEFT JOIN inventory i ON s.store_id = i.store_id AND i.quantity_in_stock <= 10
GROUP BY s.store_id, s.name
ORDER BY low_stock_items DESC;

-- Average product price by category
SELECT c.name as category_name,
       COUNT(p.product_id) as product_count,
       MIN(p.price) as min_price,
       MAX(p.price) as max_price,
       AVG(p.price) as avg_price
FROM category c
LEFT JOIN product p ON c.category_id = p.category_id
GROUP BY c.category_id, c.name
ORDER BY avg_price DESC;

-- =====================================================
-- END OF SQL QUERIES
-- =====================================================
