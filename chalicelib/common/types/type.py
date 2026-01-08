"""Custom types for the application"""
from typing import Annotated, Any
from bson import ObjectId
from pydantic import BeforeValidator, PlainSerializer, WithJsonSchema


def validate_object_id(v: Any) -> ObjectId:
    """Validate and convert to ObjectId"""
    if isinstance(v, ObjectId):
        return v
    if isinstance(v, str):
        return ObjectId(v)
    raise ValueError("Invalid ObjectId")


def serialize_object_id(v: ObjectId) -> str:
    """Serialize ObjectId to string"""
    return str(v)


ObjectIdStr = Annotated[
    ObjectId,
    BeforeValidator(validate_object_id),
    PlainSerializer(serialize_object_id, return_type=str),
    WithJsonSchema({"type": "string"}, mode="serialization"),
]
