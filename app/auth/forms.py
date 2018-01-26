from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, length, Email


class LoginForm(Form):
    email = StringField('', validators=[Required(), length(1, 64), Email()], render_kw={'placeholder': 'Username',
                                                                                        'class': 'form-control form-control-solid placeholder-no-fix',
                                                                                        'autocomplete': 'off'})
    password = PasswordField('', validators=[Required()], render_kw={'placeholder': 'Password',
                                                                     'class': 'form-control form-control-solid placeholder-no-fix',
                                                                     'autocomplete': 'off'})
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In',render_kw={'class':'btn green uppercase'})
