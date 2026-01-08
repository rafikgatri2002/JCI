"""Application schema definitions for validation"""

from datetime import datetime, timezone
from bson import CodecOptions
from pymongoose import methods
from pymongoose.mongo_types import Types, Schema
from .model import ApplicationModel
from ...config.mongodb import mongo_client

methods.database = mongo_client


class ApplicationSchema(Schema):
    schema_name = "Application"

    def __init__(self, **kwargs):
        self.schema = {
            ApplicationModel.id: {
                "type": Types.ObjectId,
                "required": True,
            },
            ApplicationModel.jobId: {
                "type": Types.ObjectId,
                "required": True,
            },
            ApplicationModel.candidatId: {
                "type": Types.ObjectId,
                "required": True,
            },
            ApplicationModel.cvUrl: {
                "type": Types.String,
                "required": False,
            },
            ApplicationModel.coverLetter: {
                "type": Types.String,
                "required": False,
            },
            ApplicationModel.status: {
                "type": Types.String,
                "required": True,
                "default": "submitted",
            },
            ApplicationModel.appliedAt: {
                "type": Types.Date,
                "default": datetime.now,
                "required": False
            },
            ApplicationModel.createdAt: {
                "type": Types.Date,
                "default": datetime.now,
                "required": False
            },
            ApplicationModel.deletedAt: {
                "type": Types.Date,
                "required": False
            },
        }
        super().__init__(self.schema_name, self.schema, kwargs)
        self.native_collection = methods.database.get_collection(
            self.schema_name,
            codec_options=CodecOptions(tz_aware=True, tzinfo=timezone.utc)
        )


application_schema = ApplicationSchema()
methods.schemas["Application"] = application_schema
