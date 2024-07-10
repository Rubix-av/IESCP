<<<<<<< HEAD
from flask_restful import Resource, fields, marshal_with, reqparse
from flask import jsonify
from .model import db, Campaigns

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

# Request parser for campaigns
campaigns_parser = reqparse.RequestParser()
campaigns_parser.add_argument("title", type=str, help="Title is required", required=True)
campaigns_parser.add_argument("description", type=str, help="Description is required", required=True)
campaigns_parser.add_argument("budget", type=int, help="Budget is required", required=True)
campaigns_parser.add_argument("visibility", type=str, help="Visibility is required", required=False)

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


    
=======
from flask_restful import Resource
from flask import jsonify
from .model import db, Campaigns
>>>>>>> 2b168d6b922924fa139402d215fb5a59a878adf6
