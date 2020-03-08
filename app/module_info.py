from flask import (
    Blueprint, flash, redirect, render_template, url_for,
    session, request)

from app import db
from app.forms import ModuleInfoForm, CommentForm
from app.models import Module, User, Comment, get_avg_stars, add_comment_by_entity

bp = Blueprint('module_info', __name__, template_folder = 'templates/module')


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


# @bp.route('/info', methods=['GET', 'POST'])
# # @login_required
# def info(id):
#     '''
#     1.根据 id 查找 module 对象
#     2.返回module页面
#     '''
#     module = Module.query.filter_by(id=id).first()
#     return render_template('module_info.html', module=module)


@bp.route('/info', methods=['GET', 'POST'])
# @login_required
def info():
    tempUserId = '1'
    moduleId = request.args.get("id")
    # 存module id 到 session
    session['moduleId'] = 'moduleId'
    userId = tempUserId
    module = Module.query.filter_by(id=moduleId).first()
    user = User.query.filter_by(id=userId).first()
    # commentList = Comment.query.filter_by(module_id=moduleId).all()
    commentList = db.session.query(User.id, User.uname, User.img, Comment.content, Comment.module_id).filter(Comment.owner_id == User.id).filter(Comment.module_id==moduleId).all()
    avg_star = get_avg_stars(moduleId)
    return render_template('module_info.html', module=module, user=user, commentList=commentList, totalComments=len(commentList), avgStar=avg_star)


@bp.route('/edit', methods=['GET', 'POST'])
# @login_required
def edit():
    form = ModuleInfoForm()
    module = Module.query.filter_by(id=form.id.data).first()
    return render_template('edit_info.html', module=module)


@bp.route('/save', methods=['GET', 'POST'])
# @login_required
def save():
    moduleInfoForm = ModuleInfoForm()
    module = Module(moduleInfoForm.id.data, moduleInfoForm.name.data, moduleInfoForm.description.data)
    # if moduleInfoForm.validate_on_submit():
    if Module.update_a_module_by_enity(module):
        return render_template('module_info.html', module=module)
    else:
        return 'Dam..........'


@bp.route('/comment', methods=['GET', 'POST'])
def comment():
    form = CommentForm()
    comment = Comment(0, '3', form.comment.data, 0, 0)
    # comment.stars = form.stars
    # comment.owner_id = session.get('uid')
    # comment.module_id = session.get('module_id')
    # comment.owner_id = '1'
    # comment.module_id = '3'
    # comment.stars = 0
    # comment.content = form.comment
    add_comment_by_entity(comment)
    return 'True'
