import functools
from app import app
from app import db
from app.forms import RegistrationForm
from flask_login import current_user
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')
# bp = Blueprint('auth', __name__)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    # return "Homepage"
    return render_template('login.html', title='Home')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    print("000000")
    print(current_user)
    print("666666")
    if current_user.is_authenticated:
        print("111111")
        return redirect(url_for('index'))

    print("222222")
    form = RegistrationForm()
    print("333333")
    #
    # if form.validate_on_submit():
    #     user = User(username=form.username.data, email=form.email.data)
    #     user.set_password(form.password.data)
    #     db.session.add(user)
    #     db.session.commit()
    #     flash('Congratulations, you are now a registered user!')
    #     return redirect(url_for('login'))
    # return render_template('register.html', title='Register', form=form)
    # return render_template('register.html', title='Register')

'''
Feature 01: login
'''

'''
Feature 02: register
-- 1. Show register page from login page
-- 2. Click submit send form to back-end
-- 3. Back end store the data into DB
-- 4. If success, redirect to homepage
-- 5. If fail, show error_info
'''