from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    #Four classes represent the field types that will be used in the form and attached with validation behaviors
    #DataRequired validator checks that the field is not submitted empty
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired])
    #email is an additional valiator that makes sure the input matches an email input
    email = StringField('Email', validators=[DataRequired, Email()])
    password = PasswordField('Password', validators=[DataRequired])
    #Equalto is an additional validator that makes sure the two password inputs are the same
    password2 = PasswordField('Repeat Password', validators=[DataRequired, EqualTo('password')])
    submit = SubmitField('Register')

    #Custome validator that makes sure the username is not in the database
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    #Custome validator that makes sure the email is not in the database
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address')
