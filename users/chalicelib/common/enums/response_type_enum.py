"""Response type enumeration"""
from enum import Enum


class ResponseTypeEnum(str, Enum):
    """Response type enumeration"""
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
