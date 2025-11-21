-- =========================
-- DATABASE SCHEMA ONLY (NO DATA)
-- This file creates tables only if they don't exist
-- It does NOT drop the database or insert sample data
-- =========================

-- Create database only if it doesn't exist
CREATE DATABASE IF NOT EXISTS mini CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE mini;

-- =========================
-- TABLE DEFINITIONS (CREATE IF NOT EXISTS)
-- =========================

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

CREATE TABLE IF NOT EXISTS store (
    store_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    location VARCHAR(255) NOT NULL
);

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

CREATE TABLE IF NOT EXISTS category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS supplier (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    contact VARCHAR(50) UNIQUE,
    address VARCHAR(255)
);

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

CREATE TABLE IF NOT EXISTS payment (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    amount DECIMAL(12,2) NOT NULL CHECK (amount >= 0),
    payment_type ENUM('CASH','CARD','UPI','ONLINE') NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_payment_order FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- =========================
-- USER TABLE FOR AUTHENTICATION
-- =========================
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

-- =========================
-- FUNCTION: ORDER TOTAL
-- =========================
DROP FUNCTION IF EXISTS fn_order_total;
DELIMITER //
CREATE FUNCTION fn_order_total(p_order_id INT)
RETURNS DECIMAL(12,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_total DECIMAL(12,2);
    SELECT IFNULL(SUM(subtotal),0) INTO v_total FROM order_item WHERE order_id = p_order_id;
    RETURN v_total;
END //
DELIMITER ;

-- =========================
-- TRIGGERS
-- =========================

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

-- Trigger 8: Log order status changes (requires audit table)
-- First create audit table if not exists
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

-- =========================
-- CRUD PROCEDURES
-- =========================
DELIMITER //

-- Customer CRUD
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
    INSERT INTO customer(first_name,middle_name,last_name,phone,email,address)
    VALUES(p_first_name,p_middle_name,p_last_name,p_phone,p_email,p_address);
    SET p_customer_id = LAST_INSERT_ID();
END //

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

DROP PROCEDURE IF EXISTS sp_delete_customer //
CREATE PROCEDURE sp_delete_customer(IN p_customer_id INT)
BEGIN
    DELETE FROM customer WHERE customer_id=p_customer_id;
END //

-- Product CRUD
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
    INSERT INTO product(name,description,price,availability,category_id,supplier_id)
    VALUES(p_name,p_description,p_price,p_availability,p_category_id,p_supplier_id);
    SET p_product_id = LAST_INSERT_ID();
END //

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
    SET name=p_name, description=p_description, price=p_price, availability=p_availability,
        category_id=p_category_id, supplier_id=p_supplier_id
    WHERE product_id=p_product_id;
END //

DROP PROCEDURE IF EXISTS sp_delete_product //
CREATE PROCEDURE sp_delete_product(IN p_product_id INT)
BEGIN
    DELETE FROM product WHERE product_id=p_product_id;
END //

-- =========================
-- TRANSACTIONAL: CREATE ORDER
-- =========================
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

    INSERT INTO orders(customer_id, employee_id, store_id) VALUES(p_customer_id, p_employee_id, p_store_id);
    SET p_order_id = LAST_INSERT_ID();
    SET v_len = JSON_LENGTH(p_items);

    WHILE v_idx < v_len DO
        SET v_prod = JSON_UNQUOTE(JSON_EXTRACT(p_items, CONCAT('$[', v_idx, '].product_id')));
        SET v_qty = JSON_UNQUOTE(JSON_EXTRACT(p_items, CONCAT('$[', v_idx, '].quantity')));
        SET v_price = JSON_UNQUOTE(JSON_EXTRACT(p_items, CONCAT('$[', v_idx, '].unit_price')));

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

        INSERT INTO order_item(order_id, product_id, quantity, unit_price)
        VALUES(p_order_id, v_prod, v_qty, v_price);

        UPDATE inventory
        SET quantity_in_stock = quantity_in_stock - v_qty
        WHERE product_id = v_prod AND store_id = p_store_id;

        SET v_idx = v_idx + 1;
    END WHILE;

    UPDATE orders
    SET total_amount = fn_order_total(p_order_id),
        status = 'PAID'
    WHERE order_id = p_order_id;

    COMMIT;
END //
DELIMITER ;

-- ✅ END OF SCHEMA - NO SAMPLE DATA INSERTED

