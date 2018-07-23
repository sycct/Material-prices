from flask import render_template, redirect, request, url_for, flash, abort
from ..decorators import admin_required
from . import manage
from flask_login import login_required, current_user
from ..models import User
from config import Config
from werkzeug.utils import secure_filename
import os
from .forms import EditProfileForm, ChangePasswordForm
from .. import db


@manage.route('/index', methods=['GET', 'POST'])
@login_required
@admin_required
def index():
    title = '首 页'
    page_name = 'Dashboard'
    page_features = 'dashboard & statistics'
    # 获取当前用户名
    get_user_id = current_user.get_id()
    return render_template("manage/index.html", name=title, pageName=page_name, description=page_name,
                           pageFeatures=page_features)


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

        flash(u'更新成功！', 'success')
    page_name = 'user'
    description = 'New User Profile'
    page_features = 'user account page'
    bg_style = 'page-container-bg-solid'
    if user is None:
        abort(404)
    return render_template('manage/user.html', name=description, user=user, pageName=page_name, description=description,
                           pageFeatures=page_features, bg_style=bg_style, form=form)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in Config.ALLOWED_EXTENSIONS


@manage.route('/upload_file', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        request_t = request.files
        print(request_t)
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(os.environ.get['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return 'ok'


@manage.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)
