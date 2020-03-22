from datetime import date

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_login import login_required, current_user
from app.decorators import check_confirmed, check_assigned_house
from app.forms import ModuleInfoForm, RequestForm
from app.models import Module, House, User, Student, Request

bp = Blueprint('notification', __name__, template_folder='templates/notification')


@bp.route('/send_request_page', methods=['GET', 'POST'])
@login_required
@check_confirmed
def send_request_page():
    module_id = session.get('moduleId')
    student = Student.get_full_info_by_id(current_user.id)
    request = Request.get_request_by_owner_id(current_user.id)
    if request is not None:
        my_house = House.get_house_by_id(request.house_from)
        target_house = House.get_house_by_id(request.house_to)
        return render_template('notification/request_result_page_student.html',
                           my_house=my_house,
                           target_house=target_house)
    houseList = House.get_houselist_by_mid(module_id)
    return render_template('notification/request_student.html', houseList=houseList, student=student)


@bp.route('/send_request', methods=['GET', 'POST'])
@login_required
@check_confirmed
def send_request():
    form = RequestForm()
    my_house = House.get_house_by_id(form.houseFrom.data)
    target_house = House.get_house_by_id(form.houseTo.data)

    request = Request.get_request_by_owner_id(current_user.id)
    if request is None:
        request = Request(current_user.id, my_house.house_id, target_house.house_id, 0, date.today())
        Request.add_request_by_entity(request)
        return render_template('notification/request_result_page_student.html',
                               my_house=my_house,
                               target_house=target_house)
    else:
        return "Request already exist......"
