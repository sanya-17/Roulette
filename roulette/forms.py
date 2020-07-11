from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from roulette.models import User, List
from flask_login import current_user


class RegistrationForm(FlaskForm):
    # DataRequired requires that the username field not be empty
    # first parameter in stringfield is label
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken Please choose a different username')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError(
                'That email is taken Please choose a different email')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log in')


class ListForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Save')
    # TODO: consider case sensitivity

    def validate_name(self, name):
        name = List.query.filter_by(
            user_id=current_user.id, title=name.data).first()
        if name:
            raise ValidationError('A list with this name already exists')


class ItemForm(FlaskForm):
    item_list = StringField(
        'Items', validators=[DataRequired()], default='Enter items as a comma separated list')
    submit = SubmitField('Enter')
