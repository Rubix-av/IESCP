from . import db
from flask_login import UserMixin
from sqlalchemy import Date

class Sponsors(db.Model, UserMixin):
    __tablename__ = "sponsors"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(150), nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(50), nullable=False)

class Influencers(db.Model, UserMixin):
    __tablename__ = "influencers"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    niche = db.Column(db.String(100), nullable=False)
    followers = db.Column(db.Integer, nullable=False)
    reach = db.Column(db.Integer, nullable=False)
    ad_requests = db.relationship("Ad_request", backref="influencers")
    password = db.Column(db.String(50), nullable=False)

class Ad_request(db.Model, UserMixin):
    __tablename__ = "ad_request"

    id = db.Column(db.Integer, primary_key=True)
    messages = db.Column(db.String(150), nullable=False)
    requirenments = db.Column(db.String(150), nullable=False)
    payment_amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default="Pending", nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey("influencers.id"))
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaigns.id"))

class Campaigns(db.Model, UserMixin):
    __tablename__ = "campaigns"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    start_date = db.Column(Date, nullable=False)
    end_date = db.Column(Date, nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    visibility = db.Column(db.String(50), default="Public", nullable=False)
    goals = db.Column(db.String(100), nullable=False)
    ad_requests = db.relationship("Ad_request", backref="campaigns")
