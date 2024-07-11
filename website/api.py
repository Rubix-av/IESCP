from flask_restful import Resource, fields, marshal_with, reqparse
from flask import jsonify
from .model import db, Campaigns, Influencers

# Add campaign fields
campaign_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "description": fields.String,
    "start_date": fields.DateTime(dt_format='iso8601'),
    "end_date": fields.DateTime(dt_format='iso8601'),
    "budget": fields.Integer,
    "visibility": fields.String
}

influencer_fields = {
    "id": fields.Integer,
    "email": fields.String,
    "username": fields.String,
    "category": fields.String,
    "niche": fields.String,
    "followers": fields.Integer,
    "reach": fields.Integer,
    "platform_preference": fields.String,
    "rank": fields.Integer
}

# Request parser for campaigns
campaigns_parser = reqparse.RequestParser()
campaigns_parser.add_argument("title", type=str, help="Title is required", required=True)
campaigns_parser.add_argument("description", type=str, help="Description is required", required=True)
campaigns_parser.add_argument("budget", type=int, help="Budget is required", required=True)
campaigns_parser.add_argument("visibility", type=str, help="Visibility is required", required=False)

# Request parser for influencers
influencers_parser = reqparse.RequestParser()
influencers_parser.add_argument("email", type=str, help="Email is required", required=True)
influencers_parser.add_argument("username", type=str, help="Username is required", required=True)
influencers_parser.add_argument("category", type=str, help="Category is required", required=True)
influencers_parser.add_argument("niche", type=str, help="Niche is required", required=True)
influencers_parser.add_argument("followers", type=int, help="No. of followers is required", required=True)
influencers_parser.add_argument("reach", type=int, help="Reach is required", required=False)
influencers_parser.add_argument("platform_preference", type=str, help="Platform Preference is required", required=True)
influencers_parser.add_argument("rank", type=int, help="Rank is required", required=True)

class Campaigns_API(Resource):
    @marshal_with(campaign_fields)
    def get(self, id=None):
        if id:
            campaign = Campaigns.query.get(id)
            if not campaign:
                return jsonify({"error": f"Campaign id {id} not found"}), 404
            else:
                return campaign
        else:
            campaigns = Campaigns.query.all()
            return campaigns

    def delete(self, id):
        campaign = Campaigns.query.filter_by(id=id).first()    
        if not campaign:
            return jsonify({"error": f"Campaign id {id} doesn't exist"})
        db.session.delete(campaign)
        db.session.commit()

class Influencers_API(Resource):
    @marshal_with(influencer_fields)
    def get(self, id=None):
        if id:
            influencer = Influencers.query.get(id)
            if not influencer:
                return jsonify({"error": f"Influencer id {id} not found"}), 404
            else:
                return influencer
        else:
            influencers = Influencers.query.all()
            return influencers

    def delete(self, id):
        influencer = Influencers.query.filter_by(id=id).first()    
        if not influencer:
            return jsonify({"error": f"Influencer id {id} doesn't exist"})
        db.session.delete(influencer)
        db.session.commit()


    
