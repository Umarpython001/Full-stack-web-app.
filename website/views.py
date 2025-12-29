from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user


views = Blueprint("views", __name__)

@views.route("/user/<id>/home")
@login_required
def home(id):
    return render_template("home.html")


@views.route("/")
@login_required
def plain_route():
    return redirect(f"/user/<{current_user.id}>/home") #Redirect the user to the home page when they visit the main route




@views.route("/user/<id>/profile")
@login_required
def profile(id):
    return render_template("profile.html")
    

