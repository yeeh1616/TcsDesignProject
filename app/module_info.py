from flask import (
    Blueprint, flash, redirect, render_template, url_for,
    session, request)
from flask_login import login_required, current_user

from app import db
from app.decorators import check_confirmed
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


@bp.route('/info', methods=['GET', 'POST'])
@login_required
@check_confirmed
def info():
    module_id = request.args.get("id")
    session['moduleId'] = module_id
    user_id = current_user.id
    module = Module.query.filter_by(id=module_id).first()
    user = User.query.filter_by(id=user_id).first()
    comment_list = db.session.query(User.id, User.uname, User.img, Comment.content, Comment.module_id).filter(Comment.owner_id == User.id).filter(Comment.module_id==module_id).all()
    avg_star = get_avg_stars(module_id)
    return render_template('module_info.html', module=module, user=user, commentList=comment_list, totalComments=len(comment_list), avgStar=avg_star)


@bp.route('/edit', methods=['GET', 'POST'])
@login_required
@check_confirmed
def edit():
    form = ModuleInfoForm()
    module = Module.query.filter_by(id=form.id.data).first()
    return render_template('edit_info.html', module=module)


@bp.route('/save', methods=['GET', 'POST'])
@login_required
@check_confirmed
def save():
    moduleInfoForm = ModuleInfoForm()
    module_id = moduleInfoForm.id.data
    module_name = moduleInfoForm.name.data
    module_desc = moduleInfoForm.description.data
    module = Module(module_id, module_name, module_desc, None)
    # if moduleInfoForm.validate_on_submit():
    if Module.update_a_module_by_enity(module):
        return redirect(url_for('module_info.info', id=module_id))
    else:
        return 'save module info error ..........'


@bp.route('/comment', methods=['GET', 'POST'])
@login_required
@check_confirmed
def comment():
    owner_id = current_user.id
    module_id = session.get('moduleId')
    content = CommentForm().comment.data
    comment = Comment(owner_id, module_id, content, 0, 0)
    add_comment_by_entity(comment)
    return redirect(url_for('module_info.info', id=module_id))
