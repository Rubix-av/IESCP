from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from .model import db, Campaigns, Ad_request, Influencer_requests
import requests
from datetime import datetime
from .chartData import count_data, sponsor_niches_data, influencer_niches_data, campaign_niches_data, ad_request_status_data, influencer_request_status_data, ad_request_budget_data

influencer = Blueprint("influencer", __name__)

# Campaings API URL
campaigns_api_url = "http://127.0.0.1:8000/api/campaign"
influencer_api_url = "http://127.0.0.1:8000/api/influencer"
ad_request_api_url = "http://127.0.0.1:8000/api/ad_request"
sponsor_api_url = "http://127.0.0.1:8000/api/sponsor"
inf_request_api_url = "http://127.0.0.1:8000/api/inf_request"

@influencer.route("/influencer-profile")
@login_required
def influencer_profile():

    return render_template("influencer_pages/influencer-profile.html", user=current_user)

@influencer.route("/influencer-dashboard")
@login_required
def influencer_dashboard():
    response = requests.get(ad_request_api_url)
    allAds = response.json()
    
    response = requests.get(campaigns_api_url)
    allCampaigns = response.json()
    
    response = requests.get(sponsor_api_url)
    allSponsors = response.json()

    response = requests.get(inf_request_api_url)
    print(response)
    allRequests = response.json()
    print(allRequests)

    allAds = [ad for ad in allAds if ad.get('influencer_id') == current_user.id]

    return render_template("influencer_pages/influencer-dashboard.html", user=current_user, allAds=allAds, allCampaigns=allCampaigns, allSponsors=allSponsors, allRequests=allRequests)

@influencer.route("/influencer-find")
@login_required
def influencer_find():
    response = requests.get(campaigns_api_url)
    allCampaigns = response.json()

    allCampaigns = [campaign for campaign in allCampaigns if campaign.get('visibility') == 'Public' or (campaign.get('visibility') == 'Private' and campaign.get('niche') == current_user.niche)]

    return render_template("influencer_pages/influencer-find.html", user=current_user, allCampaigns=allCampaigns)

@influencer.route("/influencer-stats")
@login_required
def influencer_stats():

    # Total users and data generated
    get_count_data = count_data()
    total_influencers = get_count_data[1]
    
    # Influencer platform data
    get_influencer_platform_data = influencer_request_status_data(current_user.id)
    inf_request_status_labels = get_influencer_platform_data[0]
    inf_request_status_values = get_influencer_platform_data[1]

    # Influencer ad request payment amount
    get_ad_request_payment_amount = ad_request_budget_data(current_user.id)
    ad_request_payment_amt_labels = get_ad_request_payment_amount[0]
    ad_request_payment_amt_values = get_ad_request_payment_amount[1]

    print(ad_request_payment_amt_values)

    return render_template("influencer_pages/influencer-stats.html", user=current_user, inf_request_status_values=inf_request_status_values, ad_request_payment_amt_labels=ad_request_payment_amt_labels, ad_request_payment_amt_values=ad_request_payment_amt_values, total_influencers=total_influencers)

@influencer.route("/filter", methods=["GET","POST"])
@login_required
def filter():
    if request.method == "POST":
        filter_keyword = request.form.get("filter")

        if not filter_keyword:
            flash("No filter added", category='error')
            return redirect(url_for("influencer.influencer_find"))
        
        matched_campaign = []

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
                return render_template("influencer_pages/influencer-find.html", user=current_user, allCampaigns=matched_campaign)
            else:
                flash(f"Could not find relation '{filter_keyword}'", category='error')
                return redirect(url_for("influencer.influencer_find"))
        
        else:
            matched_campaign = Campaigns.query.filter(Campaigns.title.like('%'+filter_keyword+'%')).all()
            if matched_campaign:
                return render_template("influencer_pages/influencer-find.html", user=current_user, allCampaigns=matched_campaign)

            matched_campaign = Campaigns.query.filter(Campaigns.description.like('%'+filter_keyword+'%')).all()
            if matched_campaign:
                return render_template("influencer_pages/influencer-find.html", user=current_user, allCampaigns=matched_campaign)
        
        flash(f"Could not find {filter_keyword}", category='error')
        return redirect(url_for("influencer.influencer_find"))
    
@influencer.route("reject-ad/<int:id>")
@login_required
def reject_ad(id):

    ad_rejected = Ad_request.query.filter_by(id=id).first()

    ad_rejected.status = "Rejected"
    db.session.add(ad_rejected)
    db.session.commit()

    flash("Ad rejected successfully", category='success')
    return redirect(url_for("influencer.influencer_dashboard"))
    
@influencer.route("accept-ad/<int:id>")
@login_required
def accept_ad(id):

    ad_accepted = Ad_request.query.filter_by(id=id).first()

    ad_accepted.status = "Accepted"
    db.session.add(ad_accepted)
    db.session.commit()

    flash("Ad accepted successfully", category='success')
    return redirect(url_for("influencer.influencer_dashboard"))

@influencer.route("complete-campaign/<int:id>")
@login_required
def complete_campaign(id):

    ad_completed = Ad_request.query.filter_by(id=id).first()

    ad_completed.completed = "True"
    db.session.add(ad_completed)
    db.session.commit()

    flash("Campaign Completed", category='success')
    return redirect(url_for("influencer.influencer_dashboard"))

@influencer.route("request-ad/<int:id>/<string:title>/<int:sponsor_id>", methods=["GET","POST"])
@login_required
def request_ad(id, title, sponsor_id):
    
    if request.method == "POST":
        
        goal = request.form.get("goal")
        messages = request.form.get("message")
        request_amt = request.form.get("request_amt")
        campaign_id = id
        influencer_id = current_user.id
        sponsor_id = sponsor_id

        new_request = Influencer_requests(goal=goal, message=messages, request_amt=request_amt, campaign_id=campaign_id, influencer_id=influencer_id, sponsor_id=sponsor_id)
        db.session.add(new_request)
        db.session.commit()

        flash("Ad request successfully sent!", category='success')
        return redirect(url_for("influencer.influencer_find"))

    campaign = Campaigns.query.filter_by(id=id).first()
    campaign_budget = campaign.budget

    return render_template("influencer_pages/request_ad.html", user=current_user, id=id, title=title, campaign_budget=campaign_budget)
    
@influencer.route("update-request-amt/<int:id>", methods=["GET","POST"])
def update_request_amt(id):
    if request.method == "POST":
        new_request_amt = request.form.get("request_amount")
        request_ad = Influencer_requests.query.filter_by(id=id).first()
        request_ad.request_amt = new_request_amt

        db.session.add(request_ad)
        db.session.commit()

        flash("Request amount updated!", category='success')
        return redirect(url_for("influencer.influencer_dashboard"))

@influencer.route("update-ad-amt/<int:id>", methods=["GET","POST"])
def update_ad_amt(id):
    if request.method == "POST":
        new_ad_amt = int(request.form.get("ad_amt"))
        request_ad = Ad_request.query.filter_by(id=id).first()

        campaign = Campaigns.query.filter_by(id=request_ad.campaign_id).first()

        if new_ad_amt-request_ad.payment_amount >= 0:
            if campaign.budget >= new_ad_amt-request_ad.payment_amount:
                campaign.budget -= new_ad_amt-request_ad.payment_amount
            else:
                flash(f"Sponsor has only {campaign.budget} remaining", category='error')
                return redirect(url_for("sponsor.sponsor_campaigns"))
        else:
            campaign.budget += request_ad.payment_amount-new_ad_amt

        request_ad.payment_amount = new_ad_amt

        db.session.add(request_ad)
        db.session.commit()

        flash("Payment amount updated!", category='success')
        return redirect(url_for("influencer.influencer_dashboard"))

