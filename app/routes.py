from flask import flash, url_for, render_template
from flask_login import current_user
from werkzeug.utils import redirect

from app import app
from app import db
from app.forms import RegistrationForm
from app.models.User import User


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

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