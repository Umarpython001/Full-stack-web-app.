from flask import Blueprint, render_template, redirect, request, flash, url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from .models import User, Task
from . import db
import uuid
import os



def checkFile(name: str) -> bool:
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

def checkUserConditions(firstName, lastName, email, password1, password2): 
    
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





@auth.route("/sign_up", methods = ["POST", "GET"])
def sign_up():

    if request.method == "POST":

        """
            First check for all the compulsory requirements and if they are all met, create the user instance. 
            Then check all optional user information, if they are given, just adjust the user instance with dot notation.
            Eg, user.optional_info = some_data
        """

        firstName = request.form["firstName"].strip()

        lastName = request.form["lastName"].strip()

        email = request.form["email"].strip()

        password1 = request.form["password1"].strip()

        password2 = request.form["password2"].strip()

        profilePic = request.files["profilePic"]

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
            name, ext = profilePic.filename.rsplit(".", 1) #Split the file into the name and its extension

            unique_file_name = f"{uuid.uuid4().hex}.{ext}" #Generates a unique file name for that file.

            filePath = os.path.join(current_app.root_path, "static", "uploads", "profile_pics", unique_file_name) #Create a full file path for the image

            profilePic.save(filePath) #Stores the image in the destination folder with the full file path(folder name + unique name generated). 

            user.profilePic = filePath

            
            
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