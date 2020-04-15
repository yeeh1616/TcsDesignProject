import datetime

from flask import current_app, jsonify
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, or_, PrimaryKeyConstraint
from sqlalchemy.orm import aliased
from werkzeug.security import generate_password_hash, check_password_hash
from app.__init__ import db, login_manager

# from app.__init__ import db

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
status_dict = {PENDING: 'Pending',
               REJECTED: 'Rejected',
               ACCEPTED: 'Accepted'}


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

    def __init__(self, uname, password, email, phone=None, img=None, title=None, confirmed=False,
                 confirmed_on=None):
        self.uname = uname
        self.password_hash = generate_password_hash(password)
        self.email = email
        self.phone = phone
        self.img = img
        self.title = title
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on

    def serialize(self):
        return {"id": self.id,
                "uname": self.uname,
                "password": self.password_hash,
                "role": self.title,
                "email": self.email,
                "phone": self.phone,
                "img": self.img,
                "title": self.title,
                "confirmed": self.confirmed,
                "confirmed_on": self.confirmed_on}

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_user_by_id(id):
        return User.query.filter_by(id=id).first()

    def is_tourist(email):
        if UserModule.query.filter(email=email).count() > 0:
            return False
        return True


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

    def __init__(self, user_id, module_id=None, course_id=None):
        self.user_id = user_id
        self.module_id = module_id
        self.course_id = course_id

    def serialize(self):
        return {"user_id": self.user_id,
                "module_id": self.module_id,
                "course_id": self.course_id}


class Student(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    #year = db.Column(db.Integer, nullable=False)
    house_id = db.Column(db.Integer)
    module_id = db.Column(db.Integer)
    student_email = db.Column(db.String)

    def __init__(self, house_id=None, module_id=None, student_email=None):
        #self.year = year
        self.house_id = house_id
        self.module_id = module_id
        self.student_email = student_email

    def get_full_info_by_id(id):
        student = db.session.query(User.uname, User.img, User.title, House.house_id, House.house_name, User.email).filter(
            User.id == Student.user_id).filter(Student.house_id == House.house_id).filter(User.id == id).first()
        return student

    def get_full_info_by_email(email):
        student = db.session.query(User.uname, User.img, User.title, House.house_id, House.house_name).filter(
            User.email == Student.student_email).filter(Student.house_id == House.house_id).filter(User.email == email).first()
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

    def get_houselist_by_year(year):
        houseList = House.query.filter_by(year=year).all()
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


class UserModule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    module_id = db.Column(db.Integer)
    status = db.Column(db.Integer)

    def __init__(self, email, module_id, status):
        self.email = email
        self.module_id = module_id
        self.status = status

    def serialize(self):
        return {"email": self.email,
                "module_id": self.module_id,
                "status": self.status}


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
    reason = db.Column(db.String)
    status = db.Column(db.Integer, nullable=False)
    send_date = db.Column(db.String, nullable=False)
    confirmed_date = db.Column(db.String, nullable=False)
    confirmed = db.Column(db.String)

    def __init__(self, owner_id, house_from, house_to, reason, status, send_date, confirmed_date, confirmed):
        self.owner_id = owner_id
        self.house_from = house_from
        self.house_to = house_to
        self.reason = reason
        self.status = status
        self.send_date = send_date
        self.confirmed_date = confirmed_date
        self.confirmed = confirmed

    def serialize(self):
        return {"owner_id": self.owner_id,
                "house_from": self.house_from,
                "house_to": self.house_to,
                "reason": self.reason,
                "status": self.status,
                "send_date": self.send_date,
                "confirmed_date": self.confirmed_date,
                "confirmed": self.confirmed}

    def get_request_by_owner_id(owner_id):
        request = Request.query.filter(Request.owner_id == owner_id).filter(Request.confirmed == 0).first()
        return request

    def add_request_by_entity(request):
        db.session.add(request)
        db.session.commit()
        return True

    def accept_request_by_id(id):
        request = Request.query.filter_by(id=id).first()
        request.status = ACCEPTED
        request.confirmed_date = datetime.date.today()
        student = Student.get_student_by_id(request.owner_id)
        student.house_id = request.house_to
        db.session.commit()

    def reject_request_by_id(id):
        request = Request.query.filter_by(id=id).first()
        request.status = REJECTED
        request.confirmed_date = datetime.date.today()
        db.session.commit()

    def confirm_request_by_id(id):
        request = Request.query.filter_by(id=id).first()
        request.confirmed_date = datetime.date.today()
        request.confirmed = 1
        db.session.commit()


# class Config(db.Model):
#     __tablename__ = 'config'
#     key = db.Column(db.String, nullable=False, primary_key=True)
#     value = db.Column(db.String, nullable=False)
#
#     def __init__(self, key, value):
#         self.key = key
#         self.value = value
#
#     def get_config_by_key(key):
#         config = Config.query.filter(Config.key == key).first()
#         return config
#
#     def serialize(self):
#         return {"key": self.key,
#                 "value": self.value}


class Questionnaire(db.Model):
    __tablename__ = 'questionnaire'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    abbr = db.Column(db.String, nullable=False)
    question = db.Column(db.String, nullable=False)

    def __init__(self, id, abbr, question):
        self.id = id
        self.abbr = abbr
        self.question = question

    def serialize(self):
        return {"id": self.id,
                "abbr": self.abbr,
                "question": self.question,
                "module_id": self.module_id}


class Question_rate(db.Model):
    __tablename__ = 'question_rate'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    question_id = db.Column(db.Integer, nullable=False)
    module_id = db.Column(db.Integer, nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    comment_id = db.Column(db.Integer, nullable=False)

    def __init__(self, question_id, module_id, rate, comment_id):
        self.question_id = question_id
        self.module_id = module_id
        self.rate = rate
        self.comment_id = comment_id

    def add_question_rate_list(question_rate_list):
        try:
            for q in question_rate_list:
                db.session.add(q)
            db.session.commit()
        except:
            return False
        return True

    def serialize(self):
        return {"id": self.id,
                "question": self.question,
                "owner_id": self.owner_id,
                "module_id": self.module_id,
                "rate": self.rate,
                "comment_id": self.comment_id}


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
        # print(user.serialize())
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
    return round(avg_star.avg_star, 1)


def add_comment_by_entity(comment):
    db.session.add(comment)
    db.session.commit()
    return comment


def add_house_keeper_by_entity(house_keeper):
    db.session.add(house_keeper)
    db.session.commit()
    return house_keeper.serialize()


def update_by_entity(entity):
    db.session.merge(entity)
    db.session.commit()
    return entity.serialize


def add_by_entity(entity):
    db.session.add(entity)
    db.session.commit()
    return entity.serialize


def get_request_owner_list_by_hid(house_id, limit, offset):
    return get_request_owner_list_base(house_id).limit(limit).offset(offset).all()


def get_request_owner_list_by_hid_filter(house_id, filter_para, limit, offset):
    return get_request_owner_list_base(house_id). \
        filter(Request.status == filter_para).limit(limit).offset(offset).all()


def get_request_owner_list_count(house_id):
    return get_request_owner_list_base(house_id).count()


def get_request_owner_list_count_by_status(house_id, filter_para):
    return get_request_owner_list_base(house_id).filter(Request.status == filter_para).count()


def get_request_owner_list_base(house_id):
    house_from_alias = aliased(House)
    house_to_alias = aliased(House)
    result = db.session.query(User.img,
                              User.uname,
                              User.email,
                              Request.id,
                              Request.house_from,
                              Request.house_to,
                              Request.send_date,
                              Request.confirmed_date,
                              Request.reason,
                              Request.status,
                              house_from_alias.house_name.label("house_from_name"),
                              house_to_alias.house_name.label("house_to_name")). \
        filter(Request.house_from == house_id). \
        filter(Request.owner_id == User.id). \
        filter(Request.house_from == house_from_alias.house_id). \
        filter(Request.house_to == house_to_alias.house_id)
    return result


def get_namelist_by_hid(house_id, limit, offset):
    return get_namelist(house_id).limit(limit).offset(offset).all()


def get_namelist_count(house_id):
    return get_namelist(house_id).count()


# def get_namelist(house_id):
#     result = db.session.query(User.uname,
#                               User.email,
#                               User.id). \
#         filter(Student.house_id == house_id). \
#         filter(Student.user_id == User.id)

def get_namelist(house_id):
    result = db.session.query(Student.student_email, User.uname, User.phone). \
        filter(Student.house_id == house_id).filter(Student.student_email==User.email)
    # . \
    # filter(User.title == 0)

    return result


def get_question_avg_stars(qid, mid):
    result = db.session.query(func.avg(Question_rate.rate).label('average')). \
        filter(Question_rate.module_id == mid). \
        filter(Question_rate.question_id == qid).first()

    return result


def get_questionnaire():
    uestionnaire = Questionnaire.query.all()
    return uestionnaire
