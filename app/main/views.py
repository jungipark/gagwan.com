# -*- coding: utf-8 -*-
__author__ = 'Jun'

from . import main
from flask import render_template, request, redirect, url_for, g, flash, jsonify
from flask.ext.login import login_required, current_user, user_unauthorized
from ..models import User, Lecture, Evaluation
from sqlalchemy import or_
from app.main.forms import SearchForm, EvaluationForm, EvaluationEditForm, ResetPasswordForm
from .. import db
import logging
import datetime


# 메인 페이지
@main.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    newEvl = db.session.query("nickname","profNm","lecture_id","evl_time","grade_score","grade_score","amount_score","learn_score","attendance_score","opinion","subjectNm").from_statement('select u.nickname, lec.profNm, evl.lecture_id, evl.evl_time, evl.grade_score, evl.amount_score, evl.learn_score, evl.attendance_score, evl.opinion, lec.subjectNm  from lecture as lec, evaluation as evl, user u where lec.id = evl.lecture_id and evl.user_id = u.id order by evl.id DESC limit 10;').all()
    return render_template('index.html', newEvl=newEvl)


# 검색 전역 객체 선언
@main.before_request
def before_request():
    if current_user is not None:
        g.user = current_user
        g.search_form = SearchForm()


# 검색하기
@main.route('/search', methods=['POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('main.index'))
    return redirect(url_for('main.search_results', query=g.search_form.search.data))


# 검색 결과
@main.route('/search_results/<query>')
@login_required
def search_results(query):

    results = Lecture.query.filter(or_(Lecture.subjectNm.like("%" + query + "%"),
                                       Lecture.profNm.like("%" + query + "%"))).order_by(Lecture.semester.desc()).all()
    return render_template('search_results.html', query=query, results=results)


# 내 프로필 보기
@main.route('/profile')
@login_required
def profile():
    user = User.query.filter_by(email=current_user).first()
    myopinion_count = db.session.query(Evaluation).filter(Evaluation.user_id==current_user.id).count()
    return render_template('profile.html', user=user, count=myopinion_count)


# 로그인 후 비밀번호 재설정
@main.route('/reset_password', methods=['GET','POST'])
@login_required
def reset_password():
    form = ResetPasswordForm()
    if request.method =='POST' :
        user = User.query.filter_by(email=current_user.email).first()
        if user is not None and user.verify_password(form.current_password.data):
            new_hash_passwd = user.reset_password(form.new_password.data)
            user.password_hash = new_hash_passwd
            db.session.commit()
            flash("비밀번호가 변경되었습니다.")
        else:
            flash("비밀번호 변경에 실패하였습니다. 다시 시도해주세요.")
    return render_template('password.html', form=form)


# 계정삭제 <-- 구현해야됨
@main.route('/delete_account', methods=['GET','POST'])
@login_required
def delete_account():
    return render_template('delete_account.html')


# 각 강의평가 바로가기 및 강의평가하기
@main.route('/evaluation/<lecture_id>', methods=['GET', 'POST'])
def evaluation(lecture_id):

    evlform = EvaluationForm()

    if request.method == 'POST':
        print 'test'
        now = datetime.datetime.now()
        if Evaluation.query.filter("lecture_id=:lecture_id and user_id=:user_id").params(lecture_id=lecture_id, user_id=current_user.id).first() is None:
            try:
                evldata = Evaluation(opinion=evlform.opinion.data,
                                     attendance_score=evlform.attendance_score.data,
                                     grade_score=evlform.grade_score.data,
                                     amount_score=evlform.amount_score.data,
                                     learn_score=evlform.learn_score.data,
                                     lecture_id=lecture_id,
                                     user_id=current_user.id,
                                     evl_time=now.strftime("%Y-%m-%d %H:%M:%S"))
                db.session.add(evldata)
                # 이미 평가한 댓글이 있는지 확인 후 댓글 카운트 +1
                EvlCountIs = Lecture.query.filter("id=:lecture_id").params(lecture_id=lecture_id).first()
                if EvlCountIs.evl_count is not None or 0:
                    EvlCountIs.evl_count += 1
                else :
                    EvlCountIs.evl_count = 1
                db.session.commit()
            except Exception,e:
                logging.exception(e)
                db.session.rollback()
        else :
            print "중복 강의 평가 불가"
            flash(u'각 강의당 강의 평가는 한 번만 할 수 있습니다.')
    results = Lecture.query.filter(Lecture.id == lecture_id).first()
    evlcomment = db.session.query("nickname","evl_time","grade_score","grade_score","amount_score","learn_score","attendance_score","opinion").from_statement('select * from user u, evaluation evl where u.id = evl.user_id and evl.lecture_id =:lecture_id order by evl.id desc;').params(lecture_id=lecture_id).all()
    avg = db.session.query("avg_attend","avg_grade","avg_amount","avg_learn").from_statement('SELECT round(avg(attendance_score),1) as avg_attend, round(avg(grade_score),1) avg_grade, round(avg(amount_score),1) avg_amount,round(avg(learn_score),1) avg_learn from evaluation where lecture_id=:lecture_id;').params(lecture_id=lecture_id).first()
    return render_template('evaluation.html', lecture_id=lecture_id, results=results, evlform=evlform,
                           evlcomment=evlcomment, avg=avg)


# 내 의견 보기
@main.route('/myopinion')
@login_required
def myopinion():
    myopinion = db.session.query("id","nickname","profNm","lecture_id","evl_time","grade_score","grade_score","amount_score","learn_score","attendance_score","opinion","subjectNm").from_statement('select evl.id, u.nickname, l.profNm, evl.lecture_id, evl.evl_time, evl.grade_score, evl.amount_score, evl.learn_score, evl.attendance_score, evl.opinion, l.subjectNm from evaluation evl, user u, lecture l where evl.user_id=u.id and evl.user_id=:user_id and evl.lecture_id = l.id order by evl.id desc ;').params(user_id=current_user.id).all()
    myopinion_count = db.session.query(Evaluation).filter(Evaluation.user_id==current_user.id).count()
    evlform = EvaluationEditForm()
    return render_template('myopinion.html', myopinion=myopinion, count=myopinion_count, evlform=evlform)


# 강의평가 수정
@main.route('/edit_opinion/<evl_id>', methods=['POST'])
@login_required
def edit_opinion(evl_id):
    evlform = EvaluationEditForm()

    if request.method == 'POST':
        try:
            evl_edit = Evaluation.query.filter("id=:evl_id and user_id=:user_id").params(evl_id=evl_id, user_id=current_user.id).first()
            evl_edit.attendance_score = evlform.attendance_score.data
            evl_edit.grade_score = evlform.grade_score.data
            evl_edit.amount_score = evlform.amount_score.data
            evl_edit.learn_score = evlform.learn_score.data
            evl_edit.opinion = evlform.opinion.data
            db.session.commit()
        except:
            print "update error"
    return redirect(url_for('main.myopinion'))


# 강의평가 삭제 / 삭제시 댓글 카운트 -1
@main.route('/del_opinion/<evl_id>')
@login_required
def del_opinion(evl_id):
    try:
         evl_del = Evaluation.query.filter("id=:evl_id and user_id=:user_id").params(evl_id=evl_id, user_id=current_user.id).first()
         db.session.delete(evl_del)
         evl_count = Lecture.query.filter_by(id=evl_del.lecture_id).first()
         evl_count.evl_count -= 1
         db.session.commit()
    except Exception,e :
        logging.exception(e)
        db.session.rollback()
        print "error"
    return redirect(url_for('main.myopinion'))


# 문의하기
@main.route('/contact')
@login_required
def contact():
    return render_template('contact.html')


# 안내 및 사용법
@main.route('/guide')
@login_required
def guide():
    return render_template('guide.html')

