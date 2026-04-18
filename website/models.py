from . import db
from flask_login import UserMixin
from datetime import datetime


PROFILE_PICS_SUBDIR = "profile_pics"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)

    email = db.Column(db.String(60), unique = True)

    firstName = db.Column(db.String(150))

    lastName = db.Column(db.String(150))

    userName = db.Column(db.String(150), unique=True)

    password = db.Column(db.String(250))

    profilePic = db.Column(
                            
                            db.String(250), 
                            nullable=False,
                            default=f"images/default_image_headshot.png"

                        )

    uniqueProfilePicName = db.Column(
        
                                        db.String(250), 
                                        nullable=False,
                                        default="default_image_headshot.png"
                                        
                                        )

    @property
    def chat_partners(self):
        from website.models import Message, User
        
        # Get IDs of everyone interacted with
        sent_to = Message.query.filter_by(senderID=self.id).with_entities(Message.recepientID).distinct().all()
        received_from = Message.query.filter_by(recepientID=self.id).with_entities(Message.senderID).distinct().all()
        
        chat_ids = {uid[0] for uid in sent_to} | {uid[0] for uid in received_from}
        
        # Fetch the actual User objects for those IDs
        return User.query.filter(User.id.in_(chat_ids)).all()

    tasks = db.relationship("Task")
    
    posts = db.relationship("Post", backref='author', lazy=True)


    sent_messages = db.relationship(
        'Message', 
        foreign_keys='Message.senderID', 
        backref='sender', 
        lazy=True
    )


    received_messages = db.relationship(
        'Message', 
        foreign_keys='Message.recepientID', 
        backref='recipient', 
        lazy=True
    )

    def __repr__(self):
        return f"Name: {self.userName}"


class Task(db.Model):

    id = db.Column(db.Integer, primary_key = True)

    taskName = db.Column(db.String(100), unique = True)

    taskDescription = db.Column(db.String(250))

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False) #ID of user that posted the post

    caption = db.Column(db.String(500), nullable=True)

    picture = db.Column(db.String(250), nullable=False) #A file path for where the picture is stored in the server's memory

    date_posted = db.Column(

                            db.DateTime, 
                            nullable=False,
                            default = datetime.utcnow,
                            
                            )
    
    def __repr__(self):
        return f"Id: {self.id}\n user_id: {self.user_id}"




class Message(db.Model):

    id = db.Column(db.Integer, primary_key = True)

    senderID = db.Column(
                            db.Integer, 
                            db.ForeignKey("user.id"), 
                            nullable=False
                            )

    recepientID = db.Column(
                            db.Integer, 
                            db.ForeignKey("user.id"), 
                            nullable=False
                            )

    content = db.Column(db.Text, nullable=False)

    timeStamp = db.Column(
                            db.DateTime, 
                            nullable=False,
                            default = datetime.utcnow,
                            )