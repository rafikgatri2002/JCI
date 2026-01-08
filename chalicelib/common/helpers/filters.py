"""Filters helper for query building"""
from typing import Optional, Dict, Any


class Filters:
    """Helper class for building MongoDB queries with filtering and pagination"""
    
    # Filter for non-deleted documents
    deleted_at_filter = {"deletedAt": None}
    
    def __init__(
        self,
        role: Optional[str] = None,
        status: Optional[str] = None,
        email: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
        **kwargs
    ):
        """
        Initialize filters
        
        Args:
            role: Filter by role
            status: Filter by status
            email: Filter by email
            skip: Number of documents to skip
            limit: Maximum number of documents to return
        """
        self.role = role
        self.status = status
        self.email = email
        self.skip = int(skip) if skip else 0
        self.limit = int(limit) if limit else 100
        
    def apply(self) -> Dict[str, Any]:
        """
        Build MongoDB query from filters
        
        Returns:
            Dictionary representing MongoDB query
        """
        query = {**self.deleted_at_filter}
        
        if self.role:
            query["role"] = self.role
            
        if self.status:
            query["status"] = self.status
            
        if self.email:
            query["email"] = self.email.lower()
            
        return query
