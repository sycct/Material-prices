from datetime import datetime
from flask import render_template, sessions, redirect, url_for
from flask_moment import Moment
from . import main
from .forms import NameForm
from .. import db
from ..models import User


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html',current_time=datetime.utcnow())
