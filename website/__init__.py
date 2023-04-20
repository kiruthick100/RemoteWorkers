from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
from flask_mail import Mail,Message
from dotenv.main import load_dotenv
import os
load_dotenv()

USER_NAME = os.environ['MAIL_USERNAME']
USER_PASSWORD = os.environ['MAIL_PASSWORD']
SECRET_KEY = os.environ['SECRET_KEY']
# print(USER_NAME)

db = SQLAlchemy()
mail=Mail()

DB_NAME = "workers.db"

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] =SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] =f'sqlite:///{DB_NAME}'
    app.config['MAIL_SERVER'] ='smtp.gmail.com'
    app.config['MAIL_PORT'] =465
    app.config['MAIL_USERNAME']=USER_NAME
    app.config['MAIL_PASSWORD']=USER_PASSWORD
    app.config['MAIL_USE_TLS'] =False
    app.config['MAIL_USE_SSL']=True
    mail.init_app(app)

    db.init_app(app)

    from .views import views
    app.register_blueprint(views, url_prefix='/')
    create_database(app)
    login_manager=LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)
    from .models import User,Data
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app

def create_database(app): 
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        
