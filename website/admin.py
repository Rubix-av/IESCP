from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import current_user, login_required
from .model import Campaigns, Influencers, Sponsors
import requests

admin = Blueprint("admin", __name__)

# API url
campaigns_api_url = "http://127.0.0.1:8000/api/campaign"
influencers_api_url = "http://127.0.0.1:8000/api/influencer"
sponsors_api_url = "http://127.0.0.1:8000/api/sponsor"

@admin.route("/admin-profile")
def admin_profile():
    return render_template("admin_pages/admin-profile.html", user=current_user)

@admin.route("/admin-find")
def admin_find():
    
    # Retrieving all the campaigns
    response = requests.get(campaigns_api_url)
    allCampaigns = response.json()

    # Retrieving all the influencers
    response = requests.get(influencers_api_url)
    allInfluencers = response.json()

    # Retrieving all the sponsors
    response = requests.get(sponsors_api_url)
    allSponsors = response.json()

    return render_template("admin_pages/admin-find.html", user=current_user, allCampaigns=allCampaigns, allInfluencers=allInfluencers, allSponsors=allSponsors)

@admin.route("/admin-stats")
def admin_stats():
    return render_template("admin_pages/admin-stats.html", user=current_user)

@admin.route("/filter-influencers", methods=["GET","POST"])
@login_required
def filter_influencers():
    if request.method == "POST":
        filter_keyword = request.form.get("filter")

        if not filter_keyword:
            flash("No filter added", category='error')
            return redirect(url_for("admin.admin_find"))

        matched_influencer = []

        # Retrieving campaigns
        response = requests.get(campaigns_api_url)
        allCampaigns = response.json()

        # Retrieving sponsors
        response = requests.get(sponsors_api_url)
        allSponsors = response.json()

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
                return render_template("admin_pages/admin-find.html", user=current_user, allInfluencers=matched_influencer, allCampaigns=allCampaigns, allSponsors=allSponsors)
            else:
                flash(f"Could not find relation '{filter_keyword}'", category='error')
                return redirect(url_for("sponsor.sponsor_find"))

        else:
            matched_influencer = Influencers.query.filter(Influencers.username.like('%'+filter_keyword+'%')).all()
            if matched_influencer:
                return render_template("admin_pages/admin-find.html", user=current_user, allInfluencers=matched_influencer, allCampaigns=allCampaigns, allSponsors=allSponsors)

            matched_influencer = Campaigns.query.filter(Campaigns.niche.like('%'+filter_keyword+'%')).all()
            if matched_influencer:
                return render_template("admin_pages/admin-find.html", user=current_user, allInfluencers=matched_influencer, allCampaigns=allCampaigns, allSponsors=allSponsors)

        flash(f"Could not find {filter_keyword}", category='error')
        return redirect(url_for("admin.admin_find"))

@admin.route("/filter-campaigns", methods=["GET","POST"])
@login_required
def filter_campaigns():
    if request.method == "POST":
        filter_keyword = request.form.get("filter")

        if not filter_keyword:
            flash("No filter added", category='error')
            return redirect(url_for("admin.admin_find"))

        matched_campaign = []

        # Retrieving influencers
        response = requests.get(influencers_api_url)
        allInfluencers = response.json()

        # Retrieving sponsors
        response = requests.get(sponsors_api_url)
        allSponsors = response.json()

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
                return render_template("admin_pages/admin-find.html", user=current_user, allCampaigns=matched_campaign, allInfluencers=allInfluencers, allSponsors=allSponsors)
            else:
                flash(f"Could not find relation '{filter_keyword}'", category='error')
                return redirect(url_for("admin.admin_find"))

        else:
            matched_campaign = Campaigns.query.filter(Campaigns.title.like('%'+filter_keyword+'%')).all()
            if matched_campaign:
                return render_template("admin_pages/admin-find.html", user=current_user, allCampaigns=matched_campaign, allInfluencers=allInfluencers, allSponsors=allSponsors)

            matched_campaign = Campaigns.query.filter(Campaigns.description.like('%'+filter_keyword+'%')).all()
            if matched_campaign:
                return render_template("admin_pages/admin-find.html", user=current_user, allCampaigns=matched_campaign, allInfluencers=allInfluencers, allSponsors=allSponsors)

        flash(f"Could not find {filter_keyword}", category='error')
        return redirect(url_for("admin.admin_find")) 
    
@admin.route("/filter-sponsors", methods=["GET","POST"])
@login_required
def filter_sponsors():
    if request.method == "POST":
        filter_keyword = request.form.get("filter")

        if not filter_keyword:
            flash("No filter added", category='error')
            return redirect(url_for("admin.admin_find"))

        matched_sponsor = []

        # Retrieving campaigns
        response = requests.get(campaigns_api_url)
        allCampaigns = response.json()

        # Retrieving influencers
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
                matched_sponsor_budget = Sponsors.query.filter(Sponsors.budget > filter_keyword_num).all()
            elif operator == '<':
                matched_sponsor_budget = Sponsors.query.filter(Sponsors.budget < filter_keyword_num).all()
            elif operator == '=':
                matched_sponsor_budget = Sponsors.query.filter(Sponsors.budget == filter_keyword_num).all()
            elif operator == '>=':
                matched_sponsor_budget = Sponsors.query.filter(Sponsors.budget >= filter_keyword_num).all()
            elif operator == '<=':
                matched_sponsor_budget = Sponsors.query.filter(Sponsors.budget <= filter_keyword_num).all()

            matched_sponsor.extend(matched_sponsor_budget)


        if is_number:
            if matched_sponsor:
                return render_template("admin_pages/admin-find.html", user=current_user, allCampaigns=allCampaigns, allInfluencers=allInfluencers, allSponsors=matched_sponsor)
            else:
                flash(f"Could not find relation '{filter_keyword}'", category='error')
                return redirect(url_for("admin.admin_find"))

        else:
            matched_sponsor = Sponsors.query.filter(Sponsors.username.like('%'+filter_keyword+'%')).all()
            if matched_sponsor:
                return render_template("admin_pages/admin-find.html", user=current_user, allCampaigns=allCampaigns, allInfluencers=allInfluencers, allSponsors=matched_sponsor)

            matched_sponsor = Sponsors.query.filter(Sponsors.industry.like('%'+filter_keyword+'%')).all()
            if matched_sponsor:
                return render_template("admin_pages/admin-find.html", user=current_user, allCampaigns=allCampaigns, allInfluencers=allInfluencers, allSponsors=matched_sponsor)

        flash(f"Could not find {filter_keyword}", category='error')
        return redirect(url_for("admin.admin_find"))

