from chalice import Chalice
from chalicelib.modules.controller import api as user_api

app = Chalice(app_name='users')

# Register user blueprint
app.register_blueprint(user_api)


@app.route('/')
def index():
    return {'service': 'users', 'status': 'running'}
