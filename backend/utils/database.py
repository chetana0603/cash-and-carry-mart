"""
Database initialization and connection utilities
"""
import os
import mysql.connector
from mysql.connector import Error
from flask import current_app, g
from contextlib import contextmanager

# Global database connection
db_connection = None

def get_db_connection():
    """Get MySQL database connection - creates a new connection each time and stores in g"""
    if 'db_conn' not in g:
        try:
            g.db_conn = mysql.connector.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['MYSQL_DATABASE'],
                port=current_app.config['MYSQL_PORT'],
                autocommit=False
            )
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            raise
    return g.db_conn

def close_db_connection(e=None):
    """Close database connection"""
    conn = g.pop('db_conn', None)
    if conn is not None and conn.is_connected():
        conn.close()

def execute_sql_file(file_path):
    """Execute SQL file to initialize database"""
    try:
        # Read SQL file
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_script = file.read()
        
        # Connect without database first to create it
        conn = mysql.connector.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            port=current_app.config['MYSQL_PORT']
        )
        cursor = conn.cursor()
        
        # Split script by semicolons, but handle DELIMITER statements
        statements = []
        current = ""
        delimiter = ";"
        i = 0
        
        while i < len(sql_script):
            # Check for DELIMITER statement
            if sql_script[i:i+9].upper() == "DELIMITER":
                end_line = sql_script.find('\n', i)
                if end_line != -1:
                    delimiter = sql_script[i+9:end_line].strip()
                    i = end_line + 1
                    continue
            elif i + len(delimiter) <= len(sql_script) and sql_script[i:i+len(delimiter)] == delimiter:
                if current.strip():
                    statements.append(current.strip())
                current = ""
                i += len(delimiter)
                continue
            
            current += sql_script[i]
            i += 1
        
        if current.strip():
            statements.append(current.strip())
        
        # Execute each statement (skip DROP DATABASE to preserve data)
        for statement in statements:
            if statement.strip() and not statement.strip().startswith('--'):
                # Skip DROP DATABASE statements to preserve existing data
                if 'DROP DATABASE' in statement.upper():
                    print("⚠️  Skipping DROP DATABASE statement to preserve existing data")
                    continue
                # Skip INSERT statements that add sample data
                if statement.strip().upper().startswith('INSERT INTO') and 'SAMPLE' in sql_script.upper():
                    # Check if we're in the sample data section
                    continue
                try:
                    # Execute multi-statement queries
                    for result in cursor.execute(statement, multi=True):
                        if result:
                            pass
                except Error as e:
                    # Ignore expected errors
                    error_msg = str(e)
                    if "Unknown database" not in error_msg and "doesn't exist" not in error_msg and "already exists" not in error_msg:
                        print(f"Warning executing statement: {e}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("Database initialized successfully from SQL file")
        return True
        
    except Error as e:
        print(f"Error executing SQL file: {e}")
        return False

def init_database(app):
    """Initialize database connection and create tables if needed (preserves existing data)"""
    with app.app_context():
        # Use schema-only file that doesn't drop database or insert sample data
        sql_file_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            '..', 'database', 'mini_database_schema.sql'
        )
        
        # Fallback to original file if schema file doesn't exist
        if not os.path.exists(sql_file_path):
            sql_file_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                '..', 'database', 'mini_database.sql'
            )
        
        # Check if database exists
        try:
            conn = mysql.connector.connect(
                host=app.config['MYSQL_HOST'],
                user=app.config['MYSQL_USER'],
                password=app.config['MYSQL_PASSWORD'],
                port=app.config['MYSQL_PORT']
            )
            cursor = conn.cursor()
            cursor.execute("SHOW DATABASES LIKE %s", (app.config['MYSQL_DATABASE'],))
            db_exists = cursor.fetchone() is not None
            cursor.close()
            conn.close()
            
            if not db_exists:
                print("Database not found. Creating database and tables (no sample data)...")
                execute_sql_file(sql_file_path)
            else:
                # Database exists - just ensure tables exist (preserve existing data)
                print("Database exists. Ensuring all tables are created (preserving existing data)...")
                conn = mysql.connector.connect(
                    host=app.config['MYSQL_HOST'],
                    user=app.config['MYSQL_USER'],
                    password=app.config['MYSQL_PASSWORD'],
                    database=app.config['MYSQL_DATABASE'],
                    port=app.config['MYSQL_PORT']
                )
                cursor = conn.cursor()
                
                # Execute schema file to create missing tables (CREATE TABLE IF NOT EXISTS)
                # This will only create tables that don't exist, preserving all existing data
                try:
                    with open(sql_file_path, 'r', encoding='utf-8') as file:
                        sql_script = file.read()
                    
                    # Execute statements that create tables (they use IF NOT EXISTS)
                    statements = []
                    current = ""
                    delimiter = ";"
                    i = 0
                    
                    while i < len(sql_script):
                        if sql_script[i:i+9].upper() == "DELIMITER":
                            end_line = sql_script.find('\n', i)
                            if end_line != -1:
                                delimiter = sql_script[i+9:end_line].strip()
                                i = end_line + 1
                                continue
                        elif i + len(delimiter) <= len(sql_script) and sql_script[i:i+len(delimiter)] == delimiter:
                            if current.strip():
                                statements.append(current.strip())
                            current = ""
                            i += len(delimiter)
                            continue
                        
                        current += sql_script[i]
                        i += 1
                    
                    if current.strip():
                        statements.append(current.strip())
                    
                    # Execute only CREATE statements (they use IF NOT EXISTS so safe)
                    for statement in statements:
                        if statement.strip() and not statement.strip().startswith('--'):
                            if 'CREATE' in statement.upper() or 'DROP PROCEDURE' in statement.upper() or 'DROP FUNCTION' in statement.upper() or 'DROP TRIGGER' in statement.upper():
                                try:
                                    for result in cursor.execute(statement, multi=True):
                                        if result:
                                            pass
                                except Error as e:
                                    # Ignore "already exists" errors
                                    error_msg = str(e)
                                    if "already exists" not in error_msg.lower() and "duplicate" not in error_msg.lower():
                                        print(f"Warning: {e}")
                    
                    conn.commit()
                    print("✅ All tables and procedures verified/created (existing data preserved)")
                    
                except Exception as e:
                    print(f"Warning executing schema: {e}")
                
                # Check if user table exists and create admin if needed
                cursor.execute("SHOW TABLES LIKE 'user'")
                user_table_exists = cursor.fetchone() is not None
                
                if not user_table_exists:
                    # Create user table for authentication
                    create_user_table_sql = """
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
                    """
                    cursor.execute(create_user_table_sql)
                    conn.commit()
                    print("✅ User table created")
                
                # Create default admin user only if it doesn't exist
                from werkzeug.security import generate_password_hash
                cursor.execute("SELECT username FROM user WHERE username = 'admin'")
                admin_exists = cursor.fetchone() is not None
                
                if not admin_exists:
                    admin_password = generate_password_hash('admin123')
                    cursor.execute("""
                        INSERT INTO user (username, password_hash, role) 
                        VALUES ('admin', %s, 'ADMIN')
                    """, (admin_password,))
                    conn.commit()
                    print("✅ Default admin user created (username: admin, password: admin123)")
                else:
                    print("✅ Admin user already exists")
                
                cursor.close()
                conn.close()
                
        except Error as e:
            print(f"Error initializing database: {e}")
            # Try to create database from SQL file (only if database doesn't exist)
            if not db_exists:
                execute_sql_file(sql_file_path)

# Placeholder for db object (using raw MySQL connector instead of SQLAlchemy for stored procedures)
db = None

