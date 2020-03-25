from datetime import date

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_login import login_required, current_user

from app import models
from app.decorators import check_confirmed, check_assigned_house
from app.forms import ModuleInfoForm, RequestForm
from app.models import Module, House, User, Student, Request

bp = Blueprint('notification', __name__, template_folder='templates/notification')


@bp.route('/request_page', methods=['GET', 'POST'])
@login_required
@check_confirmed
def request_page():
    user_temp = User.get_user_by_id(current_user.id)
    if user_temp.title==models.HOUSEKEEPER:
        house = House.get_house_by_housekeeper(current_user.id)
        request_owner_list = models.get_request_owner_list_by_hid(house.house_id)
        return render_template('notification/request_teacher.html', request_owner_list=request_owner_list)
    elif user_temp.title==models.STUDENT:
        module_id = session.get('moduleId')
        student = Student.get_full_info_by_id(current_user.id)
        request = Request.get_request_by_owner_id(current_user.id)
        if request is not None:
            my_house = House.get_house_by_id(request.house_from)
            target_house = House.get_house_by_id(request.house_to)
            request.status_txt = models.status_dict.get(request.status)
            return render_template('notification/request_result_page_student.html',
                                my_house=my_house,
                                target_house=target_house,
                                request=request)
        houseList = House.get_houselist_by_mid(module_id)
        return render_template('notification/request_student.html', houseList=houseList, student=student)


'''
9. accept or reject Request 改为ajax
8. 美化 teacher request页面
1. notification，右上角有数量
6. 过滤器
-- 未处理，已拒绝，已接受
7. 美化request result页
'''


@bp.route('/accept_request', methods=['GET', 'POST'])
@login_required
@check_confirmed
def accept_request():
    request_id = request.args.get("request_id")
    Request.accept_request_by_id(request_id)
    return redirect(url_for('notification.request_page'))


@bp.route('/reject_request', methods=['GET', 'POST'])
@login_required
@check_confirmed
def reject_request():
    request_id = request.args.get("request_id")
    Request.reject_request_by_id(request_id)
    return redirect(url_for('notification.request_page'))


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
