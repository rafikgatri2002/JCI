"""Custom exceptions for the application"""


# Base exceptions for each module
class UserException(Exception):
    """Base exception for user-related errors"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class JobException(Exception):
    """Base exception for job-related errors"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class EntrepriseException(Exception):
    """Base exception for entreprise-related errors"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class EmploiException(Exception):
    """Base exception for emploi-related errors"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class CandidatException(Exception):
    """Base exception for candidat-related errors"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ApplicationException(Exception):
    """Base exception for application-related errors"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


# Specific exceptions for each module

# User exceptions
class UserAlreadyExistsException(UserException):
    """Exception raised when a user already exists"""
    def __init__(self, email: str):
        super().__init__(f"User with email '{email}' already exists")


class UserNotFoundException(UserException):
    """Exception raised when a user is not found"""
    def __init__(self, user_id: str):
        super().__init__(f"User with id '{user_id}' not found")


# Job exceptions
class JobAlreadyExistsException(JobException):
    """Exception raised when a job already exists"""
    def __init__(self, message: str = "Job already exists"):
        super().__init__(message)


# Entreprise exceptions
class EntrepriseAlreadyExistsException(EntrepriseException):
    """Exception raised when an entreprise already exists"""
    def __init__(self, message: str = "Entreprise already exists"):
        super().__init__(message)


# Emploi exceptions
class EmploiAlreadyExistsException(EmploiException):
    """Exception raised when an emploi already exists"""
    def __init__(self, message: str = "Emploi already exists"):
        super().__init__(message)


# Candidat exceptions
class CandidatAlreadyExistsException(CandidatException):
    """Exception raised when a candidat already exists"""
    def __init__(self, message: str = "Candidat already exists"):
        super().__init__(message)


# Application exceptions
class ApplicationAlreadyExistsException(ApplicationException):
    """Exception raised when an application already exists"""
    def __init__(self, message: str = "Application already exists"):
        super().__init__(message)
