from flask import flash, url_for, render_template
from flask_login import current_user
from werkzeug.utils import redirect

from app import app
from app import db
from app.forms import RegistrationForm
from app.models.User import User


@app.route('/hello')
def hello():
    return "Hello, World!"


@app.route('/')
@app.route('/index')
def index():
    return "Homepage"


@app.route('/login')
def login():
    # return "Homepage"
    return render_template('login.html', title='Home')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

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