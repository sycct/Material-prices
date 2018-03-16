from flask import render_template, redirect, request, url_for, flash, abort
from ..decorators import permission_required, admin_required
from ..models import Permission
from . import manage
from flask_login import login_user, logout_user, login_required
from ..models import User


@manage.route('/index', methods=['GET', 'POST'])
@login_required
@admin_required
def index():
    title = '首 页'
    page_name = 'Dashboard'
    page_features = 'dashboard & statistics'
    return render_template("manage/index.html", name=title, pageName=page_name, description=page_name,
                           pageFeatures=page_features)


@manage.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    page_name = 'user'
    description = 'New User Profile'
    page_features = 'user account page'
    bg_style = 'page-container-bg-solid'
    if user is None:
        abort(404)
    return render_template('manage/user.html', name=description, user=user, pageName=page_name, description=description,
                           pageFeatures=page_features, bg_style=bg_style)


@manage.route('/file_upload')
@login_required
def file_upload():
    return;
