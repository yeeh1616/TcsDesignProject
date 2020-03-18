from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_login import login_required,current_user
from app.decorators import check_confirmed, check_assigned_house
from app import models
from app.models import Module
from app.forms import AssignHouseForm

bp = Blueprint('house', __name__,template_folder = 'templates/house')


@bp.route('/assignhouse', methods=['GET', 'POST'])
def assignhouse():
    form = AssignHouseForm
    if form.validate_on_submit():


    return render_template('assignhouse.html', form=form)