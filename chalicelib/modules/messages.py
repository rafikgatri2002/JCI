"""User-related messages"""


class Messages:
    """Static messages for user operations"""
    
    # Success messages
    SUCCESS_CREATED = "User created successfully"
    SUCCESS_UPDATED = "User updated successfully"
    SUCCESS_DELETED = "User deleted successfully"
    SUCCESS_SUSPENDED = "User suspended successfully"
    SUCCESS_ACTIVATED = "User activated successfully"
    
    # Error messages
    ERROR_NOT_FOUND = "User not found"
    REQUIRED_ID = "User ID is required"
    REQUIRED_EMAIL = "Email is required"
    INVALID_EMAIL = "Invalid email format"
    INVALID_ROLE = "Invalid role value"
    INVALID_STATUS = "Invalid status value"
    UNAUTHORIZED_FIELDS = "Only the following fields can be updated: {allowed_fields}"
    
    # Validation messages
    EMAIL_EXISTS = "User with this email already exists"
    WEAK_PASSWORD = "Password is too weak"
