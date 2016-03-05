# -*- coding: utf-8 -*-
__author__ = 'Jun'


import os
from app import create_app
from app import db
from app.models import User
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand



app = create_app('default')
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

