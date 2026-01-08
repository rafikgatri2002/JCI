"""Message response helper"""
from ..enums.response_type_enum import ResponseTypeEnum


class MessageResponseHelper:
    """Helper class to build standardized message responses"""
    
    @staticmethod
    def build(response_type: ResponseTypeEnum, message: str) -> dict:
        """
        Build a standardized message response
        
        Args:
            response_type: Type of response (success, error, warning)
            message: Message to include in response
            
        Returns:
            Dictionary with type and message
        """
        return {
            "type": response_type.value,
            "message": message
        }
