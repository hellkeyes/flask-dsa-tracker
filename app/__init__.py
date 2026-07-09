from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.models import db
from app.models import User
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

login_manager = LoginManager()
encrypt = Bcrypt()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///leetcode_tracker.db'
    app.config['SECRET_KEY'] = 'something'

    db.init_app(app)  # connect db to the app
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    encrypt.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes.auth import auth
    from app.routes.main import main
    app.register_blueprint(main)
    app.register_blueprint(auth)

    migrate = Migrate(app, db)

    return app
