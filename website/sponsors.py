from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import current_user, login_required
from .model import db, Campaigns, Influencers, Ad_request, Sponsors, Completed_Campaigns, Influencer_requests
from . import niches_list
from datetime import datetime
import requests

sponsor = Blueprint("sponsor", __name__)

# API url
campaigns_api_url = "http://127.0.0.1:8000/api/campaign"
influencers_api_url = "http://127.0.0.1:8000/api/influencer"
ad_request_api_url = "http://127.0.0.1:8000/api/ad_request"
completed_campaign_api_url = "http://127.0.0.1:8000/api/completed_campaign"
inf_request_api_url = "http://127.0.0.1:8000/api/inf_request"

# Sponsor Routes
@sponsor.route("/sponsor-profile")
@login_required
def sponsor_profile():
    return render_template("sponsor_pages/sponsor-profile.html", user=current_user)

@sponsor.route("/sponsor-dashboard")
@login_required
def sponsor_dashboard():

    # Ad_requests
    response = requests.get(ad_request_api_url)
    allAds = response.json()

    # Campaigns
    response = requests.get(campaigns_api_url)
    allCampaigns = response.json()

    # Influencers
    response = requests.get(influencers_api_url)
    allInfluencers = response.json()

    # Completed Campaigns
    response = requests.get(completed_campaign_api_url)
    allCompletedCampaigns = response.json()

    # Influencer_requests
    response = requests.get(inf_request_api_url)
    allRequests = response.json()

    return render_template("sponsor_pages/sponsor-dashboard.html", user=current_user, allAds=allAds, allInfluencers=allInfluencers, allCompletedCampaigns=allCompletedCampaigns, allRequests=allRequests, allCampaigns=allCampaigns)

@sponsor.route("/sponsor-campaigns")
@login_required
def sponsor_campaigns():

    response = requests.get(campaigns_api_url)
    allCampaigns = response.json()

    allCampaigns = [campaign for campaign in allCampaigns if campaign['sponsor_id'] == current_user.id]

    return render_template("sponsor_pages/sponsor-campaigns.html", user=current_user, allCampaigns=allCampaigns)

@sponsor.route("/sponsor-find")
@login_required
def sponsor_find():

    # Retrieving all the campaigns
    response = requests.get(campaigns_api_url)
    allCampaigns = response.json()
    allCampaigns = [campaign for campaign in allCampaigns if campaign['sponsor_id'] == current_user.id]

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
        sponsor_id = current_user.id
        niche = request.form.get("campaign_niche")

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

        new_campaign = Campaigns(title=title, description=desc, start_date=startDate, end_date=endDate, budget=budget, visibility=visibility, sponsor_id=sponsor_id, niche=niche)

        db.session.add(new_campaign)
        db.session.commit()

        return redirect(url_for("sponsor.sponsor_campaigns"))

    return render_template("sponsor_pages/add-campaign.html", user=current_user, allNiches=niches_list)

@sponsor.route("delete-campaign/<int:id>")
@login_required
def delete_campaign(id):
    if request.method == "GET":

        requests.delete(campaigns_api_url + f"/{id}")

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
        requirements = request.form.get("requirements")
        payment_amount = request.form.get("payment_amt")
        campaign_id = int(request.form.get("select_campaign"))
        influencer_id = id
        sponsor_id = current_user.id

        new_ad = Ad_request(messages=messages, requirements=requirements, payment_amount=payment_amount, campaign_id=campaign_id, influencer_id=influencer_id, sponsor_id=sponsor_id)
        db.session.add(new_ad)
        db.session.commit()

        flash("Ad request successfully sent!", category='success')
        return redirect(url_for("sponsor.sponsor_find"))

    response = requests.get(campaigns_api_url)
    allCampaigns = response.json()
    allCampaigns = [campaign for campaign in allCampaigns if campaign['sponsor_id'] == current_user.id]

    response = requests.get(influencers_api_url + f"/{id}")
    influencers = response.json()

    if len(allCampaigns) == 0:
        flash("No campaign is available!", category='error')
        return redirect(url_for("sponsor.sponsor_find"))

    return render_template("ad_request/create_ad.html", user=current_user, id=id, allCampaigns=allCampaigns, influencers=influencers)

@sponsor.route("confirm-completion/<int:id>")
def confirm_completion(id):
    ad_completion_confirmed = Ad_request.query.filter_by(id=id).first()
    campaign_completion_confirmed = Campaigns.query.filter_by(id=ad_completion_confirmed.campaign_id).first()
    sponsor =  Sponsors.query.filter_by(id=ad_completion_confirmed.sponsor_id).first()
    influencer = Influencers.query.filter_by(id=ad_completion_confirmed.influencer_id).first()
    
    completed_campaign_campaign_id = ad_completion_confirmed.campaign_id
    completed_campaign_title = campaign_completion_confirmed.title
    completed_campaign_desc = campaign_completion_confirmed.description
    completed_campaign_niche = campaign_completion_confirmed.niche
    completed_campaign_sponsor_name = sponsor.username
    completed_campaign_transaction_amt = ad_completion_confirmed.payment_amount
    completed_campaign_sponsor_id = sponsor.id

    new_complete_campaign = Completed_Campaigns(campaign_id=completed_campaign_campaign_id, sponsor_name=completed_campaign_sponsor_name, title=completed_campaign_title, description=completed_campaign_desc, niche=completed_campaign_niche, transaction_amount=completed_campaign_transaction_amt, sponsor_id=completed_campaign_sponsor_id)

    influencer.balance += ad_completion_confirmed.payment_amount
    db.session.add(influencer)
    db.session.add(new_complete_campaign)
    db.session.delete(ad_completion_confirmed)
    db.session.commit()

    # influencer = Influencers.query.filter_by(id=ad_completion_confirmed.influencer_id).first()
    flash("Campaign successfull!", category='success')
    return redirect(url_for("sponsor.sponsor_dashboard"))

@sponsor.route("delete-completed-campaign/<int:id>")
def delete_completed_campaign(id):
    
    response = requests.delete(completed_campaign_api_url + f"/{id}")

    flash("Successfully deleted!", category='success')
    return redirect(url_for("sponsor.sponsor_dashboard"))

@sponsor.route("delete-ad-request/<int:id>")
def delete_ad_request(id):
    
    response = requests.delete(ad_request_api_url + f"/{id}")

    flash("Successfully deleted!", category='success')
    return redirect(url_for("sponsor.sponsor_dashboard"))

@sponsor.route("accept-request/<int:id>")
@login_required
def accept_request(id):

    request_accepted = Influencer_requests.query.filter_by(id=id).first()
    message = request_accepted.message
    requirements = request_accepted.goal
    payment_amount = request_accepted.request_amt
    status = "Accepted"
    campaign_id = request_accepted.campaign_id
    influencer_id = request_accepted.influencer_id
    sponsor_id = request_accepted.sponsor_id

    new_ad_request = Ad_request(messages=message, requirements=requirements, payment_amount=payment_amount, campaign_id=campaign_id, influencer_id=influencer_id, sponsor_id=sponsor_id, status=status)

    db.session.delete(request_accepted)
    db.session.add(new_ad_request)
    db.session.commit()

    flash("Request accepted successfully", category='success')
    return redirect(url_for("sponsor.sponsor_dashboard"))

@sponsor.route("reject-request/<int:id>")
@login_required
def reject_request(id):

    request_rejected = Influencer_requests.query.filter_by(id=id).first()

    db.session.delete(request_rejected)
    db.session.commit()

    flash("Ad rejected successfully", category='success')
    return redirect(url_for("sponsor.sponsor_dashboard"))


