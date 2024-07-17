from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from .model import db, Campaigns
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

    allCampaigns = [campaign for campaign in allCampaigns if campaign.get('visibility') == 'Public']

    return render_template("influencer_pages/influencer-find.html", user=current_user, allCampaigns=allCampaigns)

@influencer.route("/influencer-stats")
@login_required
def influencer_stats():
    return render_template("influencer_pages/influencer-stats.html", user=current_user)

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