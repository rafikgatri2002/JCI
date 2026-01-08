"""Emploi schema definitions for validation"""

from datetime import datetime, timezone
from bson import CodecOptions
from pymongoose import methods
from pymongoose.mongo_types import Types, Schema
from .model import EmploiModel
from ...config.mongodb import mongo_client

methods.database = mongo_client


class EmploiSchema(Schema):
    schema_name = "Emploi"

    def __init__(self, **kwargs):
        self.schema = {
            EmploiModel.id: {
                "type": Types.ObjectId,
                "required": True,
            },
            EmploiModel.userId: {
                "type": Types.ObjectId,
                "required": True,
            },
            EmploiModel.entrepriseId: {
                "type": Types.ObjectId,
                "required": True,
            },
            EmploiModel.position: {
                "type": Types.String,
                "required": True,
            },
            EmploiModel.createdAt: {
                "type": Types.Date,
                "default": datetime.now,
                "required": False
            },
            EmploiModel.deletedAt: {
                "type": Types.Date,
                "required": False
            },
        }
        super().__init__(self.schema_name, self.schema, kwargs)
        self.native_collection = methods.database.get_collection(
            self.schema_name,
            codec_options=CodecOptions(tz_aware=True, tzinfo=timezone.utc)
        )


emploi_schema = EmploiSchema()
methods.schemas["Emploi"] = emploi_schema
