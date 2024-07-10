from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from .model import db
import requests
from datetime import datetime

influencer = Blueprint("influencer", __name__)

# Campaings API URL
campaigns_api_url = "http://127.0.0.1:8000/api/campaign"

@influencer.route("/influencer-profile")
@login_required
def influencer_profile():
    return render_template("influencer_pages/influencer-profile.html", user=current_user)

@influencer.route("/influencer-find")
@login_required
def influencer_find():
    response = requests.get(campaigns_api_url)
    allCampaigns = response.json()

    return render_template("influencer_pages/influencer-find.html", user=current_user, allCampaigns=allCampaigns)

@influencer.route("/influencer-stats")
@login_required
def influencer_stats():
    return render_template("influencer_pages/influencer-stats.html", user=current_user)