from app import models, homepage,db
from app.forms import RegistrationForm, LoginForm
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_login import current_user, login_user, logout_user, login_required
from app import login_manager
from app.models import User
from app.token import generate_confirmation_token, confirm_token
import datetime
from app.email import send_email

bp = Blueprint('auth', __name__,template_folder = 'templates/account')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route('/test')
def test():
    return 'test'


@bp.route('/test2')
def test2():
    # res = render_template('auth/index.html')
    return render_template('auth/index.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(uname=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.home'))
    return render_template('login.html', title='Sign In', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    # models.delete_a_user('dfsdfsdfa')
    # models.delete_a_user('s1956124')
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(form.username.data,form.password.data,form.email.data,None,False,None)
        db.session.add(user)
        db.session.commit()
        print(user.email)
        login_user(user)
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        html = render_template('confirm_email.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(user.email, subject, html)


        # db.session.add(user)
        # db.session.commit()
        flash('Congratulations, you are now a registered user! Please confirm your email first')
        return redirect(url_for('auth.unconfirmed'))
    return render_template('signup.html', title='Register', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user =  User.query.filter_by(email=email).first_or_404()
    print('confirm')
    print(user.serialize())
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        #db.session.add(user)
        db.session.merge(user)
        db.session.commit()
        # user = User.query.filter_by(email=email).first_or_404()
        print('check')
        print(current_user.uname)
        print(current_user.confirmed)
        print(current_user.confirmed_on)
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('main.home'))

@bp.route('/unconfirmed')
@login_required
def unconfirmed():
    print('check3')
    user = User.query.filter_by(uname=current_user.uname).first_or_404()
    print(user.serialize())
    # print(current_user.uname)
    # print(current_user.confirmed)
    # print(current_user.confirmed_on)
    if current_user.confirmed:
        return redirect('main.home')
    flash('Please confirm your account!', 'warning')
    return render_template('unconfirmed.html')


@bp.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    html = render_template('confirm_email.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('auth.unconfirmed'))