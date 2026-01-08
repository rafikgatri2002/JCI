"""Job schema definitions for validation"""

from datetime import datetime, timezone
from bson import CodecOptions
from pymongoose import methods
from pymongoose.mongo_types import Types, Schema
from .model import JobModel
from ...config.mongodb import mongo_client

methods.database = mongo_client


class JobSchema(Schema):
    schema_name = "Job"

    def __init__(self, **kwargs):
        self.schema = {
            JobModel.id: {
                "type": Types.ObjectId,
                "required": True,
            },
            JobModel.title: {
                "type": Types.String,
                "required": True,
            },
            JobModel.description: {
                "type": Types.String,
                "required": True,
            },
            JobModel.location: {
                "type": Types.String,
                "required": True,
            },
            JobModel.contractType: {
                "type": Types.String,
                "required": True,
            },
            JobModel.remote: {
                "type": Types.Boolean,
                "default": False,
                "required": False,
            },
            JobModel.salaryRange: {
                "type": Types.String,
                "required": False,
            },
            JobModel.entrepriseId: {
                "type": Types.ObjectId,
                "required": True,
            },
            JobModel.createdBy: {
                "type": Types.ObjectId,
                "required": True,
            },
            JobModel.status: {
                "type": Types.String,
                "default": "draft",
                "required": False,
            },
            JobModel.createdAt: {
                "type": Types.Date,
                "default": datetime.now,
                "required": False
            },
            JobModel.expiresAt: {
                "type": Types.Date,
                "required": False,
            },
        }
        super().__init__(self.schema_name, self.schema, kwargs)
        self.native_collection = methods.database.get_collection(
            self.schema_name,
            codec_options=CodecOptions(tz_aware=True, tzinfo=timezone.utc)
        )


job_schema = JobSchema()
methods.schemas["Job"] = job_schema
