"""Job service layer for business logic"""

from typing import Any
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel
from pymongoose import methods
from ...common.helpers.filters import Filters
from .model import JobModel, JobModelResult
from .schema import job_schema, JobSchema
from ...common.exceptions.exception import JobAlreadyExistsException


class JobService:
    """Service class for job operations"""

    def __init__(self):
        self.schema = job_schema
        self.collection = job_schema.native_collection

    def get_all_models(self, filters: Filters):
        """Get all jobs with filtering and pagination"""
        query = filters.apply()
        total_count = self.collection.count_documents(query)
        cursor = self.collection.find(
            query,
            limit=filters.limit,
            skip=filters.skip,
            sort={JobModel.createdAt: -1}
        )
        return JobModelResult(total=total_count, results=list(cursor))

    def get_model(self, _id: str):
        """Get job by ID"""
        result = self.collection.find_one({"_id": ObjectId(_id)})
        if not result:
            return None
        return JobModel.model_validate(result)

    def get_by_entreprise(self, entreprise_id: str, filters: Filters = None):
        """Get all jobs for a specific entreprise"""
        if filters is None:
            filters = Filters()
        # Add entreprise filter to existing filters
        query = filters.apply()
        # Store as string since ObjectIdStr serializes to string in MongoDB
        query[JobModel.entrepriseId] = entreprise_id
        
        total_count = self.collection.count_documents(query)
        cursor = self.collection.find(
            query,
            limit=filters.limit,
            skip=filters.skip,
            sort={JobModel.createdAt: -1}
        )
        return JobModelResult(total=total_count, results=list(cursor))

    def get_by_status(self, status: str, filters: Filters = None):
        """Get all jobs with a specific status"""
        if filters is None:
            filters = Filters()
        query = filters.apply()
        query[JobModel.status] = status
        
        total_count = self.collection.count_documents(query)
        cursor = self.collection.find(
            query,
            limit=filters.limit,
            skip=filters.skip,
            sort={JobModel.createdAt: -1}
        )
        return JobModelResult(total=total_count, results=list(cursor))

    def add_model(self, model: JobModel):
        """Create a new job"""
        # Serialize the model
        serialized_data = model.model_dump(exclude_none=True)

        # Add creation metadata
        serialized_data[JobModel.createdAt] = datetime.utcnow()

        # Insert into MongoDB collection
        inserted_id = methods.insert_one(JobSchema.schema_name, serialized_data)

        # Return the complete object after insertion
        return self.get_model(inserted_id)

    def update_title(self, _id: str, title: str):
        """Update job's title"""
        if not title:
            return
        obj_id = ObjectId(_id)
        self.schema.update(
            {"_id": obj_id},
            {"$set": {JobModel.title: title}}
        )

    def update_description(self, _id: str, description: str):
        """Update job's description"""
        if description is None:
            return
        obj_id = ObjectId(_id)
        self.schema.update(
            {"_id": obj_id},
            {"$set": {JobModel.description: description}}
        )

    def update_location(self, _id: str, location: str):
        """Update job's location"""
        if location is None:
            return
        obj_id = ObjectId(_id)
        self.schema.update(
            {"_id": obj_id},
            {"$set": {JobModel.location: location}}
        )

    def update_contract_type(self, _id: str, contract_type: str):
        """Update job's contract type"""
        if contract_type is None:
            return
        obj_id = ObjectId(_id)
        self.schema.update(
            {"_id": obj_id},
            {"$set": {JobModel.contractType: contract_type}}
        )

    def update_remote(self, _id: str, remote: bool):
        """Update job's remote status"""
        if remote is None:
            return
        obj_id = ObjectId(_id)
        self.schema.update(
            {"_id": obj_id},
            {"$set": {JobModel.remote: remote}}
        )

    def update_salary_range(self, _id: str, salary_range: str):
        """Update job's salary range"""
        if salary_range is None:
            return
        obj_id = ObjectId(_id)
        self.schema.update(
            {"_id": obj_id},
            {"$set": {JobModel.salaryRange: salary_range}}
        )

    def update_entreprise_id(self, _id: str, entreprise_id: str):
        """Update job's entreprise"""
        if entreprise_id is None:
            return
        obj_id = ObjectId(_id)
        self.schema.update(
            {"_id": obj_id},
            {"$set": {JobModel.entrepriseId: entreprise_id}}
        )

    def update_status(self, _id: str, status: str):
        """Update job's status"""
        if status is None:
            return
        obj_id = ObjectId(_id)
        self.schema.update(
            {"_id": obj_id},
            {"$set": {JobModel.status: status}}
        )

    def update_expires_at(self, _id: str, expires_at: datetime):
        """Update job's expiration date"""
        if expires_at is None:
            return
        obj_id = ObjectId(_id)
        self.schema.update(
            {"_id": obj_id},
            {"$set": {JobModel.expiresAt: expires_at}}
        )

    def delete_model(self, _id: str):
        """Hard delete a job"""
        obj_id = ObjectId(_id)
        result = self.collection.delete_one({"_id": obj_id})
        return result.deleted_count

    def check_changes(self, existing_job_model: BaseModel, job_patch_model: BaseModel) -> bool:
        """Check if there are any changes between existing and patch models"""
        for field in job_patch_model.model_fields_set:
            new_val = getattr(job_patch_model, field)
            old_val = getattr(existing_job_model, field, None)
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
