from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_login import login_required, current_user
from app.decorators import check_confirmed, check_assigned_house
from app.forms import ModuleInfoForm
from app.models import Module, House, User, Student

bp = Blueprint('notification', __name__, template_folder='templates/notification')


@bp.route('/send_request_page', methods=['GET', 'POST'])
@login_required
@check_confirmed
def send_request_page():
    module_id = session.get('moduleId')
    # user = User.query.filter_by(id=current_user.id).first()
    student = Student.get_full_info_by_id(current_user.id)
    # db.session.query().filter(User.id == Student.user_id).filter(User.id == current_user.id).first()

    houseList = House.get_houselist_by_mid(module_id)
    return render_template('notification/request_student.html', houseList=houseList, student=student)


@bp.route('/send_request', methods=['GET', 'POST'])
@login_required
@check_confirmed
def send_request():
    form = ModuleInfoForm()
    module_name = form.name.data
    module_desc = form.description.data
    module = Module(module_name, module_desc, current_user.id, None)

    if Module.add_a_module_by_enity(module) is not None:
        return redirect(url_for('main.home'))
    else:
        return 'Add module info error ..........'