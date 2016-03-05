# -*- coding: utf-8 -*-
__author__ = 'Jun'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


from flask import Flask
from config import config
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from flask.ext.pagedown import PageDown
from flask_debugtoolbar import DebugToolbarExtension



login_manager = LoginManager()
bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
pagedown = PageDown()
toolbar = DebugToolbarExtension()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.debug = True

    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    #toolbar.init_app(app)


    from . auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from . main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    return app

