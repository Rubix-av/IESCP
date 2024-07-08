from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from .model import db, Campaigns
from datetime import datetime

views = Blueprint("views", __name__)

# Sponsor Routes
@views.route("/sponsor-profile")
@login_required
def sponsor_profile():
    return render_template("sponsor/sponsor-profile.html", user=current_user)

@views.route("/sponsor-campaigns")
@login_required
def sponsor_campaigns():
    return render_template("sponsor/sponsor-campaigns.html", user=current_user)

@views.route("/sponsor-find")
@login_required
def sponsor_find():
    return render_template("sponsor/sponsor-find.html", user=current_user)

@views.route("/sponsor-stats")
@login_required
def sponsor_stats():
    return render_template("sponsor/sponsor-stats.html", user=current_user)

@views.route("/add-campaign", methods=["GET","POST"])
@login_required
def add_campaign():
    if request.method == "POST":
        title = request.form.get("title")
        desc = request.form.get("description")
        budget = int(request.form.get("budget"))
        niche = request.form.get("niche")
        startDate = datetime.fromisoformat(request.form.get("startDate"))
        endDate = datetime.fromisoformat(request.form.get("endDate"))

        if budget<=0:
            flash("You need to enter some budget!", category='error')
            return redirect(url_for("views.add_campaign"))
        if startDate > endDate:
            flash("Enter proper dates!", category='error')
            return redirect(url_for("views.add_campaign"))
        
        new_campaign = Campaigns(title=title, description=desc, start_date=startDate, end_date=endDate, budget=budget)
        
        db.session.add(new_campaign)
        db.session.commit()

        return redirect(url_for("views.sponsor_campaigns"))

    return render_template("sponsor/add-campaign.html", user=current_user)

# Influencer Routes
@views.route("/influencer-profile")
@login_required
def influencer_profile():
    return render_template("influencer/influencer-profile.html", user=current_user)
