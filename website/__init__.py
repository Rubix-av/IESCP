from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "dsakfhaosjbdjvbakshefkdsafaseh"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    # initializing logging variables

    # import modules
    from .auth import auth
    from .views import views

    # registering blueprints
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(views, url_prefix="/")

    # setting up database
    from .model import Ad_request, Campaigns, Sponsors, Influencers
    create_database(app)

    return app

def create_database(app):
    with app.app_context():
        if not path.exists("website/" + DB_NAME):
            db.create_all()
            print("Created Database!")
            