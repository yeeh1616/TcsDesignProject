import csv
import math
import codecs
import os
from datetime import date
from sqlite3 import IntegrityError

import pandas as pandas
from flask import (
    Blueprint, flash, redirect, render_template, url_for,
    session, request)
from flask_login import login_required, current_user
import tkinter.filedialog
from tkinter import *
import tkinter
from tkinter.filedialog import *
from app import db, models
from app.decorators import check_confirmed
from app.forms import ModuleInfoForm, CommentForm
from app.models import Module, User, Comment, get_avg_stars, add_comment_by_entity, House, Student, Questionnaire, \
    Question_rate, get_question_avg_stars, Student, add_by_entity, update_by_entity, UserModule
import sqlite3
import json

bp = Blueprint('module_info', __name__, template_folder='templates/module')


@bp.route('/test1', methods=['GET', 'POST'])
def test1():
    module = Module('bbb', 'bbb')
    Module.add_a_module_by_enity(module)
    return 'module test'


@bp.route('/test2', methods=['GET', 'POST'])
def test2():
    return render_template('test2.html')


@bp.route('/test3', methods=['GET', 'POST'])
def test3():
    return render_template('modules_info.html', module=None)


@bp.route('/info', methods=['GET', 'POST'])
@login_required
@check_confirmed
def info():
    title = User.get_user_by_id(current_user.id).title
    module_id = request.args.get("id")
    session['moduleId'] = module_id
    user_id = current_user.id
    module = Module.query.filter_by(id=module_id).first()
    user = User.query.filter_by(id=user_id).first()
    comment_list = db.session.query(User.id, User.uname, User.img, Comment.module_id, Comment.content, Comment.star,
                                    Comment.date).filter(Comment.owner_id == User.id).filter(
        Comment.module_id == module_id).all()
    avg_star = get_avg_stars(module_id)

    star_dict = {}
    questionnaire = Questionnaire.get_questionnaire_by_mid(module_id)
    for q in questionnaire:
        star_dict[q.id] = 0
        q.avg_star = round(get_question_avg_stars(q.id, module_id).average, 1)

    if user.title == models.HOUSEKEEPER:
        return render_template('module_info_teacher.html',
                               module=module,
                               user=user,
                               commentList=comment_list,
                               totalComments=len(comment_list),
                               avgStar=avg_star,
                               questionnaire=questionnaire,
                               star_dict=json.dumps(star_dict),
                               title=title)
    else:
        house = House.get_house_by_housekeeper(current_user.id)
        notification_num = models.get_request_owner_list_count(house.house_id)
        title = User.get_user_by_id(current_user.id).title

        return render_template('module_info_student.html',
                               module=module,
                               user=user,
                               commentList=comment_list,
                               totalComments=len(comment_list),
                               avgStar=avg_star,
                               notification_num=notification_num,
                               title=title,
                               questionnaire=questionnaire,
                               star_dict=json.dumps(star_dict))


@bp.route('/edit', methods=['GET', 'POST'])
@login_required
@check_confirmed
def edit():
    title = User.get_user_by_id(current_user.id).title
    module = Module.query.filter_by(id=session.get('moduleId')).first()
    return render_template('edit_info.html', module=module,
                           title=title)


@bp.route('/save', methods=['GET', 'POST'])
@login_required
@check_confirmed
def save():
    form = ModuleInfoForm()
    module_id = session.get('moduleId')
    module_name = form.name.data
    module_desc = form.description.data
    module = Module(module_name, module_desc, current_user.id, None)
    module.id = module_id
    # if form.validate_on_submit():
    if Module.update_a_module_by_enity(module):
        return redirect(url_for('module_info.info', id=module_id))
    else:
        return 'Save module info error ..........'


@bp.route('/comment', methods=['GET', 'POST'])
@login_required
@check_confirmed
def comment():
    today = date.today()
    owner_id = current_user.id
    module_id = session.get('moduleId')
    form = CommentForm()
    star_dict = json.loads(form.star.data)
    avg_star = 0

    for k in star_dict:
        avg_star += star_dict[k]

    avg_star = math.ceil(avg_star / len(star_dict))

    content = form.comment.data
    comment = Comment(owner_id, module_id, content, avg_star, 0, today)
    add_comment_by_entity(comment)

    question_rate_list = []
    for k in star_dict:
        q = Question_rate(k, module_id, star_dict[k], comment.id)
        question_rate_list.append(q)

    Question_rate.add_question_rate_list(question_rate_list)
    return redirect(url_for('module_info.info', id=module_id))


@bp.route('/download', methods=['GET', 'POST'])
@login_required
@check_confirmed
def download():
    student = Student.get_full_info_by_id(current_user.id)
    houseid = student.house_id
    root = Tk()
    path_ = askdirectory(initialdir=os.getcwd(), title='Please select a directory')
    path_ = path_ + '/student.csv'
    root.destroy()
    try:
        conn = db.engine.raw_connection()
        # conn = sqlite3.connect('project_database')
        with open(path_, 'w+', newline='') as write_file:
            cursor = conn.cursor()
            cursor.execute('SELECT uname,email FROM user, student WHERE student.user_id ='
                           ' user.id AND student.house_id = ' + str(houseid))
            csv_writer = csv.writer(write_file)
            csv_writer.writerow([i[0] for i in cursor.description])
            csv_writer.writerows(cursor)
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()
    return 'Download Success'


@bp.route('/upload', methods=['GET', 'POST'])
@login_required
@check_confirmed
def upload():
    #root = Tk()
    path_ = askopenfilename(title='Please select csv file')
    #root.destroy()
    house = House.get_house_by_housekeeper(current_user.id)
    csvFile = codecs.open(path_, 'r', 'utf-8-sig')
    dict_reader = csv.DictReader(csvFile)
    # print (dict_reader)
    result = []
    for item in dict_reader:
        student = Student.query.filter_by(student_email=item["student_email"]).first()
        if student is None:
            student = Student(house_id=house.house_id, module_id=None, student_email=item["student_email"])
            add_by_entity(student)
        else:
            student.house_id = house.house_id
            update_by_entity(student)
        result.append(item["student_email"])
    print(result)
    # for row in dict_reader:
    #     print(row)

    # try:
    #     conn = db.engine.raw_connection()
    #     # conn = sqlite3.connect('project_database')
    #     df = pandas.read_csv(path_)
    #     # df.to_sql('student', conn, if_exists='append', index_label='user_id')
    #     for i in range(len(df)):
    #         try:
    #             df.iloc[i:i + 1].to_sql('student', conn, if_exists='append', index=False)
    #         except IntegrityError:
    #             pass
    # except sqlite3.Error as e:
    #     print(e)
    # finally:
    #     conn.close()
    return 'Upload Success'



@bp.route('/upload_module', methods=['GET', 'POST'])
@login_required
@check_confirmed
def upload_module():
    root = Tk()
    path_ = askopenfilename(title='Please select csv file')
    root.destroy()
    module_id = int(session['moduleId'])
    csvFile = codecs.open(path_, 'r', 'utf-8-sig')
    dict_reader = csv.DictReader(csvFile)
    # print (dict_reader)
    result = []
    for item in dict_reader:
        user_module = UserModule.query.filter_by(email=item["student_email"], module_id=module_id).first()
        if user_module is None:
            user_module = UserModule(email=item["student_email"], module_id=module_id, status=1)
            add_by_entity(user_module)
        else:
            user_module.status = 1
            update_by_entity(user_module)
        result.append(item["student_email"])
    print(result)

    # for row in dict_reader:
    #     print(row)

    # try:
    #     conn = db.engine.raw_connection()
    #     # conn = sqlite3.connect('project_database')
    #     df = pandas.read_csv(path_)
    #     # df.to_sql('student', conn, if_exists='append', index_label='user_id')
    #     for i in range(len(df)):
    #         try:
    #             df.iloc[i:i + 1].to_sql('student', conn, if_exists='append', index=False)
    #         except IntegrityError:
    #             pass
    # except sqlite3.Error as e:
    #     print(e)
    # finally:
    #     conn.close()
    return 'Upload Success'

