"""Application-related messages"""


class Messages:
    """Static messages for application operations"""
    
    # Success messages
    SUCCESS_CREATED = "Application created successfully"
    SUCCESS_UPDATED = "Application updated successfully"
    SUCCESS_DELETED = "Application deleted successfully"
    
    # Error messages
    ERROR_NOT_FOUND = "Application not found"
    REQUIRED_ID = "Application ID is required"
    REQUIRED_JOB_ID = "Job ID is required"
    REQUIRED_CANDIDAT_ID = "Candidat ID is required"
    UNAUTHORIZED_FIELDS = "Only the following fields can be updated: {allowed_fields}"
    
    # Validation messages
    APPLICATION_EXISTS = "Application already exists for this job and candidate"
