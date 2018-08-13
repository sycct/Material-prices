from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, \
    SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from flask_wtf.file import FileField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import MaterialClassification, ClassificationCatalog, MaterialItem
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


class AddBrandForm(FlaskForm):
    def query_factory(*args):
        return [r.i_name for r in db.session.query(MaterialItem).all()]

    def get_pk(obj):
        return obj

    Brand_name = StringField("品牌名称：", validators=[Length(0, 64), DataRequired()])
    Brand_to_Item = QuerySelectField(label=u'材料名称', validators=[DataRequired()], query_factory=query_factory,
                                        get_pk=get_pk)
    submit = SubmitField('保存更改')


class AddMaterialItemForm(FlaskForm):
    def query_factory(*args):
        return [r.catalog_name for r in db.session.query(ClassificationCatalog).all()]

    def get_pk(obj):
        return obj

    # def child_query_factory(*args):
    #     return [r.i_name for r in db.session.query(MaterialItem).all()]

    Item_name = StringField("材料名称：", validators=[Length(0, 50), DataRequired()])
    Item_to_Catalog = QuerySelectField(label=u'目录名称：', validators=[DataRequired()], query_factory=query_factory,
                                       get_pk=get_pk)
    # Item_to_ChildItem=QuerySelectField(label=u'子品牌名称', query_factory=child_query_factory,
    #                                     get_pk=get_pk)
    submit = SubmitField('保存更改')
