"""Candidat schema definitions for validation"""

from datetime import datetime, timezone
from bson import CodecOptions
from pymongoose import methods
from pymongoose.mongo_types import Types, Schema
from .model import CandidatModel
from ...config.mongodb import mongo_client

methods.database = mongo_client


class CandidatSchema(Schema):
    schema_name = "Candidat"

    def __init__(self, **kwargs):
        self.schema = {
            CandidatModel.id: {
                "type": Types.ObjectId,
                "required": True,
            },
            CandidatModel.userId: {
                "type": Types.ObjectId,
                "required": True,
            },
            CandidatModel.cvUrl: {
                "type": Types.String,
                "required": False,
            },
            CandidatModel.skills: {
                "required": False,
            },
            CandidatModel.experience: {
                "type": Types.String,
                "required": False,
            },
            CandidatModel.education: {
                "type": Types.String,
                "required": False,
            },
            CandidatModel.createdAt: {
                "type": Types.Date,
                "default": datetime.now,
                "required": False
            },
            CandidatModel.deletedAt: {
                "type": Types.Date,
                "required": False
            },
        }
        super().__init__(self.schema_name, self.schema, kwargs)
        self.native_collection = methods.database.get_collection(
            self.schema_name,
            codec_options=CodecOptions(tz_aware=True, tzinfo=timezone.utc)
        )


candidat_schema = CandidatSchema()
methods.schemas["Candidat"] = candidat_schema
