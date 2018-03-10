from flask import render_template, redirect, request, url_for, flash
from . import manage


@manage.route('/index', methods=['GET', 'POST'])
def index():
    title = '首 页'
    return render_template("manage/index.html", name=title)
