# -*- coding: utf-8 -*-
__author__ = 'Jun'

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask.ext.login import UserMixin
from flask import current_app, request, url_for
from . import db, login_manager
from sqlalchemy.orm import relationship, backref
import flask.ext.whooshalchemy as whooshalchemy



class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    nickname = db.Column(db.String(64), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    member_since = db.Column(db.DateTime(), default=datetime.now())
    student_num = db.Column(db.Integer)
    user_confirmed = db.Column(db.Boolean, default=False)
    evaluations = relationship("Evaluation", backref="User")

    @property
    def password(self):
        raise AttributeError('password is not a readble a attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def reset_password(self, new_password):
        new_password_hash = generate_password_hash(new_password)
        return new_password_hash

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirmed(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = '1'
        db.session.add(self)
        return True

    def generate_reset_token(self,expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def uncofirmed_reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('ascii')

    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<User %r>' % self.email


class Professor(db.Model):
    __tablename__ = 'professor'

    id = db.Column(db.Integer, primary_key=True)
    profNm = db.Column(db.String(64), index=True)
    dept = db.Column(db.String(64))
    photo_addr = db.Column(db.String(128), index=True)
    proCD = db.Column(db.Integer, unique=True, index=True)


class Lecture(db.Model):
    __tablename__ = 'lecture'
    __searchable__ = ['subjectNm', 'profNm']

    id = db.Column(db.Integer, primary_key=True)
    haksuNo = db.Column(db.Integer)
    subjectNm = db.Column(db.String(64), index=True)
    areaNm = db.Column(db.String(128))
    isuNm = db.Column(db.String(64))
    sisu = db.Column(db.String(64))
    dpt = db.Column(db.String(64))
    profNm = db.Column(db.String(64), index=True)
    time = db.Column(db.String(128))
    room = db.Column(db.String(64))
    maxPerson = db.Column(db.Integer)
    proCD = db.Column(db.Integer)
    cyberYn = db.Column(db.String(64))
    semester = db.Column(db.String(64))
    evl_count = db.Column(db.Integer)



class Evaluation(db.Model):
    __tablename__ = 'evaluation'

    id = db.Column(db.Integer, primary_key=True)
    opinion = db.Column(db.Text)
    evl_time = db.Column(db.DateTime(), default=datetime.now())
    totalAvg_score = db.Column(db.Float)
    attendance_score = db.Column(db.Float)
    grade_score = db.Column(db.Float)
    amount_score = db.Column(db.Float)
    learn_score = db.Column(db.Float)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

