"""User service layer for business logic"""

from typing import Any
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel
from pymongoose import methods
from ...common.helpers.filters import Filters
from .model import UserModel, UserModelResult
from .schema import user_schema, UserSchema
from ...common.exceptions.exception import UserAlreadyExistsException


class UserService:
    """Service class for user operations"""
    
    def __init__(self):
        self.schema = user_schema
        self.collection = user_schema.native_collection

    def get_all_models(self, filters: Filters):
        """Get all users with filtering and pagination"""
        query = filters.apply()
        total_count = self.collection.count_documents(query)
        cursor = self.collection.find(
            query,
            limit=filters.limit,
            skip=filters.skip,
            sort={UserModel.createdAt: -1}
        )
        return UserModelResult(total=total_count, results=list(cursor))

    def get_model(self, _id: str):
        """Get user by ID"""
        result = self.collection.find_one({"_id": ObjectId(_id), **Filters.deleted_at_filter})
        if not result:
            return None
        return UserModel.model_validate(result)

    def get_by_email(self, email: str):
        """Get user by email"""
        result = self.collection.find_one({"email": email.lower(), **Filters.deleted_at_filter})
        if not result:
            return None
        return UserModel.model_validate(result)

    def add_model(self, model: UserModel):
        """Create a new user"""
        # Check if user with email already exists
        existing_user = self._get_existing_user(model)
        if existing_user:
            raise UserAlreadyExistsException(model.email)

        # Serialize the model
        serialized_data = model.model_dump(exclude_none=True)

        # Add creation/update metadata
        serialized_data[UserModel.createdAt] = datetime.utcnow()
        serialized_data[UserModel.updatedAt] = datetime.utcnow()
        
        # Convert email to lowercase
        serialized_data[UserModel.email] = serialized_data[UserModel.email].lower()

        # Insert into MongoDB collection
        inserted_id = methods.insert_one(UserSchema.schema_name, serialized_data)

        # Return the complete object after insertion
        return self.get_model(inserted_id)

    def _get_existing_user(self, model: UserModel):
        """Check if user with email already exists"""
        return self.collection.find_one({
            UserModel.email: model.email.lower(),
            **Filters.deleted_at_filter
        })

    def update_full_name(self, _id: str, fullName: str):
        """Update user's full name"""
        if not fullName:
            return
        obj_id = ObjectId(_id)
        self.schema.update(
            {"_id": obj_id, **Filters.deleted_at_filter},
            {"$set": {UserModel.fullName: fullName, UserModel.updatedAt: datetime.utcnow()}}
        )

    def update_email(self, _id: str, email: str):
        """Update user's email"""
        if not email:
            return
        obj_id = ObjectId(_id)
        # Check if email already exists for another user
        existing = self.collection.find_one({
            UserModel.email: email.lower(),
            "_id": {"$ne": obj_id},
            **Filters.deleted_at_filter
        })
        if existing:
            raise UserAlreadyExistsException(email)
        
        self.schema.update(
            {"_id": obj_id, **Filters.deleted_at_filter},
            {"$set": {UserModel.email: email.lower(), UserModel.updatedAt: datetime.utcnow()}}
        )

    def update_phone(self, _id: str, phone: str):
        """Update user's phone"""
        if not phone:
            return
        obj_id = ObjectId(_id)
        self.schema.update(
            {"_id": obj_id, **Filters.deleted_at_filter},
            {"$set": {UserModel.phone: phone, UserModel.updatedAt: datetime.utcnow()}}
        )

    def update_role(self, _id: str, role: str):
        """Update user's role"""
        if not role:
            return
        obj_id = ObjectId(_id)
        self.schema.update(
            {"_id": obj_id, **Filters.deleted_at_filter},
            {"$set": {UserModel.role: role, UserModel.updatedAt: datetime.utcnow()}}
        )

    def update_status(self, _id: str, status: str):
        """Update user's status"""
        if not status:
            return
        obj_id = ObjectId(_id)
        self.schema.update(
            {"_id": obj_id, **Filters.deleted_at_filter},
            {"$set": {UserModel.status: status, UserModel.updatedAt: datetime.utcnow()}}
        )

    def delete_model(self, _id: str):
        """Soft delete a user"""
        obj_id = ObjectId(_id)
        count = self.schema.update(
            {"_id": obj_id, **Filters.deleted_at_filter},
            {"$set": {UserModel.deletedAt: datetime.utcnow()}}
        )
        return count

    def check_changes(self, existing_user_model: BaseModel, user_patch_model: BaseModel) -> bool:
        """Check if there are any changes between existing and patch models"""
        for field in user_patch_model.model_fields_set:
            new_val = getattr(user_patch_model, field)
            old_val = getattr(existing_user_model, field, None)
            if self._to_plain(new_val) != self._to_plain(old_val):
                return True
        return False

    def _to_plain(self, value: Any) -> Any:
        """Convert value to plain representation for comparison"""
        if isinstance(value, BaseModel):
            return value.model_dump(exclude_none=True)
        if isinstance(value, dict):
            return {k: self._to_plain(v) for k, v in value.items()}
        if isinstance(value, (list, tuple)):
            return [self._to_plain(v) for v in value]
        return value
