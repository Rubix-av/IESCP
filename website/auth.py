from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from .model import db, Sponsors, Influencers
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

# User Login
@auth.route("/login", methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in!", category='error')
<<<<<<< HEAD
        return redirect(url_for("sponsor.sponsor_profile"))
=======
        return redirect(url_for("sponsors.sponsor_profile"))
>>>>>>> 2b168d6b922924fa139402d215fb5a59a878adf6
    
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        sponsor = Sponsors.query.filter_by(email=email).first()
        influencer = Influencers.query.filter_by(email=email).first()

        if sponsor:
            if check_password_hash(sponsor.password, password):
                login_user(sponsor, remember=True)
                flash("Login successfull!", category='success')
                return redirect(url_for("sponsor.sponsor_profile"))
            else:
                flash("Incorrect password!", category='error')
                return redirect(url_for("auth.login"))
        if influencer:
            if check_password_hash(influencer.password, password):
                login_user(influencer, remember=True)
                flash("Login successfull!", category='success')
                return redirect(url_for("influencers.influencer_profile"))
            else:
                flash("Incorrect password!", category='error')
                return redirect(url_for("auth.login"))
        else:
            flash("User doesn't exist!", category='error')
            return redirect(url_for("auth.login"))


    return render_template("login.html", user=current_user)

# Sponsor Register
@auth.route("/sponsor-register", methods=["GET","POST"])
def sponsor_register():
    if current_user.is_authenticated:
        flash("You are already logged in!", category='error')
        return redirect(url_for("sponsors.sponsor_profile"))
    
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        industry = request.form.get("industry")
        budget = int(request.form.get("budget"))
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        sponsor = Sponsors.query.filter_by(email=email).first()

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
            new_sponsor = Sponsors(email=email, username=username, industry=industry, budget=budget, password=generate_password_hash(password1))
            
            db.session.add(new_sponsor)
            db.session.commit()

            login_user(new_sponsor, remember=True)
            flash("User created successfully", category='success')
            return redirect(url_for("sponsors.sponsor_profile"))
            

    return render_template("sponsor_pages/sponsor-register.html", user=current_user)

# Influencer Register
@auth.route("/influencer-register", methods=["GET","POST"])
def influencer_register():
    if current_user.is_authenticated:
        flash("You are already logged in!", category='error')
        return redirect(url_for("influencers.influencer_profile"))
    
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        category = request.form.get("category")
        niche = request.form.get("niche")
        followers = request.form.get("followers")
        platform_preference = request.form.get("social")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        influencer = Influencers.query.filter_by(email=email).first()

        if influencer:
            flash("Influencer already exists!", category='error')
            return redirect(url_for("auth.login"))
        elif password1 != password2:
            flash("Incorrect password!", category='error')
            return redirect(url_for("auth.influencer_register"))
        else:
            new_influencer = Influencers(email=email, username=username, category=category, niche=niche, followers=followers, password=generate_password_hash(password1), platform_preference=platform_preference)
            
            db.session.add(new_influencer)
            db.session.commit()

            login_user(new_influencer, remember=True)
            flash("Influencer created successfully", category='success')
            return redirect(url_for("influencers.influencer_profile"))
        
    return render_template("influencer_pages/influencer-register.html", user=current_user)

# Logout User
@auth.route("logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", category='success')
    return redirect(url_for("auth.login"))
