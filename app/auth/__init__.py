# -*- coding: utf-8 -*-
__author__ = 'Jun'


from flask import Blueprint
auth = Blueprint('auth', __name__)
from . import views
