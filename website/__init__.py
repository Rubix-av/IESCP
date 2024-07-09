from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "dsakfhaosjbdjvbakshefkdsafaseh"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    # initializing logging variables
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # import modules
    from .sponsors import sponsor
    from .influencers import influencer
    from .auth import auth

    # registering blueprints
    app.register_blueprint(sponsor, url_prefix="/sponsor")
    app.register_blueprint(influencer, url_prefix="/influencer")
    app.register_blueprint(auth, url_prefix="/auth")

    # setting up database
    from .model import Ad_request, Campaigns, Sponsors, Influencers
    create_database(app)

    # user loader for login manager
    @login_manager.user_loader
    def load_user(user_id):
        if user_id.startswith('sponsor-'):
            user_id = user_id.replace('sponsor-', '')
            return Sponsors.query.get(int(user_id))
        elif user_id.startswith('influencer-'):
            user_id = user_id.replace('influencer-', '')
            return Influencers.query.get(int(user_id))
        return None

    return app

def create_database(app):
    with app.app_context():
        if not path.exists("website/" + DB_NAME):
            db.create_all()
            print("Created Database!")
            