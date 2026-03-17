from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash
from flask_login import login_required, current_user
from .models import User
import os
import uuid
from . import db
from werkzeug.utils import secure_filename


views = Blueprint("views", __name__)

PROFILE_PICS_SUBDIR = "profile_pics"
ALLOWED_EXTENSIONS = {"png", "gif", "jpg", "jpeg", "avif", "webp"}


@views.route("/user/home")
@login_required
def home():
    return render_template("home.html")


@views.route("/")
@login_required
def plain_route():
    return redirect(f"/user/home") #Redirect the user to the home page when they visit the main route



@views.route("/user/profile")
@login_required
def profile():
    return render_template("profile.html")
    

@views.route("/user/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    if request.method == "POST":

        user = current_user

        edited_first_name = request.form["editFirstName"]
        edited_last_name = request.form["editLastName"]
        edited_email = request.form["editEmail"]
        edited_PFP = request.files["editPFP"]


        if edited_first_name != user.firstName and len(edited_first_name) > 2: 
            user.firstName = edited_first_name

        if edited_last_name != user.lastName and len(edited_last_name) > 2:
            user.lastName = edited_last_name

        if edited_email != user.email and len(edited_email) > 7 and ("@" and ".") in edited_email:
            user.email = edited_email

        if edited_PFP:
            if user.uniqueProfilePicName != "default_image_headshot.png": #Even if a user uploads a file named "default_image_headshot.png", we won't delete that because we would have given it a unique name.
                
                old_PFP_path = os.path.join(
                    current_app.config["UPLOAD_FOLDER"], 
                    PROFILE_PICS_SUBDIR, 
                    user.uniqueProfilePicName   
                                )    

                if os.path.exists(old_PFP_path): #checks if the old profile picture exists before trying to delete it            
                    os.remove(old_PFP_path) #Removes the old profile picture from the server's local storage to save space
                else:
                    print("Old profile picture not found, skipping deletion.")

            profile_pic_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], PROFILE_PICS_SUBDIR)

            secure_uploaded_filename = secure_filename(edited_PFP.filename)

            name, ext = secure_uploaded_filename.rsplit(".", 1)  #Split the file into the name and its extension

            if ext.lower() in ALLOWED_EXTENSIONS:

                unique_file_name = f"{uuid.uuid4().hex}.{ext.lower()}"  #Generates a unique file name for that file.    
                user.uniqueProfilePicName = unique_file_name

                unique_file_path = os.path.join(profile_pic_dir, unique_file_name)
                edited_PFP.save(unique_file_path)
                
                user.profilePic = f"uploads/{PROFILE_PICS_SUBDIR}/{unique_file_name}" #Stores the relative file name in the DB. Refrences that particular image with the user. We can't use os.path.join here because in HTML, the forward slash is used as the path separator.
            else:
                flash("Profile picture is of invalid format", category='error')
                return redirect(url_for("views.edit_profile"))

        db.session.commit()
        flash("Credentials updated", category="success")
        return redirect("/user/profile")
    else:
        return render_template("edit_profile.html")


@views.route("/user/create_post", methods = ["GET", "POST"])
@login_required
def create_post():
    if request.method == "GET":
        return render_template("create_post.html")
    else:
        flash(message="Post uploaded successfully", category="success")
        return redirect(f"/user/home")