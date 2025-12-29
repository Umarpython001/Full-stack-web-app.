from flask import Blueprint, render_template, redirect, request, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from .models import User, Task
from . import db


auth = Blueprint("auth", __name__)



@auth.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":

        email = request.form["email"].strip()

        password = request.form["password"].strip()

        if not email:
            return redirect("/login")


        if not password:
            return redirect("/login")


        if email and password:

            user = User.query.filter_by(email = email).first()

            if user:

                if check_password_hash(pwhash=user.password, password=password):
                    if login_user(user=user, remember=True):
                        return redirect(f"/user/<{user.id}>/home")
                    else:
                        flash("Wrong password", category="error")
                        return redirect("/login")

                else:
                    return redirect("/login")
            else:
                flash("User account does not exist. Create an account here", category="error")
                return redirect("/sign_up")


    else:
        return render_template("login.html")





@auth.route("/sign_up", methods = ["POST", "GET"])
def sign_up():

    if request.method == "POST":
        firstName = request.form["firstName"].strip()

        lastName = request.form["lastName"].strip()

        email = request.form["email"].strip()

        password1 = request.form["password1"].strip()

        password2 = request.form["password2"].strip()

        user = User.query.filter_by(email = email).first()

        if user:
            flash("Email already exists", category="error")
            return redirect(url_for("auth.sign_up"))
            
        if len(firstName) < 2:
            flash("First name must be at least 2 characters", category='error')
            return redirect(url_for("auth.sign_up"))

        elif len(lastName) < 2:
            flash("Last name must be at least 2 characters", category='error')
            return redirect(url_for("auth.sign_up"))

        elif ("." not in email) or ("@" not in email) or (len(email) < 2):
            flash("Invalid email", category='error')
            return redirect(url_for("auth.sign_up"))

        elif len(password1) < 7:
            flash("Password must be at least 7 characters", category='error')
            return redirect(url_for("auth.sign_up"))

        elif len(password2) < 7:
            flash("Password confirm must be at least 7 characters", category='error')
            return redirect(url_for("auth.sign_up"))

        elif password1 != password2:
            flash("Passwords must match", category='error')
            return redirect(url_for("auth.sign_up"))

        else:
            user = User(email = email, firstName = firstName, lastName=lastName, password = generate_password_hash(password1))
            
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)

            flash("Account created successfully", category="success")

            return redirect(f"/user/<{user.id}>/home")
    else:
        return render_template("sign_up.html")




@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")