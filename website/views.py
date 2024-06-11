from flask import Blueprint, render_template

views = Blueprint("views", __name__)

@views.route("/sponsor-profile")
def sponsor_profile():
    return render_template("sponsor/sponsor-profile.html")

@views.route("/influencer-profile")
def influencer_profile():
    return render_template("influencer/influencer-profile.html")
