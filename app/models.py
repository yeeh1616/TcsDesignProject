import datetime

from flask import current_app, jsonify
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, or_
from sqlalchemy.orm import aliased
from werkzeug.security import generate_password_hash, check_password_hash
from app.__init__ import db, login_manager
#from app.__init__ import db

# with current_app.app_context():
#     db = SQLAlchemy(current_app)
STUDENT = 0
TEACHER_WITH_NO_HOUSE = 1
HOUSEKEEPER = 2
COORDINATOR = 3
MANAGER = 4


# status for request
PENDING = 0
REJECTED = -1
ACCEPTED = 1
CONFIRMED = 2
status_dict = {PENDING:'Pending',
               REJECTED:'Rejected',
               ACCEPTED:'Accepted',
               CONFIRMED:'Confirmed'}


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)
    phone = db.Column(db.String(20), unique=True)
    img = db.Column(db.String(80))
    title = db.Column(db.Integer)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    def __init__(self, uname, password, role, email, phone = None, img = None, title = None, confirmed=False, confirmed_on = None):
        self.uname = uname
        self.password_hash = generate_password_hash(password)
        self.title = role
        self.email = email
        self.phone = phone
        self.img = img
        self.title = title
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on

    def serialize(self):
        return {"id": self.id,
                "uname": self.uname,
                "password": self. password_hash,
                "role": self. title,
                "email" : self.email,
                "phone": self.phone,
                "img": self.img,
                "title": self.title,
                "confirmed": self.confirmed,
                "confirmed_on" : self.confirmed_on}

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_user_by_id(id):
        return User.query.filter_by(id=id).first()


class Manager(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)

    def __init__(self, user_id):
        self.user_id = user_id

    def serialize(self):
        return {"user_id": self.user_id}


class HouseKeeper(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer)
    course_id = db.Column(db.Integer)

    def __init__(self, user_id, module_id = None, course_id =None):
        self.user_id = user_id
        self.module_id = module_id
        self.course_id = course_id

    def serialize(self):
        return {"user_id": self.user_id,
                "module_id": self.module_id,
                "course_id": self.course_id}


class Student(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer)
    module_id = db.Column(db.Integer)

    def __init__(self, user_id, house_id=None, module_id=None,):
        self.user_id = user_id
        self.house_id = house_id
        self.module_id = module_id

    def get_full_info_by_id(id):
        student = db.session.query(User.uname, User.img, House.house_id, House.house_name).filter(User.id == Student.user_id).filter(Student.house_id == House.house_id).filter(User.id == id).first()
        return student

    def get_student_by_id(user_id):
        student = Student.query.filter(Student.user_id == user_id).first()
        return student

    def serialize(self):
        return {"user_id": self.user_id,
                "house_id": self.house_id,
                "module_id": self.module_id}


class House(db.Model):
    house_id = db.Column(db.Integer, primary_key=True)
    house_keeper = db.Column(db.Integer)
    year = db.Column(db.Integer)
    color = db.Column(db.String)
    house_name = db.Column(db.String(30))

    def __init__(self, house_keeper, year, color, house_name):
        self.house_keeper = house_keeper
        self.year = year
        self.color = color
        self.house_name = house_name

    def get_houselist_by_mid(mid):
        houseList = House.query.filter_by(year=mid).all()
        return houseList

    def get_house_by_id(house_id):
        house = House.query.filter_by(house_id=house_id).first()
        return house

    def get_house_by_housekeeper(hkid):
        house = House.query.filter_by(house_keeper=hkid).first()
        return house

    def serialize(self):
        return {"house_id": self.house_id,
                "house_keeper": self.house_keeper,
                "year": self.year,
                "color": self.color,
                "house_name": self.house_name}


class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String)
    owner_id = db.Column(db.Integer)
    img = db.Column(db.String(80))

    def __init__(self, name, description, owner_id, img):
        self.name = name
        self.description = description
        self.owner_id = owner_id
        self.img = img

    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                "description": self.description,
                "owner_id": self.owner_id,
                "imd": self.img}

    def add_a_module_by_enity(module):
        db.session.add(module)
        db.session.commit()
        return module.serialize()

    def update_a_module_by_enity(module_new):
        module_old = Module.query.filter_by(id=module_new.id).first()
        if module_old is not None:
            module_old.name = module_new.name
            module_old.description = module_new.description
            db.session.commit()
            return True
        else:
            return False


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String)
    module = db.Column(db.Integer)

    def __init__(self, name, description, module):
        self.name = name
        self.description = description
        self.module = module

    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                "description": self.description,
                "module": self.module}


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, unique=True)
    module_id = db.Column(db.Integer)
    content = db.Column(db.String, nullable=False)
    star = db.Column(db.Integer)
    status = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String, nullable=False)

    def __init__(self, owner_id, module_id, content, star, status, date):
        self.owner_id = owner_id
        self.module_id = module_id
        self.content = content
        self.star = star
        self.status = status
        self.date = date

    def serialize(self):
        return {"id": self.id,
                "owner_id": self.owner_id,
                "module_id": self.module_id,
                "content": self.content,
                "star": self.star,
                "status": self.status,
                "date": self.date}


class Request(db.Model):
    __tablename__ = 'request'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, nullable=False)
    house_from = db.Column(db.Integer, nullable=False)
    house_to = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String, nullable=False)

    def __init__(self, owner_id, house_from, house_to, status, date):
        self.owner_id = owner_id
        self.house_from = house_from
        self.house_to = house_to
        self.status = status
        self.date = date

    def serialize(self):
        return {"owner_id": self.owner_id,
                "house_from": self.house_from,
                "house_to": self.house_to,
                "status": self.status,
                "date": self.date}

    def get_request_by_owner_id(owner_id):
        request = Request.query.filter(Request.owner_id==owner_id).filter(or_(Request.status==-1, Request.status==0, Request.status==1)).first()
        return request

    def add_request_by_entity(request):
        db.session.add(request)
        db.session.commit()
        return True

    def accept_request_by_id(id):
        request = Request.query.filter_by(id=id).first()
        request.status = ACCEPTED
        student = Student.get_student_by_id(request.owner_id)
        student.house_id = request.house_to
        db.session.commit()

    def reject_request_by_id(id):
        request = Request.query.filter_by(id=id).first()
        request.status = REJECTED
        db.session.commit()

# database methods


def create_all_table():
    db.create_all()


def get_user_by_name(uname):
    user = User.query.filter_by(uname=uname).first()
    if user is None:
        return None
    else:
        return user.serialize()


def get_all_user():
    users = User.query.all()
    if users is None:
        return None
    else:
        return jsonify({'users': list((map(lambda ft: ft.serialize(), users)))})


def add_a_user(uname, password, role, email, phone, confirmed, confirmed_on):
    user = User(uname, password, role, email, phone, confirmed, confirmed_on)
    db.session.add(user)
    db.session.commit()
    return user.serialize()


def add_a_user_by_enity(user):
    db.session.add(user)
    db.session.commit()
    return user.serialize()


def delete_a_user(uname):
    # Maybe try this
    user = User.query.filter_by(uname=uname).first()
    if user is not None:
        #print(user.serialize())
        db.session.delete(user)
        db.session.commit()

    # User.query.filter_by(uname=uname).delete()
    # db.session.commit()


def confirm_a_user_by_email(email):
    user = User.query.filter_by(email=email).first_or_404()
    user.confirmed = True
    user.confirmed_on = datetime.datetime.now()
    db.session.add(user)
    db.session.commit()
    return user.serialize()


def get_avg_stars(module_id):
    avg_star = db.session.query(func.avg(Comment.star).label('avg_star')).filter(Comment.module_id == module_id).first()
    db.session.commit()
    if avg_star.avg_star is None:
        return 0
    return round(avg_star.avg_star)


def add_comment_by_entity(comment):
    db.session.add(comment)
    db.session.commit()
    return comment.serialize()

def add_house_keeper_by_entity(house_keeper):
    db.session.add(house_keeper)
    db.session.commit()
    return house_keeper.serialize()

def update_by_entity(entity):
    db.session.merge(entity)
    db.session.commit()
    return entity.serialize

def get_request_owner_list_by_hid(house_id):
    # result = db.session.query().filter((Request.house_from == house_id)|(Request.house_to == house_id)).filter(Request.owner_id == User.id).all()
    house_from_alias = aliased(House)
    house_to_alias = aliased(House)
    # house_from_name = aliased(house_from_alias.house_name)
    # house_to_name = aliased(house_to_alias.house_name)
    result = db.session.query(User.img,
                              Request.id,
                              Request.house_from,
                              Request.house_to,
                              Request.status,
                              house_from_alias.house_name.label("house_from_name"),
                              house_to_alias.house_name.label("house_to_name")).\
        filter(Request.house_from == house_id).\
        filter(Request.owner_id == User.id).\
        filter(Request.house_from == house_from_alias.house_id).\
        filter(Request.house_to == house_to_alias.house_id).all()
    return result
