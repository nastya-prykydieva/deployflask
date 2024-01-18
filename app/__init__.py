from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from config import config

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
jwt_manager = JWTManager()
ma = Marshmallow()


def create_app(config_name='dev'):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    jwt_manager.init_app(app)
    ma.init_app(app)
    app.app_context().push()

    with app.app_context():
        from app.portfolio import portfolio
        from app.auth import auth
        from app.cookies import cookies
        from app.todo import todo_bp
        from app.feedback import feedback_bp
        from app.post import post_bp
        from app.api import api_bp
        from app.api_users import api_users_bp
        from app.swagger import swagger_bp
        app.register_blueprint(portfolio, url_prefix='/')
        app.register_blueprint(auth, url_prefix='/auth')
        app.register_blueprint(cookies, url_prefix='/cookies')
        app.register_blueprint(todo_bp, url_prefix='/todo')
        app.register_blueprint(feedback_bp, url_prefix='/feedback')
        app.register_blueprint(post_bp, url_prefix='/post')
        app.register_blueprint(api_bp, url_prefix='/api')
        app.register_blueprint(api_users_bp, url_prefix='/api_users')
        app.register_blueprint(swagger_bp, url_prefix='/swagger')
        return app
