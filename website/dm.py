from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, session
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from flask_login import login_user, logout_user, current_user, login_required
import random
import string
from .models import User, Task, Post, Message
import os
import uuid
from . import db, socketio
import datetime
from sqlalchemy import or_


dm = Blueprint("dm", __name__)

rooms = {} #This is a dictionary that will store the room codes and the users in those rooms. The keys will be the room codes and the values will be lists of user ids. We can use this to keep track of which users are in which rooms and to send messages to the correct users when a message is sent in a room. 


@dm.route("/dm/@<userName>", methods=["GET", "POST"])
@login_required
def send_dm(userName):

    recepient = User.query.filter_by(userName=userName).first_or_404()

    session["recepient_id"] = recepient.id #We store the recepient_id in the session so that we can access it in the socketio event handlers. This way, when a message is sent, we can know who the recepient of the message is and we can save the message to the database with the correct sender and recepient ids.

    sender = current_user

    room_id = f"room_{ min(recepient.id, sender.id) }_{ max(recepient.id, sender.id) }"



    if room_id not in rooms:
        rooms[room_id] = {
                "members": {sender.id, recepient.id},
                "messages": [] #This will store the messages sent in this room. Each message will be a dictionary with the sender id, the message content, and the timestamp.
            }

    messages = Message.query.filter(
                                        or_(
                                                (Message.senderID == current_user.id) & (Message.recepientID == recepient.id),
                                                (Message.senderID == recepient.id) & (Message.recepientID == current_user.id)
                                            )
                                    ).order_by(Message.timeStamp.asc()).all()


    return render_template("dm.html", recepient = recepient, room_id = room_id, messages = messages)


@socketio.on("join")
def connect(data):

    room_id = data.get("room_id")

    if room_id in rooms:
        join_room(room_id)
        session["room_id"] = room_id

        print(f"\n'{current_user.userName}' has joined '{room_id}'\n")

        send(f"'{current_user.userName}' has entered the room.", to=room_id)   


    else:
        leave_room(room_id)


@socketio.on("disconnect")
def disconnect():

    room_id = session.get("room_id")

    print(f"\n'{current_user.userName}' has left room '{room_id}'.\n")


@socketio.on("send_message")
def send_message(data):

    room_id = data.get("room_id")
    msg_content = data.get("msg_content")                

    if not room_id or not msg_content: #This checks if the room_id or msg_content is empty. If either of them is empty, we don't want to send the message and we can just return from the function.
        return


    reply_data = {

        "sender": current_user.id,
        "msg_content": msg_content,
        "timestamp": datetime.datetime.now().strftime('%H:%M') 
    }

    print(f"\nReceived message from '{current_user.userName}' in '{room_id}': '{msg_content}'\n")

    print(f"User {current_user.userName} is {'authenticated' if current_user.is_authenticated else 'not authenticated'}.\n")

    emit("receive_message", reply_data, to=room_id)

    message = Message(senderID=current_user.id, recepientID=session.get("recepient_id"), content=msg_content, timeStamp=datetime.datetime.now())

    db.session.add(message)
    db.session.commit()    
