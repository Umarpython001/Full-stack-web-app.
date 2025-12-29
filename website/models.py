from . import db


from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)

    email = db.Column(db.String(60), unique = True)

    firstName = db.Column(db.String(150))

    lastName = db.Column(db.String(150))

    password = db.Column(db.String(250))

    tasks = db.relationship("Task")




class Task(db.Model):

    id = db.Column(db.Integer, primary_key = True)

    taskName = db.Column(db.String(100), unique = True)

    taskDescription = db.Column(db.String(250))

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

