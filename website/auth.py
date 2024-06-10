from flask import Blueprint, render_template

auth = Blueprint("auth", __name__)

@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route("/register")
def register():
    return render_template("register.html")

@auth.route("/sponsor-register")
def sponsor_register():
    return render_template("sponsor-register.html")

@auth.route("/influencer-register")
def influencer_register():
    return render_template("influencer-register.html")
