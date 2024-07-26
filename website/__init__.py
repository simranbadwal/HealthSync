from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import flask_login
db = SQLAlchemy()
DB_NAME = "database.db"


def app_create():
    app = Flask(__name__) #init flask
    app.config['SECRET_KEY'] = 'example' #key for incryption
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, HealthForm
    
    with app.app_context():
        db.create_all()

    login_manager = flask_login.LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(int(id))
    
    return app
