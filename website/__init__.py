from flask_login import LoginManager, current_user
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Message, Mail
from flask_xcaptcha import XCaptcha
from os import path

db = SQLAlchemy()
mail = Mail()
DB_NAME = "data.db"

def page_not_found(e):
    return render_template('404.html', user=current_user), 404

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.register_error_handler(404, page_not_found)

    app.config['SECRET_KEY'] = 'secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USE_SSL"] = True
    app.config["MAIL_USERNAME"] = 'acharby2007@gmail.com'
    app.config["MAIL_PASSWORD"] = 'krbatjilrlphqcjl'

    app.config['XCAPTCHA_SITE_KEY'] = "b062a75c-cc98-4f69-98e7-812e0ee1368b"
    app.config['XCAPTCHA_SECRET_KEY'] = "0x7Be2C8F0b484168f36d42a56dDea2e0d6561b596"
    app.config['XCAPTCHA_VERIFY_URL'] = "https://hcaptcha.com/siteverify"
    app.config['XCAPTCHA_API_URL'] = "https://hcaptcha.com/1/api.js"
    app.config['XCAPTCHA_DIV_CLASS'] = "h-captcha"

    db.init_app(app)
    mail.init_app(app)

    xcaptcha = XCaptcha(app=app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists(DB_NAME):
        db.create_all(app=app)
        print('Database Created!')