from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from app import models
bp = Blueprint('main', __name__)


@bp.route('/test')
def test():
    return "Hello, test!"


@bp.route('/vtest')
def vtest():
    return render_template('auth/index.html')


@bp.route('/hello')
def hello():
    #models.create_all_table()
    models.add_a_user("yeye2","bbb","bbb","bbb", False, None)
    print(models.get_user_by_name("yeye"))
    return "Hello, World!"
