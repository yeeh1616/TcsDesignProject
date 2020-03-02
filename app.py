import sqlite3

from allauth.account.forms import LoginForm
from flask import Flask, redirect, url_for, flash
from flask import render_template
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import LoginManager
from flask_login import current_user, login_user
from models import User

app = Flask(__name__)
login = LoginManager(app)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


def checkPwd(pwd):
    hash = generate_password_hash('123')

    return check_password_hash(hash, pwd)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/')
@app.route('/index')
def hello_world():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    # c.execute("""CREATE TABLE tb1(
    #         name text,
    #         age integer
    #         )""")

    c.execute("INSERT INTO tb1 VALUES ('Yeeh', 32)")

    c.execute("SELECT * FROM tb1")

    str = c.fetchone()

    conn.commit()
    conn.close()

    user = {'username':str}
    return render_template('index.html', title = 'Home', user=user)


if __name__ == '__main__':
    app.run()
