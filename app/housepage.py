from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_login import login_required,current_user
from app.decorators import check_confirmed, check_assigned_house
from app import models
from app.models import Module, db, User, HouseKeeper, House, add_house_keeper_by_entity, update_by_entity, HOUSEKEEPER
from app.forms import AssignHouseForm

bp = Blueprint('house', __name__,template_folder = 'templates/house')


@bp.route('/assignhouse', methods=['GET', 'POST'])
def assignhouse():
    form = AssignHouseForm()
    if form.validate_on_submit():
        email = form.teacher_email.data
        house_name = form.house_name.data
        user = User.query.filter_by(email=email).first()
        house = House.query.filter_by(module=session['moduleId'], house_name=house_name).first()
        # house_keeper = HouseKeeper(user.id, module_id=session['moduleId'])
        # add_house_keeper_by_entity(house_keeper)
        house.house_keeper = user.id
        update_by_entity(house)
        user.title = HOUSEKEEPER
        update_by_entity(user)
        flash("assigned house successfully")
        return render_template('assignhouse.html', form=form)
    return render_template('assignhouse.html', form=form)