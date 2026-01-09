from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, current_user



def create_db(app):
    if not path.exists(f"website\database.db"):
        with app.app_context():
            db.create_all()


db = SQLAlchemy()




def create_app():


    app = Flask(__name__)


    app.config["SECRET_KEY"] = "We ArE UnItY"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

    

    db.init_app(app)

    from .views import views
    from .auth import auth

    from .models import User


    app.register_blueprint(views)
    app.register_blueprint(auth)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = '/login'

    @login_manager.user_loader
    def get_user(id):
        person = User.query.get_or_404(int(id))
        return person

    create_db(app)

    return app






