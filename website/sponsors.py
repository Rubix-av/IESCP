from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import current_user, login_required
from .model import db, Campaigns
from datetime import datetime
<<<<<<< HEAD
import requests

sponsor = Blueprint("sponsor", __name__)

# Campaign API url
campaigns_api_url = "http://127.0.0.1:8000/api/campaign"


=======

sponsor = Blueprint("sponsor", __name__)

>>>>>>> 2b168d6b922924fa139402d215fb5a59a878adf6
# Sponsor Routes
@sponsor.route("/sponsor-profile")
@login_required
def sponsor_profile():
    return render_template("sponsor_pages/sponsor-profile.html", user=current_user)

@sponsor.route("/sponsor-campaigns")
@login_required
def sponsor_campaigns():
<<<<<<< HEAD

    response = requests.get(campaigns_api_url)
    allCampaigns = response.json()
=======
    allCampaigns = Campaigns.query.all()
>>>>>>> 2b168d6b922924fa139402d215fb5a59a878adf6

    return render_template("sponsor_pages/sponsor-campaigns.html", user=current_user, allCampaigns=allCampaigns)

@sponsor.route("/sponsor-find")
@login_required
def sponsor_find():
    return render_template("sponsor_pages/sponsor-find.html", user=current_user)

@sponsor.route("/sponsor-stats")
@login_required
def sponsor_stats():
    return render_template("sponsor_pages/sponsor-stats.html", user=current_user)

@sponsor.route("/add-campaign", methods=["GET","POST"])
@login_required
def add_campaign():
    if request.method == "POST":
        title = request.form.get("title")
        desc = request.form.get("description")
        budget = int(request.form.get("budget"))
        niche = request.form.get("niche")
<<<<<<< HEAD
        
        try:
            startDate = datetime.fromisoformat(request.form.get("startDate"))
            endDate = datetime.fromisoformat(request.form.get("endDate"))
        except ValueError:
            flash("You need to enter date", category='error')
            return redirect(url_for("sponsor.add_campaign"))

        if budget<=0:
            flash("You need to enter some budget!", category='error')
            return redirect(url_for("sponsor.add_campaign"))
        
        if startDate > endDate:
            flash("Enter proper dates!", category='error')
            return redirect(url_for("sponsor.add_campaign"))
=======
        startDate = datetime.fromisoformat(request.form.get("startDate"))
        endDate = datetime.fromisoformat(request.form.get("endDate"))

        if budget<=0:
            flash("You need to enter some budget!", category='error')
            return redirect(url_for("views.add_campaign"))
        if startDate > endDate:
            flash("Enter proper dates!", category='error')
            return redirect(url_for("views.add_campaign"))
>>>>>>> 2b168d6b922924fa139402d215fb5a59a878adf6
        
        new_campaign = Campaigns(title=title, description=desc, start_date=startDate, end_date=endDate, budget=budget)
        
        db.session.add(new_campaign)
        db.session.commit()

        return redirect(url_for("sponsor.sponsor_campaigns"))

    return render_template("sponsor_pages/add-campaign.html", user=current_user)

@sponsor.route("delete-campaign/<int:id>")
@login_required
def delete_campaign(id):
    if request.method == "GET":
<<<<<<< HEAD
        
        response = requests.delete(campaigns_api_url + f"/{id}")
=======
        campaign = Campaigns.query.filter_by(id=id).first()    
        db.session.delete(campaign)
        db.session.commit()
>>>>>>> 2b168d6b922924fa139402d215fb5a59a878adf6

        flash("Campaign deleted successfully", category='success')
        return redirect(url_for("sponsor.sponsor_campaigns"))