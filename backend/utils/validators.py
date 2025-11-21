"""
Input validation utilities
"""
import re
from datetime import datetime

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number (10 digits)"""
    pattern = r'^\d{10}$'
    return re.match(pattern, phone) is not None

def validate_required(data, fields):
    """Validate required fields"""
    missing = [field for field in fields if field not in data or not data[field]]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"
    return True, None

def validate_positive_number(value, field_name):
    """Validate positive number"""
    try:
        num = float(value)
        if num < 0:
            return False, f"{field_name} must be positive"
        return True, None
    except (ValueError, TypeError):
        return False, f"{field_name} must be a valid number"

def validate_date(date_string, field_name):
    """Validate date format (YYYY-MM-DD)"""
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True, None
    except ValueError:
        return False, f"{field_name} must be in YYYY-MM-DD format"

def sanitize_input(data):
    """Sanitize input data"""
    if isinstance(data, dict):
        return {k: sanitize_input(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_input(item) for item in data]
    elif isinstance(data, str):
        return data.strip()
    return data

