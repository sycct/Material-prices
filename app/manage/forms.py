from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, \
    SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from flask_wtf.file import FileField, FileRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import MaterialClassification
from .. import db


class EditProfileForm(FlaskForm):
    fullname = StringField('姓  名', validators=[Length(0, 64)])
    nick_name = StringField('昵  称', validators=[Length(0, 64)])
    phone_number = StringField('电  话', validators=[Length(0, 32)])
    about_me = TextAreaField('自我介绍')
    website_url = StringField('个人网址', validators=[Length(0, 128)])
    submit = SubmitField('保存更改')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm new password', validators=[DataRequired()])
    submit = SubmitField('Update Password')


class AddClassificationForm(FlaskForm):
    classification_name = StringField("类别名称：", validators=[Length(0, 64), DataRequired()])
    classification_icon = FileField("材料小图：")
    submit = SubmitField('保存更改')


class AddClassificationCatalogForm(FlaskForm):
    def query_factory(*args):
        return [r.classification_name for r in db.session.query(MaterialClassification).all()]

    def get_pk(obj):
        return obj

    ClassificationCatalog_name = StringField("类别目录：", validators=[Length(0, 64), DataRequired()])
    Catalog_to_Classification = QuerySelectField(label=u'类别名称', validators=[DataRequired()],
                                                 query_factory=query_factory, get_pk=get_pk)
    submit = SubmitField('保存更改')
