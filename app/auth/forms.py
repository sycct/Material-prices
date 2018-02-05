from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('', validators=[DataRequired(), Length(1, 64), Email()], render_kw={'placeholder': 'Username'})
    password = PasswordField('', validators=[DataRequired()], render_kw={'placeholder': 'Password'})
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('登 陆', render_kw={'class': 'btn green uppercase'})


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    name = StringField('FullName', validators=[DataRequired()])
    username = StringField('Username',
                           validators=[DataRequired(), Length(1, 64),Regexp('^[A-Za-z0-9_.]*$', 0, 'User name have only letters,''numbers,dots or underscores')])
    password = PasswordField('Password',
                             validators=[DataRequired(), EqualTo('password2', message='Password must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already is use.')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Length(1, 64),Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    password = PasswordField('New Password',
                             validators=[DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')
