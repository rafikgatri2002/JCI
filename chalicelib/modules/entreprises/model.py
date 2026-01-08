"""Entreprise model definition"""

from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from ...common.types.type import ObjectIdStr


class MetaModel(type(BaseModel)):
    def __getattr__(cls, item):
        if item.startswith('__pydantic_') or item in {'model_fields', '__fields__'}:
            raise AttributeError(f"{cls.__name__} has no attribute {item}")
        if item == "id" and cls == "EntrepriseModel":
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


class EntrepriseModel(BaseModel, metaclass=MetaModel):
    """Entreprise model for MongoDB collection"""
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    
    id: ObjectIdStr = Field(alias="_id", default=None)
    name: str
    description: Optional[str] = None
    logo: Optional[str] = None
    website: Optional[str] = None
    location: Optional[str] = None
    createdAt: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    createdBy: ObjectIdStr  # User ENTREPRISE


class EntreprisePatchModel(BaseModel, metaclass=MetaModel):
    """Entreprise patch model for partial updates"""
    model_config = ConfigDict(populate_by_name=True)
    
    name: Optional[str] = None
    description: Optional[str] = None
    logo: Optional[str] = None
    website: Optional[str] = None
    location: Optional[str] = None


class EntrepriseModelResult(BaseModel, metaclass=MetaModel):
    """Entreprise result model with pagination"""
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    
    total: int
    results: list[EntrepriseModel]
