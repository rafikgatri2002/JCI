"""MongoDB client configuration"""
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get MongoDB connection string from environment variable
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'JCI')

# Create MongoDB client
mongo_client = MongoClient(MONGODB_URI)[DATABASE_NAME]
