# JCI API - Unified Microservices Application

This application consolidates all 6 JCI microservices into a single unified API:

- **Users** - User management (`/users`)
- **Jobs** - Job postings management (`/jobs`)
- **Entreprises** - Company management (`/entreprises`)
- **Emplois** - Employment records (`/emplois`)
- **Candidats** - Candidate profiles (`/candidats`)
- **Applications** - Job applications (`/applications`)

## Architecture

The application uses AWS Chalice framework with the following structure:

```
jci-api/
├── app.py                          # Main application with all blueprints
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables
├── .chalice/
│   └── config.json                 # Chalice configuration
└── chalicelib/
    ├── common/                     # Shared utilities
    │   ├── enums/                  # Enumerations
    │   ├── exceptions/             # Custom exceptions
    │   ├── helpers/                # Helper functions
    │   └── types/                  # Custom types
    ├── config/                     # Configuration (MongoDB, etc.)
    └── modules/                    # Feature modules
        ├── users/
        ├── jobs/
        ├── entreprises/
        ├── emplois/
        ├── candidats/
        └── applications/
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables in `.env`:
```
MONGODB_URI=mongodb://localhost:27017/
DATABASE_NAME=JCI
```

3. Run locally:
```bash
chalice local
```

4. Deploy to AWS:
```bash
chalice deploy
```

## API Endpoints

### Root
- `GET /` - API information
- `GET /health` - Health check

### Users
- `POST /users` - Create user
- `GET /users` - List users
- `GET /users/{id}` - Get user by ID
- `GET /users/email/{email}` - Get user by email
- `PATCH /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user

### Jobs
- `POST /jobs` - Create job
- `GET /jobs` - List jobs
- `GET /jobs/{id}` - Get job by ID
- `GET /jobs/entreprise/{entreprise_id}` - Get jobs by company
- `GET /jobs/status/{status}` - Get jobs by status
- `PATCH /jobs/{id}` - Update job
- `DELETE /jobs/{id}` - Delete job

### Entreprises
- `POST /entreprises` - Create company
- `GET /entreprises` - List companies
- `GET /entreprises/{id}` - Get company by ID
- `GET /entreprises/name/{name}` - Get company by name
- `PATCH /entreprises/{id}` - Update company
- `DELETE /entreprises/{id}` - Delete company

### Emplois
- `POST /emplois` - Create employment record
- `GET /emplois` - List employment records
- `GET /emplois/{id}` - Get employment by ID
- `GET /emplois/user/{user_id}/entreprise/{entreprise_id}` - Get by user and company
- `PATCH /emplois/{id}` - Update employment
- `DELETE /emplois/{id}` - Delete employment

### Candidats
- `POST /candidats` - Create candidate
- `GET /candidats` - List candidates
- `GET /candidats/{id}` - Get candidate by ID
- `GET /candidats/user/{user_id}` - Get candidate by user ID
- `PATCH /candidats/{id}` - Update candidate
- `DELETE /candidats/{id}` - Delete candidate

### Applications
- `POST /applications` - Create application
- `GET /applications` - List applications
- `GET /applications/{id}` - Get application by ID
- `GET /applications/job/{job_id}` - Get applications by job
- `GET /applications/candidat/{candidat_id}` - Get applications by candidate
- `PATCH /applications/{id}` - Update application
- `DELETE /applications/{id}` - Delete application

## Features

- **CORS enabled** for all endpoints
- **Unified error handling** across all modules
- **Shared utilities** for consistent behavior
- **MongoDB integration** with Pymongoose
- **Pydantic validation** for request/response models
- **Filtering and pagination** support on list endpoints

## Development

The application follows a modular architecture where each feature is isolated in its own module with:
- `controller.py` - HTTP request handlers
- `service.py` - Business logic
- `model.py` - Pydantic models
- `schema.py` - MongoDB schemas
- `messages.py` - Response messages

All modules share common utilities from `chalicelib/common/`.
