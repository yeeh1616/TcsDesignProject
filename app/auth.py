from app import models
from app.forms import RegistrationForm, LoginForm
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_login import current_user, login_user
from app.models import User

bp = Blueprint('auth', __name__)


@bp.route('/test')
def test():
    return 'test'


@bp.route('/test2')
def test2():
    # res = render_template('auth/index.html')
    return render_template('auth/index.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    # form = LoginForm()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(username=form.username.data).first()
    #     if user is None or not user.check_password(form.password.data):
    #         flash('Invalid username or password')
    #         return redirect(url_for('login'))
    #     login_user(user, remember=form.remember_me.data)
    #     return redirect(url_for('index'))
    # return render_template('login.html', title='Sign In', form=form)
    return render_template('login.html', title='Sign In')
    # return 'Wo ni ma'


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        models.add_a_user("yeye2", "bbb", "bbb", "bbb", False, None)
        # db.session.add(user)
        # db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)