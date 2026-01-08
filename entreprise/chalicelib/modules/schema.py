"""Entreprise schema definitions for validation"""

from datetime import datetime, timezone
from bson import CodecOptions
from pymongoose import methods
from pymongoose.mongo_types import Types, Schema
from .model import EntrepriseModel
from ..config.mongodb import mongo_client

methods.database = mongo_client


class EntrepriseSchema(Schema):
    schema_name = "Entreprise"

    def __init__(self, **kwargs):
        self.schema = {
            EntrepriseModel.id: {
                "type": Types.ObjectId,
                "required": True,
            },
            EntrepriseModel.name: {
                "type": Types.String,
                "required": True,
            },
            EntrepriseModel.description: {
                "type": Types.String,
                "required": False,
            },
            EntrepriseModel.logo: {
                "type": Types.String,
                "required": False,
            },
            EntrepriseModel.website: {
                "type": Types.String,
                "required": False,
            },
            EntrepriseModel.location: {
                "type": Types.String,
                "required": False,
            },
            EntrepriseModel.createdAt: {
                "type": Types.Date,
                "default": datetime.now,
                "required": False
            },
            EntrepriseModel.createdBy: {
                "type": Types.ObjectId,
                "required": True,
            },
        }
        super().__init__(self.schema_name, self.schema, kwargs)
        self.native_collection = methods.database.get_collection(
            self.schema_name,
            codec_options=CodecOptions(tz_aware=True, tzinfo=timezone.utc)
        )


entreprise_schema = EntrepriseSchema()
methods.schemas["Entreprise"] = entreprise_schema
