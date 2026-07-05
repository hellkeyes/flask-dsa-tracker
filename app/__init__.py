from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.models import db


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///leetcode_tracker.db'

    db.init_app(app)  # connect db to the app

    from app.routes.auth import auth
    from app.routes.main import main
    app.register_blueprint(main)
    app.register_blueprint(auth)

    migrate = Migrate(app, db)

    return app


