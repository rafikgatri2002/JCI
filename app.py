"""JCI API - Unified application for all microservices"""

from chalice import Chalice
from chalicelib.modules.users.controller import api as users_api
from chalicelib.modules.jobs.controller import api as jobs_api
from chalicelib.modules.entreprises.controller import api as entreprises_api
from chalicelib.modules.emplois.controller import api as emplois_api
from chalicelib.modules.candidats.controller import api as candidats_api
from chalicelib.modules.applications.controller import api as applications_api

app = Chalice(app_name='jci-api')

# Register all module blueprints
app.register_blueprint(users_api)
app.register_blueprint(jobs_api)
app.register_blueprint(entreprises_api)
app.register_blueprint(emplois_api)
app.register_blueprint(candidats_api)
app.register_blueprint(applications_api)


@app.route('/')
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


@app.route('/health')
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
