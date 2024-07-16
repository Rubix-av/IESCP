from flask import Blueprint, render_template
from flask_login import current_user

admin = Blueprint("admin", __name__)

@admin.route("/admin-profile")
def admin_profile():
    return render_template("admin_pages/admin-profile.html", user=current_user)

@admin.route("/admin-find")
def admin_find():
    return render_template("admin_pages/admin-find.html", user=current_user)

@admin.route("/admin-stats")
def admin_stats():
    return render_template("admin_pages/admin-stats.html", user=current_user)