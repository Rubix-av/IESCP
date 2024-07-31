from .model import db, Campaigns, Influencers, Sponsors, Admins, Completed_Campaigns, Ad_request, Influencer_requests
import requests
from collections import Counter

# API url
campaigns_api_url = "http://127.0.0.1:8000/api/campaign"
influencers_api_url = "http://127.0.0.1:8000/api/influencer"
sponsors_api_url = "http://127.0.0.1:8000/api/sponsor"
ad_request_api_url = "http://127.0.0.1:8000/api/ad_request"
influencer_request_api_url = "http://127.0.0.1:8000/api/inf_request"

def count_data():

    # Total users and data generated
    count_data = [
        ("Sponsors", Sponsors.query.count()),
        ("Influencers", Influencers.query.count()),
        ("Admins", Admins.query.count()),
        ("Completed Campaigns", Completed_Campaigns.query.count()),
        ("Ad Requests", Ad_request.query.count()),
        ("Influencer Requests", Influencer_requests.query.count()),
        ("Campaigns", Campaigns.query.count()),
    ]

    count_labels = [row[0] for row in count_data]
    count_values = [row[1] for row in count_data]
    total_users = count_values[0] + count_values[1]

    return [count_labels, count_values, total_users]

def sponsor_niches_data():

    # Niches with the number of sponsors in it
    response = requests.get(sponsors_api_url)
    allSponsors = response.json()

    sponsor_niches = [sponsor['niche'] for sponsor in allSponsors]
    niche_counts = Counter(sponsor_niches)
    formatted_results = [(niche, count) for niche, count in niche_counts.items()]
    
    sponsor_niche_labels = [row[0] for row in formatted_results]
    sponsor_niche_values = [row[1] for row in formatted_results]

    return [sponsor_niche_labels, sponsor_niche_values]

def influencer_niches_data():

    # Niches with the number of sponsors in it
    response = requests.get(influencers_api_url)
    allInfluencers = response.json()

    influencer_niches = [influencer['niche'] for influencer in allInfluencers]
    niche_counts = Counter(influencer_niches)
    formatted_results = [(niche, count) for niche, count in niche_counts.items()]
    
    influencer_niche_labels = [row[0] for row in formatted_results]
    influencer_niche_values = [row[1] for row in formatted_results]

    return [influencer_niche_labels, influencer_niche_values]

def campaign_niches_data():

    # Niches with the number of campaigns in it
    response = requests.get(campaigns_api_url)
    allCampaigns = response.json()

    campaign_niches = [campaign['niche'] for campaign in allCampaigns]
    niche_counts = Counter(campaign_niches)
    formatted_results = [(niche, count) for niche, count in niche_counts.items()]
    
    campaign_niche_labels = [row[0] for row in formatted_results]
    campaign_niche_values = [row[1] for row in formatted_results]

    return [campaign_niche_labels, campaign_niche_values]

def campaign_budget_data(id):

    # Niches with the number of campaigns in it
    response = requests.get(campaigns_api_url)
    allCampaigns = response.json()

    allCampaigns = [campaign for campaign in allCampaigns if campaign.get("sponsor_id") == id]

    formatted_results = [
    (campaign.get("title"), campaign.get("budget"))
    for campaign in allCampaigns
    if campaign.get("sponsor_id") == id
]
    
    campaign_budget_labels = [row[0] for row in formatted_results]
    campaign_budget_values = [row[1] for row in formatted_results]

    return [campaign_budget_labels, campaign_budget_values]

def ad_request_status_data():

    # Status with the number of Ad Requests in it
    response = requests.get(ad_request_api_url)
    allAdRequests = response.json()

    formatted_results = []

    initial_count = {
        "Pending": 0,
        "Accepted": 0,
        "Rejected": 0,
    }

    for i in allAdRequests:
        initial_count[i.get("status")] += 1

    for (key,value) in initial_count.items():
        formatted_results.append((key,value))

    ad_request_status_labels = [row[0] for row in formatted_results]
    ad_request_status_values = [row[1] for row in formatted_results]

    return [ad_request_status_labels, ad_request_status_values]

def influencer_request_status_data(id):

    # Status with the number of Influencer in it
    response = requests.get(influencer_request_api_url)
    allInfRequests = response.json()
    allInfRequests = [infRequest for infRequest in allInfRequests if infRequest.get("influencer_id") == id]

    formatted_results = []

    initial_count = {
        "Pending": 0,
        "Accepted": 0,
        "Rejected": 0,
    }

    for i in allInfRequests:
        initial_count[i.get("status")] += 1

    for (key,value) in initial_count.items():
        formatted_results.append((key,value))

    inf_request_status_labels = [row[0] for row in formatted_results]
    inf_request_status_values = [row[1] for row in formatted_results]

    return [inf_request_status_labels, inf_request_status_values]

def ad_request_budget_data(id):

    # Niches with the number of campaigns in it
    response = requests.get(ad_request_api_url)
    allAdRequests = response.json()

    allAdRequests = [adRequest for adRequest in allAdRequests if adRequest.get("influencer_id") == id and adRequest.get("status") == "Accepted"]

    formatted_results = [
    (adRequest.get("id"), adRequest.get("payment_amount"))
    for adRequest in allAdRequests
    if adRequest.get("sponsor_id") == id
]
    
    ad_request_payment_amt_labels = [row[0] for row in formatted_results]
    ad_request_payment_amt_values = [row[1] for row in formatted_results]

    return [ad_request_payment_amt_labels, ad_request_payment_amt_values]

def campaigns_ad_request_data(id):
    response = requests.get(ad_request_api_url)
    allAdRequests = response.json()

    allAdRequests = [request for request in allAdRequests if request.get("sponsor_id") == id]

    campaign_counts = {}
    formatted_results = []

    for request in allAdRequests:
        campaign_id = request["campaign_id"]
        if campaign_id in campaign_counts:
            campaign_counts[campaign_id] += 1
        else:
            campaign_counts[campaign_id] = 1

    for (key,value) in campaign_counts.items():
        formatted_results.append((f"Campaign {key}",value))

    ad_request_budget_labels = [row[0] for row in formatted_results]
    ad_request_budget_values = [row[1] for row in formatted_results]

    return [ad_request_budget_labels, ad_request_budget_values]

def blocked_influencers_data():

    response = requests.get(influencers_api_url)
    influencers = response.json()

    formatted_results = []

    blocked_users_data = {
        "Blocked": 0,
        "Unblocked": 0,
    }

    for i in influencers:
        if i.get("flagged") == "True":
            blocked_users_data["Blocked"] += 1
        else:
            blocked_users_data["Unblocked"] += 1

    for (key,value) in blocked_users_data.items():
        formatted_results.append((key,value))

    blocked_influencers_labels = [row[0] for row in formatted_results]
    blocked_influencers_values = [row[1] for row in formatted_results]

    return [blocked_influencers_labels, blocked_influencers_values]

def blocked_sponsors_data():

    response = requests.get(sponsors_api_url)
    sponsors = response.json()

    formatted_results = []

    blocked_users_data = {
        "Blocked": 0,
        "Unblocked": 0,
    }

    for i in sponsors:
        if i.get("flagged") == "True":
            blocked_users_data["Blocked"] += 1
        else:
            blocked_users_data["Unblocked"] += 1

    for (key,value) in blocked_users_data.items():
        formatted_results.append((key,value))

    blocked_sponsors_labels = [row[0] for row in formatted_results]
    blocked_sponsors_values = [row[1] for row in formatted_results]

    return [blocked_sponsors_labels, blocked_sponsors_values]


