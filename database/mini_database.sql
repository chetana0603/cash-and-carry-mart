-- =========================
-- DATABASE SETUP
-- =========================
DROP DATABASE IF EXISTS mini;
CREATE DATABASE mini CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE mini;

-- =========================
-- TABLE DEFINITIONS
-- =========================
CREATE TABLE customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    address VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE store (
    store_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    location VARCHAR(255) NOT NULL
);

CREATE TABLE employee (
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

CREATE TABLE category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE supplier (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    contact VARCHAR(50) UNIQUE,
    address VARCHAR(255)
);

CREATE TABLE product (
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

CREATE TABLE inventory (
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

CREATE TABLE cart (
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

CREATE TABLE orders (
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

CREATE TABLE order_item (
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

CREATE TABLE payment (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    amount DECIMAL(12,2) NOT NULL CHECK (amount >= 0),
    payment_type ENUM('CASH','CARD','UPI','ONLINE') NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_payment_order FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- =========================
-- SAMPLE DATA
-- =========================
INSERT INTO customer (first_name, last_name, phone, email, address) VALUES
('Alice', 'Johnson', '9876543210', 'alice@example.com', '12 Park Lane'),
('Bob', 'Smith', '9876543211', 'bob@example.com', '34 Oak Street'),
('Charlie', 'Brown', '9876543212', 'charlie@example.com', '56 Maple Avenue');

INSERT INTO store (name, location) VALUES
('Downtown Store','33 Main St'),
('Uptown Store','55 Broadway'),
('Suburban Store','77 Market St');

INSERT INTO employee (name, job_title, hire_date, salary, store_id, email) VALUES
('David Lee','Cashier','2022-01-15',30000.00,1,'david@example.com'),
('Emma Wilson','Manager','2021-05-10',60000.00,2,'emma@example.com'),
('Frank Green','Sales Associate','2023-03-20',25000.00,3,'frank@example.com');

INSERT INTO category (name) VALUES ('Electronics'),('Groceries'),('Clothing');

INSERT INTO supplier (name, contact, address) VALUES
('TechSupply Co.','9998887777','101 Silicon Valley'),
('FreshFoods Ltd.','9998886666','55 Farm Road'),
('FashionHub','9998885555','22 Style Street');

INSERT INTO product (name, description, price, availability, category_id, supplier_id) VALUES
('Smartphone','Android phone',15000.00,TRUE,1,1),
('Apples (1kg)','Fresh apples',200.00,TRUE,2,2),
('T-Shirt','Cotton tee',500.00,TRUE,3,3);

INSERT INTO inventory (product_id, store_id, quantity_in_stock) VALUES
(1,1,50),(2,2,100),(3,3,75);

-- =========================
-- FUNCTION: ORDER TOTAL
-- =========================
DROP FUNCTION IF EXISTS fn_order_total;
DELIMITER //
CREATE FUNCTION fn_order_total(p_order_id INT)
RETURNS DECIMAL(12,2)
DETERMINISTIC
BEGIN
    DECLARE v_total DECIMAL(12,2);
    SELECT IFNULL(SUM(subtotal),0) INTO v_total FROM order_item WHERE order_id = p_order_id;
    RETURN v_total;
END //
DELIMITER ;

-- =========================
-- TRIGGERS
-- =========================
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

-- =========================
-- CRUD PROCEDURES
-- =========================
DELIMITER //

-- Customer CRUD
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

CREATE PROCEDURE sp_delete_customer(IN p_customer_id INT)
BEGIN
    DELETE FROM customer WHERE customer_id=p_customer_id;
END //

-- Product CRUD
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

CREATE PROCEDURE sp_delete_product(IN p_product_id INT)
BEGIN
    DELETE FROM product WHERE product_id=p_product_id;
END //

-- =========================
-- TRANSACTIONAL: CREATE ORDER
-- =========================
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
    SET total_amount = fn_order_total(p_order_id)
    WHERE order_id = p_order_id;

    COMMIT;
END //
DELIMITER ;

-- ✅ END OF SCRIPT
