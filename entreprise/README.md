# Entreprise Microservice

A microservice for managing entreprises using AWS Chalice framework and MongoDB.

## Features

- Create, read, update, and delete entreprises
- Filter and paginate results
- MongoDB integration with PyMongoose
- RESTful API with CORS support

## Model Schema

```
Entreprise:
  - _id: ObjectId (auto-generated)
  - name: string (required)
  - description: string (optional)
  - logo: string (optional)
  - website: string (optional)
  - location: string (optional)
  - createdAt: datetime (auto-generated)
  - createdBy: ObjectId (User ENTREPRISE)
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
Create a `.env` file with:
```
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=JCI
```

## Running Locally

```bash
chalice local --port 8001
```

## API Endpoints

- `POST /entreprises` - Create a new entreprise
- `GET /entreprises` - Get all entreprises (with pagination)
- `GET /entreprises/{id}` - Get entreprise by ID
- `GET /entreprises/name/{name}` - Get entreprise by name
- `PATCH /entreprises/{id}` - Update entreprise
- `DELETE /entreprises/{id}` - Delete entreprise

## Deployment

```bash
chalice deploy
```

## Architecture

The service follows a clean architecture pattern:

- `model.py` - Data models and schemas
- `schema.py` - MongoDB schema definitions
- `service.py` - Business logic layer
- `controller.py` - HTTP request handlers
- `messages.py` - Response messages
- `common/` - Shared utilities and helpers
