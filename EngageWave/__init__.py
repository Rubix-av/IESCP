from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path
from flask_restful import Api

db = SQLAlchemy()
DB_NAME = "database.db"

niches_list = ["Technology", "Fashion", "Automotive", "Sports", "Gaming", "Health", "Science", "Travel", "Finance", "Food and Beverage", "Gardening", "Entertainment", "Education"]


def create_app():
    app = Flask(__name__)
    api = Api(app)
    app.config['SECRET_KEY'] = "dsakfhaosjbdjvbakshefkdsafaseh"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    app.config['UPLOAD_FOLDER'] = 'EngageWave/static/uploads/'
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    db.init_app(app)

    # initializing logging variables
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # import modules
    from .sponsors import sponsor
    from .influencers import influencer
    from .auth import auth
    from .home import home
    from .admin import admin

    # registering blueprints
    app.register_blueprint(sponsor, url_prefix="/sponsor")
    app.register_blueprint(influencer, url_prefix="/influencer")
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(admin, url_prefix="/admin")

    # setting up database
    from .model import Ad_request, Campaigns, Sponsors, Influencers, Admins
    create_database(app)

    # API end points
    from .api import Campaigns_API, Influencers_API, Sponsors_API, Ad_Request_API, Completed_Campaigns_API, Influencer_Request_API
    api.add_resource(Campaigns_API, "/api/campaign/<int:id>", "/api/campaign")
    api.add_resource(Influencers_API, "/api/influencer/<int:id>", "/api/influencer")
    api.add_resource(Sponsors_API, "/api/sponsor/<int:id>", "/api/sponsor")
    api.add_resource(Ad_Request_API, "/api/ad_request/<int:id>", "/api/ad_request")
    api.add_resource(Completed_Campaigns_API, "/api/completed_campaign/<int:id>", "/api/completed_campaign")
    api.add_resource(Influencer_Request_API, "/api/inf_request/<int:id>", "/api/inf_request")

    # user loader for login manager
    @login_manager.user_loader
    def load_user(user_id):
        if user_id.startswith('sponsor-'):
            user_id = user_id.replace('sponsor-', '')
            return Sponsors.query.get(int(user_id))
        elif user_id.startswith('influencer-'):
            user_id = user_id.replace('influencer-', '')
            return Influencers.query.get(int(user_id))
        elif user_id.startswith('admin-'):
            user_id = user_id.replace('admin-', '')
            return Admins.query.get(int(user_id))
        return None

    return app

def create_database(app):
    with app.app_context():
        if not path.exists("EngageWave/" + DB_NAME):
            db.create_all()
            print("Created Database!")
            