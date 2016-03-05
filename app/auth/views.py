# -*- coding: utf-8 -*-
__author__ = 'Jun'

from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from app.auth.forms import LoginForm, RegisterationForm
from app.models import User
import logging
from ..email import send_email
import datetime



@auth.route('/', methods=['GET', 'POST'])
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method=="POST" and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash(u'E-mail 주소 혹은 비빌번호가 맞지 않습니다.')
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html', form=form)




@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


#가천대 메일로 보내기
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterationForm()
    if form.validate_on_submit():
        try:
            now = datetime.datetime.now()
            user = User(email=form.email.data,
                        nickname=form.nickname.data,
                        student_num=form.student_num.data,
                        password=form.password.data,
                        member_since=now.strftime("%Y-%m-%d %H:%M:%S"))
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token()
            send_email(user.email+gachon_mail, 'Confirm your Account', 'auth/email/confirm', user=user, token=token)
            flash('A Confirmation email has been sent to your e-mail.')
            return redirect(url_for('auth.login'))
        except Exception, e:
            logging.exception(e)
            db.session.rollback()

    return render_template('auth/register.html', form=form)
