from flask import render_template, redirect, request, url_for, flash, abort, current_app
from ..decorators import admin_required
from . import manage
from flask_login import login_required, current_user
from ..models import User, MaterialClassification
from config import Config
from werkzeug.utils import secure_filename
import os
from .forms import EditProfileForm, ChangePasswordForm, AddClassificationForm
from .. import db
import uuid
from pypinyin import lazy_pinyin


@manage.route('/index', methods=['GET', 'POST'])
@login_required
@admin_required
def index():
    title = '首 页'
    page_name = 'Dashboard'
    page_features = 'dashboard & statistics'
    # 获取当前用户id
    id = current_user.id
    user_info = User.query.get_or_404(id)
    return render_template("manage/index.html", name=title, pageName=page_name, description=page_name,
                           pageFeatures=page_features, user_info=user_info)


@manage.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    # 判断当前登陆用户名
    get_current_username = current_user.username
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    form = EditProfileForm()
    # 判断当前用户
    if (get_current_username == user):
        form.fullname.data = user.fullname
        form.phone_number.data = user.phone_number
        form.nick_name.data = user.nick_name
        form.about_me.data = user.about_me
        form.website_url.data = user.website_url
    else:
        user_real = User.query.filter_by(username=get_current_username).first()
        form.fullname.data = user_real.fullname
        form.phone_number.data = user_real.phone_number
        form.nick_name.data = user_real.nick_name
        form.about_me.data = user_real.about_me
        form.website_url.data = user_real.website_url

    # 验证提交
    if form.validate_on_submit():
        current_user.fullname = request.values.get('fullname', 0)
        current_user.phone_number = request.values.get('phone_number', 0)
        current_user.nick_name = request.values.get('nick_name', 0)
        current_user.about_me = request.values.get('about_me', 0)
        current_user.website_url = request.values.get('website_url', 0)
        db.session.add(current_user._get_current_object())
        db.session.commit()
        # success
        return '0'
    page_name = 'user'
    description = 'New User Profile'
    page_features = 'user account page'
    bg_style = 'page-container-bg-solid'

    # 获取当前用户id
    id = current_user.id
    user_info = User.query.get_or_404(id)
    if user is None:
        abort(404)
    return render_template('manage/user.html', name=description, user=user, pageName=page_name, description=description,
                           pageFeatures=page_features, bg_style=bg_style, form=form, user_info=user_info)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in Config.ALLOWED_EXTENSIONS


@manage.route('/upload_file', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        new_filename = file_upload(file)
        # save as file name to database
        current_user.profile_picture = new_filename
        db.session.add(current_user._get_current_object())
        db.session.commit()
        return '0'
    return '1'


@manage.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            return '0'
        else:
            return '1'
    return render_template("auth/change_password.html", form=form)


@manage.route('/admin_add_classification', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_add_classification():
    # 获取当前用户id
    id = current_user.id
    # 页面信息
    user_info = User.query.get_or_404(id)
    title = '首 页'
    page_name = 'Dashboard'
    page_features = 'dashboard & statistics'
    # get classification tables
    get_classification_material = MaterialClassification.query.all()
    # form
    form = AddClassificationForm()
    if form.validate_on_submit():
        file = form.classification_icon.data
        new_filename = file_upload(file)
        material_classification = MaterialClassification(classification_name=form.classification_name.data,
                                                         classification_icon=new_filename)
        db.session.add(material_classification)
        db.session.commit()
        flash(u'保存成功！', 'success')
    return render_template('manage/admin_material_classification.html', user_info=user_info, name=title,
                           pageName=page_name, description=page_name, pageFeatures=page_features, form=form,
                           classification_lists=get_classification_material)


# Ajax file upload common
def file_upload(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        if filename.startswith('.'):
            name = file.filename.split('.')[0]
            ext = file.filename.split('.')[1]
            filename = '_'.join(lazy_pinyin(name)) + '.' + ext
        else:
            name = file.filename.split('.')[0]
            ext = file.filename.split('.')[1]
            filename = '_'.join(lazy_pinyin(name)) + '.' + ext
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        new_filename = str(uuid.uuid4()) + '.' + filename.rsplit('.', 1)[1]
        new_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
        # rename file
        os.rename(old_path, new_path)
        # return new file name e.g.:example.png
        return new_filename


@manage.route('/admin_list_classification', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_list_classification():
    # 获取当前用户id
    id = current_user.id
    # 页面信息
    user_info = User.query.get_or_404(id)
    title = '首 页'
    page_name = 'Dashboard'
    page_features = 'dashboard & statistics'
    # get classification tables
    get_classification_material = MaterialClassification.query.all()
    # form

    return render_template('manage/admin_list_classification.html', user_info=user_info, name=title,
                           pageName=page_name, description=page_name, pageFeatures=page_features,
                           classification_lists=get_classification_material)


@manage.route('/admin_edit_classification/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit_classification(id):
    # get classification item
    classification_item = MaterialClassification.query.get_or_404(id)
    # 获取当前用户id
    id = current_user.id
    # 页面信息
    user_info = User.query.get_or_404(id)
    title = '首 页'
    page_name = 'Dashboard'
    page_features = 'dashboard & statistics'
    # get classification tables
    get_classification_material = MaterialClassification.query.all()
    # form
    form = AddClassificationForm()
    form.classification_name.data = classification_item.classification_name
    form.classification_icon.data = classification_item.classification_icon
    return render_template('manage/admin_edit_classification.html', user_info=user_info, name=title,
                           pageName=page_name, description=page_name, pageFeatures=page_features,
                           classification_lists=get_classification_material, form=form)
