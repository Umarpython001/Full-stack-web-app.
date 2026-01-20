from flask import Blueprint, render_template, redirect, request, flash, url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from .models import User, Task
from . import db
import uuid
import os


PROFILE_PICS_SUBDIR = "profile_pics"


def checkFile(name: str) -> bool: #This checks the file name to ensure that it is compatible
    allowed = {"png", "gif", "jpg", "jpeg", "avif", "webp"}
    if "." in set(name):
        diff = name.split(".")

        if len(diff) == 2:

            name, ext = diff[0], diff[1]

            if ext.lower() in allowed:

                return True

            return False
        return False
    return False

def checkUserConditions(firstName, lastName, email, password1, password2): #This collects all the user's primary info and checks if it's correct. It then creates a user model if it is.
    
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

    elif password1 != password2:
        flash("Passwords must match", category='error')
        return redirect(url_for("auth.sign_up"))

    user = User(email = email, 
                firstName = firstName, 
                lastName=lastName, 
                password = generate_password_hash(password1),
                )
            
    return user

auth = Blueprint("auth", __name__) #Initianlises the auth blueprint



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
                        flash("Logged in successfully", category="success")
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




"""Add a feature such that a user doesn't have to type all their information again if one thing goes wrong"""
@auth.route("/sign_up", methods = ["POST", "GET"])
def sign_up():

    if request.method == "POST":

        """
            First check for all the compulsory requirements and if they are all met, create the user instance. 
            Then check all optional user information, if they are given, just adjust the user instance with dot notation.
            Eg, user.optional_info = some_data
        """

        firstName = request.form["firstName_signUp"].strip()

        lastName = request.form["lastName_signUp"].strip()

        email = request.form["email_signUp"].strip()

        password1 = request.form["password1_signUp"].strip()

        password2 = request.form["password2_signUp"].strip()

        profilePic = request.files["profilePic"]

        print(profilePic)

        user = checkUserConditions(firstName, lastName, email, password1, password2)


        if profilePic:
            if not checkFile(profilePic.filename): #If the picture is of an invalid format
                flash("Profile picture is of invalid format", category='success')
                return redirect(url_for("auth.sign_up"))

            """
                Here we process the file given as the PFP.
                Get the file. 
                Generaate a unique file naem for that file. 
                Save it to the destination folder. 
                Add it to the user model.
            """
            profile_pic_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], PROFILE_PICS_SUBDIR)

            name, ext = profilePic.filename.rsplit(".", 1) #Split the file into the name and its extension

            unique_file_name = f"{uuid.uuid4().hex}.{ext.lower()}" #Generates a unique file name for that file.

            unique_file_path = os.path.join(profile_pic_dir, unique_file_name) #Generates a unique file path for that picture with the uique file name

            profilePic.save(unique_file_path) #Stores the image in the destination folder with the full file path(folder name + unique name generated). It means "Save this image at this location on my device"

            user.profilePic = f"uploads/{PROFILE_PICS_SUBDIR}/{unique_file_name}" #Stores the relative file name in the DB. Refrences that particular image with the user.

            
            
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
    flash("Logged out successfully", category="success")
    return redirect("/login")