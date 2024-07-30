from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import current_user, login_required
from .model import db, Campaigns, Influencers, Sponsors, Admins, Completed_Campaigns, Ad_request, Influencer_requests
import requests
from collections import Counter
from .chartData import count_data, sponsor_niches_data, influencer_niches_data, campaign_niches_data, ad_request_status_data

admin = Blueprint("admin", __name__)

# API url
campaigns_api_url = "http://127.0.0.1:8000/api/campaign"
influencers_api_url = "http://127.0.0.1:8000/api/influencer"
sponsors_api_url = "http://127.0.0.1:8000/api/sponsor"
ad_request_api_url = "http://127.0.0.1:8000/api/ad_request"

@admin.route("/admin-profile")
def admin_profile():

    # Retrieving all the campaigns
    response = requests.get(campaigns_api_url)
    allCampaigns = response.json()
    allCampaigns = [campaign for campaign in allCampaigns if campaign['flagged'] == "True"]

    # Retrieving all the influencers
    response = requests.get(influencers_api_url)
    allInfluencers = response.json()
    allInfluencers = [influencer for influencer in allInfluencers if influencer['flagged'] == "True"]

    # Retrieving all the sponsors
    response = requests.get(sponsors_api_url)
    allSponsors = response.json()
    allSponsors = [sponsor for sponsor in allSponsors if sponsor['flagged'] == "True"]

    return render_template("admin_pages/admin-profile.html", user=current_user, allCampaigns=allCampaigns, allInfluencers=allInfluencers, allSponsors=allSponsors)

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

    # Total users and data generated
    get_count_data = count_data()
    count_labels = get_count_data[0]
    count_values = get_count_data[1]
    total_users = get_count_data[2]

    # Niches with the number of sponsors in it
    get_sponor_nice_data = sponsor_niches_data()
    sponsor_niche_labels = get_sponor_nice_data[0]
    sponsor_niche_values = get_sponor_nice_data[1]
    print(sponsor_niche_values)

    # Niches with the number of influencers in it
    get_influencer_nice_data = influencer_niches_data()
    influencer_niche_labels = get_influencer_nice_data[0]
    influencer_niche_values = get_influencer_nice_data[1]
    print(influencer_niche_values)

    # Niches with the number of campaigns in it
    get_campaign_nice_data = campaign_niches_data()
    campaign_niche_labels = get_campaign_nice_data[0]
    campaign_niche_values = get_campaign_nice_data[1]
    print(campaign_niche_values)

    # Status with the number of Ad Requests in it
    get_ad_request_status_data = ad_request_status_data()
    ad_request_status_labels = get_ad_request_status_data[0]
    ad_request_status_values = get_ad_request_status_data[1]
    print(ad_request_status_values)

    return render_template("admin_pages/admin-stats.html", user=current_user, labels=count_labels, values=count_values, total_users=total_users, sponsor_niche_labels=sponsor_niche_labels, sponsor_niche_values=sponsor_niche_values, influencer_niche_labels=influencer_niche_labels, influencer_niche_values=influencer_niche_values, campaign_niche_labels=campaign_niche_labels, campaign_niche_values=campaign_niche_values, ad_request_status_labels=ad_request_status_labels, ad_request_status_values=ad_request_status_values)

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

@admin.route("/flag-campaign/<int:id>")
@login_required
def flag_campaign(id):

    campaign = Campaigns.query.filter_by(id=id).first()
    campaign.flagged = "True"
    db.session.add(campaign)
    db.session.commit()

    flash("Campaign flagged successfully", category='success')
    return redirect(url_for("admin.admin_find"))

@admin.route("/unflag-campaign/<int:id>")
@login_required
def unflag_campaign(id):

    campaign = Campaigns.query.filter_by(id=id).first()
    campaign.flagged = "False"
    db.session.add(campaign)
    db.session.commit()

    flash("Flag removed successfully", category='success')
    return redirect(url_for("admin.admin_profile"))

@admin.route("/flag-influencer/<int:id>")
@login_required
def flag_influencer(id):
    
    influencer = Influencers.query.filter_by(id=id).first()
    influencer.flagged = "True"
    db.session.add(influencer)
    db.session.commit()

    flash("Influencer flagged successfully", category='success')
    return redirect(url_for("admin.admin_find"))

@admin.route("/unflag-influencer/<int:id>")
@login_required
def unflag_influencer(id):
    
    influencer = Influencers.query.filter_by(id=id).first()
    influencer.flagged = "False"
    db.session.add(influencer)
    db.session.commit()

    flash("Flag removed successfully", category='success')
    return redirect(url_for("admin.admin_profile"))

@admin.route("/flag-sponsor/<int:id>")
@login_required
def flag_sponsor(id):
    
    sponsor = Sponsors.query.filter_by(id=id).first()
    sponsor.flagged = "True"
    db.session.add(sponsor)
    db.session.commit()

    flash("Sponsor flagged successfully", category='success')
    return redirect(url_for("admin.admin_find"))

@admin.route("/unflag-sponsor/<int:id>")
@login_required
def unflag_sponsor(id):
    
    sponsor = Sponsors.query.filter_by(id=id).first()
    sponsor.flagged = "False"
    db.session.add(sponsor)
    db.session.commit()

    flash("Flag removed successfully", category='success')
    return redirect(url_for("admin.admin_profile"))

