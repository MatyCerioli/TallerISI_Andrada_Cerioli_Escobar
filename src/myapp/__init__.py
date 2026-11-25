from flask import Flask

from myapp.api.health import health_bp
from myapp.config import Config
from myapp.extensions import db
from myapp.web.users import users_bp
from myapp.api.auth import api_auth_bp
from myapp.web.auth import web_auth_bp

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)

    app.register_blueprint(health_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(api_auth_bp)
    app.register_blueprint(web_auth_bp)

    return app