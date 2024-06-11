from flask import Blueprint, render_template, request, url_for, redirect

auth = Blueprint("auth", __name__)

@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route("/sponsor-register", methods=["GET","POST"])
def sponsor_register():
    if request.method == "POST":
        username = request.form.get("username")
        industry = request.form.get("industry")
        budget = request.form.get("budget")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

    return render_template("sponsor/sponsor-register.html")

@auth.route("/influencer-register")
def influencer_register():
    return render_template("influencer/influencer-register.html")
