from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from app import models
bp = Blueprint('main', __name__)

@bp.route('/hello')
def hello():
    #models.create_all_table()
    models.add_a_user("xia","try","lplp","0976", False, None)
    print(models.get_user_by_name("xia"))
    return "Hello, World!"