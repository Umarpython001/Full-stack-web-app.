from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager, current_user
from flask_socketio import SocketIO, emit, join_room, leave_room


def create_db(app):
    if not os.path.exists(f"website\database.db"):
        with app.app_context():
            db.create_all()


db = SQLAlchemy()
socketio = SocketIO()



def create_app():


    app = Flask(__name__)


    app.config["SECRET_KEY"] = "We ArE UnItY"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static", "uploads")

    

    db.init_app(app)

    from .views import views
    from .auth import auth
    from .posts import posts
    from .dm import dm
    
    from .models import User


    app.register_blueprint(views)
    app.register_blueprint(auth)
    app.register_blueprint(posts)
    app.register_blueprint(dm)



    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = '/login'

    @login_manager.user_loader
    def get_user(id):
        person = User.query.get_or_404(int(id))
        return person

    create_db(app)

    return app






