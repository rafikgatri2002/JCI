"""Job-related messages"""


class Messages:
    """Static messages for job operations"""

    # Success messages
    SUCCESS_CREATED = "Job created successfully"
    SUCCESS_UPDATED = "Job updated successfully"
    SUCCESS_DELETED = "Job deleted successfully"

    # Error messages
    ERROR_NOT_FOUND = "Job not found"
    REQUIRED_ID = "Job ID is required"
    REQUIRED_TITLE = "Title is required"
    REQUIRED_ENTREPRISE_ID = "Entreprise ID is required"
    REQUIRED_STATUS = "Status is required"
    REQUIRED_CREATED_BY = "Created by user ID is required"
    UNAUTHORIZED_FIELDS = "Only the following fields can be updated: {allowed_fields}"

    # Validation messages
    INVALID_CONTRACT_TYPE = "Invalid contract type"
    INVALID_STATUS = "Invalid status"
