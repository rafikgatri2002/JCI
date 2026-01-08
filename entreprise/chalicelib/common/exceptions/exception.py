"""Custom exceptions for the application"""


class UserException(Exception):
    """Base exception for user-related errors"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class UserAlreadyExistsException(UserException):
    """Exception raised when a user already exists"""
    def __init__(self, email: str):
        super().__init__(f"User with email '{email}' already exists")


class UserNotFoundException(UserException):
    """Exception raised when a user is not found"""
    def __init__(self, user_id: str):
        super().__init__(f"User with id '{user_id}' not found")


class EntrepriseException(Exception):
    """Base exception for entreprise-related errors"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class EntrepriseAlreadyExistsException(EntrepriseException):
    """Exception raised when an entreprise already exists"""
    def __init__(self, name: str):
        super().__init__(f"Entreprise with name '{name}' already exists")


class EntrepriseNotFoundException(EntrepriseException):
    """Exception raised when an entreprise is not found"""
    def __init__(self, entreprise_id: str):
        super().__init__(f"Entreprise with id '{entreprise_id}' not found")
