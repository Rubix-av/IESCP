from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from .model import db
from datetime import datetime

influencer = Blueprint("influencer", __name__)

@influencer.route("/influencer-profile")
@login_required
def influencer_profile():
    return render_template("influencer_page/influencer-profile.html", user=current_user)