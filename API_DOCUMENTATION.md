# Cash & Carry Mart Management System - API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication

All endpoints (except `/auth/login` and `/auth/register`) require a JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

---

## Authentication Endpoints

### Login
**POST** `/auth/login`

Request Body:
```json
{
  "username": "admin",
  "password": "admin123"
}
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "username": "admin",
    "role": "ADMIN",
    "employee_id": null
  }
}
```

### Register (Admin Only)
**POST** `/auth/register`

Request Body:
```json
{
  "username": "newuser",
  "password": "password123",
  "role": "EMPLOYEE",
  "employee_id": 1
}
```

---

## Customer Endpoints

### Get All Customers
**GET** `/customers`

Response:
```json
{
  "customers": [
    {
      "customer_id": 1,
      "first_name": "Alice",
      "last_name": "Johnson",
      "phone": "9876543210",
      "email": "alice@example.com",
      "address": "12 Park Lane"
    }
  ]
}
```

### Get Customer by ID
**GET** `/customers/:id`

### Create Customer
**POST** `/customers`
- Requires: Employee or Admin role

Request Body:
```json
{
  "first_name": "John",
  "middle_name": "Doe",
  "last_name": "Smith",
  "phone": "9876543210",
  "email": "john@example.com",
  "address": "123 Main St"
}
```

### Update Customer
**PUT** `/customers/:id`
- Requires: Admin role

### Delete Customer
**DELETE** `/customers/:id`
- Requires: Admin role

---

## Product Endpoints

### Get All Products
**GET** `/products`

Response:
```json
{
  "products": [
    {
      "product_id": 1,
      "name": "Smartphone",
      "description": "Android phone",
      "price": 15000.00,
      "availability": true,
      "category_id": 1,
      "supplier_id": 1,
      "category_name": "Electronics",
      "supplier_name": "TechSupply Co."
    }
  ]
}
```

### Get Product by ID
**GET** `/products/:id`

### Create Product
**POST** `/products`
- Requires: Employee or Admin role
- Uses stored procedure: `sp_create_product`

Request Body:
```json
{
  "name": "Laptop",
  "description": "Gaming laptop",
  "price": 50000.00,
  "availability": true,
  "category_id": 1,
  "supplier_id": 1
}
```

### Update Product
**PUT** `/products/:id`
- Requires: Admin role
- Uses stored procedure: `sp_update_product`

### Delete Product
**DELETE** `/products/:id`
- Requires: Admin role
- Uses stored procedure: `sp_delete_product`

---

## Order Endpoints

### Get All Orders
**GET** `/orders`

Response:
```json
{
  "orders": [
    {
      "order_id": 1,
      "customer_id": 1,
      "employee_id": 1,
      "store_id": 1,
      "order_date": "2024-01-15T10:30:00",
      "total_amount": 15000.00,
      "status": "PENDING",
      "first_name": "Alice",
      "last_name": "Johnson"
    }
  ]
}
```

### Get Order by ID
**GET** `/orders/:id`

Response includes order items:
```json
{
  "order": {
    "order_id": 1,
    "customer_id": 1,
    "total_amount": 15000.00,
    "status": "PENDING",
    "items": [
      {
        "order_item_id": 1,
        "product_id": 1,
        "quantity": 1,
        "unit_price": 15000.00,
        "subtotal": 15000.00,
        "product_name": "Smartphone"
      }
    ]
  }
}
```

### Create Order
**POST** `/orders`
- Requires: Employee or Admin role
- Uses stored procedure: `sp_create_order`
- Automatically updates inventory via triggers

Request Body:
```json
{
  "customer_id": 1,
  "store_id": 1,
  "employee_id": 1,
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "unit_price": 15000.00
    }
  ]
}
```

### Update Order Status
**PUT** `/orders/:id/status`
- Requires: Admin role

Request Body:
```json
{
  "status": "PAID"
}
```

Valid statuses: `PENDING`, `PAID`, `CANCELLED`, `SHIPPED`

### Delete Order
**DELETE** `/orders/:id`
- Requires: Admin role

---

## Inventory Endpoints

### Get All Inventory
**GET** `/inventory`

### Get Low Stock Items
**GET** `/inventory/low-stock?threshold=10`

Response:
```json
{
  "items": [
    {
      "inventory_id": 1,
      "product_id": 1,
      "store_id": 1,
      "quantity_in_stock": 5,
      "product_name": "Smartphone",
      "store_name": "Downtown Store"
    }
  ]
}
```

### Create Inventory Record
**POST** `/inventory`
- Requires: Employee or Admin role

Request Body:
```json
{
  "product_id": 1,
  "store_id": 1,
  "quantity_in_stock": 100
}
```

### Update Inventory
**PUT** `/inventory/:id`
- Requires: Admin role

### Delete Inventory
**DELETE** `/inventory/:id`
- Requires: Admin role

---

## Cart Endpoints

### Get Cart by Customer
**GET** `/cart/customer/:customer_id`

Response:
```json
{
  "cart": [
    {
      "cart_id": 1,
      "customer_id": 1,
      "product_id": 1,
      "quantity": 2,
      "product_name": "Smartphone",
      "price": 15000.00
    }
  ]
}
```

### Add Item to Cart
**POST** `/cart`
- Requires: Employee or Admin role

Request Body:
```json
{
  "customer_id": 1,
  "product_id": 1,
  "quantity": 2
}
```

### Update Cart Item
**PUT** `/cart/:cart_id`
- Requires: Employee or Admin role

Request Body:
```json
{
  "quantity": 3
}
```

### Remove Item from Cart
**DELETE** `/cart/:cart_id`
- Requires: Employee or Admin role

### Clear Cart
**DELETE** `/cart/customer/:customer_id`
- Requires: Employee or Admin role

---

## Dashboard Endpoints

### Get Dashboard Statistics
**GET** `/dashboard/stats`

Response:
```json
{
  "stats": {
    "total_customers": 10,
    "total_products": 25,
    "total_stores": 3,
    "total_employees": 5,
    "total_orders": 50,
    "total_revenue": 500000.00,
    "today_revenue": 5000.00,
    "month_revenue": 50000.00,
    "low_stock_count": 3
  }
}
```

### Get Best Selling Products
**GET** `/dashboard/best-selling?limit=10`

Response:
```json
{
  "products": [
    {
      "product_id": 1,
      "name": "Smartphone",
      "total_sold": 50,
      "total_revenue": 750000.00
    }
  ]
}
```

### Get Recent Orders
**GET** `/dashboard/recent-orders?limit=10`

### Get Sales by Date Range
**GET** `/dashboard/sales?start_date=2024-01-01&end_date=2024-01-31`

---

## Store Endpoints

### Get All Stores
**GET** `/stores`

### Get Store by ID
**GET** `/stores/:id`

### Create Store
**POST** `/stores`
- Requires: Employee or Admin role

### Update Store
**PUT** `/stores/:id`
- Requires: Admin role

### Delete Store
**DELETE** `/stores/:id`
- Requires: Admin role

---

## Employee Endpoints

### Get All Employees
**GET** `/employees`

### Get Employee by ID
**GET** `/employees/:id`

### Create Employee
**POST** `/employees`
- Requires: Employee or Admin role

### Update Employee
**PUT** `/employees/:id`
- Requires: Admin role

### Delete Employee
**DELETE** `/employees/:id`
- Requires: Admin role

---

## Category Endpoints

### Get All Categories
**GET** `/categories`

### Get Category by ID
**GET** `/categories/:id`

### Create Category
**POST** `/categories`
- Requires: Employee or Admin role

### Update Category
**PUT** `/categories/:id`
- Requires: Admin role

### Delete Category
**DELETE** `/categories/:id`
- Requires: Admin role

---

## Supplier Endpoints

### Get All Suppliers
**GET** `/suppliers`

### Get Supplier by ID
**GET** `/suppliers/:id`

### Create Supplier
**POST** `/suppliers`
- Requires: Employee or Admin role

### Update Supplier
**PUT** `/suppliers/:id`
- Requires: Admin role

### Delete Supplier
**DELETE** `/suppliers/:id`
- Requires: Admin role

---

## Error Responses

All endpoints may return the following error formats:

### 400 Bad Request
```json
{
  "message": "Validation error message",
  "error": "validation_error"
}
```

### 401 Unauthorized
```json
{
  "message": "Authorization required",
  "error": "authorization_required"
}
```

### 403 Forbidden
```json
{
  "message": "Admin access required",
  "error": "insufficient_permissions"
}
```

### 404 Not Found
```json
{
  "message": "Resource not found",
  "error": "not_found"
}
```

### 500 Internal Server Error
```json
{
  "message": "Server error message",
  "error": "server_error"
}
```

---

## Database Stored Procedures Used

1. **sp_create_customer** - Creates a new customer
2. **sp_update_customer** - Updates customer information
3. **sp_delete_customer** - Deletes a customer
4. **sp_create_product** - Creates a new product
5. **sp_update_product** - Updates product information
6. **sp_delete_product** - Deletes a product
7. **sp_create_order** - Creates an order with items (transactional, updates inventory)

## Database Triggers

1. **trg_update_order_total** - Automatically updates order total when order items are added

## Database Functions

1. **fn_order_total** - Calculates total amount for an order

---

## Notes

- All monetary values are in decimal format (e.g., 15000.00)
- Dates are in ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
- Phone numbers must be 10 digits
- Email addresses are validated
- Inventory is automatically updated when orders are created via `sp_create_order`
- Order totals are automatically calculated via database triggers

