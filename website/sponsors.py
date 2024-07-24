from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import current_user, login_required
from .model import db, Campaigns, Influencers, Ad_request
from datetime import datetime
import requests

sponsor = Blueprint("sponsor", __name__)

# API url
campaigns_api_url = "http://127.0.0.1:8000/api/campaign"
influencers_api_url = "http://127.0.0.1:8000/api/influencer"


# Sponsor Routes
@sponsor.route("/sponsor-profile")
@login_required
def sponsor_profile():
    return render_template("sponsor_pages/sponsor-profile.html", user=current_user)

@sponsor.route("/sponsor-campaigns")
@login_required
def sponsor_campaigns():

    response = requests.get(campaigns_api_url)
    allCampaigns = response.json()

    return render_template("sponsor_pages/sponsor-campaigns.html", user=current_user, allCampaigns=allCampaigns)

@sponsor.route("/sponsor-find")
@login_required
def sponsor_find():

    # Retrieving all the campaigns
    response = requests.get(campaigns_api_url)
    allCampaigns = response.json()

    # Retrieving all the influencers
    response = requests.get(influencers_api_url)
    allInfluencers = response.json()

    return render_template("sponsor_pages/sponsor-find.html", user=current_user, allCampaigns=allCampaigns, allInfluencers=allInfluencers)

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
        visibility = request.form.get("campaign_visibility")

        try:
            startDate = datetime.fromisoformat(request.form.get("startDate"))
            endDate = datetime.fromisoformat(request.form.get("endDate"))
        except ValueError:
            flash("You need to enter date", category='error')
            return redirect(url_for("sponsor.add_campaign"))

        if budget<=0:
            flash("You need to enter some budget!", category='error')
            return redirect(url_for("sponsor.add_campaign"))

        if not visibility:
            flash("You need to set visibility!", category='error')
            return redirect(url_for("sponsor.add_campaign"))

        if startDate > endDate:
            flash("Enter proper dates!", category='error')
            return redirect(url_for("sponsor.add_campaign"))

        new_campaign = Campaigns(title=title, description=desc, start_date=startDate, end_date=endDate, budget=budget, visibility=visibility)

        db.session.add(new_campaign)
        db.session.commit()

        return redirect(url_for("sponsor.sponsor_campaigns"))

    return render_template("sponsor_pages/add-campaign.html", user=current_user)

@sponsor.route("delete-campaign/<int:id>")
@login_required
def delete_campaign(id):
    if request.method == "GET":

        response = requests.delete(campaigns_api_url + f"/{id}")

        flash("Campaign deleted successfully", category='success')
        return redirect(url_for("sponsor.sponsor_campaigns"))

@sponsor.route("edit-campaign/<int:id>", methods=["GET","POST"])
@login_required
def update_campaign(id):
    if request.method=="POST":
        title = request.form.get("title")
        desc = request.form.get("description")
        budget = int(request.form.get("budget"))
        visibility = request.form.get("campaign_visibility")

        try:
            startDate = datetime.fromisoformat(request.form.get("startDate"))
            endDate = datetime.fromisoformat(request.form.get("endDate"))
        except ValueError:
            flash("You need to enter date", category='error')
            return redirect(url_for("sponsor.sponsor_campaigns"))

        if budget<=0:
            flash("You need to enter some budget!", category='error')
            return redirect(url_for("sponsor.sponsor_campaigns"))

        if not visibility:
            flash("You need to set visibility!", category='error')
            return redirect(url_for("sponsor.add_campaign"))

        if startDate > endDate:
            flash("Enter proper dates!", category='error')
            return redirect(url_for("sponsor.sponsor_campaigns"))

        campaign = Campaigns.query.filter_by(id=id).first()
        campaign.title = title
        campaign.description = desc
        campaign.budget = budget
        campaign.visibility = visibility
        campaign.startDate = startDate
        campaign.endDate = endDate
        db.session.add(campaign)
        db.session.commit()
        return redirect(url_for("sponsor.sponsor_campaigns"))

    updateCampaign = Campaigns.query.filter_by(id=id).first()
    return render_template("sponsor_pages/campaign-edit.html", user=current_user, campaign=updateCampaign)

@sponsor.route("/filter-influencers", methods=["GET","POST"])
@login_required
def filter_influencers():
    if request.method == "POST":
        filter_keyword = request.form.get("filter")

        if not filter_keyword:
            flash("No filter added", category='error')
            return redirect(url_for("sponsor.sponsor_find"))

        matched_influencer = []

        # Retrieving campaigns
        response = requests.get(campaigns_api_url)
        allCampaigns = response.json()

        operators = ['>', '<', '=']
        operator = None

        if filter_keyword[0:2] in ['>=', '<=']:
            try:
                filter_keyword_num = float(filter_keyword[2:].strip())
                if filter_keyword[0:2] == "<=":
                    operator = "<="
                else:
                    operator = ">="
                is_number = True
            except ValueError:
                is_number = False

        else:
            for op in operators:
                if filter_keyword.startswith(op):
                    operator = op
                    try:
                        filter_keyword_num = float(filter_keyword[len(op):].strip())
                        is_number = True
                    except ValueError:
                        is_number = False
                    break
                else:
                    is_number = False

        if operator and is_number:
            if operator == '>':
                matched_influencer_followers = Influencers.query.filter(Influencers.followers > filter_keyword_num).all()
            elif operator == '<':
                matched_influencer_followers = Influencers.query.filter(Influencers.followers < filter_keyword_num).all()
            elif operator == '=':
                matched_influencer_followers = Influencers.query.filter(Influencers.followers == filter_keyword_num).all()
            elif operator == '>=':
                matched_influencer_followers = Influencers.query.filter(Influencers.followers >= filter_keyword_num).all()
            elif operator == '<=':
                matched_influencer_followers = Influencers.query.filter(Influencers.followers <= filter_keyword_num).all()

            matched_influencer.extend(matched_influencer_followers)


        if is_number:
            if matched_influencer:
                return render_template("sponsor_pages/sponsor-find.html", user=current_user, allInfluencers=matched_influencer, allCampaigns=allCampaigns)
            else:
                flash(f"Could not find relation '{filter_keyword}'", category='error')
                return redirect(url_for("sponsor.sponsor_find"))

        else:
            matched_influencer = Influencers.query.filter(Influencers.username.like('%'+filter_keyword+'%')).all()
            if matched_influencer:
                return render_template("sponsor_pages/sponsor-find.html", user=current_user, allInfluencers=matched_influencer, allCampaigns=allCampaigns)

            matched_influencer = Campaigns.query.filter(Campaigns.niche.like('%'+filter_keyword+'%')).all()
            if matched_influencer:
                return render_template("sponsor_pages/sponsor-find.html", user=current_user, allInfluencers=matched_influencer, allCampaigns=allCampaigns)

        flash(f"Could not find {filter_keyword}", category='error')
        return redirect(url_for("sponsor.sponsor_find"))

@sponsor.route("/filter-campaigns", methods=["GET","POST"])
@login_required
def filter_campaigns():
    if request.method == "POST":
        filter_keyword = request.form.get("filter")

        if not filter_keyword:
            flash("No filter added", category='error')
            return redirect(url_for("sponsor.sponsor_find"))

        matched_campaign = []

        # Retrieving campaigns
        response = requests.get(influencers_api_url)
        allInfluencers = response.json()

        operators = ['>', '<', '=']
        operator = None

        if filter_keyword[0:2] in ['>=', '<=']:
            try:
                filter_keyword_num = float(filter_keyword[2:].strip())
                if filter_keyword[0:2] == "<=":
                    operator = "<="
                else:
                    operator = ">="
                is_number = True
            except ValueError:     
                is_number = False

        else:
            for op in operators:
                if filter_keyword.startswith(op):
                    operator = op
                    try:
                        filter_keyword_num = float(filter_keyword[len(op):].strip())
                        is_number = True
                    except ValueError:
                        is_number = False
                    break
                else:
                    is_number = False

        if operator and is_number:
            if operator == '>':
                matched_campaign_budget = Campaigns.query.filter(Campaigns.budget > filter_keyword_num).all()
            elif operator == '<':
                matched_campaign_budget = Campaigns.query.filter(Campaigns.budget < filter_keyword_num).all()
            elif operator == '=':
                matched_campaign_budget = Campaigns.query.filter(Campaigns.budget == filter_keyword_num).all()
            elif operator == '>=':
                matched_campaign_budget = Campaigns.query.filter(Campaigns.budget >= filter_keyword_num).all()
            elif operator == '<=':
                matched_campaign_budget = Campaigns.query.filter(Campaigns.budget <= filter_keyword_num).all()

            matched_campaign.extend(matched_campaign_budget)


        if is_number:
            if matched_campaign:
                return render_template("sponsor_pages/sponsor-find.html", user=current_user, allCampaigns=matched_campaign, allInfluencers=allInfluencers)
            else:
                flash(f"Could not find relation '{filter_keyword}'", category='error')
                return redirect(url_for("sponsor.sponsor_find"))

        else:
            matched_campaign = Campaigns.query.filter(Campaigns.title.like('%'+filter_keyword+'%')).all()
            if matched_campaign:
                return render_template("sponsor_pages/sponsor-find.html", user=current_user, allCampaigns=matched_campaign, allInfluencers=allInfluencers)

            matched_campaign = Campaigns.query.filter(Campaigns.description.like('%'+filter_keyword+'%')).all()
            if matched_campaign:
                return render_template("sponsor_pages/sponsor-find.html", user=current_user, allCampaigns=matched_campaign, allInfluencers=allInfluencers)

        flash(f"Could not find {filter_keyword}", category='error')
        return redirect(url_for("sponsor.sponsor_find"))

@sponsor.route("campaign-view/<int:id>")
def campaign_view(id):
    if request.method == "GET":

        response = requests.get(campaigns_api_url + f"/{id}")
        campaign = response.json()

        return render_template("sponsor_pages/campaign-view.html",user=current_user, campaign=campaign)

@sponsor.route("create-ad/<int:id>", methods=["GET","POST"])
def create_ad(id):
    if request.method == "POST":
        
        messages = request.form.get("message")
        requirenments = request.form.get("requirements")
        payment_amount = request.form.get("payment_amt")
        campaign_id = request.form.get("select_campaign")
        influencer_id = id

        new_ad = Ad_request(messages=messages, requirenments=requirenments, payment_amount=payment_amount, campaign_id=campaign_id, influencer_id=influencer_id)
        db.session.add(new_ad)
        db.session.commit()

        flash("Ad request successfully sent!", category='success')
        return redirect(url_for("sponsor.sponsor_campaigns"))


    response = requests.get(campaigns_api_url)
    allCampaigns = response.json()

    return render_template("ad_request/create_ad.html", user=current_user, id=id, allCampaigns=allCampaigns)