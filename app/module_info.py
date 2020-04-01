import csv
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
from app.models import Module, User, Comment, get_avg_stars, add_comment_by_entity, House
import sqlite3

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
    module_id = request.args.get("id")
    session['moduleId'] = module_id
    user_id = current_user.id
    module = Module.query.filter_by(id=module_id).first()
    user = User.query.filter_by(id=user_id).first()
    comment_list = db.session.query(User.id, User.uname, User.img, Comment.module_id, Comment.content, Comment.star,
                                    Comment.date).filter(Comment.owner_id == User.id).filter(
        Comment.module_id == module_id).all()
    avg_star = get_avg_stars(module_id)
    if user.title == models.HOUSEKEEPER:
        return render_template('module_info_teacher.html', module=module, user=user, commentList=comment_list,
                               totalComments=len(comment_list), avgStar=avg_star)
    else:
        house = House.get_house_by_housekeeper(current_user.id)
        notification_num = models.get_request_owner_list_count(house.house_id)
        title = User.get_user_by_id(current_user.id).title
        return render_template('module_info_student.html',
                               module=module, user=user,
                               commentList=comment_list,
                               totalComments=len(comment_list),
                               avgStar=avg_star,
                               notification_num=notification_num,
                               title=title)


@bp.route('/edit', methods=['GET', 'POST'])
@login_required
@check_confirmed
def edit():
    module = Module.query.filter_by(id=session.get('moduleId')).first()
    return render_template('edit_info.html', module=module)


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
    star = form.star.data
    content = form.comment.data
    comment = Comment(owner_id, module_id, content, star, 0, today)
    add_comment_by_entity(comment)
    return redirect(url_for('module_info.info', id=module_id))


@bp.route('/download', methods=['GET', 'POST'])
@login_required
@check_confirmed
def download():
    root = Tk()
    path_ = askdirectory(initialdir=os.getcwd(), title='Please select a directory')
    path_ = path_ + '/student.csv'
    root.destroy()
    try:
        conn = sqlite3.connect('project_database')
        with open(path_, 'w+', newline='') as write_file:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM user')
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
    root = Tk()
    path_ = askopenfilename(title='Please select a directory')
    root.destroy()
    try:
        conn = sqlite3.connect('project_database')
        df = pandas.read_csv(path_)
        # df.to_sql('student', conn, if_exists='append', index_label='user_id')
        for i in range(len(df)):
            try:
                df.iloc[i:i + 1].to_sql('student', conn, if_exists='append', index=False)
            except IntegrityError:
                pass
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()
    return 'Upload Success'
