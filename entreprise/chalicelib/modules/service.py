"""Entreprise service layer for business logic"""

from typing import Any
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel
from pymongoose import methods
from ..common.helpers.filters import Filters
from .model import EntrepriseModel, EntrepriseModelResult
from .schema import entreprise_schema, EntrepriseSchema
from ..common.exceptions.exception import EntrepriseAlreadyExistsException


class EntrepriseService:
    """Service class for entreprise operations"""
    
    def __init__(self):
        self.schema = entreprise_schema
        self.collection = entreprise_schema.native_collection

    def get_all_models(self, filters: Filters):
        """Get all entreprises with filtering and pagination"""
        query = filters.apply()
        total_count = self.collection.count_documents(query)
        cursor = self.collection.find(
            query,
            limit=filters.limit,
            skip=filters.skip,
            sort={EntrepriseModel.createdAt: -1}
        )
        return EntrepriseModelResult(total=total_count, results=list(cursor))

    def get_model(self, _id: str):
        """Get entreprise by ID"""
        result = self.collection.find_one({"_id": ObjectId(_id)})
        if not result:
            return None
        return EntrepriseModel.model_validate(result)

    def get_by_name(self, name: str):
        """Get entreprise by name"""
        result = self.collection.find_one({"name": name})
        if not result:
            return None
        return EntrepriseModel.model_validate(result)

    def add_model(self, model: EntrepriseModel):
        """Create a new entreprise"""
        # Check if entreprise with name already exists
        existing_entreprise = self._get_existing_entreprise(model)
        if existing_entreprise:
            raise EntrepriseAlreadyExistsException(model.name)

        # Serialize the model
        serialized_data = model.model_dump(exclude_none=True)

        # Add creation metadata
        serialized_data[EntrepriseModel.createdAt] = datetime.utcnow()
        
        # Insert into MongoDB collection
        inserted_id = methods.insert_one(EntrepriseSchema.schema_name, serialized_data)

        # Return the complete object after insertion
        return self.get_model(inserted_id)

    def _get_existing_entreprise(self, model: EntrepriseModel):
        """Check if entreprise with name already exists"""
        return self.collection.find_one({
            EntrepriseModel.name: model.name
        })

    def update_name(self, _id: str, name: str):
        """Update entreprise's name"""
        if not name:
            return
        obj_id = ObjectId(_id)
        # Check if name already exists for another entreprise
        existing = self.collection.find_one({
            EntrepriseModel.name: name,
            "_id": {"$ne": obj_id}
        })
        if existing:
            raise EntrepriseAlreadyExistsException(name)
        
        self.schema.update(
            {"_id": obj_id},
            {"$set": {EntrepriseModel.name: name}}
        )

    def update_description(self, _id: str, description: str):
        """Update entreprise's description"""
        if description is None:
            return
        obj_id = ObjectId(_id)
        self.schema.update(
            {"_id": obj_id},
            {"$set": {EntrepriseModel.description: description}}
        )

    def update_logo(self, _id: str, logo: str):
        """Update entreprise's logo"""
        if logo is None:
            return
        obj_id = ObjectId(_id)
        self.schema.update(
            {"_id": obj_id},
            {"$set": {EntrepriseModel.logo: logo}}
        )

    def update_website(self, _id: str, website: str):
        """Update entreprise's website"""
        if website is None:
            return
        obj_id = ObjectId(_id)
        self.schema.update(
            {"_id": obj_id},
            {"$set": {EntrepriseModel.website: website}}
        )

    def update_location(self, _id: str, location: str):
        """Update entreprise's location"""
        if location is None:
            return
        obj_id = ObjectId(_id)
        self.schema.update(
            {"_id": obj_id},
            {"$set": {EntrepriseModel.location: location}}
        )

    def delete_model(self, _id: str):
        """Hard delete an entreprise"""
        obj_id = ObjectId(_id)
        result = self.collection.delete_one({"_id": obj_id})
        return result.deleted_count

    def check_changes(self, existing_entreprise_model: BaseModel, entreprise_patch_model: BaseModel) -> bool:
        """Check if there are any changes between existing and patch models"""
        for field in entreprise_patch_model.model_fields_set:
            new_val = getattr(entreprise_patch_model, field)
            old_val = getattr(existing_entreprise_model, field, None)
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
