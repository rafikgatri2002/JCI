"""Emploi-related messages"""


class Messages:
    """Static messages for emploi operations"""
    
    # Success messages
    SUCCESS_CREATED = "Emploi created successfully"
    SUCCESS_UPDATED = "Emploi updated successfully"
    SUCCESS_DELETED = "Emploi deleted successfully"
    
    # Error messages
    ERROR_NOT_FOUND = "Emploi not found"
    REQUIRED_ID = "Emploi ID is required"
    REQUIRED_USER_ID = "User ID is required"
    REQUIRED_ENTREPRISE_ID = "Entreprise ID is required"
    REQUIRED_POSITION = "Position is required"
    UNAUTHORIZED_FIELDS = "Only the following fields can be updated: {allowed_fields}"
    
    # Validation messages
    EMPLOI_EXISTS = "This user already has an emploi at this entreprise"
