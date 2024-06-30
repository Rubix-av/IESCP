from flask import Blueprint, render_template
from flask_login import current_user

views = Blueprint("views", __name__)

# Sponsor Routes
@views.route("/sponsor-profile")
def sponsor_profile():
    return render_template("sponsor/sponsor-profile.html", user=current_user)

@views.route("/sponsor-campaigns")
def sponsor_campaigns():
    return render_template("sponsor/sponsor-campaigns.html", user=current_user)

@views.route("/sponsor-find")
def sponsor_find():
    return render_template("sponsor/sponsor-find.html", user=current_user)

@views.route("/sponsor-stats")
def sponsor_stats():
    return render_template("sponsor/sponsor-stats.html", user=current_user)

@views.route("/add-campaign")
def add_campaign():
    return render_template("sponsor/add-campaign.html", user=current_user)

# Influencer Routes
@views.route("/influencer-profile")
def influencer_profile():
    return render_template("influencer/influencer-profile.html", user=current_user)
