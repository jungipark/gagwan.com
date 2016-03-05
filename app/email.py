__author__ = 'Jun'

# -*- coding: utf-8 -*-

from threading import Thread
from flask import current_app, render_template
from flask.ext.mail import Message
from app import mail


def send_anysc_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['GAGWAN_MAIL_SUBJECT_PRIFIX'] + '' + subject,
                  sender=app.config['GAGWAN_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_anysc_email, args=[app,msg])
    thr.start()
    return thr