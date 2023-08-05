import re

def sanitize_input(input_str):
    input_str = input_str.strip()
    input_str = remove_special_characters(input_str)
    input_str = remove_consecutive_whitespaces(input_str)
    input_str = input_str.lower()
    return input_str

def remove_special_characters(input_str):
    input_str = re.sub(r"[^\w\s@.-]", "", input_str)
    return input_str

def remove_consecutive_whitespaces(input_str):
    input_str = re.sub(r"\s+", " ", input_str)
    return input_str

def validate_email(email):
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    return re.match(email_regex, email) is not None

def is_secure_password(password):
    if len(password) < 8:
        return False

    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False

    # Check for special characters
    if not any(char in "!@#$%^&*()-_=+{}[]|;:,<.>/?`~" for char in password):
        return False

    return True