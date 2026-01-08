"""Application service layer for business logic"""

from typing import Any
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel
from pymongoose import methods
from ...common.helpers.filters import Filters
from .model import ApplicationModel, ApplicationModelResult
from .schema import application_schema, ApplicationSchema
from ...common.exceptions.exception import ApplicationAlreadyExistsException


class ApplicationService:
    """Service class for application operations"""
    
    def __init__(self):
        self.schema = application_schema
        self.collection = application_schema.native_collection
        
    def get_all_models(self, filters: Filters):
        """Get all applications with filtering and pagination"""
        query = filters.apply()
        total_count = self.collection.count_documents(query)
        cursor = self.collection.find(
            query,
            limit=filters.limit,
            skip=filters.skip,
            sort={ApplicationModel.appliedAt: -1}
        )
        return ApplicationModelResult(total=total_count, results=list(cursor))
    
    def get_model(self, _id: str):
        """Get application by ID"""
        result = self.collection.find_one({"_id": ObjectId(_id), "deletedAt": None})
        if not result:
            return None
        return ApplicationModel.model_validate(result)
    
    def get_by_job(self, job_id: str):
        """Get applications by job ID"""
        results = self.collection.find({
            "jobId": job_id,
            "deletedAt": None
        }).sort({ApplicationModel.appliedAt: -1})
        applications = [ApplicationModel.model_validate(result) for result in results]
        return ApplicationModelResult(total=len(applications), results=applications)
    
    def get_by_candidat(self, candidat_id: str):
        """Get applications by candidate ID"""
        results = self.collection.find({
            "candidatId": candidat_id,
            "deletedAt": None
        }).sort({ApplicationModel.appliedAt: -1})
        applications = [ApplicationModel.model_validate(result) for result in results]
        return ApplicationModelResult(total=len(applications), results=applications)
    
    def add_model(self, model: ApplicationModel):
        """Create a new application"""
        # Check if application already exists for this job and candidate
        existing_application = self._get_existing_application(model)
        if existing_application:
            raise ApplicationAlreadyExistsException("Application already exists for this job and candidate")
        
        # Serialize the model
        serialized_data = model.model_dump(exclude_none=True)
        
        # Add creation metadata
        serialized_data[ApplicationModel.appliedAt] = datetime.utcnow()
        serialized_data[ApplicationModel.createdAt] = datetime.utcnow()
        
        # Insert into MongoDB collection
        inserted_id = methods.insert_one(ApplicationSchema.schema_name, serialized_data)
        
        # Return the complete object after insertion
        return self.get_model(inserted_id)
    
    def _get_existing_application(self, model: ApplicationModel):
        """Check if application already exists for job and candidate"""
        return self.collection.find_one({
            ApplicationModel.jobId: model.jobId,
            ApplicationModel.candidatId: model.candidatId,
            "deletedAt": None
        })

    def update_application(self, _id: str, patch_model: BaseModel):
        """Update application fields"""
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
        """Soft delete an application"""
        obj_id = ObjectId(_id)
        result = self.schema.update(
            {"_id": obj_id, "deletedAt": None},
            {"$set": {"deletedAt": datetime.utcnow()}}
        )
        return result.modified_count

    def check_changes(self, existing_application_model: BaseModel, application_patch_model: BaseModel) -> bool:
        """Check if there are any changes between existing and patch models"""
        for field in application_patch_model.model_fields_set:
            new_val = getattr(application_patch_model, field)
            old_val = getattr(existing_application_model, field, None)
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
