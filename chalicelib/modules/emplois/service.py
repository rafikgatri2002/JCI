"""Emploi service layer for business logic"""

from typing import Any
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel
from pymongoose import methods
from ...common.helpers.filters import Filters
from .model import EmploiModel, EmploiModelResult
from .schema import emploi_schema, EmploiSchema
from ...common.exceptions.exception import EmploiAlreadyExistsException


class EmploiService:
    """Service class for emploi operations"""
    
    def __init__(self):
        self.schema = emploi_schema
        self.collection = emploi_schema.native_collection
    
    def get_all_models(self, filters: Filters):
        """Get all emplois with filtering and pagination"""
        query = filters.apply()
        total_count = self.collection.count_documents(query)
        cursor = self.collection.find(
            query,
            limit=filters.limit,
            skip=filters.skip,
            sort={EmploiModel.createdAt: -1}
        )
        return EmploiModelResult(total=total_count, results=list(cursor))
    
    def get_model(self, _id: str):
        """Get emploi by ID"""
        result = self.collection.find_one({"_id": ObjectId(_id), "deletedAt": None})
        if not result:
            return None
        return EmploiModel.model_validate(result)
    
    def get_by_user_and_entreprise(self, user_id: str, entreprise_id: str):
        """Get emploi by user ID and entreprise ID"""
        result = self.collection.find_one({
            "userId": user_id,
            "entrepriseId": entreprise_id,
            "deletedAt": None
        })
        if not result:
            return None
        return EmploiModel.model_validate(result)
    
    def add_model(self, model: EmploiModel):
        """Create a new emploi"""
        # Check if user already has an emploi at this entreprise
        existing_emploi = self._get_existing_emploi(model)
        if existing_emploi:
            raise EmploiAlreadyExistsException("This user already has an emploi at this entreprise")
        
        # Serialize the model
        serialized_data = model.model_dump(exclude_none=True)
        
        # Add creation metadata
        serialized_data[EmploiModel.createdAt] = datetime.utcnow()
        
        # Insert into MongoDB collection
        inserted_id = methods.insert_one(EmploiSchema.schema_name, serialized_data)
        
        # Return the complete object after insertion
        return self.get_model(inserted_id)
    
    def _get_existing_emploi(self, model: EmploiModel):
        """Check if emploi already exists for user and entreprise"""
        return self.collection.find_one({
            EmploiModel.userId: model.userId,
            EmploiModel.entrepriseId: model.entrepriseId,
            "deletedAt": None
        })

    def update_position(self, _id: str, position: str):
        """Update emploi's position"""
        if position is None:
            return
        obj_id = ObjectId(_id)
        self.schema.update(
            {"_id": obj_id, "deletedAt": None},
            {"$set": {EmploiModel.position: position}}
        )

    def delete_model(self, _id: str):
        """Soft delete an emploi"""
        obj_id = ObjectId(_id)
        result = self.schema.update(
            {"_id": obj_id, "deletedAt": None},
            {"$set": {"deletedAt": datetime.utcnow()}}
        )
        return result.modified_count

    def check_changes(self, existing_emploi_model: BaseModel, emploi_patch_model: BaseModel) -> bool:
        """Check if there are any changes between existing and patch models"""
        for field in emploi_patch_model.model_fields_set:
            new_val = getattr(emploi_patch_model, field)
            old_val = getattr(existing_emploi_model, field, None)
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
