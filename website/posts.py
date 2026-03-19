from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from .models import User, Task, Post
from . import db
import uuid
import os
from werkzeug.utils import secure_filename
import time

posts = Blueprint("posts", __name__)

POSTS_SUBDIR = "user_posts"


@posts.route("/user/create_post", methods = ["GET", "POST"])
@login_required
def create_post():
    if request.method == "GET":
        return render_template("create_post.html")
    else: #The method is post which means that the user has submitted the post form
        
        caption = request.form["caption"]

        picture = request.files["post_image"]

        post = Post(user_id = current_user.id)

        if caption.strip() not in {"", " "} and len(caption) >2:
            post.caption = caption


        if picture:
            from .auth import checkFile
            if not checkFile(picture.filename):
                flash("Picture is of invalid format", category='error')
                return redirect(url_for("posts.create_post"))
                

            posts_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], POSTS_SUBDIR)

            uploaded_post_filename = picture.filename
            secure_uploaded_post_filename = secure_filename(uploaded_post_filename) #This gives a secure format for the file name to avoid any issues.

            name, ext = secure_uploaded_post_filename.rsplit(".", 1)  #Split the file into the name and its extension

            unique_post_name = f"{uuid.uuid4().hex}.{ext.lower()}" #Generates a unique file name for that file.
            
            post.picture = unique_post_name #Stores the unique file name in the DB for reference.

            unique_post_file_path = os.path.join(posts_dir, unique_post_name) #Generates a unique file path for that picture with the uique file name. It is the path that the picture will be stored in.

            picture.save(unique_post_file_path) #Stores the image in the destination folder with the full file path(folder name + unique name generated). It means "Save this image at this location on my device"

            db.session.add(post)
            db.session.commit()
        else:
            flash(message="Post must have a picture", category="error")
            return redirect(url_for('posts.create_post'))



        flash(message="Post uploaded successfully", category="success")
        return redirect(url_for('views.home'))