from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, InputRequired
from app.models import User, delete_a_user, House
import datetime

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    #submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'confirm_password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(uname=username.data).first()
        if user is not None:
            print(user.serialize())
            #delete_a_user(username.data)
            username.data = ""
            raise ValidationError('Duplicate username.')

    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            email.data = ""
            raise ValidationError('Duplicate email address.')


class ModuleInfoForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])


class CommentForm(FlaskForm):
    star = StringField('Star', validators=[DataRequired()])
    comment = StringField('Comment', validators=[DataRequired()])


class RequestForm(FlaskForm):
    houseFrom = StringField('HouseFrom', validators=[DataRequired()])
    houseTo = StringField('HouseTo', validators=[DataRequired()])
    reason = StringField('HouseTo', validators=[DataRequired()])


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    #submit = SubmitField('Request Password Reset')

    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Email address does not exists')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'confirm_password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')


class AssignHouseForm(FlaskForm):
    teachers = SelectField('Teacher Email', coerce=int, validators=[InputRequired()])
    houses = SelectField('Houses', coerce=int, validators=[InputRequired()])
    # teacher_email = StringField('Email', validators=[DataRequired()])
    # study_year = StringField('StudyYear', validators=[DataRequired()])
    # house_name = StringField('HouseName', validators=[DataRequired()])

    # def validate_teacher_email(self, teacher_email):
    #     user = User.query.filter_by(email=teacher_email.data).first()
    #     if user is None:
    #         raise ValidationError('Wrong email or this teacher have not registered yet')
    #
    # def validate_house_name(self, house_name):
    #     house = House.query.filter_by(year=self.study_year.data, house_name=house_name.data).first()
    #
    #     if house is None:
    #         housen = house_name.data
    #         house_name.data = ''
    #         raise ValidationError("{0} is not existed in year {1}".format(housen, self.study_year.data))


class DeleteHouseForm(FlaskForm):

    houses = SelectField('Houses', coerce=int, validators=[InputRequired()])

class AddHouseForm(FlaskForm):
    # teacher_email = StringField('Email', validators=[DataRequired()])
    current_year = datetime.datetime.today().year
    study_year = SelectField('StudyYear', validators=[DataRequired()], choices=[(1, current_year-2), (2, current_year-1), (3, current_year)], default=3,
                             coerce=int)
    house_name = StringField('HouseName', validators=[DataRequired()])