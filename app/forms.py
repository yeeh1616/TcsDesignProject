from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, delete_a_user


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
            delete_a_user(username.data)
            #raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class ModuleInfoForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])


class CommentForm(FlaskForm):
    star = StringField('Star', validators=[DataRequired()])
    star2 = StringField('Star', validators=[DataRequired()])
    star3 = StringField('Star', validators=[DataRequired()])
    star4 = StringField('Star', validators=[DataRequired()])
    comment = StringField('Comment', validators=[DataRequired()])


class AssignHouseForm(FlaskForm):
    teacher_email = StringField('Email', validators=[DataRequired()])
    house_number = StringField('HouseNumber', validators=[DataRequired()])