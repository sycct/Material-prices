from flask import render_template, redirect, request, url_for, flash, abort
from ..decorators import permission_required, admin_required
from . import receive
from flask_login import login_user, logout_user, login_required
from ..models import User
from config import Config
from werkzeug.utils import secure_filename
import os


@receive.route('/index')
def index():
    title = '首 页'
    page_name = 'Dashboard'
    page_features = 'dashboard & statistics'
    return render_template("SMS_Receive/index.html", name=title, pageName=page_name, description=page_name,
                           pageFeatures=page_features)

@receive.route('/SMSContent')
def SMSContent():
    title = '首 页'
    page_name = 'Dashboard'
    page_features = 'dashboard & statistics'
    return render_template("SMS_Receive/sms_content.html", name=title, pageName=page_name, description=page_name,
                           pageFeatures=page_features)