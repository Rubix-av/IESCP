from . import db
from flask_login import UserMixin
from sqlalchemy import Date

class Admins(db.Model, UserMixin):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    rank = db.Column(db.Integer, default=0, nullable=False)

    def get_id(self):
        return f"admin-{self.id}"

class Influencers(db.Model, UserMixin):
    __tablename__ = "influencers"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    niche = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Integer, default=0, nullable=False)
    reach = db.Column(db.Integer)
    image = db.Column(db.String(200))
    platform_preference = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    rank = db.Column(db.Integer, default=1, nullable=False)
    ad_requests = db.relationship("Ad_request", backref="influencers")
    flagged = db.Column(db.String(10), default="False", nullable=False)

    def get_id(self):
        return f"influencer-{self.id}"
    
class Sponsors(db.Model, UserMixin):
    __tablename__ = "sponsors"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    niche = db.Column(db.String(150), nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    rank = db.Column(db.Integer, default=2, nullable=False)
    flagged = db.Column(db.String(10), default="False", nullable=False)
    campaigns = db.relationship("Campaigns", backref="sponsors")

    def get_id(self):
        return f"sponsor-{self.id}"

class Ad_request(db.Model, UserMixin):
    __tablename__ = "ad_request"

    id = db.Column(db.Integer, primary_key=True)
    messages = db.Column(db.String(150), nullable=False)
    requirements = db.Column(db.String(150), nullable=False)
    payment_amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default="Pending", nullable=False)
    completed = db.Column(db.String(10), default="False", nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey("influencers.id"))
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaigns.id"))
    sponsor_id = db.Column(db.Integer, db.ForeignKey("sponsors.id"))

    def get_id(self):
        return f"ad_request-{self.id}"

class Campaigns(db.Model, UserMixin):
    __tablename__ = "campaigns"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    start_date = db.Column(Date, nullable=False)
    end_date = db.Column(Date, nullable=False)
    niche = db.Column(db.String(150), nullable=True)
    budget = db.Column(db.Integer, nullable=False)
    visibility = db.Column(db.String(50), default="Public", nullable=False)
    flagged = db.Column(db.String(10), default="False", nullable=False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey("sponsors.id"))
    ad_requests = db.relationship("Ad_request", backref="campaigns")

    def get_id(self):
        return f"campaigns-{self.id}"

class Completed_Campaigns(db.Model, UserMixin):
    __tablename__ = "completed_campaigns"

    id = db.Column(db.Integer, primary_key=True)
    sponsor_name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    niche = db.Column(db.String(150), default="None", nullable=True)
    transaction_amount = db.Column(db.Integer, nullable=False)
    sponsor_id = db.Column(db.Integer, nullable=False)

    def get_id(self):
        return f"completed_campaigns-{self.id}"
