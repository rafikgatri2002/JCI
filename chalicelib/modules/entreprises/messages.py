"""Entreprise-related messages"""


class Messages:
    """Static messages for entreprise operations"""
    
    # Success messages
    SUCCESS_CREATED = "Entreprise created successfully"
    SUCCESS_UPDATED = "Entreprise updated successfully"
    SUCCESS_DELETED = "Entreprise deleted successfully"
    
    # Error messages
    ERROR_NOT_FOUND = "Entreprise not found"
    REQUIRED_ID = "Entreprise ID is required"
    REQUIRED_NAME = "Name is required"
    REQUIRED_CREATED_BY = "Created by user ID is required"
    UNAUTHORIZED_FIELDS = "Only the following fields can be updated: {allowed_fields}"
    
    # Validation messages
    NAME_EXISTS = "Entreprise with this name already exists"
