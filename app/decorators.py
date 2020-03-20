from functools import wraps
from flask import flash, redirect, url_for, session
from flask_login import current_user

from app.models import User, TEACHER_WITH_NO_HOUSE, COORDINATOR, Module, MANAGER


def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        print('check2')
        user = User.query.filter_by(uname=current_user.uname).first_or_404()
        print(user.serialize())
        # print(current_user.uname)
        # print(current_user.confirmed)
        # print(current_user.confirmed_on)
        if current_user.confirmed is False:
            flash('Please confirm your account!', 'warning')
            return redirect(url_for('auth.unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function


def check_assigned_house(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        print('check_assigned')
        user = User.query.filter_by(uname=current_user.uname).first_or_404()
        print(user.serialize())
        # print(current_user.uname)
        # print(current_user.confirmed)
        # print(current_user.confirmed_on)
        if current_user.title == TEACHER_WITH_NO_HOUSE:
            flash('You have not been assigned a house', 'warning')
            return redirect(url_for('auth.unassigned'))
        return func(*args, **kwargs)

    return decorated_function


def check_manager(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        print('coordinator')
        user = User.query.filter_by(uname=current_user.uname).first_or_404()
        print(user.serialize())
        # print(current_user.uname)
        # print(current_user.confirmed)
        # print(current_user.confirmed_on)
        if current_user.title != MANAGER:
            flash('You can not assign house', 'warning')
            return redirect(url_for('auth.unassigned'))
        return func(*args, **kwargs)

    return decorated_function


# def own_module():
#     module_list = Module.query.filter_by(owner_id=current_user.id)
#     for module in module_list:
#         if session['moduleId'] == module.id:
#             return True
#     return False