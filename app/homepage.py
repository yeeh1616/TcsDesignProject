from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_login import login_required,current_user
from app.decorators import check_confirmed
from app import models
from app.models import Module

bp = Blueprint('main', __name__,template_folder = 'templates')


@bp.route('/test')
@login_required
def test():
    return "Hello, test!"


@bp.route('/home')
# @login_required
# @check_confirmed
def home():
    moduleList = Module.query.filter_by(owner_id=current_user.id).all()
    return render_template('index.html', moduleList=moduleList)


@bp.route('/hello')
def hello():
    # models.create_all_table()
    # models.add_a_user("yeye2","bbb","bbb","bbb", False, None)
    print(models.get_user_by_name("yeye2"))
    return "Hello, World!"
