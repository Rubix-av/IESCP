from flask import Blueprint, render_template, request, url_for, redirect, flash
from .model import db, Sponsors, Influencers
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

# ==============User Login==============
@auth.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        sponsor = Sponsors.query.filter_by(username=username).first()
        influencer = Influencers.query.filter_by(username=username).first()

        if sponsor:
            if check_password_hash(sponsor.password, password):
                flash("Login successfull!", category='success')
                return redirect(url_for("views.sponsor_profile"))
            else:
                flash("Incorrect password!", category='error')
                return redirect(url_for("auth.login"))
        if influencer:
            if check_password_hash(influencer.password, password):
                flash("Login successfull!", category='success')
                return redirect(url_for("views.influencer_profile"))
            else:
                flash("Incorrect password!", category='error')
                return redirect(url_for("auth.login"))
        else:
            flash("User doesn't exist!", category='error')
            return redirect(url_for("auth.login"))


    return render_template("login.html")

# ==============Sponsor Register==============
@auth.route("/sponsor-register", methods=["GET","POST"])
def sponsor_register():
    if request.method == "POST":
        username = request.form.get("username")
        industry = request.form.get("industry")
        budget = int(request.form.get("budget"))
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        sponsor = Sponsors.query.filter_by(username=username).first()

        if sponsor:
            flash("User already exists!", category='error')
            return redirect(url_for("auth.login"))
        elif password1 != password2:
            flash("Incorrect password!", category='error')
            return redirect(url_for("auth.sponsor_register"))
        elif budget < 0:
            flash("You need to add some budget", category='error')
            return redirect(url_for("auth.sponsor_register"))
        else:
            new_sponsor = Sponsors(username=username, industry=industry, budget=budget, password=generate_password_hash(password1))
            
            db.session.add(new_sponsor)
            db.session.commit()

            flash("User created successfully", category='success')
            return redirect(url_for("views.sponsor_profile"))
            

    return render_template("sponsor/sponsor-register.html")

# ==============Influencer Register==============
@auth.route("/influencer-register", methods=["GET","POST"])
def influencer_register():
    if request.method == "POST":
        username = request.form.get("username")
        category = request.form.get("category")
        niche = request.form.get("niche")
        followers = request.form.get("followers")
        platform_preference = request.form.get("social")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        influencer = Influencers.query.filter_by(username=username).first()

        if influencer:
            flash("Influencer already exists!", category='error')
            return redirect(url_for("auth.login"))
        elif password1 != password2:
            flash("Incorrect password!", category='error')
            return redirect(url_for("auth.influencer_register"))
        else:
            new_influencer = Influencers(username=username, category=category, niche=niche, followers=followers, password=generate_password_hash(password1), platform_preference=platform_preference)
            
            db.session.add(new_influencer)
            db.session.commit()

            flash("Influencer created successfully", category='success')
            return redirect(url_for("views.influencer_profile"))
        
    return render_template("influencer/influencer-register.html")
