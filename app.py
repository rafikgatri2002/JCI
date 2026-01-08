"""JCI API - Unified application for all microservices"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from chalicelib.modules.users.controller import router as users_router
from chalicelib.modules.jobs.controller import router as jobs_router
from chalicelib.modules.entreprises.controller import router as entreprises_router
from chalicelib.modules.emplois.controller import router as emplois_router
from chalicelib.modules.candidats.controller import router as candidats_router
from chalicelib.modules.applications.controller import router as applications_router

app = FastAPI(title='JCI API', version='1.0.0')

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Content-Type", "Authorization"],
    expose_headers=["Content-Length"],
    max_age=600
)

# Register all module routers
app.include_router(users_router)
app.include_router(jobs_router)
app.include_router(entreprises_router)
app.include_router(emplois_router)
app.include_router(candidats_router)
app.include_router(applications_router)


@app.get('/')
def index():
    """Main API endpoint"""
    return {
        'service': 'JCI API',
        'status': 'running',
        'version': '1.0.0',
        'modules': [
            'users',
            'jobs',
            'entreprises',
            'emplois',
            'candidats',
            'applications'
        ]
    }


@app.get('/health')
def health():
    """Health check endpoint"""
    return {
        'status': 'healthy',
        'modules': {
            'users': 'active',
            'jobs': 'active',
            'entreprises': 'active',
            'emplois': 'active',
            'candidats': 'active',
            'applications': 'active'
        }
    }
