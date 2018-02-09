from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
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
    fullname = StringField('FullName', validators=[DataRequired()])
    username = StringField('Username',
                           validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z0-9_.]*$', 0,
                                                                             'User name have only letters,''numbers,dots or underscores')])
    password = PasswordField('Password',
                             validators=[DataRequired(), EqualTo('password2', message='Password must match.')])
    address = StringField('Address', validators=[DataRequired()])
    province_region_id = StringField('')
    city_region_id = StringField('')
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already is use.')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    password = PasswordField('New Password',
                             validators=[DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')
