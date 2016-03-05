# -*- coding: utf-8 -*-
__author__ = 'Jun'


from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextField, FloatField, TextAreaField
from wtforms.validators import Required, Length, Email, EqualTo, DataRequired, NumberRange
from wtforms import ValidationError
from ..models import User, Evaluation, Lecture

class SearchForm(Form):
    search = TextField('검색', validators=[DataRequired()])


class EvaluationForm(Form):
    opinion = TextAreaField('의견')
    attendance_score = StringField('출석',validators=[NumberRange(1,5)])
    grade_score = StringField('성적',validators=[NumberRange(1,5)])
    amount_score = StringField('학습량',validators=[NumberRange(1,5)])
    learn_score = StringField('배운점',validators=[NumberRange(1,5)])
    group_ox = StringField('그룹활동여부')
    submit = SubmitField('평가')

class EvaluationEditForm(Form):
    opinion = TextAreaField('의견')
    attendance_score = FloatField('출석',validators=[NumberRange(1,5)])
    grade_score = FloatField('성적',validators=[NumberRange(1,5)])
    amount_score = FloatField('학습량',validators=[NumberRange(1,5)])
    learn_score = FloatField('배운점',validators=[NumberRange(1,5)])
    submit = SubmitField('평가')

class ResetPasswordForm(Form):
    current_password = PasswordField(validators=[Required()])
    new_password = PasswordField(validators=[Required(), EqualTo('new_password_confirm', message='비밀번호가 맞지 않습니다.')])
    new_password_confirm = PasswordField(validators=[Required()])
    reset_button = SubmitField('비밀번호변경')