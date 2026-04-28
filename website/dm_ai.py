from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, session
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from flask_login import login_user, logout_user, current_user, login_required
import random
import string
from website import dm
from .models import User, Task, Post, Message
import os
import uuid
from . import db, socketio
import datetime
from sqlalchemy import or_
import json
import requests
import time


def ask_model(question):
    url = "http://127.0.0.1:11434/api/generate" 
    payload = {
            "model": "qwen3-vl:4b",
            "prompt": question,
    }

    print("Sending request to the model...")
    start = time.time()
    response = requests.post(url, json=payload, timeout=60)
    response.raise_for_status()

    answer = ""
    for line in response.iter_lines(decode_unicode=True):
        if line:
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                print(f"Failed to decode JSON: {line}")
            else:
                if data["response"] not in {"", None}:
                    answer += data["response"]
    
    end = time.time()

    time_taken = end - start
    
    result = {
        "answer": answer,
        "time_taken": time_taken
    }

    return result



dm_ai = Blueprint("dm_ai", __name__)


@dm_ai.route("/dm/ai_chatbot/@<model_name>", methods=["GET", "POST"])
@login_required
def dm_ai_model(model_name):

    print("TExting with AI model!!")

    model = User.query.filter_by(userName=model_name).first()

    session["model_name"] = model.userName

    messages = Message.query.filter(
                                        or_(
                                                (Message.senderID == current_user.id) & (Message.recepientID == model.id),
                                                (Message.senderID == model.id) & (Message.recepientID == current_user.id)
                                            )
                                    ).order_by(Message.timeStamp.asc()).all()


    return render_template("dm_ai.html", model=model, messages=messages)



@socketio.on("send_message_to_ai")
def send_message(data):

    msg_content = data.get("msg_content")
    model_id = data.get("model_id")
    model_name = data.get("modelName")

    reply_data = {
        "msg_content": msg_content,
        "timestamp": datetime.datetime.now().strftime('%H:%M') 
    }


    emit("receive_message_from_human", reply_data,)

    user_message = Message(senderID=current_user.id, recepientID=model_id, content=msg_content, timeStamp=datetime.datetime.now())

    db.session.add(user_message)
    db.session.commit()

    """
    PART TWO - Send the message to the model and get the response, then emit the response back to the client
    """

    try:
        ai_response = ask_model(msg_content) 
    except Exception as e:
        print(f"Error communicating with the model: {e}")
        ai_response = {
            "answer": "Sorry, there was an error communicating with the model. Please try again later.",
            "timestamp": datetime.datetime.now().strftime('%H:%M')
        }
        emit("ai_reply", ai_response)
    else:   
        answer = ai_response["answer"]
        time_taken = ai_response["time_taken"]


        emit("ai_reply", {"answer": answer, "time_taken": time_taken, "timestamp": datetime.datetime.now().strftime('%H:%M')},)

        model_message = Message(senderID=model_id, recepientID=current_user.id, content=answer, timeStamp=datetime.datetime.now())

        db.session.add(model_message)
        db.session.commit()    
