"""Employee controller"""
from utils.database import get_db_connection
from utils.validators import validate_required, validate_date, validate_positive_number, sanitize_input

def get_all_employees():
    """Get all employees"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT e.*, s.name as store_name, s.location as store_location
            FROM employee e
            LEFT JOIN store s ON e.store_id = s.store_id
            ORDER BY e.employee_id DESC
        """)
        employees = cursor.fetchall()
        cursor.close()
        return employees, None
    except Exception as e:
        return None, str(e)

def get_employee_by_id(employee_id):
    """Get employee by ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT e.*, s.name as store_name, s.location as store_location
            FROM employee e
            LEFT JOIN store s ON e.store_id = s.store_id
            WHERE e.employee_id = %s
        """, (employee_id,))
        employee = cursor.fetchone()
        cursor.close()
        if not employee:
            return None, "Employee not found"
        return employee, None
    except Exception as e:
        return None, str(e)

def create_employee(data):
    """Create employee"""
    try:
        is_valid, error = validate_required(data, ['name'])
        if not is_valid:
            return None, error
        
        if 'salary' in data and data['salary']:
            is_valid, error = validate_positive_number(data['salary'], 'Salary')
            if not is_valid:
                return None, error
        
        if 'hire_date' in data and data['hire_date']:
            is_valid, error = validate_date(data['hire_date'], 'Hire date')
            if not is_valid:
                return None, error
        
        data = sanitize_input(data)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO employee (name, job_title, hire_date, salary, store_id, email)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data['name'],
            data.get('job_title'),
            data.get('hire_date'),
            data.get('salary'),
            data.get('store_id'),
            data.get('email')
        ))
        employee_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        
        return get_employee_by_id(employee_id)
    except Exception as e:
        return None, str(e)

def update_employee(employee_id, data):
    """Update employee"""
    try:
        if 'salary' in data and data['salary']:
            is_valid, error = validate_positive_number(data['salary'], 'Salary')
            if not is_valid:
                return None, error
        
        if 'hire_date' in data and data['hire_date']:
            is_valid, error = validate_date(data['hire_date'], 'Hire date')
            if not is_valid:
                return None, error
        
        data = sanitize_input(data)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE employee 
            SET name = %s, job_title = %s, hire_date = %s, salary = %s, store_id = %s, email = %s
            WHERE employee_id = %s
        """, (
            data.get('name'),
            data.get('job_title'),
            data.get('hire_date'),
            data.get('salary'),
            data.get('store_id'),
            data.get('email'),
            employee_id
        ))
        conn.commit()
        cursor.close()
        
        return get_employee_by_id(employee_id)
    except Exception as e:
        return None, str(e)

def delete_employee(employee_id):
    """Delete employee"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employee WHERE employee_id = %s", (employee_id,))
        conn.commit()
        cursor.close()
        return True, None
    except Exception as e:
        return False, str(e)

