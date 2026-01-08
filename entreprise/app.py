from chalice import Chalice
from chalicelib.modules.controller import api as entreprise_api

app = Chalice(app_name='entreprise')

# Register entreprise blueprint
app.register_blueprint(entreprise_api)


@app.route('/')
def index():
    return {'service': 'entreprise', 'status': 'running'}
