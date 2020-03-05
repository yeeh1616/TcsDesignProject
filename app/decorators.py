from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

from app.models import User


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

