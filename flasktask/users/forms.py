from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flasktask.models import User
from flask_login import current_user
from flasktask.config import FieldConfig as cfg
import safe

def raise_if_username_exists(username, err_msg='That Username already exists!'):
    user = User.query.filter_by(username=username).first()
    if user:
        raise ValidationError(err_msg)
def raise_if_email_exists(email, err_msg='That Email already exists!'):
    user = User.query.filter_by(email=email).first()
    if user:
        raise ValidationError(err_msg)

def get_strong_password_field():
    return PasswordField('Password', validators=[DataRequired(),
        Length(min=cfg.MIN_PW_LENGTH, max=cfg.MAX_PW_LENGTH)])
def get_username_field():
    return StringField('Username', validators=[DataRequired(),
        Length(min=cfg.MIN_USERNAME_LENGTH, max=cfg.MAX_USERNAME_LENGTH)])
def get_email_field():
    return StringField('Email', validators=[DataRequired(), Email(),
        Length(min=0, max=cfg.MAX_EMAIL_LENGTH)])


class RegistrationForm(FlaskForm):
    username = get_username_field()
    email = get_email_field()
    password = get_strong_password_field()
    confirm_password = PasswordField('Confirm Password',
            validators=[DataRequired(), EqualTo('password')])
    recaptcha = RecaptchaField()
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        raise_if_username_exists(username.data)
    def validate_email(self, email):
        raise_if_email_exists(email.data)

class LoginForm(FlaskForm):
    email = get_email_field()
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    recaptcha = RecaptchaField()
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = get_username_field()
    email = get_email_field()
    picture = FileField('Update Profile Picture',
            validators=[FileAllowed(['jpg', 'png', 'bmp'])])
    submit = SubmitField('Update Info')

    def validate_username(self, username):
        if current_user.username != username.data:
            raise_if_username_exists(username.data)
    def validate_email(self, email):
        if current_user.email != email.data:
            raise_if_email_exists(email.data)


class RequestResetForm(FlaskForm):
    email = get_email_field()
    submit = SubmitField('Request Password Reset')
    def validate_email(self, email):
        if not User.query.filter_by(email=email.data).first():
            raise ValidationError('An account with that email does not exist.')

class ResetPasswordForm(FlaskForm):
    password = get_strong_password_field()
    confirm_password = PasswordField('Confirm Password',
            validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

