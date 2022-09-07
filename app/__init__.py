from flask import Flask
from flask_moment import Moment
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.static_folder = config_class.STATIC_FOLDER 
    app.template_folder = config_class.TEMPLATE_FOLDER
    moment = Moment()
    moment.init_app(app)
    db.init_app(app)
    login.init_app(app)


    from app.Controller.auth_routes import bp_auth as auth
    app.register_blueprint(auth)
    
    from app.Controller.routes import bp_routes as routes
    app.register_blueprint(routes)

    return app