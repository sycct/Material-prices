from datetime import datetime
from flask import render_template, sessions, redirect, url_for
from flask_moment import Moment
from . import main
from .forms import NameForm
from .. import db
from ..models import User
from twilio.twiml.messaging_response import MessagingResponse


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html',current_time=datetime.utcnow())


@main.route('/sms', methods=['GET', 'POST'])
def sms():
    """Respond to incoming messages with a friendly SMS."""
    # Start our response
    resp = MessagingResponse()

    return render_template('sms.html', current_time=datetime.utcnow(), message=resp)
