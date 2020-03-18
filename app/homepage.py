from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_login import login_required,current_user
from app.decorators import check_confirmed, check_assigned_house
from app import models
from app.forms import ModuleInfoForm
from app.models import Module

bp = Blueprint('main', __name__,template_folder = 'templates')


@bp.route('/test')
@login_required
def test():
    return "Hello, test!"


@bp.route('/home')
@login_required
@check_confirmed
@check_assigned_house
def home():
    moduleList = Module.query.filter_by(owner_id=current_user.id).all()
    return render_template('index.html', moduleList=moduleList)


@bp.route('/add_module_page', methods=['GET', 'POST'])
@login_required
@check_confirmed
def add_module_page():
    return render_template('add_module.html')


@bp.route('/add_module', methods=['GET', 'POST'])
@login_required
@check_confirmed
def add_module():
    form = ModuleInfoForm()
    module_name = form.name.data
    module_desc = form.description.data
    module = Module(module_name, module_desc, current_user.id, None)
    if Module.add_a_module_by_enity(module) is not None:
        return redirect(url_for('main.home'))
    else:
        return 'Add module info error ..........'


@bp.route('/hello')
def hello():
    # models.create_all_table()
    # models.add_a_user("yeye2","bbb","bbb","bbb", False, None)
    print(models.get_user_by_name("yeye2"))
    return "Hello, World!"

