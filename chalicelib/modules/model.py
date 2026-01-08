"""User model definition"""

from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from enum import Enum
from ..common.types.type import ObjectIdStr


class Role(str, Enum):
    """User role types"""
    ADMIN = "ADMIN"
    ENTREPRISE = "ENTREPRISE"
    EMPLOI = "EMPLOI"
    CANDIDAT = "CANDIDAT"


class Status(str, Enum):
    """User status types"""
    ACTIVE = "active"
    SUSPENDED = "suspended"


class MetaModel(type(BaseModel)):
    def __getattr__(cls, item):
        if item.startswith('__pydantic_') or item in {'model_fields', '__fields__'}:
            raise AttributeError(f"{cls.__name__} has no attribute {item}")
        if item == "id" and cls == "UserModel":
            return "_id"
        fields = getattr(cls, '__pydantic_fields__', {})
        if item in fields:
            return item
        for field_name, field_info in fields.items():
            field_type = getattr(field_info, 'outer_type_', None) or getattr(field_info, 'type_', None)
            if field_type and isinstance(field_type, type) and issubclass(field_type, BaseModel):
                nested_fields = getattr(field_type, '__fields__', {})
                if item in nested_fields:
                    return f"{field_name}.{item}"
        raise AttributeError(f"{cls.__name__} has no attribute {item}")


class UserModel(BaseModel, metaclass=MetaModel):
    """User model for MongoDB collection"""
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    
    id: ObjectIdStr = Field(alias="_id", default=None)
    fullName: str
    email: str
    passwordHash: str
    role: Role
    phone: str
    status: Optional[Status] = Status.ACTIVE
    createdAt: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    deletedAt: Optional[datetime] = None


class UserPatchModel(BaseModel, metaclass=MetaModel):
    """User patch model for partial updates"""
    model_config = ConfigDict(populate_by_name=True)
    
    fullName: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[Role] = None
    status: Optional[Status] = None


class UserModelResult(BaseModel, metaclass=MetaModel):
    """User result model with pagination"""
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    
    total: int
    results: list[UserModel]
