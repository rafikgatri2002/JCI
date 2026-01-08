"""User schema definitions for validation"""

from datetime import datetime, timezone
from bson import CodecOptions
from pymongoose import methods
from pymongoose.mongo_types import Types, Schema
from .model import UserModel
from ..config.mongodb import mongo_client

methods.database = mongo_client


class UserSchema(Schema):
    schema_name = "User"

    def __init__(self, **kwargs):
        self.schema = {
            UserModel.id: {
                "type": Types.ObjectId,
                "required": True,
            },
            UserModel.fullName: {
                "type": Types.String,
                "required": True,
            },
            UserModel.email: {
                "type": Types.String,
                "required": True,
            },
            UserModel.passwordHash: {
                "type": Types.String,
                "required": True,
            },
            UserModel.role: {
                "type": Types.String,
                "enum": ["ADMIN", "ENTREPRISE", "EMPLOI", "CANDIDAT"],
                "required": True
            },
            UserModel.phone: {
                "type": Types.String,
                "required": True,
            },
            UserModel.status: {
                "type": Types.String,
                "enum": ["active", "suspended"],
                "required": True
            },
            UserModel.createdAt: {
                "type": Types.Date,
                "default": datetime.now,
                "required": False
            },
            UserModel.updatedAt: {
                "type": Types.Date,
                "default": datetime.now,
                "required": False
            },
            UserModel.deletedAt: {
                "type": Types.Date,
                "required": False
            },
        }
        super().__init__(self.schema_name, self.schema, kwargs)
        self.native_collection = methods.database.get_collection(
            self.schema_name,
            codec_options=CodecOptions(tz_aware=True, tzinfo=timezone.utc)
        )


user_schema = UserSchema()
methods.schemas["User"] = user_schema
