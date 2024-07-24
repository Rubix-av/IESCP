from flask_restful import Resource, fields, marshal_with, reqparse
from flask import jsonify
from .model import db, Campaigns, Influencers, Sponsors, Ad_request

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

sponsor_fields = {
    "id": fields.Integer,
    "email": fields.String,
    "username": fields.String,
    "industry": fields.String,
    "budget": fields.Integer,
    "rank": fields.Integer
}

ad_request_fields = {
    "id": fields.Integer,
    "messages": fields.String,
    "requirenments": fields.String,
    "payment_amount": fields.Integer,
    "status": fields.String,
    "influencer_id": fields.Integer,
    "campaign_id": fields.Integer,
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

# Request parser for sponsors
sponsors_parser = reqparse.RequestParser()
sponsors_parser.add_argument("email", type=str, help="Email is required", required=True)
sponsors_parser.add_argument("username", type=str, help="Username is required", required=True)
sponsors_parser.add_argument("industry", type=str, help="Industry is required", required=True)
sponsors_parser.add_argument("budget", type=int, help="Budget is required", required=True)
sponsors_parser.add_argument("rank", type=int, help="Rank is required", required=True)

# Request parser for ad_request
campaigns_parser = reqparse.RequestParser()
campaigns_parser.add_argument("messages", type=str, help="Messages is required", required=True)
campaigns_parser.add_argument("requirenments", type=str, help="Requirenments is required", required=True)
campaigns_parser.add_argument("payment_amount", type=int, help="Payment Amount is required", required=True)
campaigns_parser.add_argument("status", type=str, help="Status is required", required=False)
campaigns_parser.add_argument("influencer_id", type=int, help="Influenecer id is required", required=True)
campaigns_parser.add_argument("campaign_id", type=int, help="Campaign id is required", required=True)

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
            campaigns = Campaigns.query.order_by(Campaigns.title).all()
            return campaigns

    def delete(self, id):
        campaign = Campaigns.query.filter_by(id=id).first()    
        if not campaign:
            return jsonify({"error": f"Campaign id {id} doesn't exist"})
        
        ads = Ad_request.query.filter_by(campaign_id=id).all()
        if ads:
            for ad in ads:
                db.session.delete(ad)
            db.session.commit()

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
            influencers = Influencers.query.order_by(Influencers.username).all()
            return influencers

    def delete(self, id):
        influencer = Influencers.query.filter_by(id=id).first()    
        if not influencer:
            return jsonify({"error": f"Influencer id {id} doesn't exist"})
        db.session.delete(influencer)
        db.session.commit()

class Sponsors_API(Resource):
    @marshal_with(sponsor_fields)
    def get(self, id=None):
        if id:
            sponsor = Sponsors.query.get(id)
            if not sponsor:
                return jsonify({"error": f"Sponsor id {id} not found"}), 404
            else:
                return sponsor
        else:
            sponsor = Sponsors.query.order_by(Sponsors.username).all()
            return sponsor

class Ad_Request_API(Resource):
    @marshal_with(ad_request_fields)
    def get(self, id=None):
        if id:
            ad = Ad_request.query.get(id)
            if not ad:
                return jsonify({"error": f"Ad id {id} not found"}), 404
            else:
                return ad
        else:
            ad = Ad_request.query.order_by(Ad_request.messages).all()
            return ad
        
    def delete(self, id):
        ad = Ad_request.query.filter_by(id=id).first()    
        if not ad:
            return jsonify({"error": f"Ad id {id} doesn't exist"})
        db.session.delete(ad)
        db.session.commit()

    
