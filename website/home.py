from flask import Blueprint, render_template
from flask_login import login_user

home = Blueprint("home", __name__)

@home.route("/")
def home_page():
    return render_template("home.html", user=login_user)