# -*- coding: utf-8 -*-
__author__ = 'Jun'

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextField
from wtforms.validators import Required, Length, Email, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
    email = StringField('E-mail', validators=[Required(), Length(1, 64)])
    password = PasswordField('비밀번호', validators=[Required()])
    submit = SubmitField('로그인')



class RegisterationForm(Form):
    email = StringField('E-mail', validators=[Required(), Length(1, 64), Email(u'E-mail 주소를 입력해주세요') ])
    nickname = StringField('닉네임', validators=[Required(), Length(1, 20)])
    student_num = IntegerField('입학년도')
    password = PasswordField('비밀번호', validators=[Required(), EqualTo('password_confirm', message='똑같은 비밀번호를 입력해주세요.')])
    password_confirm = PasswordField('비밀번호 확인', validators=[Required()])
    submit = SubmitField('회원가입')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'입력하신 E-Mail 이 이미 사용중 입니다.')

    def validate_nikname(self, field):
        if User.nickname.filter_by(nikname=field.data).first():
            raise ValidationError(u'입력하신 닉네임이 사용중입니다.')
