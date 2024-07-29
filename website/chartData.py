from .model import db, Campaigns, Influencers, Sponsors, Admins, Completed_Campaigns, Ad_request, Influencer_requests
import requests
from collections import Counter

# API url
campaigns_api_url = "http://127.0.0.1:8000/api/campaign"
influencers_api_url = "http://127.0.0.1:8000/api/influencer"
sponsors_api_url = "http://127.0.0.1:8000/api/sponsor"
ad_request_api_url = "http://127.0.0.1:8000/api/ad_request"

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





