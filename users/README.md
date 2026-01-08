# User Microservice

User management microservice built with AWS Chalice and MongoDB.

## Features

- Create, read, update, and delete users
- User roles: ADMIN, ENTREPRISE, EMPLOI, CANDIDAT
- User status management (active, suspended)
- Soft delete functionality
- Email uniqueness validation
- Filtering and pagination

## Installation

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file or set the following environment variables:

```
MONGODB_URI=mongodb://localhost:27017/
DATABASE_NAME=users_db
```

## Running Locally

```bash
chalice local
```

## API Endpoints

### Create User
```
POST /users
Body: {
  "fullName": "John Doe",
  "email": "john@example.com",
  "passwordHash": "hashed_password",
  "role": "CANDIDAT",
  "phone": "+1234567890",
  "status": "active"
}
```

### Get All Users
```
GET /users?role=CANDIDAT&status=active&skip=0&limit=10
```

### Get User by ID
```
GET /users/{id}
```

### Get User by Email
```
GET /users/email/{email}
```

### Update User
```
PATCH /users/{id}
Body: {
  "fullName": "Jane Doe",
  "email": "jane@example.com",
  "phone": "+9876543210",
  "role": "ADMIN",
  "status": "active"
}
```

### Delete User
```
DELETE /users/{id}
```

### Suspend User
```
PATCH /users/{id}/suspend
```

### Activate User
```
PATCH /users/{id}/activate
```

## Project Structure

```
users/
├── app.py                          # Main Chalice application
├── requirements.txt                # Python dependencies
├── chalicelib/
│   ├── config/
│   │   └── mongodb.py             # MongoDB configuration
│   ├── common/
│   │   ├── types/
│   │   │   └── type.py            # Custom types (ObjectIdStr)
│   │   ├── enums/
│   │   │   └── response_type_enum.py  # Response type enums
│   │   ├── exceptions/
│   │   │   └── exception.py       # Custom exceptions
│   │   └── helpers/
│   │       ├── error_middleware.py    # Error handling decorator
│   │       ├── filters.py         # Query filter helper
│   │       └── message_response_helper.py  # Response builder
│   └── modules/
│       ├── __init__.py            # Module exports
│       ├── model.py               # Pydantic models
│       ├── schema.py              # PyMongoose schema
│       ├── service.py             # Business logic
│       ├── controller.py          # Route handlers
│       └── messages.py            # Static messages
```

## Architecture

This microservice follows a layered architecture pattern:

1. **Controller Layer** (`controller.py`): Handles HTTP requests/responses
2. **Service Layer** (`service.py`): Contains business logic
3. **Schema Layer** (`schema.py`): Defines MongoDB schema with PyMongoose
4. **Model Layer** (`model.py`): Pydantic models for validation and serialization

## Deployment

```bash
chalice deploy
```
