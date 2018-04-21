from flask import render_template, redirect, request, url_for, flash, abort
from ..decorators import permission_required, admin_required
from . import manage
from flask_login import login_user, logout_user, login_required
from ..models import User
from config import Config
from werkzeug.utils import secure_filename
import os


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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in Config.ALLOWED_EXTENSIONS


@manage.route('/file_upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(os.environ.get['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return 'ok'
