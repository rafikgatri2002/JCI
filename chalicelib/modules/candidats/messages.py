"""Candidat-related messages"""


class Messages:
    """Static messages for candidat operations"""
    
    # Success messages
    SUCCESS_CREATED = "Candidat created successfully"
    SUCCESS_UPDATED = "Candidat updated successfully"
    SUCCESS_DELETED = "Candidat deleted successfully"
    
    # Error messages
    ERROR_NOT_FOUND = "Candidat not found"
    REQUIRED_ID = "Candidat ID is required"
    REQUIRED_USER_ID = "User ID is required"
    UNAUTHORIZED_FIELDS = "Only the following fields can be updated: {allowed_fields}"
    
    # Validation messages
    CANDIDAT_EXISTS = "This user already has a candidat profile"
