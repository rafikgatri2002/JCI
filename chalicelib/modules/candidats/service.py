"""Candidat service layer for business logic"""

from typing import Any
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel
from pymongoose import methods
from ...common.helpers.filters import Filters
from .model import CandidatModel, CandidatModelResult
from .schema import candidat_schema, CandidatSchema
from ...common.exceptions.exception import CandidatAlreadyExistsException


class CandidatService:
    """Service class for candidat operations"""
    
    def __init__(self):
        self.schema = candidat_schema
        self.collection = candidat_schema.native_collection
        
    def get_all_models(self, filters: Filters):
        """Get all candidats with filtering and pagination"""
        query = filters.apply()
        total_count = self.collection.count_documents(query)
        cursor = self.collection.find(
            query,
            limit=filters.limit,
            skip=filters.skip,
            sort={CandidatModel.createdAt: -1}
        )
        return CandidatModelResult(total=total_count, results=list(cursor))
    
    def get_model(self, _id: str):
        """Get candidat by ID"""
        result = self.collection.find_one({"_id": ObjectId(_id), "deletedAt": None})
        if not result:
            return None
        return CandidatModel.model_validate(result)
    
    def get_by_user(self, user_id: str):
        """Get candidat by user ID"""
        result = self.collection.find_one({
            "userId": user_id,
            "deletedAt": None
        })
        if not result:
            return None
        return CandidatModel.model_validate(result)
    
    def add_model(self, model: CandidatModel):
        """Create a new candidat"""
        # Check if user already has a candidat profile
        existing_candidat = self._get_existing_candidat(model)
        if existing_candidat:
            raise CandidatAlreadyExistsException("This user already has a candidat profile")
        
        # Serialize the model
        serialized_data = model.model_dump(exclude_none=True)
        
        # Add creation metadata
        serialized_data[CandidatModel.createdAt] = datetime.utcnow()
        
        # Insert into MongoDB collection
        inserted_id = methods.insert_one(CandidatSchema.schema_name, serialized_data)
        
        # Return the complete object after insertion
        return self.get_model(inserted_id)
    
    def _get_existing_candidat(self, model: CandidatModel):
        """Check if candidat already exists for user"""
        return self.collection.find_one({
            CandidatModel.userId: model.userId,
            "deletedAt": None
        })

    def update_candidat(self, _id: str, patch_model: BaseModel):
        """Update candidat fields"""
        obj_id = ObjectId(_id)
        update_data = {}
        
        # Build update data from patch model
        patch_dict = patch_model.model_dump(exclude_none=True)
        for field, value in patch_dict.items():
            if value is not None:
                update_data[field] = value
        
        if not update_data:
            return
        
        self.schema.update(
            {"_id": obj_id, "deletedAt": None},
            {"$set": update_data}
        )

    def delete_model(self, _id: str):
        """Soft delete a candidat"""
        obj_id = ObjectId(_id)
        result = self.schema.update(
            {"_id": obj_id, "deletedAt": None},
            {"$set": {"deletedAt": datetime.utcnow()}}
        )
        return result.modified_count

    def check_changes(self, existing_candidat_model: BaseModel, candidat_patch_model: BaseModel) -> bool:
        """Check if there are any changes between existing and patch models"""
        for field in candidat_patch_model.model_fields_set:
            new_val = getattr(candidat_patch_model, field)
            old_val = getattr(existing_candidat_model, field, None)
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
